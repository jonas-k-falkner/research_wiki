---
type: project
domain: embedding-models
project: P2
status: active
stage: seed
confidence: medium
updated: 2026-07-01
sources:
- src-2026-06-p2-causal-embedding-model
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-eldele-ts-tcc
- src-2026-06-yue-ts2vec
- src-2026-06-li-ti-mae
- src-2026-06-cheng-timemae
- src-2026-06-foumani-series2vec
- src-2026-06-choi-multitask-ssl
- src-2026-06-eldele-ca-tcc
- src-2026-06-eldele-label-efficient-review
- src-2026-06-jawed-ssl-semisupervised
- src-2026-06-yang-timeclr
- src-2026-06-fraikin-trep
- src-2026-06-talukder-totem
- src-2026-06-he-moco
- src-2026-06-kazemi-time2vec
- src-2026-06-musgrave-metric-learning-reality
- src-2026-06-liu-ssl-comparison
- src-2026-06-ericsson-ssl-survey
- src-2026-06-liu-ssl-medical-review
- src-2026-06-um-wearable-augmentation
- src-2026-06-lewis-bart
- src-2026-06-pascual-speech-ssl
- src-2026-06-embedding-model-v1
tags:
- embeddings
- causality
- covariate-retrieval
- ssl
---

# P2 — Causal embedding model v2

## Purpose

Retrain the time-series embedding model with a directed, asymmetric objective so that vector proximity approximates causal influence rather than only shape similarity. At inference time, embed a target series and retrieve high-impact covariates from a large candidate universe using vector search.

## Current thesis

P2 is a research moat and P1 enabler. It should run as a parallel research thread, not block P3 delivery. Its first validation should combine retrieval metrics with downstream forecasting improvements in P1-like tasks.

## Chosen design paradigm (decided 2026-07-01)

P2's directed objective uses a **Series2Vec-style similarity-preserving pretext task** — not knowledge distillation. This is a direct extension of v1's SL head:

- V1 SL head: train z-space to preserve pairwise Soft-DTW distances → `SmoothL1(Soft-DTW(x_A, x_B), ||z_A − z_B||)` → symmetric by construction (DTW(A,B) = DTW(B,A))
- P2 SL head: same paradigm, replace Soft-DTW with Transfer Entropy or Granger causality as the pairwise similarity target → `loss(TE(x_A→x_B), directed_dist(z_A, z_B))` → asymmetric because TE(A→B) ≠ TE(B→A)

The full **asymmetric pairwise similarity matrix** M where M_{ij} = TE(x_i → x_j) becomes the training target. The z-space distance function must therefore also be directed — this requires separate source/target projections (z_src, z_tgt) or an explicit asymmetric distance function so that sim(z_A_src, z_B_tgt) ≠ sim(z_B_src, z_A_tgt).

**Why this is simpler than knowledge distillation:** TE/Granger scores are used directly as pairwise labels in the similarity objective — no teacher model, no two-stage training, no logit matching. The mechanism is identical to Series2Vec's Eq. 3, with the similarity function swapped.

```text
sample series pairs (length-binned via SimMemoryBuffer)
  → compute TE(x_i → x_j) scores for batch pairs
  → supervised-similarity loss: directed z-space distance ≈ TE score
  → index 200M embeddings at inference
  → query target series
  → retrieve top-k causal drivers (A→target)
  → feed covariates into P1 selector or P3/P4 explanation layers
```

**Key open question:** Whether TE/Granger can be computed efficiently at batch-training granularity, or whether a precomputed lookup table is needed. The `GrangerSelector` / `TransferEntropySelector` components in v1 are the label generators for this matrix.

## Conceptual sources for v1 and P2 learning paradigm

V1's learning paradigm is built from two papers. P2 extends the same paradigm with an asymmetric target:

| Paper | Role in v1 | Role in P2 |
|---|---|---|
| **Series2Vec** (Foumani et al. 2024, DMKD) — [src-2026-06-foumani-series2vec](../sources/src-2026-06-foumani-series2vec.md) | SL head design: similarity-preserving pretext with Soft-DTW as pairwise target. Replaces augmentation-based contrastive. V1's SL head (Eq. 3) directly implements this. | Direct predecessor of P2's directed SL head. Same loss structure; symmetric Soft-DTW replaced with asymmetric TE/Granger matrix. |
| **Ti-MAE** (Li et al. 2023, ICLR workshop) — [src-2026-06-li-ti-mae](../sources/src-2026-06-li-ti-mae.md) | GL head design: masked autoencoder paradigm (75% masking → reconstruction forces global temporal context rather than local autocorrelation). V1's GL head is a MAE-style masked reconstruction objective. | GL head reused unchanged. Indirectly validates MAE as a distribution-shift-robust pretraining stage for non-stationary commodity series. |

