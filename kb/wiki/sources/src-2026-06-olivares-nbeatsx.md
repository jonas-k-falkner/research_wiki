---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-olivares-nbeatsx
tags:
- timeseries-forecasting
- backbone
- mlp
- exogenous
zotero: olivaresNeuralBasisExpansion2023
source_hash: 7ebad96aaa0d337dd828bcda9667fe8671071782c5700c41e5fc20aab0f5229d
---

# NBEATSx: Neural Basis Expansion Analysis with Exogenous Variables

**Olivares et al. (CMU + Wroclaw, 2023)**

## Summary

NBEATSx extends N-BEATS to incorporate time-dependent exogenous variables via a convolutional sub-network inside each FCNN block. Applied to electricity price forecasting (EPF), achieving ~20% improvement over original N-BEATS and up to 5% over specialized statistical/ML EPF methods.

## Architecture

- N-BEATS block architecture retained (doubly residual stacking, backcast/forecast expansion coefficients).
- **Covariate integration**: FCNN in each block receives (y^back, X) — the target backcast window concatenated with exogenous matrix X.
- X is encoded via a convolutional sub-structure to capture temporal dynamics of covariates.
- Interpretable stack variant extends decomposition to show exogenous factor contributions alongside trend and seasonality.

## Key results

- ~20% improvement over N-BEATS and ESRNN on EPF across 5 power markets and 2-year out-of-sample periods.
- Up to 5% over established statistical (LEAR) and DNN EPF baselines.
- Interpretable variant decomposes predictions into trend, seasonality, and exogenous contribution.

## Claims

- **Concatenating exogenous variables into N-BEATS FCNN blocks improves accuracy by ~20%** over the original N-BEATS model on electricity price forecasting. [Evidence: Section 4, Table 3]
- **Interpretable basis functions can be extended to show exogenous factor effects** on top of trend/seasonality decomposition. [Evidence: Section 3.3]

## Caveats / Applicability to P1

High direct relevance. NBEATSx is the most direct covariate-enabled MLP backbone for P1 — it combines the strong N-BEATS residual architecture with exogenous variable support via concatenation (simple but effective). The electricity price forecasting setting directly parallels P1's demand forecasting with promotional/price covariates. NBEATSx establishes that the MLP + concatenated covariates approach is viable without architectural complexity.

## Related

- [src-2026-06-oreshkin-nbeats](src-2026-06-oreshkin-nbeats.md) — N-BEATS: parent architecture
- [src-2026-06-challu-nhits](src-2026-06-challu-nhits.md) — N-HiTS: hierarchical extension (no exogenous natively)
- [src-2026-06-wang-timexer](src-2026-06-wang-timexer.md) — TimeXer: Transformer equivalent with exogenous
