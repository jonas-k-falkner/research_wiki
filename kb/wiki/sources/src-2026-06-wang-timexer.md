---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-wang-timexer
tags:
- timeseries-forecasting
- backbone
- transformer
- exogenous
zotero: wangTimeXerEmpoweringTransformers
source_hash: c2ec27241da87e0559c4f797f5a23d20f725c215c1decb8f007afeb5bfd85964
---

# TimeXer: Empowering Transformers for Time Series Forecasting with Exogenous Variables

**Wang et al. (Tsinghua, NeurIPS 2024)**

## Summary

TimeXer is a Transformer-based model that explicitly separates endogenous (target) and exogenous (covariate) variables through different embedding strategies, then reconciles them via patch-level self-attention on the endogenous side and variate-level cross-attention from exogenous to endogenous. A learnable global token on the endogenous side acts as a bridge between the two modalities.

## Architecture

**Endogenous embedding**: target series split into non-overlapping patches → N patch tokens + 1 learnable global token.

**Exogenous embedding**: each exogenous series projected to a single variate-level token via a linear layer (handles arbitrary look-back lengths, missing values, frequency mismatches).

**Endogenous self-attention**: patch tokens + global token attend to each other (Patch-to-Patch and Patch-to-Global).

**Exogenous cross-attention**: global endogenous token attends to all exogenous variate tokens (Variate-to-Global). The global token then propagates exogenous context to all patches via the Global-to-Patch direction in the next self-attention pass.

**Output**: linear projection over [P_en, G_en] → forecast for endogenous series only.

For multivariate forecasting without explicit exogenous variables: treats each channel as endogenous with all others as exogenous, applied in parallel with shared weights.

## Key results

- Achieves consistent state-of-the-art on 5 EPF (electricity price forecasting with exogenous) datasets: avg MSE 0.307 vs iTransformer 0.335, DLinear 0.366, Autoformer 0.453.
- On multivariate long-term benchmarks (ETT, ECL, Weather, Traffic): best or near-best across 7 datasets vs iTransformer, PatchTST, DLinear.
- Ablation: removing global token degrades performance notably; cross-attention outperforms simple add/concat of exogenous.
- Robust to missing exogenous data: replacing exogenous with zeros/random causes mild degradation, not collapse.

## Claims

- **TimeXer separates endogenous series (patch-level self-attention) and exogenous variables (variate-level cross-attention) through a dual-representation design** with a learnable global token as bridge. [Evidence: Section 3, Figure 2]
- **The endo/exo split with cross-attention outperforms concatenation-based approaches**, confirming the importance of asymmetric treatment of target vs. covariate variables. [Evidence: Table 4 ablation]
- **TimeXer achieves SOTA on electricity price forecasting benchmarks with exogenous variables**, outperforming DLinear and other linear models by a significant margin when covariates are informative. [Evidence: Table 2]
- **Exogenous variate-level encoding handles irregularities** (missing values, frequency mismatch, different look-back lengths) without requiring time-alignment. [Evidence: Section 4.3.1]

## Caveats

- Standard benchmarks (ETT, Weather, Electricity) have weak inter-variate signal; gains from exogenous variables only materialize on EPF-type datasets with genuine exogenous drivers.
- Transformer backbone is heavier than DLinear or N-BEATS — not trivially deployable at 200M-series scale without additional engineering.
- Cross-attention cost scales with number of exogenous variables; sparse covariate selection upstream (P2) would be needed.

## Applicability to P1

**High and direct — Priority 2 backbone for P1.** P1's domain (commodity/energy price forecasting) aligns directly with TimeXer's EPF evaluation setting. TimeXer is validated on 5 EPF datasets where genuine exogenous covariates (load, gas price, weather) drive price — exactly the covariate-rich, non-stationary data P1 targets. The endo/exo asymmetric design is the template for P1's covariate architecture: cluster-pretrained backbone handles endogenous temporal dynamics; cross-attention layer handles exogenous macro/supply/weather indicators. The global token bridge aligns with P1's sparse hierarchical covariate selection goal. Use TimeXer when exo effect is confirmed to be large; use NBEATSx when a simpler concatenation baseline suffices.

## Related

- [src-2026-06-lim-tft-2021](src-2026-06-lim-tft-2021.md) — TFT: earlier endo/exo split baseline with variable selection
- [src-2026-06-arango-chronosx](src-2026-06-arango-chronosx.md) — ChronosX: similar adapter approach for pretrained models
- [src-2026-06-lu-cats-ats](src-2026-06-lu-cats-ats.md) — CATS-ATS: alternative constructed auxiliary series approach