Together: Series2Vec → SL head (weight 0.7, dominant objective); Ti-MAE → GL head (weight 0.3, auxiliary reconstruction). P2 changes the SL head only; the GL head, encoder, and data pipeline remain.

## V1 production baseline (I-P2-v1, 2026-06-30)

V1 is a production symmetric SSL embedding model. P2 v2 is a **minimal surgical change** to v1: replace the SL head (Soft-DTW symmetric) with a directed asymmetric head. All other components are reused. See [sources/src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md).

**Encoder:** `ConvAttnEncoder` — TCN → multi-head attention → meanmax pooling → `z` (128-dim, for retrieval) + `z_seq` (sequential, for decoder). INPUT_DIM=1, HIDDEN_DIM=128, EMB_DIM=128, MAX_SEQ_LEN=180.

**SSL heads (default weights):**

| Head | Loss | Weight | Purpose |
|---|---|---|---|
| GL | MSE on 30% masked tokens | 0.3 | Reconstruction / imputation |
| SL | SmoothL1(Soft-DTW_x, L2_z) | **0.7** | Shape similarity — **P2 replaces this** |
| CL | NT-Xent τ=0.07 | 0.0 (off) | Augmentation invariance |

**`SimMemoryBuffer`** groups `(x, z)` pairs by length bin, providing same-length negatives across batches. Reused by P2's directed negative sampling.

**Production KPIs (v1):** MAP@50 > 0.95, combined_rank_score > 0.925, reconstruction_error < 0.31.

**Inference API (must be preserved by P2 v2):**
```python
z = model.transform(x)                      # (BS, T, 1) → (BS, 128)
x_hat, mask = model.reconstruct(x)          # impute NaN values
z, x_hat, mask = model.transform_and_reconstruct(x)
```

**P2 component disposition:**

| Component | P2 action |
|---|---|
| `ConvAttnEncoder` | Reuse (freeze or fine-tune) |
| GL head + `RNNAttnDecoder` | Reuse |
| `SimMemoryBuffer` | Reuse for directed negative sampling |
| SL head (Soft-DTW) | **Replace with directed TE/Granger head** |
| `GrangerSelector` / `TransferEntropySelector` | Label generator for the asymmetric pairwise similarity matrix (not a distillation teacher — scores are used directly as similarity targets) |

## Implementation design (from code review, 2026-07-01)

V1 implementation is in `raw/code/embedding_model_v1/`. P2 is a minimal surgical delta — three places where v1 bakes in symmetry, plus one model addition for directed z-space.

### Where symmetry lives in v1 (all three must change)

**1 — `TorchSoftDTW._forward(symmetric=True)` — `ts_similarity.py:152–169`**
When `symmetric=True` and `x is y`, v1 computes only the upper triangle via `torch.triu_indices` and mirrors to the lower triangle. This is a valid O(N²/2) shortcut for DTW because DTW(A,B) = DTW(B,A). For P2, TE(A→B) ≠ TE(B→A) — the full NxN matrix is required. Replace with a `TorchTransferEntropy` (or `TorchGranger`) class that computes the full asymmetric pairwise matrix. The `soft_dtw()` helper already computes full NxN when called with `symmetric=False` (the expand-broadcast path at lines 178–192); the new TE class follows the same shape contract.

**2 — `SimMemoryBuffer.compute_sim()` — `ts_similarity.py:325`**
Hard-codes `sim_fn.forward(x, x, symmetric=True)`. Change to `symmetric=False`. The return signature `(x_similarity, x_sample_similarity, z_sample_sim)` is unchanged — `x_similarity` becomes `(BS, BS)` full asymmetric matrix instead of upper-triangle-mirrored symmetric matrix.

**3 — `_sl_loss()` lower-triangular mask — `pl_model.py:936–937`**
```python
mask = torch.tril(torch.ones_like(z_similarity), diagonal=-1).bool()
```
This extracts only unique pairs from the lower triangle — correct for symmetric matrices where lower ≡ upper. For P2, the directed pair (i→j) carries different information than (j→i). Change to the full off-diagonal mask:
```python
mask = ~torch.eye(n, n, dtype=torch.bool, device=z_similarity.device)
```
This preserves both M[i,j] and M[j,i] in the loss. The loss normalization divides by `n` — with the full matrix it now covers `n*(n-1)` pairs rather than `n*(n-1)/2`.

