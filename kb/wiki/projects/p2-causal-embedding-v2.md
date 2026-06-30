---
type: project
domain: embedding-models
project: P2
status: active
stage: seed
confidence: medium
updated: 2026-06-30
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

## Candidate approach

```text
sample series pairs
  → compute Transfer Entropy / Granger scores on tractable subset
  → train directed/asymmetric embedding objective from soft labels
  → index 200M embeddings
  → query target series
  → retrieve top-k causal drivers
  → feed covariates into P1 selector or P3/P4 explanation layers
```

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
| `GrangerSelector` / `TransferEntropySelector` | Reuse as distillation teacher |

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
- **Series2Vec** (Foumani et al. 2024): similarity-preserving pretext (Soft-DTW target) outperforms augmentation-based contrastive. P2 can adopt the same design but with TE/Granger as directed similarity target.
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
