#
import itertools
import logging
import warnings
from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import umap
from matplotlib.pyplot import Axes, Figure
from scipy.stats import ConstantInputWarning, kendalltau, spearmanr
from sklearn.manifold import TSNE
from sklearn.metrics import ndcg_score
from torch import Tensor
from torchmetrics.retrieval import RetrievalMAP

from aid_embedding.clustering import KMeansClustering, compute_clustering_metrics
from aid_embedding.model_wrapper.utils import timed

__all__ = ["compute_ranking_metrics", "compute_mapk", "evaluate_clustering", "evaluate_retrieval", "evaluate_reconstruction"]

logger = logging.getLogger(__name__)
TGT_COLOR = "blue"
NBH_COLOR = "orange"
BG_COLOR = "gray"
MISS_MARKER = "x"
_TIMED = False


def _ndcg_score(gt: np.ndarray, pred: np.ndarray, k: int) -> float | None:
    try:
        return ndcg_score(gt, pred, k=k)
    except ValueError:
        return None


def _rank_tests(gt: np.ndarray, pred: np.ndarray, p_val_threshold: float):
    try:
        tau, p_val_k = kendalltau(gt, pred)
    except ValueError as err:
        logger.error(f"Error in kendalltau: {err}")
        tau = 0.0
    else:
        tau = tau if not np.isnan(tau) and p_val_k < p_val_threshold else 0.0

    try:
        rho, p_val_s = spearmanr(gt, pred)
    except ValueError as err:
        logger.error(f"Error in spearmanr: {err}")
        rho = 0.0
    else:
        rho = rho if not np.isnan(rho) and p_val_s < p_val_threshold else 0.0

    return tau, rho


@timed(enable=_TIMED)
def compute_ranking_metrics(
    gt_ranks: np.ndarray,
    pred_ranks: np.ndarray,
    k: int | None = None,
    p_val_threshold: float = 0.1,
    per_sample: bool = False,
    **kwargs,
) -> dict:
    """Compute different ranking metrics.

    What is considered "good" performance:
        kendall:
            tau > 0.7           is indicating a good level of agreement between the predicted and true rankings.
            0.5 < tau < 0.7     reflects moderate agreement and is often deemed acceptable in real-world ranking tasks.
            tau < 0.5           suggests that the model's ranking performance is suboptimal, requiring refinement.

        spearman:
            r > 0.8           is typically considered strong agreement between rankings.
            0.5 < r < 0.8     suggests moderate agreement, and is generally acceptable,
                              but improvements might be desired.
            r < 0.5           indicates weak correlation, which is usually a sign that the model needs improvement.

        NDCG:
            NDCG > 0.9          is considered excellent performance, indicating that the most
                                relevant items are ranked very high.
            0.8 < NDCG < 0.9    is usually considered good and reflects solid ranking performance,
                                especially in difficult tasks like search or recommendation.
            0.7 < NDCG < 0.8    might be acceptable, depending on the complexity of the task,
                                but there could be room for improvement.
            NDCG < 0.7          indicates a need for model refinement (^= fucking bad!)

    Args:
        gt_ranks: ground truth ranks (BS, N)
        pred_ranks: predicted ranking scores (BS, N)
        k: optional top k to compute ranking metric @ k
        p_val_threshold: significance level threshold for p-value
        per_sample: if flagged, return results on a per-sample basis instead of averaging

    """
    if per_sample:
        ndcg = [_ndcg_score(gt_row[None, :], pred_row[None, :], k=k) for gt_row, pred_row in zip(gt_ranks, pred_ranks, strict=False)]
        ndcg = [v for v in ndcg if v is not None]
    else:
        ndcg = _ndcg_score(gt_ranks, pred_ranks, k=k)

    if k is not None:
        assert isinstance(k, int) and k > 0
        order = np.argsort(-gt_ranks, axis=1)
        gt_ranks = [gt_ranks[i, ordr][:k] for i, ordr in enumerate(order)]
        pred_ranks = [pred_ranks[i, ordr][:k] for i, ordr in enumerate(order)]
    taus, rhos = [], []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ConstantInputWarning)
        for gt_row, pred_row in zip(gt_ranks, pred_ranks, strict=False):
            tau, rho = _rank_tests(gt_row, pred_row, p_val_threshold=p_val_threshold)
            taus.append(tau)
            rhos.append(rho)

    # tau and rho are in [-1, 1], so rescale them to [0, 1]
    taus = np.array(taus) if per_sample else np.nanmean(taus)
    rhos = np.array(rhos) if per_sample else np.nanmean(rhos)
    norm_tau = (taus + 1) / 2
    norm_rho = (rhos + 1) / 2
    combined_rank_score = (norm_tau + norm_rho + ndcg) / 3 if ndcg is not None else (norm_tau + norm_rho) / 2
    at_k = f"@{k}" if k is not None else ""
    out = {
        f"kendall_tau{at_k}": taus,
        f"spearman_rank_corr{at_k}": rhos,
        "combined_rank_score": combined_rank_score,
    }
    if ndcg is not None:
        out[f"ndcg{at_k}"] = ndcg
    return out


