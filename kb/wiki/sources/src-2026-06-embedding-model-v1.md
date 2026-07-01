---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-embedding-model-v1
tags:
- embedding
- ssl
- production
- v1
source_hash: 1f2f0070d33561e626ebcdfb977ae834e0a5f854d745c6f3ac5566839b977b80
---

# Source: Embedding model v1 — production architecture context

## Metadata

- Source ID: `src-2026-06-embedding-model-v1`
- Raw path: `raw/seed/embedding_model_v1_context.md`
- Source type: seed implementation context (production repo)
- Date: June 2026
- Relevant projects: P2 (v1 is the symmetric baseline; P2 replaces the SL head with a directed asymmetric objective)

## One-line takeaway

V1 is a production symmetric SSL embedding model (ConvAttnEncoder + three SSL heads) whose SL head (Soft-DTW similarity, weight 0.7) is P2's direct upgrade target — P2 replaces symmetric Soft-DTW with a directed Transfer-Entropy/Granger objective while reusing the backbone, GL head, and SimMemoryBuffer.

## Architecture

**Model class:** `SSLModel` (`src/core_model/model.py`)

**Encoder: `ConvAttnEncoder`**
- TCN (temporal convolutional network) → multi-head attention → meanmax pooling
- Output: `z` (128-dim pooled, for retrieval) + `z_seq` (sequential, for decoder input)
- INPUT_DIM=1, HIDDEN_DIM=128, EMB_DIM=128, MAX_SEQ_LEN=180

**Decoder: `RNNAttnDecoder`**
- sLSTM + cross-attention; reconstructs masked timesteps from `z_seq`
- Used only by the GL head during training; not deployed at inference

**Alternative encoders (not default):** DualConvAttnEncoder, RNNEncoder, FFTRNNEncoder, RTDRNNEncoder

## SSL objectives

| Head | Paradigm | Loss | Default weight | Purpose |
|---|---|---|---|---|
| GL | Generative | MSE on masked tokens | 0.3 | Reconstruction / imputation |
| SL | Structural | SmoothL1(Soft-DTW_x, L2_z) | 0.7 | Preserve shape-similarity structure |
| CL | Contrastive | NT-Xent τ=0.07 | 0.0 (off) | Augmentation invariance |
| REG | Regulariser | L2 norm | 0.0001 | Unit-norm embeddings |

**GL head:** 30% masking + 25% batch reserved for 6-step forecast; `RNNAttnDecoder` reconstructs from `z_seq`.

**SL head:** Soft-DTW (differentiable, Sakoe-Chiba bandwidth) in x-space; L2 in z-space. `SimMemoryBuffer` groups `(x, z)` pairs by length bin so negatives are always same-length across batches. GPU-accelerated via Triton.

**CL head:** NT-Xent with 10+ augmentations; `x_contrast` shape is `(BS, 2, T, 1)`. Off by default in production.

## Data pipeline

- Format: Parquet, length-binned under `data/`
- Dataset/loader: `BinnedTSDataset` + `ContinuousDataLoader`
- Normalization: per-series z-score (mean=0, std=1) at load time
- Batch size: TRAIN_BS=512

## Training configuration

- Optimizer: Adam, lr=5e-4
- Scheduler: `PlateauCycleLRScheduler` — ReduceLROnPlateau (patience=3, factor=0.5) + triangular2 cycling
- Precision: bfloat16-mixed
- Gradient clipping: 0.99
- Max epochs: 99
- Monitor metric: `val_combined_rank_score`

## Evaluation KPIs (production targets)

| Metric | Target |
|---|---|
| MAP@50 | > 0.95 |
| combined_rank_score | > 0.925 |
| reconstruction_error | < 0.31 |
| Kendall's τ | (ranked retrieval agreement) |
| Spearman ρ | (ranked retrieval agreement) |
| NDCG@k | (ranked retrieval quality) |

## Inference API

```python
z = model.transform(x)                      # (BS, T, 1) → (BS, 128)
x_hat, mask = model.reconstruct(x)          # impute NaN values
z, x_hat, mask = model.transform_and_reconstruct(x)
```

## Key design decisions

| Decision | Choice | Rationale |
|---|---|---|
| x-space similarity | Soft-DTW (not Euclidean) | Handles variable lengths and temporal warping |
| Negative sampling | Length-binned via `SimMemoryBuffer` | Prevents series length as spurious similarity feature |
| Decoder RNN cell | sLSTM (not LSTM) | Simpler, better gradient flow |
| Pooling | MeanMax | Captures both average (smooth trends) and peak (spiky events) |
| Encoder | TCN + MHA | Local patterns (TCN) + long-range dependencies (attention) |
| Pretext task | Masked reconstruction (not global AE) | Explicitly forces handling missing values |

## Relevance to P1

V1 embeddings enable a **two-stream P1 architecture** where the selection layer gets rich representation for free and the backbone can remain shallow:

