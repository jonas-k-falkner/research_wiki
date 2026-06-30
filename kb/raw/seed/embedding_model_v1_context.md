# Repository Context: `embedding_model v1 (similarity-based)`
 
**Project**: Self-supervised time series embedding model for univariate time series. Learns 128-dim embeddings that preserve similarity structure, enable reconstruction of missing values, and are useful for retrieval, clustering, anomaly detection, and classification.
 
---
 
## Architecture
 
**Framework**: PyTorch + PyTorch Lightning, Hydra config, MLFlow logging.
 
**Core class**: `SSLModel` (`src/core_model/model.py`) — encoder-decoder architecture with three SSL heads.
 
**Default encoder**: `ConvAttnEncoder` — TCN (temporal convolutional network) feature extractor → multi-head attention stack → meanmax pooling → two outputs: `z` (pooled, 128-dim) and `z_seq` (sequential for decoder).
 
**Default decoder**: `RNNAttnDecoder` — sLSTM (simplified LSTM) + cross-attention, reconstructs masked regions.
 
**Alternative encoders**: `DualConvAttnEncoder` (TCN+FFT dual-branch), `RNNEncoder`, `FFTRNNEncoder`, `RTDRNNEncoder`.
 
**Key dims**: `INPUT_DIM=1`, `HIDDEN_DIM=128`, `EMB_DIM=128`, `MAX_SEQ_LEN=180`.
 
---
 
## Three SSL Objectives (combined as weighted sum)
 
| Paradigm | Loss | Weight (default sl_gl) | Purpose |
|---|---|---|---|
| **GL** (Generative Learning) | MSE on masked regions | 0.3 | Reconstruction / missing value imputation |
| **SL** (Similarity Learning) | SmoothL1 between DTW(x-space) and L2(z-space) | 0.7 | Preserve series relationships |
| **CL** (Contrastive Learning) | NT-Xent, τ=0.07 | 0.0 (off in default) | Augmentation invariance |
| **REG** | L2 norm regularization | 0.0001 | Encourage unit-norm embeddings |
 
**Config variants**: `sl_gl` (default), `sl`, `gl`, `cl`, `all` (all three), `sl_gl_v2/v3`.
 
---
 
## Generative Learning (GL) — Ti-MAE inspired
 
- Random masking: 30% of timesteps masked per sample
- Forecast ratio: 25% of batch reserved for future-step prediction (6 steps ahead)
- Mask applied to encoder input; decoder reconstructs masked positions from `z_seq`
- Enables `model.reconstruct(x)` for imputing NaN values at inference
---
 
## Similarity Learning (SL) — Series2Vec inspired
 
- Computes **Soft DTW** distance matrix in x-space (differentiable, Sakoe-Chiba bandwidth)
- Computes L2 distance matrix in z-space
- Loss: align normalized z-distances to normalized x-distances
- **SimMemoryBuffer**: maintains history of (x, z) pairs grouped by sequence-length bin; samples same-length negatives across batches for harder training signal
- GPU-accelerated DTW via Triton kernels
---
 
## Contrastive Learning (CL) — MoCo/TS-TCC inspired
 
- NT-Xent loss with temperature 0.07
- 10+ augmentations: jitter, scale, time-warp, shift, flip, blur, smooth, point dropout, sequence dropout
- `x_contrast` shape: `(BS, 2, T, 1)` — two augmented views per sample
---
 
## Data Pipeline
 
- **Format**: Parquet files organized in length bins: `data/{train,val,test}/bin_<start>_<end>/`
- **`BinnedTSDataset`**: Iterable dataset; async parquet loading (`ContinuousDataLoader`)
- **Preprocessing**: per-series standardization (mean=0, std=1); optional imputation
- **Length bins**: prevents length becoming a spurious discriminative feature; enables same-length negative sampling
- **Batch size**: `TRAIN_BS=512`, `EVAL_BS=256`
---
 
## Training Setup
 
- **Optimizer**: Adam, lr=5e-4
- **Scheduler**: `PlateauCycleLRScheduler` — ReduceLROnPlateau (patience=3, factor=0.5) + triangular2 cycling (cycle_len=10)
- **Monitor metric**: `val_combined_rank_score` (maximize)
- **Precision**: bfloat16-mixed
- **Gradient clipping**: 0.99 (L2 norm)
- **Max epochs**: 99
- **Checkpointing**: top-2 by `val_combined_rank_score` + last
---
 
## Inference API
 
```python
z = model.transform(x)                        # (BS, T, 1) → (BS, 128)  encoder only
x_hat, mask = model.reconstruct(x)            # impute NaN values
z, x_hat, mask = model.transform_and_reconstruct(x)
```
 
---
 
## Evaluation Metrics
 
- **Ranking**: Kendall's τ, Spearman ρ, NDCG@k — compare rank order in x-space vs z-space
- **Retrieval**: MAP@50 — mean average precision of true neighbors
- **Clustering**: Silhouette, Davies-Bouldin, Calinski-Harabasz on z embeddings
- **Reconstruction**: MSE on masked regions (GL)
- **Target KPIs**: MAP@50 > 0.95, combined_rank_score > 0.925, reconstruction_error < 0.31
---
 
## Key Files
 
| File | Role |
|---|---|
| `src/core_model/model.py` | `SSLModel` — forward, encode, decode, masking, inference |
| `src/core_model/models/encoders.py` | `ConvAttnEncoder`, `DualConvAttnEncoder`, etc. |
| `src/core_model/models/decoders.py` | `RNNAttnDecoder`, `RNNDecoder`, etc. |
| `src/core_model/blocks/` | `SLSTMBlock`, `HGRNBlock`, `RNNBlock` |
| `src/model_wrapper/pl_model.py` | `PLModel` — Lightning wrapper, all loss computation |
| `src/model_wrapper/ssl/ts_similarity.py` | `TorchSoftDTW`, `SimMemoryBuffer` |
| `src/model_wrapper/ssl/augmentations.py` | `TSAugmentor` — 10+ TS augmentations |
| `src/model_wrapper/ssl/evaluation.py` | All evaluation metrics |
| `src/model_wrapper/utils/ts_dataset.py` | `BinnedTSDataset`, `ContinuousDataLoader` |
| `src/model_wrapper/utils/lr_schedule.py` | `PlateauCycleLRScheduler` |
| `conf_model/` | Hydra configs (meta, encoder, decoder, ssl) |
| `run_emb_model.py` / `run_emb_model.sh` | Training entry point |
 
---
 
## Design Decisions Summary
 
- **Hybrid SSL** (GL+SL+CL): complementary objectives; GL handles missing data, SL preserves structure, CL enforces invariance
- **Soft DTW** (not Euclidean) for x-space similarity: handles variable lengths and temporal warping
- **Length-binned data**: prevents length as spurious feature; enables same-length negative sampling in SL
- **sLSTM over LSTM**: simpler, better gradient flow
- **MeanMax pooling**: captures both average (smooth) and peak (spiky) temporal features
- **TCN + Attention**: TCN for local patterns, attention for long-range dependencies
- **Masked reconstruction** (not global AE): forces model to handle missing values explicitly

