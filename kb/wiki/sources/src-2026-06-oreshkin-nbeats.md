---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-oreshkin-nbeats
tags:
- timeseries-forecasting
- backbone
- mlp
zotero: oreshkinNBEATSNeuralBasis2020
source_hash: e442ca4707ebdf0be09cc61d80adab6075734fc5bb8430bfe8719a800fa09ce2
---

# N-BEATS: Neural Basis Expansion Analysis for Interpretable Time Series Forecasting

**Oreshkin et al. (ICLR 2020)**

## Summary

N-BEATS is a deep MLP architecture for univariate point forecasting built on backward/forward residual links and a doubly residual stacking principle. It requires no time-series-specific components in its generic configuration, yet outperforms statistical benchmarks and the M4 competition winner. An interpretable variant constrains basis functions to polynomial (trend) and Fourier (seasonality) forms.

## Architecture

- **Basic block**: 4-layer FC stack → linear projections for forecast and backcast coefficients → basis expansion to produce partial forecast and backcast.
- **Doubly residual stacking**: backcast branch subtracts what each block modeled from the input, forcing downstream blocks to focus on residuals. Forecast branch sums partial predictions hierarchically.
- **Generic (N-BEATS-G)**: learnable basis functions (no TS-specific inductive bias).
- **Interpretable (N-BEATS-I)**: polynomial basis for trend stack, Fourier basis for seasonality stack — outputs interpretable seasonal/trend decomposition with no accuracy penalty.

## Key results

- N-BEATS achieves state-of-the-art on M4 (OWA 0.795 vs. M4 winner 0.821), M3 (sMAPE 12.37 vs. best statistical 12.71), and TOURISM datasets.
- M4 gap between N-BEATS and winner (0.026) exceeds the gap between winner and second place (0.017).
- Generic configuration uses zero TS-specific knowledge: no scaling, no feature engineering, no seasonal adjustment — yet wins.
- Ensemble of 180 models (diverse loss metrics, window lengths, seeds) used for competition setting. Single model is also competitive.

## Claims

- **Pure deep learning (N-BEATS) without any time-series-specific components outperforms statistical M4 benchmarks and the M4 competition winner** (a DL/stat hybrid). [Evidence: Table 1, ICLR 2020]
- **MLP residual stacking with explicit basis functions enables interpretable seasonality-trend decomposition** at no accuracy cost. [Evidence: Section 3.3, Figure 2]
- Architecture generalizes across M4, M3, TOURISM without hyperparameter changes per dataset. [Evidence: Section 5.2]

## Caveats

- Univariate only — no inter-variate modeling.
- No exogenous covariates.
- Competition results use large ensembles; single-model results are still strong but not always SOTA.
- Evaluated on competition datasets (business/financial/economic/demographic); performance on demand forecasting at SKU level is extrapolated.

## Applicability to P1

High. N-BEATS represents the MLP stack backbone option for P1. The interpretable variant's seasonality-trend decomposition aligns well with the goal of transparency. The residual block design is computationally efficient and scales well. No covariate support natively — would need extension (see NBEATSx).

## Related

- [src-2026-06-challu-nhits](src-2026-06-challu-nhits.md) — N-HiTS: hierarchical extension of N-BEATS with better long-horizon efficiency
- [src-2026-06-olivares-nbeatsx](src-2026-06-olivares-nbeatsx.md) — NBEATSx: N-BEATS extended with exogenous variables
- [src-2026-06-zeng-dlinear](src-2026-06-zeng-dlinear.md) — DLinear: simpler linear alternative
