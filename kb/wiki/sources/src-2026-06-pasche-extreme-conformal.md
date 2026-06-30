---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-pasche-extreme-conformal
tags:
- conformal-prediction
- uncertainty-quantification
- extreme-value-theory
- price-spikes
zotero: pascheExtremeConformalPrediction2025
source_hash: 96a9f099e922382b202091d4f916c1819a24d4acba3a5fcb9370862ab6366a92
---

# Extreme Conformal Prediction: Reliable Intervals for High-Impact Events

**Pasche, Lam, Engelke (University of Geneva, Columbia University, 2025)**

## Summary

Standard conformal prediction constructs prediction intervals with marginal coverage guarantees by computing an empirical quantile over calibration scores. This fails at very high confidence levels (e.g., 99.9%) when the calibration set is small: fewer than one calibration score exceeds the required quantile, making the estimator infinite or unreliable.

The paper bridges **extreme value theory (EVT)** and **conformal prediction** by fitting a Generalised Pareto Distribution (GPD) to the tail of the calibration scores, then using the fitted GPD to extrapolate quantile estimates beyond the empirical range. Applied to one-day-ahead flood risk interval forecasting for water flow.

## Method

1. Fit a base prediction model (any black-box quantile regression method, e.g., XGBoost, neural network).
2. Compute nonconformity scores on a calibration set.
3. Fit a GPD to the upper tail of calibration scores (peaks-over-threshold approach).
4. Use GPD quantile estimates at extreme levels to set the prediction interval boundary.
5. Result: reliable prediction intervals with high-confidence coverage even when calibration data is scarce relative to the required confidence level.

## Claims

- **Classical conformal prediction fails for very high confidence requirements** (confidence level close to 1) because the empirical quantile estimator becomes undefined when fewer than one calibration score exceeds the required level. [Evidence: Section 1, Equation (2)]
- **GPD-extended conformal prediction provides reliable coverage even at extreme confidence levels** where classical methods yield infinite or vacuous intervals. [Evidence: Sections 2–3, simulation study]
- **The method wraps any black-box base model** — it does not require modifying the forecasting model, only the calibration/interval step. [Evidence: Section 2.1]
- **Application to flood risk**: GPD conformal intervals improve coverage vs classical conformal at high confidence levels for water flow prediction. [Evidence: Section 4]

## Caveats

- Demonstrated on flood data (continuous hydrology) — no direct application to financial/commodity price data.
- Marginal (unconditional) coverage guarantee only — conditional coverage at specific input values is not guaranteed.
- Requires a calibration set of reasonable size to estimate GPD tail parameters; not applicable with very few calibration points.
- Does not address structural breaks or regime changes — assumes exchangeability of calibration and test distributions.

## Applicability to P1

**High and direct for the uncertainty quantification component of P1.**

P1's success criterion "forecast accuracy degrades gracefully under price spikes, not catastrophically" requires reliable prediction intervals precisely at the extreme tail — the exact regime where classical conformal fails. Commodity and energy prices exhibit fat-tailed distributions with periodic spikes (oil supply shocks, natural gas price spikes, electricity scarcity events). Standard conformal prediction would either:
- Yield infinite intervals (uninformative) at required extreme confidence levels, or
- Undercover at tail events (undercoverage), understating spike risk.

GPD-extended conformal prediction wraps around any forecasting backbone (NBEATSx, N-HiTS) without modification. It is the natural companion to P1's point forecasting model for generating **risk-calibrated intervals under price spikes**.

This paper directly addresses the P1 open research question: "do MLP-based models handle price spike distributions robustly?" — the answer is to decouple the point forecast from the interval calibration, and use EVT-based conformal for the interval step.

## Related

- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md) — P1 risk: "forecast accuracy degrades gracefully under price spikes"
- [src-2026-06-olivares-nbeatsx](src-2026-06-olivares-nbeatsx.md) — NBEATSx: primary backbone whose intervals could be calibrated with this method
