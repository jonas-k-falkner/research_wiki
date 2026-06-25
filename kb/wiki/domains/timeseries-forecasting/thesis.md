---
type: domain
domain: timeseries-forecasting
project: P1
status: active
confidence: medium
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-p1-cluster-pretrained-deep-models
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

## Sources & related

- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../../sources/src-2026-06-p1-cluster-pretrained-deep-models.md), [sources/src-2026-06-p1-cluster-pretrained-deep-models](../../sources/src-2026-06-p1-cluster-pretrained-deep-models.md)
- Project: [projects/p1-cluster-pretrained-deep-models](../../projects/p1-cluster-pretrained-deep-models.md)