@timed(enable=_TIMED)
def compute_mapk(
    x_distance: Tensor,
    z_distance: Tensor,
    k: int,
):
    """Compute the Mean Average Precision at k (MAP@k) score.

    Args:
        x_distance: A tensor representing the distance between the query samples and target samples
                    in the x space (original TS space).
        z_distance: A tensor representing the distance between the query samples and target samples
                    in the z space (latent embedding space).
        k: An integer specifying the number of positions to consider.
            If not provided, all points will be considered.

    Returns:
        The retrieval mean average precision @ k (MAP@k) score.

    """
    if z_distance.isnan().any():
        raise RuntimeError("z_distance contains NaN values")
    if x_distance.isnan().any():
        raise RuntimeError("x_distance contains NaN values")
    bs = x_distance.shape[0]
    # set self distance to inf
    x_distance = x_distance.clone()
    x_distance[torch.eye(bs).bool()] = torch.inf
    z_distance = z_distance.clone()
    z_distance[torch.eye(bs).bool()] = torch.inf
    # convert distance to pseudo probability
    pred = 1.0 / (1.0 + z_distance)
    # get top k indices according to distance between original TS
    # and mark them as targets of the query
    # i.e. we treat the k closest TS in the original space as positive retrievals
    # for the query and all others as negatives
    x_order = torch.argsort(x_distance, dim=1)
    x_top_k_nn = x_order[:, :k]
    tgt = torch.zeros_like(x_distance)
    tgt.scatter_(1, x_top_k_nn, 1)
    tgt = tgt.bool()
    return RetrievalMAP(top_k=k)(pred.view(-1), tgt.view(-1), indexes=torch.arange(bs)[:, None].expand(-1, bs).reshape(-1))


def plot_ts(target_ts: Tensor, neighbour_ts: Tensor, x_dists: Tensor, z_dists: Tensor, show: bool = False, **kwargs):
    """
    Plots the target time series and its nearest neighbours, with distances.

    Args:
        target_ts (Tensor): The target time series of shape (sequence_length,).
        neighbour_ts (Tensor): The time series of nearest neighbours of shape (num_neighbours, sequence_length).
        x_dists (Tensor): Distances between the target and neighbours in the time series space.
        z_dists (Tensor): Distances between the target and neighbours in the embedding space.
        show: flag to directly display the plot using matplotlib

    Returns:
        plt.Figure: The plot showing the target and neighbours.
    """
    num_neighbours = neighbour_ts.shape[0]
    fig, ax = plt.subplots(num_neighbours + 1, 1, figsize=(10, 2 * (num_neighbours + 1)))

    # Plot the target time series
    tgt_ts = target_ts.cpu().numpy()
    ax[0].plot(tgt_ts, label="Target Time Series", color=TGT_COLOR)
    ax[0].set_title("Target Time Series")
    ax[0].legend()

    # Plot each neighbour time series
    nb_ts = neighbour_ts.cpu().numpy()
    for i in range(num_neighbours):
        ax[i + 1].plot(nb_ts[i], label=f"Neighbour {i + 1} | x_dist: {x_dists[i]:.4f}, z_dist: {z_dists[i]:.4f}", color=NBH_COLOR)
        ax[i + 1].set_title(f"Neighbour {i + 1} Time Series")
        ax[i + 1].legend()

    fig.tight_layout()
    if show:
        plt.show()
    return fig


