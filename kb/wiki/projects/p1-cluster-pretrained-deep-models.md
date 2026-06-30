---
type: project
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
  - src-2026-06-p1-cluster-pretrained-deep-models
  - src-2026-06-tsf-literature-review
  - src-2026-06-chen-channel-clustering
  - src-2026-06-qiu-duet-clustering
  - src-2026-06-aghabozorgi-ts-clustering-survey
  - src-2026-06-sen-global-local-forecasting
  - src-2026-06-peters-sparse-seq2seq-2019
  - src-2026-06-lim-tft-2021
  - src-2026-06-jain-attention-not-explanation-2019
  - src-2026-06-wiegreffe-attention-not-not-2019
  - src-2026-06-liu-rethinking-attention-explainability-2022
  - src-2026-06-zeng-dlinear
  - src-2026-06-chen-closer-look-transformers
  - src-2026-06-wang-timexer
  - src-2026-06-arango-chronosx
  - src-2026-06-han-unica
  - src-2026-06-potapczinski-apollopfn
  - src-2026-06-lu-cats-ats
  - src-2026-06-challu-nhits
  - src-2026-06-oreshkin-nbeats
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
- **Moat rating — individual components now primary-confirmed; combination remains unmatched.** A primary-source literature pass (I-P1-A/B/C, 2026-06-29) confirms each P1 component has precedent: cluster-first channel routing (CCM, DUET), α-entmax sparse selection (Peters et al. 2019), AttGrad faithful attribution (Liu et al. 2022), and endo/exo backbone split (TimeXer). However, no 2024–2026 paper combines all of these — query-dependent sparse hierarchical gating + cluster-level AttGrad attribution + diversity regularization + MC-dropout stability — in one system. The combination remains a distinct direction. Confidence upgraded from "self-assessed" to "primary-supported" for the component claims; the full-combination novelty is still an inference from coverage gaps, not a direct experimental comparison. Medium confidence. Tracked on [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md).

## Open research questions

- See [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md) (global-vs-clustered-vs-local) and [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md) (entmax vs hard gates). Backbone choice (D-Linear vs MLP) is an unresolved deck open question.

## External literature positioning

A deep-research synthesis ([sources/src-2026-06-tsf-literature-review](../sources/src-2026-06-tsf-literature-review.md)) finds adjacent validators for the parts of P1 — TimeXer (asymmetric target/covariate), Channel Clustering → DUET (cluster-first) — while TS foundation models are background, not blueprints, for sparse covariate selection. It also supports a compact backbone (spend the budget on the selector) and no residual bypass.

**Updated with primary-source verification (I-P1-C, 2026-06-29):**
- Compact backbone preference is now evidence-backed: Zeng et al. 2023 ([src-2026-06-zeng-dlinear](../sources/src-2026-06-zeng-dlinear.md)) shows DLinear outperforms all Transformer LTSF models by 20–50% MSE on 9 standard benchmarks; Chen et al. 2025 ([src-2026-06-chen-closer-look-transformers](../sources/src-2026-06-chen-closer-look-transformers.md)) confirms standard benchmarks are self-dependent/stationary, so architecture investment should go into the covariate layer, not backbone complexity.
- Covariate gap is confirmed: four 2025–2026 papers (ChronosX, UNICA, ApolloPFN, CATS-ATS) independently identify that Chronos, TimesFM, MOMENT, and other leading TSFMs do not support exogenous covariates; TimeXer ([src-2026-06-wang-timexer](../sources/src-2026-06-wang-timexer.md)) provides the strongest validated endo/exo cross-attention template. See [comparisons/tsf-backbone-comparison](../comparisons/tsf-backbone-comparison.md) for full model table.

## Sources

- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md) — cluster models, gate protocol, covariate-selection mechanism, risks.
- [sources/src-2026-06-tsf-literature-review](../sources/src-2026-06-tsf-literature-review.md) — external TSF literature positioning (secondary synthesis; key claims now verified against named primaries in I-P1-A/B/C).

## Related pages

- [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md)
- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [domains/timeseries-forecasting/thesis](../domains/timeseries-forecasting/thesis.md)