### Making z-space directed (one model addition)

**Dual projection heads: `W_src` and `W_tgt`**

Currently `_sl_loss` computes z-space distance as:
```python
z_similarity = self.emb_distance(z, z)   # LpDistance(p=2, normalize_embeddings=True)
```
This is symmetric: `d(z_i, z_j) = d(z_j, z_i)`. To make it directed, add two thin linear heads — source projection and target projection — applied on top of the shared z:
```python
z_src = W_src(z)   # shape: (BS, D_proj) — "cause" role
z_tgt = W_tgt(z)   # shape: (BS, D_proj) — "effect" role
```
Then the directed distance matrix is:
```python
directed_dist[i, j] = ||W_src(z_i) − W_tgt(z_j)||₂
```
This gives `directed_dist[i,j] ≠ directed_dist[j,i]` because the source/target roles are different.

`W_src` and `W_tgt` are `nn.Linear(D_emb, D_proj, bias=False)` heads added to `SSLModel` (or kept in `PLModel`). `D_proj = D_emb = 128` is the natural first choice. The base encoder `ConvAttnEncoder` and its `z` output are unchanged.

### Query process (inference)

The `model.transform(x) → z (BS, 128)` API is unchanged. The role projection is a post-inference step:

| Query | Operation | Index |
|---|---|---|
| "What drives target T?" | `q = W_tgt @ z_T` | search `src_index` (all candidates encoded via `W_src`) |
| "What does source S drive?" | `q = W_src @ z_S` | search `tgt_index` (all candidates encoded via `W_tgt`) |

Two FAISS indices replace the single v1 index. Both are built offline once; the base `z` is shared. Candidates are indexed under both their source projection (for "what does this drive?" queries) and their target projection (for "what drives this?" queries).

### What the SimMemoryBuffer does not need to change

`SimMemoryBuffer` stores `(x, z)` pairs and samples by length bin — both unchanged. The projections `W_src`, `W_tgt` are applied at compute time inside `_sl_loss`, not stored in the buffer. `memory.add(x_sim, z_sim)` and `memory.sample(t, n)` are unmodified.

### Summary delta

| Component | V1 state | P2 change |
|---|---|---|
| `TorchSoftDTW` (or new TE class) | `symmetric=True` shortcut | `symmetric=False` — full NxN or new `TorchTransferEntropy` class |
| `SimMemoryBuffer.compute_sim` | `sim_fn.forward(x, x, symmetric=True)` | `sim_fn.forward(x, x, symmetric=False)` |
| `_sl_loss` mask | `torch.tril(..., diagonal=-1)` | `~torch.eye(n, n, ...)` (full off-diagonal) |
| z-space distance | `LpDistance(z, z)` — symmetric | `directed_dist(W_src(z), W_tgt(z))` — asymmetric |
| `SSLModel` | no projection heads | add `W_src`, `W_tgt: Linear(128, 128, bias=False)` |
| FAISS index | single symmetric index | two indices: `src_index`, `tgt_index` |
| Inference API | `model.transform(x) → z` | unchanged; role projection at query time |
| GL head | masked reconstruction | unchanged |
| `SimMemoryBuffer` storage | `(x, z)` | unchanged |

## Key assumptions

| Assumption | Status | Failure mode | Test |
|---|---|---|---|
| TE/Granger scores can provide useful soft labels | unvalidated | Labels are noisy or fail outside sampled regimes | Compare retrieval against held-out TE/Granger and downstream forecast lift |
| Asymmetric geometry will converge | unvalidated | Embedding collapses to symmetric or unstable geometry | Track directional ranking and A→B vs B→A consistency |
| Vector retrieval can approximate causal discovery cheaply | partially validated conceptually | Fast retrieval returns correlated but non-causal variables | Forecasting and intervention-style validation |
| P2 improves P1 | unvalidated | P1 gains no lift over shape/DTW covariates | Use P1 cluster models as downstream validation |

## Decision impact

- P2 should be measured on both retrieval quality and forecast impact.
- P2 can upgrade P1's covariate layer, but P1 should not wait for P2 to complete.
- P2 should not produce causal claims without caveats; retrieved drivers are candidate causal covariates until validated.

## SSL research baseline (I-P2-A, 2026-06-30)

Primary literature pass confirms: **no existing SSL TS method implements an asymmetric/directed objective.** The four main SSL methods evaluated as P2 baselines:

