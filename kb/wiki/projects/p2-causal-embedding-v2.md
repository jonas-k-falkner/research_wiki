---
type: project
domain: embedding-models
project: P2
status: active
confidence: medium
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-p2-causal-embedding-model
  - src-2026-06-p1-cluster-pretrained-deep-models
tags:
  - embeddings
  - causality
  - covariate-retrieval
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

## Sources

- [sources/src-2026-06-p2-causal-embedding-model](../sources/src-2026-06-p2-causal-embedding-model.md) — bottleneck framing, asymmetric-objective proposal, moat.
- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md) — how retrieved covariates feed the selector.

## Related pages

- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [experiments/exp-p2-causal-retrieval-validation](../experiments/exp-p2-causal-retrieval-validation.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [domains/embedding-models/thesis](../domains/embedding-models/thesis.md)
- [projects/p1-cluster-pretrained-deep-models](p1-cluster-pretrained-deep-models.md)
