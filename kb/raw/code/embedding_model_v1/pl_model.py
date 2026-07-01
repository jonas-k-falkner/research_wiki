#
import logging
import os
import tempfile
import traceback
from copy import deepcopy
from pathlib import Path
from timeit import default_timer as timer

import mlflow
import numpy as np
import torch
from mlflow.entities import DatasetInput, InputTag
from mlflow.tracking import MlflowClient
from pytorch_lightning import LightningModule
from pytorch_metric_learning import distances, losses
from torch import Tensor, nn, optim
from torch.utils.data import DataLoader

from aid_embedding.core_model import SSLModel

from .ssl.evaluation import (
    compute_mapk,
    compute_ranking_metrics,
    evaluate_clustering,
    evaluate_reconstruction,
    evaluate_retrieval,
)
from .ssl.ts_similarity import SimMemoryBuffer, TorchSoftDTW, compute_similarity
from .utils.lr_schedule import PlateauCycleLRScheduler
from .utils.ts_dataset import create_dataset

logger = logging.getLogger(__name__)
EPS32 = float(np.finfo(np.float32).eps)
EPS16 = float(np.finfo(np.float16).eps)
_TIMED = False


class PLModel(LightningModule):
    """

    Args:
        data_cfg: config dict for data handling and loading
        model_cfg: config dict for neural network model
        optimizer_cfg: config dict for optimizer and optional lr scheduler
        similarity_fn_cfg: config dict for similarity function used
                            in similarity_learning and evaluation
        preprocessor_cfg: config dict for data preprocessing, including
                formatting, normalization, and potential time series augmentation.
        generative_learning: flag to use generative learning (autoencoder)
        generative_learning_cfg: config dict for generative learning
        contrastive_learning: flag to use contrastive learning (augmentations)
        contrastive_learning_cfg: config dict for contrastive learning
        similarity_learning: flag to use similarity learning
        similarity_learning_cfg: config dict for similarity learning
        alphas: dict with weights for the different objectives/loss functions:
                - gl: generative learning loss
                - cl: contrastive learning loss
                - sl: similarity learning loss
                - reg: regularization loss
                if the weight for a component is set to 0, it will not be computed
        eval_cfg: config dict for evaluation
        data_is_pre_processed: Set this to True when the fed data is already preprocessed.
        seed: seed for random number generator

    """

    def __init__(
        self,
        data_cfg: dict,
        model_cfg: dict,
        optimizer_cfg: dict,
        similarity_fn_cfg: dict,
        preprocessor_cfg: dict | None = None,
        generative_learning: bool = False,
        generative_learning_cfg: dict | None = None,
        contrastive_learning: bool = False,
        contrastive_learning_cfg: dict | None = None,
        similarity_learning: bool = False,
        similarity_learning_cfg: dict | None = None,
        alphas: dict | None = None,
        eval_cfg: dict | None = None,
        data_is_pre_processed: bool = False,
        seed: int = 666,
        compile_submodules: bool = False,
        debug: bool | int = False,
        **kwargs,
    ):
        super().__init__()
        if not (generative_learning or contrastive_learning or similarity_learning):
            raise RuntimeError("requires at least one SSL approach to be used.")
        self.data_cfg = data_cfg
        self.model_cfg = model_cfg
        self.optimizer_cfg = optimizer_cfg
        self.similarity_fn_cfg = similarity_fn_cfg
        self.preprocessor_cfg = preprocessor_cfg
        self.use_gl = generative_learning
        self.gl_cfg = generative_learning_cfg or {}
        self.use_cl = contrastive_learning
        self.cl_cfg = contrastive_learning_cfg or {}
        self.use_sl = similarity_learning
        self.sl_cfg = similarity_learning_cfg or {}
        self.sim_memory_cfg = self.sl_cfg.get("sim_memory_cfg", {}) or {}
        # alphas --> weights for different loss components
        alphas = alphas or {}
        self.alpha_gl = alphas.get("gl", float(self.use_gl))
        self.alpha_cl = alphas.get("cl", float(self.use_cl))
        self.alpha_sl = alphas.get("sl", float(self.use_sl))
        self.alpha_reg = alphas.get("reg", 0.0)
        # config for evaluation
        eval_cfg = eval_cfg or {}
        self.eval_ranking_cfg = eval_cfg.get("ranking_cfg", {})
        self.eval_clustering_cfg = eval_cfg.get("clustering_cfg", {})
        self.eval_retrieval_cfg = eval_cfg.get("retrieval_cfg", {})
        self.retrieve_every_n_epochs = int(eval_cfg.get("retrieve_every_n_epochs", 1))
        self.retrieve_n_batches = int(eval_cfg.get("retrieve_n_batches", 3))
        self.map_k = eval_cfg.get("map_k", 10)

        self.data_is_pre_processed = data_is_pre_processed
        self.seed = seed
        self.debug = debug
        self.moco = False  # TODO: to be implemented

        self.save_hyperparameters()
        self._seed_inc = 0

        # initialize actual model
        self.model = SSLModel(
            generative_learning=self.use_gl,
            contrastive_learning=self.use_cl,
            similarity_learning=self.use_sl,
            random_mask_cfg=self.gl_cfg.get("random_mask_cfg", None),
            seed=self._get_next_seed(),
            compile_submodules=compile_submodules,
            **self.model_cfg,
        )

        # init losses
        self.emb_distance = distances.LpDistance(p=2, normalize_embeddings=True)
        self.reconstruction_loss_fn = nn.MSELoss()
        self.contrastive_loss_fn = losses.NTXentLoss(
            temperature=self.cl_cfg.get("ntx_ent_temp", 0.07),  # tau=0.07 like in MoCo
            distance=self.emb_distance,
        )
        # we use sum reduction and normalize ourselves to avoid a mean-of-means calculation
        self.similarity_loss_fn = nn.SmoothL1Loss(reduction="sum")
        # init general similarity function for both, sim-learning and evaluation
        self.similarity_fn = TorchSoftDTW(**self.similarity_fn_cfg)

        # create memory buffers
        self.cl_memory = None
        self.num_cl_samples = self.cl_cfg.get("num_memory_samples", 0)
        self.sl_memory = None
        self.num_sl_samples = self.sl_cfg.get("num_memory_samples", 0)

        if self.use_cl and self.num_cl_samples:
            # instantiate a memory buffer for contrastive samples
            self.cl_memory = losses.CrossBatchMemory(
                loss=self.contrastive_loss_fn,
                embedding_size=self.model.latent_dim,
                memory_size=self.num_cl_samples,  # since will always use full memory
            )
        else:
            # wrap loss function for SSL loss
            self.contrastive_loss_fn = losses.SelfSupervisedLoss(self.contrastive_loss_fn)
        if self.use_sl:
            # instantiate a memory buffer for similarity learning samples
            train_bs = self.data_cfg["train_ds_cfg"]["batch_size"]
            self.sl_memory = SimMemoryBuffer(sim_fn=self.similarity_fn, seed=self._get_next_seed(), memory_size=train_bs * self.num_sl_samples, **self.sim_memory_cfg)

        self.train_ds = None
        self.val_ds = None
        self.test_ds = None

        self._optimizer = None
        self._scheduler = None
        self._scheduler_monitor_metric = None
        self._num_eval_batches = None

    def _get_next_seed(self) -> int:
        """
        Increments the seed counter and returns the next seed value.

        Returns:
            int: The next seed value.

        """
        self._seed_inc += 1
        return int(self.seed + self._seed_inc)

    @property
    def embedding_dim(self) -> int:
        return self.model.latent_dim

    @property
    def min_num_samples(self) -> int:
        n_cl = self.num_cl_samples if self.num_cl_samples > 0 else 10e6
        n_sl = self.num_sl_samples if self.num_sl_samples > 0 else 10e6
        return min(n_cl, n_sl)

    def forward(self, inputs, target):
        # Do not use directly. Instead, implement predict_step for inference,
        # which also enables model.predict(...) and trainer.predict(...)
        raise RuntimeError("do not use forward method for PLModel")

    def setup(self, stage) -> None:
        """
        Sets up the datasets for training, validation, testing, or prediction phases. Depending on the specified
        stage ('fit', 'validate', 'test', or 'predict'), the method initializes and prepares the corresponding dataset
        interfaces.

        Args:
            stage: The stage indicating the operation mode:
                 'fit' initializes both training and validation datasets.
                 'validate' initializes only the validation dataset.
                 'test' initializes the test dataset.
                 'predict' skips dataset setup for prediction.
        """
        stage = stage.value

        # load, process and split data -> train/val/test
        # Here we just initialize and load the different train, val and test dataset interfaces.
        ddir = Path(self.data_cfg["data_dir"])

        logger.info("setting up datasets...")
        ds_handles = {}
        if stage == "fit":
            shuffle = not self.debug
            cfg = self.data_cfg["train_ds_cfg"]
            dpth = ddir / "train"
            self.train_ds = create_dataset(
                data_dir=dpth,
                batch_size=cfg.get("batch_size"),
                min_seq_len=cfg.get("min_seq_len", 24),
                seed=self._get_next_seed(),
                shuffle_bins=shuffle,
                shuffle_batches=shuffle,
                cl_augmentations=self.use_cl,
                aug_cfg=self.cl_cfg.get("augmentation_cfg", None),
                pre_process=not self.data_is_pre_processed or self.use_cl,
            )
            ds_handles[dpth] = self.train_ds
        if stage in ["fit", "validate"]:
            cfg = self.data_cfg["val_ds_cfg"]
            dpth = ddir / "val"
            self.val_ds = create_dataset(
                data_dir=dpth,
                batch_size=cfg.get("batch_size"),
                min_seq_len=cfg.get("min_seq_len", 24),
                seed=self._get_next_seed(),
                # no shuffling for val and test
                shuffle_bins=False,
                shuffle_batches=False,
                # no contrastive augs for val or test
                cl_augmentations=False,
                aug_cfg=None,
                pre_process=not self.data_is_pre_processed,
            )
            ds_handles[dpth] = self.val_ds
        if stage == "test":
            cfg = self.data_cfg["test_ds_cfg"]
            dpth = ddir / "test"
            self.test_ds = create_dataset(
                data_dir=dpth,
                batch_size=cfg.get("batch_size"),
                min_seq_len=cfg.get("min_seq_len", 24),
                seed=self._get_next_seed(),
                # no shuffling for val and test
                shuffle_bins=False,
                shuffle_batches=False,
                # no contrastive augs for val or test
                cl_augmentations=False,
                aug_cfg=None,
                pre_process=not self.data_is_pre_processed,
            )
            ds_handles[dpth] = self.test_ds
        if stage == "predict":
            return

        # log dataset metadata to MLFlow
        if hasattr(self.logger, "experiment"):
            logger_experiment = self.logger.experiment
            if "mlflow" in str(type(logger_experiment)).lower():
                ds_to_log = []
                for dpth, ds in ds_handles.items():
                    mlf_ds = mlflow.data.from_numpy(
                        # fake empty features, for the time being we just want to save metadata
                        features=np.array([]),
                        name=f"{dpth.parent.name!s}_{dpth.name!s}",
                        digest=str(ds.version_hash),
                        # source=str(dpth.resolve())
                    )
                    ds_to_log.append(DatasetInput(dataset=mlf_ds._to_mlflow_entity(), tags=[InputTag(key="mlflow.data.context", value=str(stage))]))
                logger_experiment.log_inputs(run_id=self.logger.run_id, datasets=ds_to_log)
                logger.info("tracking datasets on MLFlow.")
                # check remote artifact location
                exp_nm = os.getenv("MLFLOW_EXPERIMENT_NAME", "emb_model_v0")
                try:
                    exp = MlflowClient().get_experiment_by_name(exp_nm)
                    logger.info(f"experiment artifact_location: {exp.artifact_location}")
                except Exception as err:
                    logger.error(f"error on remote tracking server request for '{exp_nm}': {err}")

        logger.info("done.")

    def on_fit_start(self) -> None:
        if self.on_gpu and self.similarity_fn is not None:
            self.similarity_fn.to(self.device)

    def on_validation_start(self):
        if self.on_gpu and self.similarity_fn is not None:
            self.similarity_fn.to(self.device)

    def on_test_start(self):
        if self.on_gpu and self.similarity_fn is not None:
            self.similarity_fn.to(self.device)

    def cleanup(self):
        """
        Cleanup the resources or datasets held by the multi-processing logic. This method is used
        to clean up any active datasets or functions, ensuring proper resource deallocation and
        avoiding potential memory leaks.

        Raises:
            No exceptions are raised explicitly by this method.

        """
        if self.train_ds is not None:
            self.train_ds.teardown()
            self.train_ds = None
        if self.val_ds is not None:
            self.val_ds.teardown()
            self.val_ds = None
        if self.test_ds is not None:
            self.test_ds.teardown()
            self.test_ds = None

    def train_dataloader(self) -> DataLoader:
        self.train_ds.reset()
        logger.debug(f"loaded dataset with time series in the following sequence length bins: {self.train_ds.bins}.")
        return DataLoader(self.train_ds, batch_size=None, num_workers=0, shuffle=False)

    def val_dataloader(self) -> DataLoader:
        self.val_ds.reset()
        logger.debug(f"loaded dataset with time series in the following sequence length bins: {self.val_ds.bins}.")
        return DataLoader(self.val_ds, batch_size=None, num_workers=0, shuffle=False)

    def test_dataloader(self) -> DataLoader:
        self.test_ds.reset()
        logger.debug(f"loaded dataset with time series in the following sequence length bins: {self.test_ds.bins}.")
        return DataLoader(self.test_ds, batch_size=None, num_workers=0, shuffle=False)

    def _ssl_forward(self, batch: tuple):
        """
        Executes the forward pass for the self-supervised learning process. Handles
        the application of data augmentations, memory updating, and computation
        of losses required for self-supervised learning. The method integrates
        similarity computations, model forward pass, and loss calculations.

        Args:
            batch (Tuple): A tuple containing input time-series data (original and contrastive samples).

        Returns:
            Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]: A tuple
            containing the following loss values:
            - gl_loss: Generative learning loss computed from reconstruction.
            - cl_loss: Contrastive learning loss computed on latent space embeddings.
            - sl_loss: Similarity learning loss for self-supervised learning.
            - reg_loss: Regularization loss computed on normalized embeddings.

        Raises:
            ValueError: If the number of minimum samples is less than or equal
                to half of the batch size, as this is required for correct split
                for similarity computation.
            NotImplementedError: If certain functionalities (e.g., MoCo operations)
                are not yet implemented.
        """
        # augmentations and optional TS feature engineering are done during preprocessing
        # and/or when using the Dataset iterator with the dataloader
        x_org, x_contrast = batch
        _bs, t, d = x_org.shape

        x_sim, x_similarity, x_sample_similarity, z_sim, z_sample_sim = None, None, None, None, None
        if self.use_sl:
            # use the original and augmented data if contrastive learning is enabled
            x_sim = torch.cat((x_org[:, None, :], x_contrast), dim=1).view(-1, t, d) if self.use_cl and x_contrast is not None else x_org

            if _TIMED:
                # for profiling and debugging
                if self.on_gpu:
                    torch.cuda.synchronize()
                t = timer()
                x_similarity, x_sample_similarity, z_sample_sim = self.sl_memory.compute_sim(x_sim, self.num_sl_samples)
                if self.on_gpu:
                    torch.cuda.synchronize()
                t = timer() - t
                print(f"time for similarity computation: {t}s")
            else:
                x_similarity, x_sample_similarity, z_sample_sim = self.sl_memory.compute_sim(x_sim, self.num_sl_samples)

        # run model forward
        z_org, z_contrast, x_hat, mask, z_norm = self.model(x_org, x_contrast)

        if self.use_sl:
            if self.moco:
                # get the latent embeddings of the momentum updated encoder encK and only add these to the memory
                raise NotImplementedError
            # add to memory
            z_sim = torch.cat((z_org[:, None, :], z_contrast), dim=1).view(-1, z_org.size(-1)) if self.use_cl and x_contrast is not None else z_org
            self.sl_memory.add(x_sim, z_sim)

        # compute losses
        gl_loss = self._gl_loss(x_org, x_hat, mask)
        cl_loss = self._cl_loss(z_org, z_contrast)
        sl_loss = self._sl_loss(x_similarity, z_sim, x_sample_similarity, z_sample_sim)
        reg_loss = self._reg_loss(z_norm)
        return gl_loss, cl_loss, sl_loss, reg_loss

    def training_step(self, batch: tuple) -> Tensor:
        """
        Performs a single training step by computing the total loss based on provided
        weights for different components of the loss:
            - gl_loss: Generative learning loss computed from reconstruction.
            - cl_loss: Contrastive learning loss computed on latent space embeddings.
            - sl_loss: Similarity learning loss for self-supervised learning.
            - reg_loss: Regularization loss computed on normalized embeddings.
        Logs each component loss, the total loss, and manages logging configuration based on their relevance.

        Args:
            batch (Tuple): Input batch containing the data for training.

        Returns:
            Tensor: Computed total loss for the current training step.
        """
        bs = batch[0].shape[0]
        gl_loss, cl_loss, sl_loss, reg_loss = self._ssl_forward(batch)
        loss = self.alpha_gl * gl_loss + self.alpha_cl * cl_loss + self.alpha_sl * sl_loss + self.alpha_reg * reg_loss
        # log losses
        self.log("loss", loss, batch_size=bs, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        if self.use_gl:
            self.log("gl_loss", gl_loss, batch_size=bs, on_step=False, on_epoch=True, prog_bar=False, logger=True)
        if self.use_cl:
            self.log("cl_loss", cl_loss, batch_size=bs, on_step=False, on_epoch=True, prog_bar=False, logger=True)
        if self.use_sl:
            self.log("sl_loss", sl_loss, batch_size=bs, on_step=False, on_epoch=True, prog_bar=False, logger=True)
        if self.alpha_reg > 0:
            self.log("reg_loss", reg_loss, batch_size=bs, on_step=False, on_epoch=True, prog_bar=False, logger=True)
        return loss

    def on_train_epoch_end(self):
        """
        Handles the end-of-epoch operations during training.

        This method resets the stateful memory object if it exists and updates the
        scheduler based on its configuration. If a monitor metric is specified for
        the scheduler, it uses the corresponding value from the callback metrics.

        Raises:
            KeyError: If the monitor metric is specified but not found in the
                callback metrics.
        """
        if self.sl_memory is not None:
            self.sl_memory.reset()
        if self._scheduler is not None:
            metr_id = self._scheduler_monitor_metric
            if metr_id is not None and metr_id in self.trainer.callback_metrics:
                metr = self.trainer.callback_metrics[self._scheduler_monitor_metric]
                self._scheduler.step(metr)

    def lr_schedulers(self):
        """Override Lightning's scheduler handling."""
        # Returning None prevents Lightning from stepping any scheduler automatically
        return []

    @torch.inference_mode()
    def _eval_forward(self, batch: tuple, eval_plots: bool) -> tuple[dict, list, list]:
        """
        Evaluates a batch by performing forward pass computations and calculating
        various metrics for time series data, such as similarity, ranking,
        clustering, retrieval, and reconstruction errors.

        Args:
            batch (Tuple): A tuple containing the input data.
            eval_plots (bool): A flag to indicate whether to generate evaluation plots.

        Returns:
            Tuple[Dict, List, List]: A tuple comprising:
                - A dictionary containing calculated evaluation metrics.
                - A list of plots for retrieval evaluation (if `eval_plots` is True).
                - A list of plots for reconstruction evaluation (if `eval_plots` is True).
        """
        x_org, _ = batch
        bs = x_org.size(0)
        # run model forward
        z_org, *_ = self.model(x_org)

        # evaluation tasks
        # ==============================
        # - SL: ts similarity in terms of DTW, etc.
        #       -> measure by ranking scores of relative distances
        #       -> measure by mean average precision (MAP), treating closest k in x space as positive items
        #       -> measure by general unsupervised clustering metrics applied to embeddings
        # - GL: imputation of missing values
        #       -> directly measured by reconstruction error
        metrics = {}
        retrieval_plots, recon_plots = [], []

        ### ========== ###
        ### === SL === ###
        ### ========== ###
        # compute_similarity() also handles NaN values, such that x_similarity will not have any NaNs
        # and latent embedding vector z should never have any NaNs
        x_similarity = compute_similarity(self.similarity_fn, x_org, x_org, raise_on_nan=False, symmetric=True)
        z_similarity = self.emb_distance(z_org, z_org)
        z_org = z_org.float()

        # 1) clustering
        # =====================
        if self.eval_clustering_cfg and bs >= 32:
            # cluster embedding space and compute unsupervised clustering metrics
            try:
                clst_metrics = evaluate_clustering(z=z_org, seed=self.seed + 1, **self.eval_clustering_cfg)
            except (RuntimeError, ValueError) as err:
                logger.error(f"evaluate clustering error: {err}\n{traceback.format_exc()}")
            else:
                metrics.update(clst_metrics)

        # convert types for other downstream eval tasks
        x_similarity = x_similarity.float()
        z_similarity = z_similarity.float()
        if (x_similarity < 0).any():
            x_similarity = torch.clamp(x_similarity, min=0) + EPS32

        # 2) ranking
        # =====================
        if self.eval_ranking_cfg:
            # we basically compare the relative consistency of the absolute similarities/differences
            # between the original time series and their latent representations
            # To measure this, we compute several ranking metrics in terms of the rank consistency
            # of the distances between the original TS and between their latent vectors.
            # In plain english: we check, how often the rank is correct, i.e. check if the
            # time series x_i which is closest to time series x_1 is also the closest vector z_i to vector z_1.
            # We do this for all i or, if specified, for the top k ranking positions
            # and compute the accordance of ranks using Kendall's Tau, Spearman Rank Correlation and NDCG.
            try:
                rnk_metrics = compute_ranking_metrics(gt_ranks=x_similarity.cpu().numpy(), pred_ranks=z_similarity.cpu().numpy(), per_sample=False, **self.eval_ranking_cfg)
            except (RuntimeError, ValueError) as err:
                logger.error(f"evaluate ranking error: {err}\n{traceback.format_exc()}")
            else:
                metrics.update(rnk_metrics)

        # 3) retrieval
        # =====================
        if eval_plots and self.eval_retrieval_cfg:
            # run some ANN retrieval on the batch in the embedding space and
            # plot the corresponding time series of the retrieved neighbours
            try:
                retrieval_plots = evaluate_retrieval(x=x_org.float(), z=z_org, x_distance=x_similarity, z_distance=z_similarity, **self.eval_retrieval_cfg)
            except (RuntimeError, ValueError) as err:
                logger.error(f"evaluate retrieval error: {err}\n{traceback.format_exc()}")

        # 4) MAP@k (Mean Average Precision at k)
        # =====================
        if self.map_k:
            try:
                metrics[f"MAP@{self.map_k}"] = compute_mapk(
                    x_distance=x_similarity,
                    z_distance=z_similarity,
                    k=self.map_k,
                )
            except (RuntimeError, ValueError) as err:
                logger.error(f"compute MAP@k error: {err}\n{traceback.format_exc()}")

        ### ========== ###
        ### === GL === ###
        ### ========== ###
        # --> TS reconstruction
        if self.use_gl:
            # compute reconstruction error
            x_hat, mask = self.model.reconstruct_dummy(x_org)
            metrics["reconstruction_error"] = self._gl_loss(x_org, x_hat, mask)
            if eval_plots and self.eval_retrieval_cfg:
                n = self.eval_retrieval_cfg.get("num_targets", 5)
                # create reconstruction example plots contrasting x_org and x_hat
                try:
                    recon_plots = evaluate_reconstruction(x_org, x_hat.to(dtype=x_org.dtype), mask, n)
                except (RuntimeError, ValueError) as err:
                    logger.error(f"evaluate reconstruction error: {err}\n{traceback.format_exc()}")

        return metrics, retrieval_plots, recon_plots

    def _log_metrics(self, metrics: dict, batch_size: int, prefix: str = ""):
        """
        Logs the given metrics with specified prefix and batch size to the logger.

        Iterates through the provided metrics dictionary, appending the prefix to the
        metric keys, and logs them using the internal `log` mechanism. Metrics are
        logged on epoch-level granularity by default, without appearing in the
        progress bar.

        Args:
            metrics (Dict): A dictionary containing metric names as keys and their
                corresponding values to be logged.
            batch_size (int): The size of the batch, associated with the metrics.
            prefix (str, optional): A string to prepend to each metric name. Defaults
                to an empty string.
        """
        pref = f"{prefix}_" if len(prefix) > 0 else ""
        for metr, v in metrics.items():
            m_str = f"{pref}{metr}".replace("@", "_at_")
            self.log(m_str, v, batch_size=batch_size, on_step=False, on_epoch=True, prog_bar=False, logger=True)

    def _old_add_eval_plots(self, ret_plots: list, rec_plots: list, batch_idx: int, prefix: str = ""):
        """
        Adds evaluation plots to the logger for visualization purposes.

        This method logs several types of plots (e.g., neighbor plots, latent
        embedding plots, reconstruction plots) to the tensorboard logger
        associated with the current experiment.

        Args:
            ret_plots (List): A list containing the return triplet plots
                (neighbor plots and latent embedding plots) to be logged.
            rec_plots (List): A list containing the reconstruction plots
                to be logged.
            batch_idx (int): The current batch index, used to uniquely
                tag plots for the specific training iteration.
            prefix (str): An optional prefix to attach to the plot tags
                for better organization in tensorboard. Defaults to an
                empty string.
        """
        pref = f"{prefix}_" if len(prefix) > 0 else ""
        tb = self.logger.experiment
        if ret_plots:
            x_plots, z_plots = ret_plots
            tb.add_figure(tag=f"{pref}ts_neighbour_plots_{batch_idx}", figure=x_plots, global_step=self.global_step)
            tb.add_figure(tag=f"{pref}ts_latent_emb_plots_{batch_idx}", figure=z_plots, global_step=self.global_step)
        if rec_plots:
            tb.add_figure(tag=f"{pref}ts_reconstruction_plots_{batch_idx}", figure=rec_plots, global_step=self.global_step)

    def _add_eval_plots(self, ret_plots: list, rec_plots: list, batch_idx: int, prefix: str = ""):
        """
        Adds evaluation plots to the logger for visualization purposes.

        This method logs several types of plots (e.g., neighbor plots, latent
        embedding plots, reconstruction plots) to the tensorboard logger
        associated with the current experiment.

        Args:
            ret_plots (List): A list containing the retrieval plots
                (neighbor plots and latent embedding plots) to be logged.
            rec_plots (List): A list containing the reconstruction plots to be logged.
            batch_idx (int): The current batch index, used to uniquely
                tag plots for the specific training iteration.
            prefix (str): An optional prefix to attach to the plot tags
                for better organization in tensorboard. Defaults to an
                empty string.
        """
        # Handle different logger types
        if hasattr(self.logger, "experiment"):
            logger_experiment = self.logger.experiment

            # Check if it is a TensorBoard logger
            if hasattr(logger_experiment, "add_figure"):
                pref = f"{prefix}_" if len(prefix) > 0 else ""
                # TensorBoard logger
                tb = logger_experiment
                if ret_plots:
                    x_plots, z_plots = ret_plots
                    tb.add_figure(tag=f"{pref}ts_neighbour_plots_{batch_idx}", figure=x_plots, global_step=self.global_step)
                    tb.add_figure(tag=f"{pref}ts_latent_emb_plots_{batch_idx}", figure=z_plots, global_step=self.global_step)
                if rec_plots:
                    tb.add_figure(tag=f"{pref}ts_reconstruction_plots_{batch_idx}", figure=rec_plots, global_step=self.global_step)
            elif "mlflow" in str(type(logger_experiment)).lower():
                # MLFlow logger - log figures as artifacts
                pref = f"{prefix}_run" if len(prefix) > 0 else "run"
                if ret_plots or rec_plots:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_dir = Path(temp_dir)
                        try:
                            if ret_plots:
                                x_plots, z_plots = ret_plots

                                # Save and log nearest neighbour plots
                                plt_type = "nearest_neighbour_plots"
                                fdir = temp_dir / plt_type
                                fdir.mkdir(parents=True, exist_ok=True)
                                for i, xplt in enumerate(x_plots):
                                    fpath = fdir / f"plot_{batch_idx}_{i}.png"
                                    xplt.savefig(fpath, format="png", dpi=150, bbox_inches="tight")
                                    self.logger.experiment.log_artifact(self.logger.run_id, fpath, f"plots/{pref}/ep_{self.current_epoch}/{plt_type}")

                                # Save and log latent embedding plots
                                plt_type = "latent_embedding_plots"
                                fdir = temp_dir / plt_type
                                fdir.mkdir(parents=True, exist_ok=True)
                                for i, zplt in enumerate(z_plots):
                                    fpath = fdir / f"plot_{batch_idx}_{i}.png"
                                    zplt.savefig(fpath, format="png", dpi=150, bbox_inches="tight")
                                    self.logger.experiment.log_artifact(self.logger.run_id, fpath, f"plots/{pref}/ep_{self.current_epoch}/{plt_type}")

                            if rec_plots:
                                # Save and log reconstruction plots
                                plt_type = "reconstruction_plots"
                                fdir = temp_dir / plt_type
                                fdir.mkdir(parents=True, exist_ok=True)
                                for i, rplt in enumerate(rec_plots):
                                    fpath = fdir / f"plot_{batch_idx}_{i}.png"
                                    rplt.savefig(fpath, format="png", dpi=150, bbox_inches="tight")
                                    self.logger.experiment.log_artifact(self.logger.run_id, fpath, f"plots/{pref}/ep_{self.current_epoch}/{plt_type}")

                                # for rplt in rec_plots:
                                #     with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
                                #         rplt.savefig(tmp.name, format='png', dpi=150, bbox_inches='tight')
                                #         self.logger.experiment.log_artifact(
                                #             self.logger.run_id,
                                #             tmp.name,
                                #             f"plots/{pref}ts_reconstruction_plots_{batch_idx}"
                                #         )
                        except Exception as e:
                            logger.error(f"Failed to log plots: {e}")
            else:
                logger.warning(f"Unknown logger type: {type(logger_experiment)}")
        else:
            logger.warning("Logger does not have experiment attribute, skipping plot logging!")

    def validation_step(self, batch: tuple, batch_idx: int) -> None:
        """
        Performs the validation step during the evaluation phase of model training. This step includes
        processing a batch of data, computing metrics, and optionally generating evaluation plots for
        retrieval and reconstruction results. Logs validation metrics and adds evaluation plots if
        conditions for plotting are met.

        Args:
            batch: A tuple containing the data for the current batch.
            batch_idx: Index of the current batch being processed.

        """
        if self.current_epoch == 0 or self._num_eval_batches is None:
            # first epoch, check how many batches to evaluate
            self._num_eval_batches = batch_idx + 1
            # simply plot first n batches
            plot_eval = batch_idx <= self.retrieve_n_batches
        elif self.current_epoch % self.retrieve_every_n_epochs == 0:
            # only plot retrieval and reconstruction results for some number of batches in some epochs
            # get divisor to know on which batches to plot
            div = max(1, self._num_eval_batches // self.retrieve_n_batches)
            plot_eval = batch_idx % div == 0
        else:
            plot_eval = False

        bs = batch[0].shape[0]
        # run eval forward pass including metrics computation
        metrics, ret_plots, rec_plots = self._eval_forward(batch, eval_plots=plot_eval)
        # log validation metrics
        self._log_metrics(metrics, batch_size=bs, prefix="val")
        if plot_eval:
            self._add_eval_plots(ret_plots, rec_plots, batch_idx, prefix="val")

    def test_step(self, batch: tuple, batch_idx: int) -> None:
        """
        Executes a single test step, which includes running an evaluation forward pass, logging
        test metrics, and adding evaluation plots. This method is intended to be called during
        the testing phase of the model lifecycle.

        Args:
            batch (Tuple): A batch of input data, where the first element of the tuple is
                expected to have a shape.
            batch_idx (int): The index of the batch within the current testing epoch.

        Returns:
            None
        """
        bs = batch[0].shape[0]
        # run eval forward pass including metrics computation
        metrics, ret_plots, rec_plots = self._eval_forward(batch, eval_plots=True)
        # log test metrics
        self._log_metrics(metrics, batch_size=bs, prefix="test")
        self._add_eval_plots(ret_plots, rec_plots, batch_idx, prefix="test")

    def predict_step(self, batch) -> Tensor:
        x_org, _ = batch
        return self.transform(x_org)

    def transform(self, *args, **kwargs):
        """
        Transforms (i.e. encodes) input data using the specified model.

        Args:
            *args: Positional arguments to be passed to the model's `transform` method.
            **kwargs: Keyword arguments to be passed to the model's `transform` method.

        Returns:
            The result of passing the provided arguments through the model's
            `transform` function.
        """
        return self.model.transform(*args, **kwargs)

    def reconstruct(self, *args, **kwargs):
        """
        Reconstructs inputs through the model.

        Args:
            *args: Positional arguments passed directly to the underlying
                model reconstruction method.
            **kwargs: Keyword arguments passed directly to the underlying
                model reconstruction method.

        Returns:
            Any: The reconstructed outputs as determined by the underlying
            model's reconstruct method.
        """
        return self.model.reconstruct(*args, **kwargs)

    def configure_optimizers(self):
        """
        Configures the optimizers and learning rate schedulers for the model training process.

        This method sets up the optimizer and learning rate (LR) scheduling configurations by
        extracting them from the `optimizer_cfg`. It supports multiple optimizers and LR
        schedulers, ensuring compatibility with the training framework. The function also logs
        the selected optimizer and scheduler for better traceability and debugging.

        Returns:
            dict: A dictionary containing the optimizer under the key 'optimizer', and potentially
            other training-related elements if extended in the future.

        Raises:
            NotImplementedError: If the specified learning rate scheduler is not implemented
            or unsupported.
        """
        opt_setup = {}
        opt_cfg = deepcopy(self.optimizer_cfg)
        schedule_cfg = opt_cfg.pop("lr_schedule", {})

        # optimizer
        opt_nm = opt_cfg.pop("optimizer")
        opt = getattr(optim, opt_nm)(self.model.parameters(), **opt_cfg)
        opt_setup["optimizer"] = opt

        # LR schedule
        schedule_nm = None
        if schedule_cfg:
            self._scheduler_monitor_metric = schedule_cfg.get("metric_to_track", "loss")
            self._optimizer = opt
            schedule_nm = schedule_cfg["scheduler"]
            if schedule_nm == "ReduceLROnPlateau":
                self._scheduler = optim.lr_scheduler.ReduceLROnPlateau(opt, **schedule_cfg.get("scheduler_cfg", {}))
            elif schedule_nm == "PlateauCycleLRScheduler":
                self._scheduler = PlateauCycleLRScheduler(opt, **schedule_cfg.get("scheduler_cfg", {}))
            else:
                raise NotImplementedError(f"lr_schedule '{schedule_nm}' not implemented")

        logger.info(f"running with: \n    optimizer:    '{opt_nm}'\n    lr_schedule:  '{schedule_nm}'")
        return opt_setup

    def _gl_loss(self, x: Tensor, x_hat: Tensor, mask: Tensor) -> Tensor | float:
        """
        Generative learning - reconstruction loss

        Args:
            x (Tensor): The original input tensor.
            x_hat (Tensor): The reconstructed input tensor.
            mask (Tensor): A binary mask indicating the valid indices for the computation.

        Returns:
            Union[Tensor, float]: The computed generative learning loss as a Tensor, or 0.0 if
            alpha_gl is less than or equal to zero.
        """
        if self.alpha_gl <= 0:
            return 0.0
        # check if any original input is NAN and remove it from the mask
        mask[torch.isnan(x.squeeze(-1))] = 0
        return self.reconstruction_loss_fn(x[mask], x_hat[mask])

    def _cl_loss(self, z_org: Tensor, z_contrast: Tensor) -> Tensor | float:
        """
        Computes the contrastive learning (CL) loss given original latent embeddings and
        their augmented counterparts. The function supports handling embeddings with or
        without a memory bank. If the alpha_cl parameter is less than or equal to zero,
        the function returns a loss of 0.0.

        Args:
            z_org: Original latent embeddings tensor.
            z_contrast: Tensor containing augmented latent embeddings.

        Returns:
            The computed contrastive learning loss as a tensor or a float value.
        """
        if self.alpha_cl <= 0:
            return 0.0
        bs, n_aug, _d = z_contrast.shape
        assert n_aug == 2
        # TODO: could implement this for n > 2 and then also directly
        #  add the un-augmented latent z_org as another candidate?

        if self.cl_memory is not None:
            z_contrast = torch.cat((z_contrast[:, 0, :], z_contrast[:, 1, :]), dim=0)
            previous_max_label = self.cl_memory.label_memory.max()
            labels = self._create_labels(bs, previous_max_label, device=z_contrast.device)
            enqueue_mask = self._create_enqueue_mask(bs, device=z_contrast.device, moco=self.moco)
            loss = self.cl_memory(z_contrast, labels, enqueue_mask=enqueue_mask)
        else:
            loss = self.contrastive_loss_fn(
                z_contrast[:, 0, :],  # aug1 embeddings
                z_contrast[:, 1, :],  # aug2 embeddings
            )
        return loss

    def _sl_loss(
        self,
        x_similarity: Tensor,
        z: Tensor,
        x_samp_similarity: Tensor | None = None,
        z_samp: Tensor | None = None,
    ) -> Tensor | float:
        """Computes similarity loss as the smooth L1 loss between

        - sim_x(x_i, x_j), the similarity/distance of the original time series and
        - sim_z(z_i, z_j), the similarity/distance between their latent representations

        In order to compute sim_x, we use time series similarity measured e.g. by DTW.
        For sim_z we simply compute the Euclidean distance between the latent representations.

        Args:
            x_similarity: similarity matrix between each of the org series (BS, BS)
            z: latent representations of x (BS, D_emb)
            x_samp_similarity: similarity matrix between each of the org series and each of the samples (BS, N_samp)
            z_samp: latent representations of samples (N_samp, D_emb)

        """
        if self.alpha_sl <= 0:
            return 0.0
        n = z.size(0)
        z_similarity = self.emb_distance(z, z)
        # create a mask to select only the lower triangular dist matrix
        mask = torch.tril(torch.ones_like(z_similarity), diagonal=-1).bool()
        z_similarity = torch.masked_select(z_similarity, mask)
        # x_similarity = x_similarity.result()    # get async future results
        x_similarity = x_similarity.to(z.device, dtype=z.dtype)
        x_similarity = torch.masked_select(x_similarity, mask)
        # normalize the x and z similarities (which are actually distances!)
        # because the relative differences are what matters in the optimization
        loss = self.similarity_loss_fn(  # input, target
            self._min_max_norm(z_similarity),
            self._min_max_norm(x_similarity),
        )
        if x_samp_similarity is not None and z_samp is not None:
            n += z_samp.size(0)
            z_samp_similarity = self.emb_distance(z, z_samp.to(z.device))
            mask = torch.tril(torch.ones_like(z_samp_similarity), diagonal=-1).bool()
            z_samp_similarity = torch.masked_select(z_samp_similarity, mask)  # reuse mask
            x_samp_similarity = x_samp_similarity.to(z.device, dtype=z.dtype)
            x_samp_similarity = torch.masked_select(x_samp_similarity, mask)
            # get future result
            loss += self.similarity_loss_fn(self._min_max_norm(x_samp_similarity), self._min_max_norm(z_samp_similarity))
        return loss / n

    def _reg_loss(self, z_norm: Tensor) -> Tensor | float:
        """Regularization loss of norm of the latent embedding vectors."""
        return torch.abs(1.0 - z_norm).mean() if self.alpha_reg > 0 else 0.0

    @staticmethod
    def _create_labels(
        num_pos_pairs: int,
        previous_max_label: int,
        device: torch.device,
    ) -> Tensor:
        """
        Args:
            num_pos_pairs: An integer indicating the number of positive pairs.
            previous_max_label: An integer representing the previous maximum label.
            device: A torch device object specifying the device to be used.

        Returns:
            labels: A tensor containing the created labels representing the positive pairs.

        """
        # create labels that indicate what the positive pairs are
        labels = torch.arange(0, num_pos_pairs, device=device)
        labels = torch.cat((labels, labels))
        # add an offset so that the labels do not overlap with any labels in the memory queue
        labels += previous_max_label + 1
        return labels

    @staticmethod
    def _create_enqueue_mask(
        num_pos_pairs: int,
        device: torch.device,
        moco: bool = False,
    ):
        """
        Args:
            num_pos_pairs: The number of positive pairs to create.
                            Each positive pair consists of a query sample
                            and its corresponding positive sample.
            device: The device on which to create the enqueue mask.
            moco: A boolean indicating whether the method is used for MoCo
                    (Momentum Contrastive Learning) or not. Default is False.

        Returns:
            The enqueue mask, which is a Boolean tensor of size (num_pos_pairs * 2),
            indicating which samples should be enqueued.

        """
        m_size = num_pos_pairs * 2
        if moco:
            # we want to enqueue the output of the momentum updated encoder encK,
            # which is the 2nd half of the batch (at least that is how it was implemented in
            # https://github.com/KevinMusgrave/pytorch-metric-learning/blob/master/examples/notebooks/MoCoCIFAR10.ipynb)
            enqueue_mask = torch.zeros(m_size).bool()
            enqueue_mask[num_pos_pairs:] = True
            raise NotImplementedError
        else:
            enqueue_mask = torch.ones(m_size).bool()
        return enqueue_mask.to(device)

    @staticmethod
    def _min_max_norm(x: Tensor) -> Tensor:
        """Apply min-max normalization to x."""
        mn = torch.min(x)
        return (x - mn) / (torch.max(x) - mn)