| Method | Type | TS Classification | TS Forecasting | Symmetric? |
|---|---|---|---|---|
| TS-TCC (Eldele et al. 2021, IJCAI) | Contrastive | HAR 90.37% (≈supervised) | — | Yes |
| TS2Vec (Yue et al. 2022, AAAI) | Contrastive hierarchical | SOTA 125 UCR | −32.6% MSE | Yes |
| Ti-MAE (Li et al. 2023, ICLR ws) | Masked autoencoder | — | Best SSL forecasting 2023 | Yes |
| TimeMAE (Cheng et al. 2023, TKDE) | Decoupled MAE | HAR 91.31% linear eval | — | Yes |

**P2 novelty is confirmed across all 12 reviewed SSL papers:** no published SSL TS encoder implements an asymmetric/directed objective. P2 development should use TimeMAE as the primary symmetric baseline (strongest classification encoder) and TS2Vec as the universal baseline across tasks.

**Additional design inputs from I-P2-A MEDIUM (2026-06-30):**
- **T-Rep** (Fraikin et al. 2024, ICLR): learned time-embeddings in pretext tasks; divergence prediction as continuous temporal distance; outperforms TS2Vec; robust to missing data. Time-embedding approach could condition P2's directed pretext on regime/seasonality.
- **CA-TCC** (Eldele et al. 2023, TPAMI): 4-phase semi-supervised (pretrain → fine-tune → pseudo-label → class-aware contrastive); 1% labels ≈ fully supervised. Reference architecture for P2's label-efficient training with expensive TE/Granger labels.
- **Series2Vec** (Foumani et al. 2024, [src-2026-06-foumani-series2vec](../sources/src-2026-06-foumani-series2vec.md)): **primary design ancestor for P2's SL head.** See "Conceptual sources" section above. Confirmed that similarity-preserving pretext with a TS-specific distance function outperforms augmentation-based contrastive; P2 extends this by replacing symmetric Soft-DTW with asymmetric TE/Granger as the pairwise target.
- **Multi-task SSL** (Choi & Kang 2023): shared encoder + multiple loss heads. P2 could combine a symmetric backbone loss with a directed asymmetric head.

## Additional design inputs (ingest 2026-06-30)

**Architecture & mechanism inputs:**
- **MoCo** ([src-2026-06-he-moco](../sources/src-2026-06-he-moco.md), He et al. 2020, CVPR): momentum-updated key encoder (EMA, m=0.999) + FIFO queue of 65,536 negatives. P2 training design: use EMA encoder for the "source" (cause) branch and gradient-updated encoder for the "target" (effect) branch; queue-based negatives are essential at scale where directed positive pairs are sparse.
- **xLSTM mLSTM** ([src-2026-06-beck-xlstm](../sources/src-2026-06-beck-xlstm.md), Beck et al. 2024, NeurIPS): matrix memory C ∈ ℝ^{d×d} with covariance update C_t = f_t·C_{t-1} + i_t·v_t·k_t^T provides an explicit associative key–value memory that is fully parallelizable. Architectural analogy for P2's directed embedding: the mLSTM maps (k, v, q) → retrieval in the same way P2 maps (source series, target label, query) → directed similarity. Validates that asymmetric key–value geometries are trainable end-to-end.
- **Time2Vec** ([src-2026-06-kazemi-time2vec](../sources/src-2026-06-kazemi-time2vec.md), Kazemi et al. 2019): t2v(τ)[i] = sin(ωᵢτ + φᵢ) with learned ω, φ. P2 pretext task input: concatenate t2v(timestamp) with the series representation to condition the asymmetric similarity head on temporal regime/seasonality — makes TE/Granger label quality regime-aware.

**Pretraining strategy:**
- **Liu SSL comparison** ([src-2026-06-liu-ssl-comparison](../sources/src-2026-06-liu-ssl-comparison.md), 2024): SimCLR vs MAE on TS — MAE wins at sparse label ratio ≤ 0.1; SimCLR wins at label ratio ≥ 0.5. P2 decision: pretrain with MAE backbone (TE/Granger labels are expensive → sparse → MAE regime). MAE is also 25.6% faster to pretrain.

**Evaluation protocol:**
- **Musgrave** ([src-2026-06-musgrave-metric-learning-reality](../sources/src-2026-06-musgrave-metric-learning-reality.md), 2020): metric learning reality check — equal architecture, equal dimension, Bayesian-optimized hyperparameters, no test-set feedback required to get fair comparisons. P2 evaluation must: fix backbone across baselines, fix embedding dim (768), tune with cross-val, use MAP@R (not Recall@K). Loss function choice is less important than label quality.

