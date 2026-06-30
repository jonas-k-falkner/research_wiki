---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-rizvi-glinear
tags:
- timeseries-forecasting
- backbone
- linear-model
- simplicity
zotero: rizviBridgingSimplicitySophistication2025
source_hash: 442d572826f6116c171e4d3df9b2896815a576c1caeefd983985590b07aeed81
---

# GLinear: Gaussian-Activated Linear Model for Time Series Forecasting

**Rizvi et al. (University of Stavanger, 2025)**

## Summary

GLinear is a data-efficient linear architecture for multivariate long-term time series forecasting. It uses a Gaussian activation function (as opposed to DLinear's ReLU-split decomposition) combined with Reversible Instance Normalization (RevIN) to handle distribution shifts. Despite being a single-layer architecture, GLinear outperforms NLinear, DLinear, and RLinear on most multivariate LTSF tasks while requiring less historical data. The paper motivates "bridging simplicity and sophistication" — achieving near-Transformer accuracy with linear complexity.

## Architecture

- **Core operation**: linear mapping from lookback window → forecast horizon, with Gaussian activation instead of raw linear or decomposed-linear.
- **RevIN**: Reversible Instance Normalization applied to input; inverted after prediction. Normalizes per-instance statistics (mean, std) to handle distribution shifts between train and test.
- **Data efficiency**: requires shorter lookback window than DLinear/RLinear to match performance; demonstrated on ETTh1 with reduced input lengths.
- **No attention, no positional encoding, no complex blocks** — pure linear + activation.

## Benchmarks

Evaluated on **academic LTSF datasets only**: ETTh1, Electricity, Weather, Traffic. Forecast horizons: 96, 192, 336, 720 steps.

- Outperforms NLinear, DLinear, RLinear on most multivariate tasks across these benchmarks.
- Competitive with Autoformer while being orders of magnitude simpler.
- **No evaluation on EPF, M4/M5, or commodity price data.**

## Claims

- **GLinear outperforms NLinear, DLinear, and RLinear on most multivariate LTSF benchmarks** while being data-efficient — requiring less historical data to achieve competitive accuracy. [Evidence: Tables 1–2, Section VI]
- **Gaussian activation better captures periodic patterns in time series** than raw linear mappings — the activation's smooth nonlinearity provides regularization without adding complexity. [Evidence: Section IV, ablation study]
- **RevIN normalizes instance-level distribution shifts** and allows the linear model to generalize across varying statistical properties in the test set. [Evidence: Section IV]
- **Data efficiency**: GLinear achieves its best performance with shorter input windows than DLinear/RLinear, making it more practical for datasets with limited history. [Evidence: Section VI, input length experiments]

## Caveats

- Benchmarks are academic LTSF only (ETTh1, Electricity, Weather, Traffic) — Chen et al. 2025 shows these benchmarks are self-dependent and stationary, so results may not transfer to non-stationary price data.
- No exogenous covariate support — univariate channel-independent design (each series forecasted independently).
- Not tested on EPF, M4 monthly, or any commodity price dataset.
- Outperformed by iTransformer, TimeMixer, TimeKAN on the same academic benchmarks — GLinear's advantage is data efficiency and simplicity, not raw accuracy.

## Applicability to P1

**Medium — useful as a data-efficient simplicity baseline for weekly/monthly forecasting.**

P1's primary horizon (weekly/monthly long-horizon commodity prices) creates smaller effective datasets than hourly/daily series. GLinear's data efficiency is a direct advantage: fewer months of historical data needed, which is realistic for commodity price series that have limited clean history. RevIN handles the distribution shift that is common in commodity prices (changing mean/variance over time).

GLinear is not a primary backbone candidate because it has no exogenous covariate support (P1's core value proposition is covariate attribution), but it is the right **simplicity-first ablation baseline** — "does adding covariates to N-HiTS/NBEATSx outperform a plain GLinear?" is a well-specified experiment.

Priority: **5 in the P1 backbone table** (after NBEATSx, N-HiTS, TimeXer, iTransformer). More relevant than DLinear as a simplicity baseline due to data efficiency and RevIN.

## Related

- [src-2026-06-zeng-dlinear](src-2026-06-zeng-dlinear.md) — DLinear: the original benchmark GLinear competes against
- [src-2026-06-challu-nhits](src-2026-06-challu-nhits.md) — N-HiTS: stronger MLP baseline for long-horizon
- [src-2026-06-olivares-nbeatsx](src-2026-06-olivares-nbeatsx.md) — NBEATSx: primary backbone with covariates
- [comparisons/tsf-backbone-comparison](../comparisons/tsf-backbone-comparison.md)
