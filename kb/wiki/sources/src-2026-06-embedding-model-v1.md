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

## Relevance to P2

V1 is the **symmetric baseline** P2 must beat. The target change is narrow: replace the SL head (Soft-DTW symmetric, weight 0.7) with an asymmetric directed head trained from Transfer Entropy / Granger soft labels.

| Component | P2 disposition |
|---|---|
| `ConvAttnEncoder` | Reuse (freeze or fine-tune backbone) |
| `RNNAttnDecoder` (GL head) | Reuse |
| `SimMemoryBuffer` | Reuse for directed negative sampling |
| SL head (Soft-DTW) | **Replace with directed asymmetric head** |
| CL head (NT-Xent) | Optional; off by default |
| `GrangerSelector` / `TransferEntropySelector` | Reuse as distillation teacher for soft labels |

The v1 inference API (`model.transform(x)`) is the production contract; P2 v2 must maintain it.

## Related pages

- [sources/src-2026-06-p2-causal-embedding-model](src-2026-06-p2-causal-embedding-model.md) — P2 design framing (asymmetric objective proposal)
- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
- [experiments/exp-p2-causal-retrieval-validation](../experiments/exp-p2-causal-retrieval-validation.md)
