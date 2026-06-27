---
type: concept
domain: timeseries-forecasting
project: P1
status: active
confidence: medium
stage: seed
updated: 2026-06-27
sources:
  - src-2026-06-p1-cluster-pretrained-deep-models
  - src-2026-06-tsf-literature-review
tags:
  - concept
---

# Cluster-pretrained deep models

## Definition

A forecasting family where similar time series are grouped into clusters, each cluster has a lightweight deep model trained on its members, and a new series is embedded and routed (FAISS) to the matching cluster model for zero-shot or minimal-fold-in forecasting. See [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md).

## Why it matters

It reframes SKU onboarding from per-series analyst tuning into a routing problem, which is the P1 scalability thesis. The load-bearing assumption is that a single shared model can serve a cluster without underfitting mixed regimes — unvalidated at seed stage.

## Open research questions

- Is "global model over clustered series" actually better than one global model or per-series local models for our data? This is a known, contested tradeoff in the forecasting literature and must be checked, not assumed.
- Does shape-based clustering produce regime-consistent clusters, or is shape + regime sub-clustering required? (This is the [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md) question.)
- What backbone — D-Linear vs MLP vs a small foundation-model-style architecture — and does the choice interact with cluster granularity?

## Literature to integrate `[verify]`

- Global vs local forecasting models for grouped series (e.g. Montero-Manso & Hyndman line of work) `[verify]`
- Linear-baseline deep forecasters: D-Linear / "Are Transformers Effective for Time Series Forecasting?" (Zeng et al.) `[verify]`
- Pretrained / zero-shot time-series foundation models as a comparison class: Chronos, Moirai, TimesFM, Lag-Llama `[verify]`
- Clustering quality metrics appropriate to time series (not just Euclidean silhouette)

## What the external review says `[verify]`

A deep-research synthesis ([sources/src-2026-06-tsf-literature-review](../sources/src-2026-06-tsf-literature-review.md)) reports that **cluster-first handling of correlated channels is the best-supported piece of this design** in the 2024–2026 literature: Channel Clustering ("From Similarity to Superiority", NeurIPS 2024) groups similar channels with interpretability gains, and DUET (KDD 2025) extends this to dual clustering with soft assignment and sparsification. It also infers a design principle — **keep the forecasting backbone simple and spend the modeling budget on the covariate selector** (from the "A Closer Look at Transformers for TSF" / linear-baseline line) — and supports **no residual bypass around the selector** (a design inference, not a direct recommendation). All `[verify]` against the named primaries; the synthesis carries no resolvable citations, so this page stays `seed`.

## Cross-project relevance

- Consumes covariate selection from [concepts/hierarchical-entmax-covariate-selection](hierarchical-entmax-covariate-selection.md) and, later, embeddings from [concepts/causal-covariate-embeddings](causal-covariate-embeddings.md).

## Related pages

- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
- [domains/timeseries-forecasting/thesis](../domains/timeseries-forecasting/thesis.md)
