---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-challu-nhits
tags:
- timeseries-forecasting
- backbone
- mlp
- hierarchical
zotero: challuNHiTSNeuralHierarchical2022
source_hash: d8450c02ec3026fca6064769904ff4faa59808ac2daf9d226565ec0a57acec5b
---

# N-HiTS: Neural Hierarchical Interpolation for Time Series Forecasting

**Challu et al. (AAAI 2023)**

## Summary

N-HiTS extends N-BEATS with two innovations designed for long-horizon forecasting: multi-rate signal sampling (MaxPool at different rates per block) and hierarchical interpolation (each block predicts a coarse resolution, then upsamples). This forces blocks to specialize in different frequency bands, reducing compute and improving accuracy over long horizons.

## Architecture

- S stacks × B blocks (MLP per block), built on N-BEATS doubly residual stacking principle.
- **Multi-rate input pooling**: block ℓ applies MaxPool with kernel k_ℓ, larger k → more aggressive smoothing, forcing block to focus on low-frequency content.
- **Hierarchical interpolation**: block ℓ predicts only ⌈r_ℓ·H⌉ coefficients (r_ℓ < 1 expressiveness ratio) then interpolates to full H horizon. Blocks closer to input have smaller r_ℓ and larger k_ℓ (low-frequency, coarse); later blocks have larger r_ℓ and smaller k_ℓ (higher frequency, fine).
- Final forecast is sum of hierarchically interpolated outputs across all blocks.

## Key results

- N-HiTS achieves ~20% average accuracy improvement over Autoformer, Informer, and related Transformer-based models on 6 large-scale long-horizon benchmarks (ETTm2, Exchange, Electricity, Traffic, Weather, ILI).
- Computation time 50x lower than Transformer-based approaches for long horizons.
- Memory footprint substantially smaller due to reduced effective input width per block.

## Claims

- **N-HiTS outperforms Transformer-based LTSF models by ~20% on average across 6 long-horizon benchmarks** while being 50x more compute-efficient. [Evidence: Table 1, AAAI 2023]
- **Hierarchical interpolation reduces parameter count and compute quadratically in horizon length**, solving the scalability problem of direct multi-step MLP forecasters. [Evidence: Section 3]
- **Multi-rate input sampling induces frequency specialization across blocks**, allowing the model to efficiently decompose signals into hierarchical frequency bands without explicit decomposition supervision. [Evidence: Figure 3, ablations]

## Caveats

- Univariate per-variable (univariate architecture applied to each series independently).
- No exogenous covariates in the base model.
- Evaluated on same long-horizon benchmarks where DLinear also outperforms Transformers — further testing on diverse competition datasets would be useful.

## Applicability to P1

High. N-HiTS is computationally efficient and well-suited for long-horizon demand forecasting. The multi-scale design naturally handles the weekly/monthly/yearly seasonality patterns in retail demand. No covariate support natively, but the residual block structure is amenable to covariate injection (similar to NBEATSx approach). This makes N-HiTS a strong candidate backbone for P1.

## Related

- [src-2026-06-oreshkin-nbeats](src-2026-06-oreshkin-nbeats.md) — N-BEATS: the parent architecture
- [src-2026-06-olivares-nbeatsx](src-2026-06-olivares-nbeatsx.md) — NBEATSx: covariate extension to N-BEATS family
- [src-2026-06-zeng-dlinear](src-2026-06-zeng-dlinear.md) — DLinear: simpler linear baseline