def plot_emb_space(ax: Axes, z_2d: np.ndarray, tgt_idx: int, neighbour_idx: np.ndarray):
    """
    Helper function to plot the embedding space with the target and neighbours.

    Args:
        ax (Axes): Matplotlib axes to plot on.
        z_2d (ndarray): 2D projection of the embedding space.
        tgt_idx (int): Index of the target time series in the embedding space.
        neighbour_idx (ndarray): Indices of the nearest neighbours in the embedding space.
    """
    # Plot all points in the embedding space
    ax.scatter(z_2d[:, 0], z_2d[:, 1], color=BG_COLOR, alpha=0.5, label="Embeddings")

    # Highlight the target point
    ax.scatter(z_2d[tgt_idx, 0], z_2d[tgt_idx, 1], color=TGT_COLOR, label="Target", s=100)

    # Highlight the neighbour points
    ax.scatter(z_2d[neighbour_idx, 0], z_2d[neighbour_idx, 1], color=NBH_COLOR, label="Neighbours", s=100)

    ax.legend()
    ax.grid(True)


def plot_emb(z: Tensor, tgt_idx: int, neighbour_idx: Tensor, reduction_method: str = "tsne", num_workers: int = 4, show: bool = False, **kwargs):
    """
    Plots the 2D projection of the embedding space with the target and its nearest neighbours highlighted.

    Args:
        z (Tensor): Embedding tensor of shape (batch_size, embedding_dim).
        tgt_idx (int): Index of the target time series in the embedding space.
        neighbour_idx (Tensor): Indices of the nearest neighbours in the embedding space.
        reduction_method (str): Dimensionality reduction method to use ("umap", "tsne", "all").
        num_workers (int): Number of parallel workers to use for dimensionality reduction.
        show: flag to directly display the plot using matplotlib

    Returns:
        plt.Figure: The plot showing the embedding space and nearest neighbours.
    """
    # Convert the tensor to a numpy array
    z_np = z.cpu().numpy()
    nb_idx = neighbour_idx.cpu().numpy()
    n = z.shape[0]

    # Prepare the figure based on the reduction method
    if reduction_method == "umap":
        fig, ax = plt.subplots(figsize=(8, 8))
        z_2d = umap.UMAP(random_state=1 if num_workers == 1 else None, n_jobs=num_workers, n_neighbors=max(1, n // 2), **kwargs).fit_transform(z_np)
        ax.set_title("2D Embedding (UMAP)")
        plot_emb_space(ax, z_2d, tgt_idx, nb_idx)
    elif reduction_method == "tsne":
        fig, ax = plt.subplots(figsize=(8, 8))
        z_2d = TSNE(perplexity=max(1, min(n // 2, 45)), n_components=2, random_state=1, n_jobs=num_workers, **kwargs).fit_transform(z_np)
        ax.set_title("2D Embedding (t-SNE)")
        plot_emb_space(ax, z_2d, tgt_idx, nb_idx)
    elif reduction_method == "all":
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        # UMAP
        z_2d_umap = umap.UMAP(random_state=1 if num_workers == 1 else None, n_jobs=num_workers, n_neighbors=max(1, n // 2), **kwargs).fit_transform(z_np)
        axes[0].set_title("2D Embedding (UMAP)")
        plot_emb_space(axes[0], z_2d_umap, tgt_idx, nb_idx)
        # t-SNE
        z_2d_tsne = TSNE(perplexity=max(1, min(n // 2, 45)), n_components=2, random_state=1, n_jobs=num_workers, **kwargs).fit_transform(z_np)
        z_2d_tsne = z_2d_tsne.to_numpy() if isinstance(z_2d_tsne, pd.DataFrame) else z_2d_tsne
        axes[1].set_title("2D Embedding (t-SNE)")
        plot_emb_space(axes[1], z_2d_tsne, tgt_idx, nb_idx)
    else:
        raise ValueError(f"Unknown reduction method: {reduction_method}")

    fig.tight_layout()
    if show:
        plt.show()
    return fig


@timed(enable=_TIMED)
def evaluate_retrieval(
    x: Tensor, z: Tensor, x_distance: Tensor, z_distance: Tensor, num_targets: int = 3, num_neighbours: int = 4, reduction_method: str = "all", plot_x: bool = True, plot_z: bool = True, show: bool = False, **kwargs
) -> tuple[list[Figure], list[Figure]]:
    """
    Evaluates and visualizes the retrieval of nearest neighbors based on time series and embedding distances.

    This function retrieves the nearest neighbors of each target time series based on distances in the
    embedding space. It plots the nearest neighbors of each target time series and their corresponding distances.
    Additionally, it can project the embedding space to 2D and highlight the neighbors for each target
    time series using UMAP or t-SNE.

    Args:
        x (Tensor):
            A tensor of shape `(batch_size, sequence_length, ...)` representing the time series data.
        z (Tensor):
            A tensor of shape `(batch_size, embedding_dim)` representing the latent space embeddings.
        x_distance (Tensor):
            A tensor of shape `(batch_size, batch_size)` representing pairwise distances between time series.
        z_distance (Tensor):
            A tensor of shape `(batch_size, batch_size)` representing pairwise distances in the embedding space.
        num_targets (int, optional):
            The number of target time series to retrieve neighbors for. Defaults to 3.
        num_neighbours (int, optional):
            The number of nearest neighbors to retrieve for each target time series. Defaults to 4.
        reduction_method (str, optional):
            The dimensionality reduction method for projecting the embedding space. Options are "umap",
            "tsne", or "all" to plot both. Defaults to "all".
        plot_x (bool, optional):
            Whether to plot the time series and their neighbors. Defaults to True.
        plot_z (bool, optional):
            Whether to plot the 2D projection of the embedding space with highlighted neighbors. Defaults to True.
        show (bool, optional):
            Whether to display the plots directly. Defaults to False.
        **kwargs:
            Additional keyword arguments passed to the `plot_ts` and `plot_emb` functions.

    Returns:
        Tuple[List[Figure], List[Figure]]:
            A tuple of two lists containing:
            - `tgt_neighbour_plots`: List of figures plotting each target time series and its neighbors in
              the time series space.
            - `z_space_emb_plots`: List of figures plotting the 2D projection of the embedding space and
              highlighting the target and its nearest neighbors.
    """
    if z_distance.isnan().any():
        raise RuntimeError("z_distance contains NaN values")
    if x_distance.isnan().any():
        raise RuntimeError("x_distance contains NaN values")
    x = x.squeeze()
    bs, t = x.shape
    # set self distance to inf
    z_distance = z_distance.clone()
    z_distance[torch.eye(bs).bool()] = torch.inf

    # validate num targets and num neighbours
    if num_targets < bs:
        x_tgt = x[:num_targets]
        x_distance = x_distance[:num_targets]
        z_distance = z_distance[:num_targets]
    else:
        x_tgt = x.clone()
    if num_neighbours > bs - 1:
        raise RuntimeError(f"batch of size {bs} is to small to produce valid neighbours.")

    # get top k neighbour indices according to latent vectors
    z_order = torch.argsort(z_distance, dim=1)
    top_k_nn = z_order[:, :num_neighbours]
    # select distances and neighbours
    z_dists = z_distance.gather(dim=1, index=top_k_nn)
    x_dists = x_distance.gather(dim=1, index=top_k_nn)
    x_neighbours = x.gather(dim=0, index=top_k_nn.reshape(-1)[:, None].expand(-1, t)).view(num_targets, num_neighbours, t)

    # create plots of each time series in x_tgt and its neighbours
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        tgt_neighbour_plots = []
        if plot_x:
            tgt_neighbour_plots = [plot_ts(x_tgt[i], x_neighbours[i], x_dists[i], z_dists[i], show=show, **kwargs) for i in range(num_targets)]
        # for each target time series in x_tgt create a plot of latent space z. highlighting its neighbours
        z_space_emb_plots = []
        if plot_z:
            z_space_emb_plots = [plot_emb(z, tgt_idx=i, neighbour_idx=top_k_nn[i], reduction_method=reduction_method, show=show, **kwargs) for i in range(num_targets)]

    return tgt_neighbour_plots, z_space_emb_plots


def plot_ts_recon(
    x_org: np.ndarray,
    x_hat: np.ndarray,
    mask: np.ndarray,
    show: bool = False,
):
    """Plotting helper function."""
    fig, ax = plt.subplots(figsize=(12, 6))
    # Plot original and reconstructed signals
    x_hat[~mask] = np.nan
    x_org_masked = x_org.copy()
    x_org_masked[~mask] = np.nan
    x_org_else = x_org.copy()
    x_org_else[mask] = np.nan
    ax.plot(x_org, color=TGT_COLOR, alpha=0.15)
    ax.plot(x_org_masked, color=TGT_COLOR, linestyle="dotted", marker=MISS_MARKER, label="Original masked")
    ax.plot(x_org_else, color=TGT_COLOR, marker=".", label="Original")
    ax.plot(x_hat, color=NBH_COLOR, marker=MISS_MARKER, label="Reconstructed")

    # Highlight by changing background color of the masked parts
    mask_indices = np.where(mask == 1)[0]
    n = 0
    for start, end in itertools.pairwise(mask_indices):
        n += 1
        if start + 1 != end:
            if n == 1:
                ax.axvspan(start - 0.4, start + 0.4, facecolor=BG_COLOR, alpha=0.2)
            n = 0
            continue
        ax.axvspan(start, end, facecolor=BG_COLOR, alpha=0.2)

    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.set_title("Time Series Reconstruction")
    # ax.legend(handles=handles, labels=labels)
    ax.legend()

    fig.tight_layout()
    if show:
        plt.show()
    return fig


@timed(enable=_TIMED)
def evaluate_reconstruction(
    x_org: Tensor,
    x_hat: Tensor,
    mask: Tensor,
    num_plot: int = 5,
    show: bool = False,
):
    """
    Args:
        x_org: The original tensor of shape (batch_size, T).
        x_hat: The reconstructed tensor of shape (batch_size, T).
        mask: The mask tensor of shape (batch_size, T).
        num_plot: The number of time series to plot. Defaults to 3.
        show: A boolean indicating whether to display the plotted figures (default=False).

    Returns:
        A list of plotted time series reconstructions.

    """
    # Convert tensors to numpy arrays
    x_org = x_org.squeeze().cpu().numpy()
    x_hat = x_hat.squeeze().cpu().numpy()
    mask = mask.squeeze().cpu().numpy()
    n = int(min(num_plot, len(x_org)))
    return [plot_ts_recon(x_org[i], x_hat[i], mask[i], show=show) for i in range(n)]


def evaluate_clustering(z: Tensor, ks: Sequence[int] | None = None, seed: int = 666, **kwargs) -> dict:
    """
    Compute clustering metrics for given tensor `z` over specified cluster sizes `ks`.

    This function performs KMeans clustering on the input tensor `z` for each
    cluster size provided in `ks`. If `ks` is not specified, it automatically
    selects a range of cluster sizes based on the batch size of `z`. Clustering
    results are then evaluated and averaged to produce aggregated metrics.

    Args:
        z: Tensor containing the data points to cluster.
        ks: Sequence of integers specifying the number of clusters to test.
        seed: Random seed for reproducibility.
        **kwargs: Additional keyword arguments for the KMeansClustering class.

    Returns:
        Dict: Aggregated clustering metrics over the specified cluster sizes.
    """
    z_array = z.cpu().numpy()
    d_emb = z.shape[1]
    if ks is None or len(ks) == 0:
        # select some ks based on batch size
        n = z_array.shape[0]
        if n < 32:
            raise RuntimeError(f"z has only {n} elements, cannot select ks automatically. Please specify ks manually.")
        ks = list({max(4, n // (2**i)) for i in range(3, 7)})
        ks.sort()

    metrics = []
    for k in ks:
        kmeans = KMeansClustering(input_dim=d_emb, cluster_dim=min(d_emb, 128), k=k, center_init_method="random", seed=seed, verbose=False, **kwargs)
        results = kmeans.fit(z_array, assign_labels=True)
        metrics.append(compute_clustering_metrics(x=z_array, result=results, seed=seed, n_digits=10, **kwargs))
    mtrs = list(metrics[0].keys())
    # average over different ks
    aggr_metrics = {}
    for m in mtrs:
        aggr_metrics[m] = float(np.mean([vals[m] for vals in metrics]))

    return aggr_metrics
