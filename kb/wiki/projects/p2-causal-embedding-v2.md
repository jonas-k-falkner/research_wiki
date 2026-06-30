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

## Related pages

- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [experiments/exp-p2-causal-retrieval-validation](../experiments/exp-p2-causal-retrieval-validation.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [domains/embedding-models/thesis](../domains/embedding-models/thesis.md)
- [projects/p1-cluster-pretrained-deep-models](p1-cluster-pretrained-deep-models.md)
