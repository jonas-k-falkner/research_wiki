---
type: comparison
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
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
- src-2026-06-wang-timemixer
- src-2026-06-huang-timekan
- src-2026-06-zanotti-retraining-frequency
tags:
- backbone
- comparison
- timeseries-forecasting
---

# TSF Backbone Comparison for P1

This table compares backbone architectures and covariate-adapter approaches reviewed during I-P1-C. "Relevant for P1?" reflects direct applicability to cluster-pretrained demand forecasting with sparse exogenous covariates.

## Backbone landscape

**IMPORTANT: benchmark dependency.** Academic LTSF benchmarks (ETT×4, Weather, Electricity, Traffic) are self-dependent and stationary per Chen et al. 2025 — intra-variate temporal patterns dominate, so ranking there does not transfer to real retail demand with promotional covariates. Real competition benchmarks (M5, VN1, M4, EPF) show a different picture. Both tiers are tracked below.

### Academic LTSF benchmarks (ETT, Weather, Electricity — NOT retail demand)

**Tier 1 — 2024–2025 SOTA**: TimeKAN, TimeMixer++, iTransformer  
**Tier 2 — 2023–2024 strong baselines**: PatchTST, TimeMixer, N-HiTS, N-BEATS  
**Tier 3 — minimal baselines**: DLinear, NLinear — outperformed by Tier 1 by a significant margin  
**Background only**: Autoformer, Informer, FEDformer

### Real price / energy benchmarks (EPF, commodity prices — **primary for P1**)

**P1 primary domain: procurement-side input forecasting** — commodity prices, energy futures, electricity prices, FX. Non-stationary, volatile, exo-covariate-rich.

**EPF (electricity price forecasting) — primary real benchmark:**  
- NBEATSx: SOTA, ~20% over N-BEATS; MLP + exo concatenation  
- TimeXer: SOTA on 5 EPF datasets, avg MSE 0.307 vs DLinear 0.366; best validated endo/exo cross-attention  
- TimeKAN, iTransformer, TimeMixer: **no published EPF evaluation**

