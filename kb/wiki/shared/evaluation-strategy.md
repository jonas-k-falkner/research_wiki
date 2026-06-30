---
type: shared
domain: shared
project: shared
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-px-cross-project-strategy
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-p4-availability-nowcasting
tags:
- evaluation
---

# Evaluation strategy

## P1

- Cluster QA: within-cluster variance of stationarity, seasonality, heteroscedasticity flags.
- Forecast accuracy: compare against default and tuned LGBM, plus existing baselines.
- Operational value: analyst-time reduction and marginal SKU onboarding cost.
- Explanation quality: cluster-level and covariate-level importance stability.

## P2

- Directional retrieval accuracy against held-out TE/Granger labels.
- A→B versus B→A asymmetry tests.
- Top-k causal covariate retrieval latency.
- Downstream forecast lift inside P1 cluster models.

## P3

- Scenario backtests.
- CPCV-validated error and calibration.
- User trust and actionability.
- Accuracy and usefulness of named driver explanations.

## P4

- Entity-resolution accuracy.
- Event/relation extraction precision and recall.
- Alert lead time.
- Availability-score calibration.
- Explanation completeness.
- Coverage separation: distinguish unknown hidden truth from publicly observable truth.
