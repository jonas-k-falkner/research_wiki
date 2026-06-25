---
type: project
domain: timeseries-forecasting
project: P1
status: active
confidence: medium
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-p1-cluster-pretrained-deep-models
tags:
  - forecasting
  - deep-learning
  - scalability
---

# P1 — Cluster-pretrained deep models

## Purpose

Train lightweight deep forecasting models per cluster of similar time series. A new SKU is embedded, routed to a cluster model, and forecast zero-shot or with minimal fold-in. The business objective is to remove the analyst bottleneck when client SKU counts grow from tens to hundreds or thousands.

## Current thesis

P1 is the scalability unlock, but it should not start as a full build until the cluster-quality gate is passed. The most important near-term question is whether shape-based clusters are regime-consistent enough for shared models, or whether shape + regime sub-clustering is required.

## Candidate architecture

```text
200M series
  → time-series embedding model
  → FAISS cluster routing
  → optional regime sub-clustering
  → cluster-specific D-Linear or MLP model
  → sparse covariate selector / attention over P2-style covariate embeddings
  → forecast
```

## Important design update from `p1_cluster-pretrained_deep-models.md`

Source: [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md). This is the [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md) routing target plus a covariate layer. For covariate selection, the preferred direction is:

- shared encoder for target and covariate series
- precomputed covariate embedding clusters
- target-query-dependent hierarchical cluster→feature α-entmax
- no residual path bypassing selection
- feature importance by weight × gradient and cluster sensitivity
- MC-dropout stability checks for confidence

This makes the explanation layer more robust than raw attention weights, especially when covariates are highly correlated.

## Success criteria

| Criterion | Target |
|---|---|
| Scalability | Near-zero marginal analyst effort per new SKU after onboarding |
| Accuracy | Match or exceed default/tuned LGBM on relevant benchmarks and internal data |
| Cluster quality | Low within-cluster variance for stationarity, seasonality, heteroscedasticity, or improved quality after sub-clustering |
| Integration | `ClusterDeepModel` fits forecast pipeline Model ABC and serialization constraints |
| Explanation | Report useful cluster-level and covariate-level importance without treating attention weights as causal proof |

## Main risks

| Risk | Mitigation |
|---|---|
| Shape similarity does not imply regime similarity | Run detector-suite cluster QA and introduce regime sub-clusters if needed |
| PyTorch integration violates library layering/determinism | Implement first-class optional `ClusterDeepModel`; persist routing index and state dict cleanly |
| Deep model does not beat tuned LGBM | Treat analyst-time elimination and zero-shot onboarding as primary value, not only raw accuracy |
| Covariate selection is unstable under correlated macro inputs | Use hierarchical entmax, cluster-level importance, diversity regularization, and stability diagnostics |

## Dependencies

- P2 provides causal covariate embeddings that can upgrade the covariate layer.
- P3 creates commercial pressure for P1 by surfacing SKU-scaling bottlenecks.

## Contradictions & tensions

- **Determinism vs MC-dropout `[cross-layer, unresolved]`.** `p1_cluster-pretrained_deep-models.md` recommends MC-dropout (multiple stochastic passes) for importance stability, but the `forecast_pipeline` library is deterministic-by-default with explicitly seeded randomness. A `ClusterDeepModel` will need a documented stochasticity carve-out for uncertainty/importance estimation. Cannot be fully resolved until the `forecast_pipeline` repo context is ingested — tracked in [shared/research-backlog](../shared/research-backlog.md).
- **Moat rating is self-assessed.** "Very high" technical moat (deck) is an interested estimate from the proposer; pretrained TS foundation models may compress it. Flagged on [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md) for the literature pass.

## Open research questions

- See [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md) (global-vs-clustered-vs-local) and [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md) (entmax vs hard gates). Backbone choice (D-Linear vs MLP) is an unresolved deck open question.

## Sources

- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md) — strategy/sequencing, gate protocol, risks.
- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md) — covariate selection mechanism.

## Related pages

- [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md)
- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [domains/timeseries-forecasting/thesis](../domains/timeseries-forecasting/thesis.md)
