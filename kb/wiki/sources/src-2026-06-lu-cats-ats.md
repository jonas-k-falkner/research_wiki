---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-lu-cats-ats
tags:
- timeseries-forecasting
- backbone
- exogenous
- multivariate
zotero: luCATSEnhancingMultivariate2026
source_hash: b906185242f2b668da651ecbabc37bd88c2dbe3c2278a5caf94000f2f55a15b7
---

# CATS: Enhancing Multivariate Time Series Forecasting by Constructing Auxiliary Time Series as Exogenous Variables

**Lu et al. (Georgia Tech + AWS, ICML 2024)**

## Summary

CATS addresses the paradox that univariate models often outperform multivariate models by introducing Auxiliary Time Series (ATS). These are constructed from the original multivariate input to explicitly represent inter-series relationships, then fed as exogenous variables to the predictor. The predictor (even a simple 2-layer MLP) jointly forecasts original and auxiliary series, then a linear projection merges the multivariate information back into the original series predictions via residual correction.

## Architecture

- **ATS construction**: M constructors F_m: R^{L_I×C} → R^{L_I×n_m} produce N auxiliary series.
- **First-stage prediction**: predictor Φ_{N+C}([A_I, X_I]) → [Â_P, X̂_P].
- **Projection**: linear mapping P_ij contracts the N+C channels back to C-dimensional OTS space → X̃_P capturing inter-series trends.
- **Final output**: X̂*_P = X̂_P + X̃_P (intra-series temporal + inter-series multivariate residual).
- Three key principles for ATS: continuity (low-pass via L_cont loss), sparsity (channel attention + adaptive temporal cutoff), variability.
- With 2-layer MLP backbone, CATS achieves SOTA on multivariate benchmarks.

## Key results

- With a simple MLP predictor, CATS achieves state-of-the-art on long-term multivariate forecasting benchmarks, outperforming complex Transformer models.
- Substantially fewer parameters than prior multivariate models.
- Works even when inter-series relationships are weak: channel sparsity mechanism zeroes out unnecessary ATS.

## Claims

- **A 2-layer MLP with CATS auxiliary series achieves state-of-the-art multivariate forecasting**, confirming that the key challenge is modeling inter-series relationships, not backbone expressiveness. [Evidence: Table 1, ICML 2024]
- **Constructing auxiliary series as exogenous variables and enforcing continuity/sparsity/variability enables adaptive inter-series relationship capture** without requiring complex attention mechanisms. [Evidence: Section 3.2]
- **Channel sparsity makes CATS robust when inter-series relationships are weak**, preventing overfitting by zeroing out uninformative auxiliary channels. [Evidence: Section 3.2.2]

## Caveats

- ATS are constructed from the same input series (not true external covariates) — this is multivariate modeling disguised as exogenous variable modeling.
- No true exogenous support: covariates external to the system are not handled.
- The "enhancing" framing treats constructed ATS as exogenous, which may confuse the endo/exo distinction in practical applications.

## Applicability to P1

Adjacent. CATS's insight about separating intra-series temporal modeling from inter-series relationship modeling via a residual correction mechanism is architecturally interesting for P1's covariate integration. The sparsity mechanism (zeroing uninformative ATS channels) is analogous to P1's sparse hierarchical covariate selection goal. However, CATS does not handle true exogenous covariates from outside the system.

## Related

- [src-2026-06-wang-timexer](src-2026-06-wang-timexer.md) — TimeXer: proper exogenous variable handling
- [src-2026-06-zeng-dlinear](src-2026-06-zeng-dlinear.md) — DLinear: simpler baseline CATS improves upon
- [src-2026-06-oreshkin-nbeats](src-2026-06-oreshkin-nbeats.md) — N-BEATS: comparable MLP backbone
