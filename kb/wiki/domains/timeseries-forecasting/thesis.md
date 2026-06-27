---
type: domain
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
  - thesis
  - forecasting
---

# Domain thesis: Time-series forecasting

## Current thesis

The portfolio needs a scalable forecasting layer that can move from analyst-tuned SKU workflows to cluster-routed, low-touch global models. P1 is the main architecture for this transition.

## Most important unresolved question

Do shape-based clusters provide sufficiently consistent regimes for a shared model, or must clusters be split by stationarity, seasonality, heteroscedasticity, and related detector flags?

## Preferred near-term path

1. Run the P1 cluster-quality gate.
2. Prototype a single cluster with D-Linear and MLP if the gate passes or after regime sub-clustering.
3. Integrate sparse hierarchical covariate selection.
4. Validate against LGBM and existing forecasting baselines.
5. Track analyst-time elimination as a first-class success metric.

## Key assumptions

| Assumption | Status | Decision impact |
|---|---|---|
| 200M series provide enough training diversity | unvalidated in current wiki | Determines whether P1 can generalize zero-shot |
| Shape + regime clusters are learnable and useful | testing required | Determines P1 viability |
| Hierarchical entmax can stabilize covariate selection | plausible | Influences P1 model architecture |
| P2 embeddings improve covariate layer | unvalidated | Influences sequencing of full P1 build |

## External literature positioning `[verify]`

A deep-research synthesis of 2024–2026 TSF ([sources/src-2026-06-tsf-literature-review](../../sources/src-2026-06-tsf-literature-review.md)) splits the field into two streams: stronger general backbones (iTransformer, TimeMixer, the TSFM wave — Chronos, Moirai, TimesFM, Time-MoE, Sundial, Timer) and a smaller, more relevant stream on using covariates / clustering channels / adapting pretrained models (TimeXer, Channel Clustering, DUET, ChronosX, UniCA, ApolloPFN). Two takeaways for this domain: **TS foundation models are background, not the center of gravity** — the covariate-adapter papers exist precisely because leading TSFMs ignore exogenous covariates; and **a compact backbone with the right covariate inductive bias may suffice** (no exotic architecture needed). All `[verify]` against named primaries; thesis stays `seed`.

## Sources & related

- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../../sources/src-2026-06-p1-cluster-pretrained-deep-models.md), [sources/src-2026-06-tsf-literature-review](../../sources/src-2026-06-tsf-literature-review.md)
- Project: [projects/p1-cluster-pretrained-deep-models](../../projects/p1-cluster-pretrained-deep-models.md)
