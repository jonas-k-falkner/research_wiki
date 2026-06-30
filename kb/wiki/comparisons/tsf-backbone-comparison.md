---
type: comparison
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-zeng-dlinear
- src-2026-06-oreshkin-nbeats
- src-2026-06-challu-nhits
- src-2026-06-olivares-nbeatsx
- src-2026-06-wang-timexer
- src-2026-06-arango-chronosx
- src-2026-06-han-unica
- src-2026-06-potapczinski-apollopfn
- src-2026-06-lu-cats-ats
- src-2026-06-wu-autoformer
- src-2026-06-ekambaram-ttm
- src-2026-06-chen-closer-look-transformers
- src-2026-06-lim-tft-2021
tags:
- backbone
- comparison
- timeseries-forecasting
---

# TSF Backbone Comparison for P1

This table compares backbone architectures and covariate-adapter approaches reviewed during I-P1-C. "Relevant for P1?" reflects direct applicability to cluster-pretrained demand forecasting with sparse exogenous covariates.

## Backbone landscape

| Model | Type | Exogenous covariates | Key benchmark result | Relevant for P1? |
|---|---|---|---|---|
| DLinear | Linear (one-layer) | No | Outperforms FEDformer/Autoformer/Informer by 20–50% MSE on 9 LTSF benchmarks (ETT, Electricity, Traffic, Weather, ILI, Exchange-Rate) | **Yes — compact backbone baseline** |
| N-BEATS | MLP stack (residual basis expansion) | No | Best OWA 0.795 on M4 (winner 0.821); SOTA on M3, TOURISM; pure DL, no TS-specific components | **Yes — strong MLP backbone** |
| N-HiTS | MLP + hierarchical interpolation | No | ~20% avg improvement over Autoformer/Informer on 6 long-horizon benchmarks; 50x compute reduction | **Yes — best long-horizon MLP** |
| NBEATSx | MLP stack (N-BEATS + exogenous) | Yes (concatenation) | ~20% over N-BEATS; SOTA on EPF across 5 power markets; interpretable decomposition | **Yes — MLP + covariate baseline** |
| TFT | Transformer (LSTM+attn, variable selection) | Yes (softmax VarSelect + LSTM encoders) | SOTA on retail/energy tasks requiring exogenous (traffic, electricity, retail). Already ingested in I-P1-B. | **Yes — baseline with variable selection** |
| TimeXer | Transformer (patch-self-attn + variate cross-attn) | Yes (cross-attention) | SOTA on 5 EPF datasets; SOTA/near-SOTA on 7 LT multivariate benchmarks; avg MSE 0.307 vs DLinear 0.366 on EPF | **Yes — endo/exo split template for P1** |
| ChronosX | TSFM adapter (Chronos + IIB/OIB FFN) | Yes (adapter modules) | 22% improvement over Chronos on 32 synthetic covariate datasets; evaluated on 18 real covariate datasets | Adjacent — adapter pattern reference |
| UNICA | TSFM adapter (homogenization + dual attention fusion) | Yes (homogeneous + heterogeneous) | Outperforms ChronosX and task-specific models on 12 unimodal + 2 multimodal covariate datasets | Adjacent — heterogeneous covariate template |
| ApolloPFN | Prior-fitted network (time-aware PFN) | Yes (native, zero-shot) | SOTA on M5 (with promotions) and EPF benchmarks in zero-shot setting | Adjacent — zero-shot covariate reference |
| CATS-ATS | MLP + constructed auxiliary series | Constructed (not external) | SOTA multivariate benchmarks with 2-layer MLP; matches or beats Transformer methods | Adjacent — inter-series relationship method |
| TTM (Tiny Time Mixer) | TSFM MLP-Mixer | Optional (fine-tuning Exogenous Mixer) | Outperforms Chronos/TimesFM/Moirai/MOMENT zero-shot; 1M–5M params; CPU-runnable | Adjacent — compact TSFM reference |
| Autoformer | Transformer (auto-correlation + decomposition) | No | 38% improvement over Informer on 6 LT benchmarks (NeurIPS 2021). Outperformed by DLinear. | Background only |
| TimeMixer++ | MLP-Mixer (multi-scale, multi-resolution) | No | SOTA across 8 TS analysis tasks (forecasting, classification, anomaly detection, imputation) | Background — if multi-task needed |
| TiRex | xLSTM (zero-shot TSFM) | No | SOTA on GiftEval and Chronos-ZS zero-shot benchmarks | Background — no covariate support |

## Key findings for P1

### 1. Compact backbone sufficiency (DLinear evidence)

DLinear (a one-layer linear model) consistently outperforms all Transformer-based LTSF models on standard benchmarks by 20–50% MSE. Chen et al. (2025) explains why: these benchmarks are predominantly self-dependent and stationary, so intra-variate temporal modeling (captured perfectly by a linear layer) dominates. This strongly supports the P1 hypothesis that **a compact linear or MLP backbone suffices for the temporal component**, and the architecture investment should go into covariate integration, not backbone complexity.

**Caveat**: standard benchmark results may not transfer to demand data with genuine exogenous drivers (promotions, holidays). TimeXer shows that Transformer cross-attention beats DLinear when covariates are informative (EPF datasets). P1 must validate on real covariate-rich data.

### 2. Covariate gap in leading TSFMs

All four covariate-adapter papers (ChronosX, UNICA, ApolloPFN, CATS-ATS) explicitly identify that Chronos, TimesFM, MOMENT, Sundial, TimeMoE, LagLlama, and TimeLLM do not support exogenous covariates. Only Moirai partially supports homogeneous covariates via any-variate attention, but with mixed results. This **validates the covariate adapter research direction** and confirms that P1's covariate architecture is not solved by existing TSFMs.

### 3. Preferred P1 backbone architecture

Evidence points toward an **MLP-stack backbone (N-BEATS / N-HiTS / NBEATSx family) or compact linear (DLinear) with a separate exogenous adapter** rather than a full Transformer architecture:
- MLP + covariate concatenation (NBEATSx) is proven effective for demand-like tasks with real covariates.
- TimeXer's cross-attention pattern is the strongest template if a Transformer backbone is chosen.
- Transformer complexity is not justified for the temporal backbone given DLinear's results.
- TTM demonstrates that MLP-Mixer pretraining is viable at <5M parameters — relevant for P1's cluster-pretrained scale.

### 4. Exogenous integration strategies ranked

| Strategy | Model | Complexity | Validated on real covariates |
|---|---|---|---|
| Concatenation | NBEATSx, NHiTS | Low | Yes (EPF) |
| Cross-attention (variate-level) | TimeXer | Medium | Yes (EPF, multi-task) |
| FFN adapter (frozen pretrained) | ChronosX | Low | Partial (synthetic + 18 real) |
| Dual attention fusion | UNICA | Medium | Yes (multimodal) |
| Native PFN joint attention | ApolloPFN | High | Yes (M5, EPF) |
| Constructed auxiliary series | CATS-ATS | Medium | Yes (MV benchmarks) |

## Open questions

- Does DLinear/N-BEATS performance on standard benchmarks generalize to retail demand SKU series with strong promotional effects?
- Can sparse hierarchical covariate selection (P2 embeddings → top-k covariates) improve over TimeXer's full cross-attention for P1's high-cardinality covariate setting?
- Is cluster-pretraining meaningful on top of a frozen general TSFM (TTM/Chronos approach), or does domain-specific cluster training from scratch outperform?