| P1 role | How v1 is used |
|---|---|
| FAISS cluster routing | `z_target = model.transform(target)` → nearest cluster prototype |
| Covariate selection query | `z_target` (projected or direct) as the query vector |
| Covariate selection keys | `z_cov_k = model.transform(cov_k)` as per-covariate key vectors |
| Selection semantics | Soft-DTW structural similarity: "covariates whose dynamics resemble the target" |
| Shallow backbone justification | v1 handles representational heavy lifting; backbone only needs temporal dynamics at forecast resolution (1-2 layer TCN/patch encoder) |

**Why v1 is a good covariate prior for P1:** The SL head (Soft-DTW, weight 0.7) trains the embedding space to map structurally similar series to nearby vectors — this is exactly the structural relevance prior needed for covariate selection. The L2 norm regularization makes embeddings near-unit-norm, so cosine similarity is directly applicable without a learned projection (though a projection W ∈ ℝ^{d_sel × 128} remains an option).

**Phase 0 → Phase 1 upgrade path:** When P2's directed embeddings are ready, replace `z_cov_k` with P2 directed embeddings at the covariate key interface only. The selection mechanism (projection, α-entmax, AttGrad), the backbone, and the inference API are unchanged.

## Relevance to P2 — implementation delta (from code review, 2026-07-01)

V1 bakes in symmetry in three specific places in the SL loss pipeline. P2 changes exactly these three, adds dual projection heads, and adds a second FAISS index. Everything else is reused.

### Three symmetry assumptions that must change

**1. `TorchSoftDTW._forward(symmetric=True)` — `ts_similarity.py:152–169`**
When called with `x is y` and `symmetric=True`, computes only upper triangle via `torch.triu_indices`, mirrors to lower. Valid for DTW; invalid for TE. P2 replaces `TorchSoftDTW` with a `TorchTransferEntropy` (or `TorchGranger`) class that always computes the full NxN matrix — the existing `soft_dtw()` helper (lines 178–192) already does this when `symmetric=False`.

**2. `SimMemoryBuffer.compute_sim()` — `ts_similarity.py:325`**
`sim_fn.forward(x, x, symmetric=True)` hardcoded. Change to `symmetric=False`.

**3. `_sl_loss()` mask — `pl_model.py:936–937`**
`mask = torch.tril(torch.ones_like(z_similarity), diagonal=-1).bool()` — selects only lower triangle (unique pairs for symmetric matrix). For directed matrix, change to:
`mask = ~torch.eye(n, n, dtype=torch.bool, device=z_similarity.device)` — all off-diagonal pairs (includes both i→j and j→i).

### One model addition: dual projection heads

`_sl_loss` currently computes:
```python
z_similarity = self.emb_distance(z, z)    # LpDistance — symmetric
```
P2 adds `W_src, W_tgt: nn.Linear(128, 128, bias=False)` to `SSLModel`. The directed distance matrix becomes:
```python
directed_dist[i, j] = ||W_src(z_i) − W_tgt(z_j)||₂
```
Asymmetric because `W_src(z_i)` encodes the "source/cause" role and `W_tgt(z_j)` the "target/effect" role — `directed_dist[i,j] ≠ directed_dist[j,i]`.

### Inference API and FAISS index

`model.transform(x) → z (BS, 128)` is unchanged. Role projection at query time:
- "What drives T?": `q = W_tgt @ z_T`, KNN over `src_index` (candidates projected via `W_src`)  
- "What does S drive?": `q = W_src @ z_S`, KNN over `tgt_index` (candidates projected via `W_tgt`)

Two FAISS indices built offline from the shared `z`. `SimMemoryBuffer` storage `(x, z)` is unchanged — projections applied at loss-compute time, not stored.

| Component | V1 | P2 change |
|---|---|---|
| `ConvAttnEncoder` | base encoder | reuse unchanged |
| GL head + `RNNAttnDecoder` | masked reconstruction | reuse unchanged |
| `SimMemoryBuffer` | `(x, z)` length-binned buffer | reuse unchanged |
| `TorchSoftDTW` | `symmetric=True` NxN shortcut | replace with `TorchTransferEntropy` (full NxN) |
| `compute_sim` | `sim_fn.forward(x, x, symmetric=True)` | → `symmetric=False` |
| `_sl_loss` mask | `torch.tril` (lower triangle only) | → `~torch.eye` (all off-diagonal) |
| z-space distance | `LpDistance(z, z)` — symmetric | → `directed_dist(W_src(z), W_tgt(z))` |
| `SSLModel` | no projection heads | add `W_src`, `W_tgt: Linear(128, 128, bias=False)` |
| FAISS index | single symmetric | two: `src_index`, `tgt_index` |
| Inference API | `model.transform(x) → z` | unchanged |

## Related pages

- [sources/src-2026-06-p2-causal-embedding-model](src-2026-06-p2-causal-embedding-model.md) — P2 design framing (asymmetric objective proposal)
- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
- [experiments/exp-p2-causal-retrieval-validation](../experiments/exp-p2-causal-retrieval-validation.md)