**Real retail demand benchmarks (M5, VN1, M4 — less relevant to P1's price focus):**  
- N-BEATS, N-HiTS: DL SOTA on M5/VN1 (Zanotti 2025); competition-benchmark proven  
- LGBM/XGBoost: top solutions in M5 and other demand competitions  
- ApolloPFN: zero-shot SOTA on M5 with promotions/prices

Demand benchmarks (M5/VN1) inform backbone design decisions at the methodological level but are not P1's primary validation target.

| Model | Type | Exo covariates | Key benchmark result | Relevant for P1? |
|---|---|---|---|---|
| DLinear | Linear (one-layer) | No | Outperforms FEDformer/Autoformer/Informer by 20–50% MSE (AAAI 2023). **Outperformed by PatchTST, iTransformer, TimeMixer, TimeMixer++, TimeKAN.** "Significant gap" vs 2025 SOTA. | **Yes — minimal ablation baseline only** |
| PatchTST | Transformer (patch-wise, intra-variate attn) | No | Outperforms DLinear on standard benchmarks (ICLR 2023). Outperformed by iTransformer, TimeMixer on most benchmarks. | Yes — intermediate reference (not primary) |
| iTransformer | Transformer (variate-level tokens, inter-variate attn) | No | Described as "current SOTA in TSF" by multiple 2024 papers. Best on high-dimensional datasets (Electricity). Outperformed by TimeMixer++ on most tasks. | **Yes — strong compact backbone candidate** |
| N-BEATS | MLP stack (residual basis expansion) | No | Best OWA 0.795 on M4; SOTA on M3, TOURISM | **Yes — strong MLP backbone** |
| N-HiTS | MLP + hierarchical interpolation | No | ~20% avg improvement over Autoformer/Informer; 50× compute reduction | **Yes — best long-horizon MLP** |
| NBEATSx | MLP stack (N-BEATS + exogenous) | Yes (concatenation) | ~20% over N-BEATS; SOTA on EPF; interpretable decomposition | **Yes — MLP + covariate baseline** |
| TFT | Transformer (LSTM+attn, variable selection) | Yes (softmax VarSelect) | SOTA on retail/energy with exogenous. Already ingested I-P1-B. | **Yes — baseline with variable selection** |
| TimeXer | Transformer (patch-self-attn + variate cross-attn) | Yes (cross-attention) | SOTA on 5 EPF datasets; avg MSE 0.307 vs DLinear 0.366 on EPF | **Yes — endo/exo split template for P1** |
| TimeMixer++ | MLP-Mixer (multi-scale, multi-resolution) | No | SOTA across 8 TS tasks. 7.3% over iTransformer on Electricity. | **Yes — strongest backbone without covariates** |
| TimeKAN | KAN + frequency decomposition | No | 2025 SOTA on most LT benchmarks. Smaller params than TimeMixer. "DLinear shows significant gap." Best except iTransformer on Electricity. | **Yes — current performance ceiling** |
| ChronosX | TSFM adapter (Chronos + FFN) | Yes (adapter) | 22% over Chronos on covariate datasets | Adjacent — adapter pattern reference |
| UNICA | TSFM adapter (dual attention fusion) | Yes (homogeneous + heterogeneous) | Outperforms ChronosX; multimodal covariate datasets | Adjacent — heterogeneous covariate template |
| ApolloPFN | Prior-fitted network | Yes (native, zero-shot) | SOTA on M5 (with promotions) and EPF in zero-shot | Adjacent — zero-shot covariate reference |
| CATS-ATS | MLP + constructed auxiliary series | Constructed | SOTA multivariate benchmarks with 2-layer MLP | Adjacent — inter-series relationship method |
| TTM | TSFM MLP-Mixer | Optional (fine-tuning) | Outperforms Chronos/TimesFM zero-shot; 1M–5M params | Adjacent — compact TSFM reference |
| Autoformer | Transformer (auto-correlation) | No | Outperformed by DLinear. | Background only |
| TiRex | xLSTM (zero-shot TSFM) | No | SOTA on GiftEval and Chronos-ZS | Background — no covariate support |

## Key findings for P1

### 1. Compact backbone sufficiency — updated (2025)

**Original finding (2022–2023):** DLinear outperforms Transformer-based LTSF models by 20–50% MSE. The thesis "compact backbone suffices for temporal modeling" holds.

**Updated finding (2024–2025):** DLinear is no longer competitive with current SOTA. PatchTST (2023), iTransformer (2024), TimeMixer/TimeMixer++ (2024), and TimeKAN (2025) all outperform DLinear — and TimeKAN explicitly notes DLinear shows a "significant gap." The performance frontier has moved well past DLinear.

**What remains valid:** Chen et al. (2025) — [src-2026-06-chen-closer-look-transformers](../sources/src-2026-06-chen-closer-look-transformers.md) — explains why ALL models (DLinear and iTransformer alike) succeed on standard benchmarks: intra-variate patterns dominate because benchmarks are self-dependent and stationary. The core implication for P1 is unchanged: **architecture investment should go into covariate integration, not backbone complexity.** But the *starting baseline* should be iTransformer or TimeMixer rather than DLinear.

**Why DLinear is still useful:** as the minimal ablation baseline to isolate covariate contribution. "Does the covariate layer add value over DLinear?" is a well-specified ablation.

**Caveat**: benchmark results may not transfer to demand data with genuine exogenous drivers. TimeXer shows Transformer cross-attention beats all alternatives when covariates are informative (EPF). P1 must validate on real covariate-rich data.

### 2. Covariate gap in leading TSFMs

All four covariate-adapter papers (ChronosX, UNICA, ApolloPFN, CATS-ATS) explicitly identify that Chronos, TimesFM, MOMENT, Sundial, TimeMoE, LagLlama, and TimeLLM do not support exogenous covariates. Only Moirai partially supports homogeneous covariates via any-variate attention, but with mixed results. This **validates the covariate adapter research direction** and confirms that P1's covariate architecture is not solved by existing TSFMs.

### 3. Preferred P1 backbone architecture (updated 2026-06-30 — price/commodity focus)

**P1 domain: procurement-side price/commodity/energy forecasting.** Primary real benchmark: EPF.

- **NBEATSx** (Priority 1 — start here): MLP + exo concatenation; SOTA on EPF; interpretable basis decomposition shows exogenous contribution alongside trend/seasonality. **Simplest architecture validated on EPF with genuine covariates.**
- **TimeXer** (Priority 2 — when exo drives the forecast): patch-attn + cross-attn; SOTA on 5 EPF datasets; asymmetric endo/exo design is the template for P1's covariate architecture. Use when the exo covariate effect is confirmed large.
- **iTransformer** (Priority 3 — correlated price series): channel-wise attention appropriate for commodity complex (energy, metals) where inter-series dependencies carry signal; no exo natively; academic benchmark proven.
- **N-HiTS** (Priority 4 — MLP ablation without exo; demand-domain proof): strong MLP baseline; proven on M4/M5/real retail; less directly validated on price/EPF domain. Useful as a no-exo ablation.
- **DLinear**: minimal ablation baseline only.
- **TimeKAN** (Priority 5 — academic LTSF frontier only): 2025 SOTA on ETT/Weather; **no EPF or commodity evaluation**; KAN blocks complicate AttGrad attribution; significantly more complex.

**Simplified decision tree for P1 price forecasting:**
1. Start: NBEATSx (EPF-proven; MLP + exo; interpretable)
2. Exo effect large → upgrade to TimeXer (cross-attention)
3. Correlated series (energy complex, metals) → add iTransformer as a comparison
4. Ablation baselines → DLinear (linear) and N-HiTS (MLP without exo)

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