**Augmentation design:**
- **Um wearable** ([src-2026-06-um-wearable-augmentation](../sources/src-2026-06-um-wearable-augmentation.md), 2017): jitter + scaling + window slicing are safe (preserve causal direction). Permutation and rotation destroy temporal structure and must not be used as positive-pair augmentations.
- **Liu medical review** ([src-2026-06-liu-ssl-medical-review](../sources/src-2026-06-liu-ssl-medical-review.md), 2023): augmentation survey for dense physiological TS — frequency domain perturbation (phase/magnitude) is safe; cross-subject mixing is not. Backbone preference: Transformer or TCN > LSTM.

## Sources

- [sources/src-2026-06-p2-causal-embedding-model](../sources/src-2026-06-p2-causal-embedding-model.md) — bottleneck framing, asymmetric-objective proposal, moat.
- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md) — how retrieved covariates feed the selector.
- [sources/src-2026-06-eldele-ts-tcc](../sources/src-2026-06-eldele-ts-tcc.md), [sources/src-2026-06-yue-ts2vec](../sources/src-2026-06-yue-ts2vec.md), [sources/src-2026-06-li-ti-mae](../sources/src-2026-06-li-ti-mae.md), [sources/src-2026-06-cheng-timemae](../sources/src-2026-06-cheng-timemae.md) — HIGH SSL baselines
- [sources/src-2026-06-fraikin-trep](../sources/src-2026-06-fraikin-trep.md) — T-Rep (ICLR 2024): time-embeddings in pretext tasks
- [sources/src-2026-06-eldele-ca-tcc](../sources/src-2026-06-eldele-ca-tcc.md) — CA-TCC (TPAMI 2023): semi-supervised reference
- [sources/src-2026-06-foumani-series2vec](../sources/src-2026-06-foumani-series2vec.md) — Series2Vec (DMKD 2024): similarity-preserving pretext
- [sources/src-2026-06-choi-multitask-ssl](../sources/src-2026-06-choi-multitask-ssl.md) — multi-task SSL (ICLR 2023 ws)
- [sources/src-2026-06-talukder-totem](../sources/src-2026-06-talukder-totem.md) — TOTEM (ICML 2024): VQVAE cross-domain tokenizer
- [sources/src-2026-06-eldele-label-efficient-review](../sources/src-2026-06-eldele-label-efficient-review.md), [sources/src-2026-06-yang-timeclr](../sources/src-2026-06-yang-timeclr.md), [sources/src-2026-06-jawed-ssl-semisupervised](../sources/src-2026-06-jawed-ssl-semisupervised.md) — survey + early methods
- [sources/src-2026-06-he-moco](../sources/src-2026-06-he-moco.md) — MoCo (CVPR 2020): momentum encoder + queue; P2 negative sampling design
- [sources/src-2026-06-kazemi-time2vec](../sources/src-2026-06-kazemi-time2vec.md) — Time2Vec (2019): learnable sinusoidal time embedding; P2 temporal conditioning
- [sources/src-2026-06-musgrave-metric-learning-reality](../sources/src-2026-06-musgrave-metric-learning-reality.md) — metric learning reality check; P2 evaluation protocol
- [sources/src-2026-06-liu-ssl-comparison](../sources/src-2026-06-liu-ssl-comparison.md) — SimCLR vs MAE for TS; P2 pretraining stage decision
- [sources/src-2026-06-ericsson-ssl-survey](../sources/src-2026-06-ericsson-ssl-survey.md) — SSL survey (2022); SSL landscape reference
- [sources/src-2026-06-liu-ssl-medical-review](../sources/src-2026-06-liu-ssl-medical-review.md) — medical TS contrastive SSL review (2023); augmentation catalog
- [sources/src-2026-06-um-wearable-augmentation](../sources/src-2026-06-um-wearable-augmentation.md) — wearable TS augmentation (2017); canonical augmentation reference
- [sources/src-2026-06-lewis-bart](../sources/src-2026-06-lewis-bart.md) — BART (ACL 2020); MAE-style pretraining background
- [sources/src-2026-06-pascual-speech-ssl](../sources/src-2026-06-pascual-speech-ssl.md) — PASE speech SSL (2019); multi-task SSL background
- [sources/src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md) — v1 production architecture (ConvAttnEncoder, SSL heads, SimMemoryBuffer, KPIs); P2 symmetric baseline

## Related pages

- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [experiments/exp-p2-causal-retrieval-validation](../experiments/exp-p2-causal-retrieval-validation.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [domains/embedding-models/thesis](../domains/embedding-models/thesis.md)
- [projects/p1-cluster-pretrained-deep-models](p1-cluster-pretrained-deep-models.md)
