---
type: experiment
domain: timeseries-forecasting
project: P1
status: draft
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p1-cluster-pretrained-deep-models
tags:
- experiment
---

# Experiment: P1 cluster quality gate

## Status

Designed-from-source, not yet run. Owner unassigned (see [shared/open-questions](../shared/open-questions.md)). Deck scopes this at **2–3 weeks, run immediately**, before committing P1 engineering bandwidth.

## Hypothesis

Shape-based clusters of time series are regime-consistent enough that a single per-cluster model will not underfit its members. Falsifiable: if within-cluster variance of regime flags is high, shape clustering alone is insufficient and regime sub-clustering is required.

## Protocol (from deck Slide 3 — verbatim intent, to be expanded)

1. Embed ~150 benchmark series with the existing time-series embedding model.
2. Cluster the embeddings.
3. Run the existing detector suite per cluster — `NonstationarityDetector`, `SeasonalityDetector`, `HeteroscedasticityDetector`.
4. Measure **within-cluster variance** of stationarity, seasonality, and heteroscedasticity flags.

## Decision rule (from source)

- **Low within-cluster variance →** proceed directly to per-cluster models.
- **High within-cluster variance →** implement shape + regime sub-clustering, then proceed.

## Metrics

- Primary: within-cluster variance/entropy of each detector flag (lower = more regime-consistent).
- Threshold for "low" vs "high" is **not yet defined in source** — must be set before the run, ideally against a baseline of random clustering.

## To specify before running `[seed gaps]`

- Embedding model + clustering algorithm and k (and how k is chosen).
- The numeric pass/fail threshold and its justification.
- Whether 150 benchmark series are representative of client SKU distributions.

## Literature to integrate `[verify]`

- Cluster validity indices suited to time series; stability-based cluster validation `[verify]`
- Global-vs-clustered-vs-local forecasting evidence (Montero-Manso & Hyndman) `[verify]`

## Expected failure modes (project-specific)

- Threshold is arbitrary, so "low/high" is not decision-relevant → fix by pre-registering threshold vs a random-clustering baseline.
- 150 series under-represent client regimes → gate passes but production clusters are mixed.
- Detector flags are themselves noisy on short series → variance reflects detector instability, not regime mixing.

## Decision impact

Produces a clear **go / sub-cluster / defer** decision for the full P1 build (ADR-0001 step 4 depends on it).

## Related pages

- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
- [decisions/adr-0001-project-sequencing](../decisions/adr-0001-project-sequencing.md)
