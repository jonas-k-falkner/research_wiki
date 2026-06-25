---
type: concept
domain: scenario-engine
project: P3
status: active
confidence: medium
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-p3-scenario-engine
tags:
  - concept
---

# CPCV validation

## Definition

Combinatorial Purged Cross-Validation: a time-series validation scheme that trains/tests over multiple combinatorial splits with purging and embargoing to prevent leakage from temporally adjacent samples. Used in P3 to make scenario outputs trustworthy enough for procurement decisions. See [sources/src-2026-06-p3-scenario-engine](../sources/src-2026-06-p3-scenario-engine.md).

## Why it matters

Scenario answers drive money decisions, so leakage-inflated validation error is a direct trust risk. CPCV also yields a distribution of out-of-sample paths rather than a single backtest, which suits scenario confidence bounds.

## Open research questions

- Is full CPCV worth its compute here versus simpler purged walk-forward, given P3's "low cost / mostly wiring" framing?
- How are scenario interventions (e.g. "cotton +15%") validated out-of-sample, given the counterfactual has no ground truth?
- What calibration target makes the confidence interval trustworthy to a CFO/CPO rather than merely present?

## Literature to integrate `[verify]`

- Combinatorial Purged CV, purging/embargo (López de Prado, *Advances in Financial Machine Learning*) `[verify]`
- Conformal prediction / conformalized quantile regression for calibrated intervals (Vovk; Romano, Patterson, Candès) `[verify]`
- Diebold-Mariano forecast-comparison testing (already present in forecast_pipeline) `[verify]`
- Scenario/counterfactual backtesting practice for econometric what-if queries

## Cross-project relevance

- Validation backbone for [concepts/scenario-re-run-api](scenario-re-run-api.md); calibration thinking is reusable for P4 availability-score calibration ([concepts/mixed-frequency-nowcasting](mixed-frequency-nowcasting.md)).

## Related pages

- [projects/p3-scenario-engine](../projects/p3-scenario-engine.md)
