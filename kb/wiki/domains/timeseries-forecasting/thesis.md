---
type: domain
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-tsf-literature-review
- src-2026-06-zeng-dlinear
- src-2026-06-chen-closer-look-transformers
- src-2026-06-oreshkin-nbeats
- src-2026-06-challu-nhits
- src-2026-06-olivares-nbeatsx
- src-2026-06-wang-timexer
- src-2026-06-arango-chronosx
- src-2026-06-han-unica
- src-2026-06-potapczinski-apollopfn
- src-2026-06-lu-cats-ats
- src-2026-06-wang-timemixer
- src-2026-06-huang-timekan
- src-2026-06-zanotti-retraining-frequency
- src-2026-06-rizvi-glinear
- src-2026-06-pasche-extreme-conformal
- src-2026-06-zhang-switching-ssm
- src-2026-06-kumar-mixbeats
- src-2026-06-liang-itfkan
- src-2026-06-fein-ashley-spectre
- src-2026-06-tsitsulin-embedding-quality
tags:
- thesis
- forecasting
---

# Domain thesis: Time-series forecasting

## Current thesis

P1 is the attribution and robust forecasting layer for **procurement-side intelligence**: commodity prices, energy futures, electricity prices, FX — volatile, non-stationary input data, not demand/sales. **Primary forecast horizon: weekly/monthly long-horizon** (e.g., 4–52 week ahead commodity prices). Day-ahead scenarios are a secondary use case (e.g., power markets). The cluster approach groups price series by market type and volatility regime. The architecture investment priority is the covariate attribution layer (sparse hierarchical α-entmax + AttGrad), not the backbone.

**Real benchmark context**: EPF (electricity price forecasting) is validated on NBEATSx and TimeXer, but EPF is a **day-ahead benchmark** — a frequency mismatch with P1's primary weekly/monthly use case. M4 monthly series are frequency-matched but are demand/macro series, not commodity prices. There is currently no standardised weekly/monthly commodity price forecasting benchmark in the literature — this is an open gap.

## Most important unresolved question

Do volatility-regime clusters derived from price-series embeddings produce regime-consistent groups for shared models, or is explicit regime detection (structural break tests, vol-regime classifiers) required before clustering?

## Preferred near-term path

1. Run the P1 cluster-quality gate — adapted for price/commodity series (volatility regime consistency, not demand-seasonality consistency).
2. Prototype a single cluster with **NBEATSx** (MLP + exo concatenation; EPF-proven architecture; note EPF is day-ahead, frequency mismatch with primary use case — validate separately on weekly/monthly data) if the gate passes or after regime sub-clustering.
3. Add cross-attention covariate integration via **TimeXer** if exo effect is confirmed large on the target dataset.
4. Validate against GARCH/ARIMAX and LGBM on **internal weekly/monthly commodity/price data** and EPF benchmarks (secondary; day-ahead only). M4 monthly is the best available frequency-matched public benchmark proxy until a commodity price benchmark is established.
5. Track attribution quality (AttGrad polarity consistency) as a first-class success metric alongside forecast accuracy.

## Key assumptions

| Assumption | Status | Decision impact |
|---|---|---|
| 200M series provide enough training diversity | unvalidated in current wiki | Determines whether P1 can generalize zero-shot |
| Shape + regime clusters are learnable and useful | testing required | Determines P1 viability |
| Compact backbone suffices for temporal modeling; invest budget in covariate layer | **evidence-backed and strengthened** ([Chen 2025](../../sources/src-2026-06-chen-closer-look-transformers.md)): all 2022–2025 models succeed on standard benchmarks due to benchmark nature, not architecture. For **real benchmarks** (M5, VN1) N-HiTS/N-BEATS are DL SOTA ([Zanotti 2025](../../sources/src-2026-06-zanotti-retraining-frequency.md)); iTransformer/TimeKAN SOTA is academic LTSF only. Starting point is now **N-HiTS** (real benchmark proof) with NBEATSx for covariates. | Supports covariate architecture focus; use N-HiTS not iTransformer as the real-benchmark starting point |
| Hierarchical entmax can stabilize covariate selection | plausible | Influences P1 model architecture |
| P2 embeddings improve covariate layer | unvalidated | Influences sequencing of full P1 build |
| Standard benchmark results transfer to commodity/energy price data with real covariates | **not confirmed** ([Chen 2025](../../sources/src-2026-06-chen-closer-look-transformers.md) warns benchmarks are self-dependent/stationary; EPF is genuinely non-stationary and spike-prone) | Requires P1 validation on price/commodity data; EPF is the primary target |

## External literature positioning

A deep-research synthesis of 2024–2026 TSF ([sources/src-2026-06-tsf-literature-review](../../sources/src-2026-06-tsf-literature-review.md)) splits the field into two streams: stronger general backbones and a covariate-adapter stream. This is now verified against named primaries (I-P1-C ingest, 2026-06-29). Key confirmed findings:

**1. Compact backbone sufficiency — confirmed and updated.**
Zeng et al. 2023 ([src-2026-06-zeng-dlinear](../../sources/src-2026-06-zeng-dlinear.md)) shows DLinear outperforms the Transformer-based LTSF models of its era by 20–50% MSE. Chen et al. 2025 ([src-2026-06-chen-closer-look-transformers](../../sources/src-2026-06-chen-closer-look-transformers.md)) explains: standard benchmarks are self-dependent and stationary, so intra-variate temporal modeling dominates — this is why DLinear could match or beat complex Transformers.

**2024–2025 update:** DLinear is no longer the performance frontier. PatchTST (ICLR 2023) outperformed it; iTransformer (ICLR 2024) is described as "current SOTA in TSF" by multiple 2024 papers; TimeMixer/TimeMixer++ (2024) further outperform iTransformer; TimeKAN (2025, [src-2026-06-huang-timekan](../../sources/src-2026-06-huang-timekan.md)) is 2025 SOTA and explicitly notes "DLinear already shows a significant gap compared to SOTA." The core thesis is unchanged — invest in covariate architecture — but the appropriate baseline is now iTransformer or TimeMixer. DLinear is retained as the minimal ablation baseline.

**Caveat**: Chen et al.'s insight applies to ALL these models: on non-stationary data with genuine inter-variate signal (e.g. demand with promotional covariates), the performance ordering can change. TimeXer shows cross-attention beats DLinear on EPF. P1 must validate on covariate-rich data.

**Real benchmark note:** TimeKAN, iTransformer, and TimeMixer have no published evaluation on EPF or commodity price data. Their SOTA claims are **exclusively on academic LTSF benchmarks** (ETT×4, Weather, Electricity). For P1's price/commodity/energy focus, NBEATSx ([src-2026-06-olivares-nbeatsx](../../sources/src-2026-06-olivares-nbeatsx.md)) and TimeXer ([src-2026-06-wang-timexer](../../sources/src-2026-06-wang-timexer.md)) are the architectures validated on EPF. For retail/demand context, Zanotti 2025 ([src-2026-06-zanotti-retraining-frequency](../../sources/src-2026-06-zanotti-retraining-frequency.md)) uses N-BEATS and N-HiTS as DL SOTA on M5/VN1 — useful as methodological background but not P1's primary domain.

**2. Covariate gap in TSFMs — confirmed across four papers.**
ChronosX ([src-2026-06-arango-chronosx](../../sources/src-2026-06-arango-chronosx.md)), UNICA ([src-2026-06-han-unica](../../sources/src-2026-06-han-unica.md)), ApolloPFN ([src-2026-06-potapczinski-apollopfn](../../sources/src-2026-06-potapczinski-apollopfn.md)), and CATS-ATS ([src-2026-06-lu-cats-ats](../../sources/src-2026-06-lu-cats-ats.md)) each explicitly identify that leading TSFMs — Chronos, TimesFM, MOMENT, Sundial, TimeMoE, LagLlama — ignore exogenous covariates. Only Moirai partially handles homogeneous covariates. This confirms that the covariate-adapter research stream exists precisely because the dominant TSFMs have this gap.

**3. TimeXer as endo/exo split template — confirmed.**
TimeXer ([src-2026-06-wang-timexer](../../sources/src-2026-06-wang-timexer.md)) demonstrates that separating endogenous (patch-level self-attention) from exogenous (variate-level cross-attention) through a learnable global token bridge achieves SOTA on electricity price forecasting benchmarks with covariates, outperforming DLinear by a significant margin when covariates are genuinely informative.

**4. TS foundation models are background, not blueprints.**
The TSFM wave (Chronos, TimesFM, Moirai, TTM, TiRex) is best understood as a zero-shot generalization paradigm without covariate support. For P1's cluster-pretrained + covariate design, the MLP/linear backbone family (N-BEATS, N-HiTS, NBEATSx, DLinear) is more directly relevant than large-scale TSFMs.

## Backbone landscape

See [comparisons/tsf-backbone-comparison](../../comparisons/tsf-backbone-comparison.md) for the full comparison table covering 15 models.

**Summary recommendation for P1 backbone (updated 2026-06-30 — price/commodity/EPF focus)**:

**Primary horizon: weekly/monthly long-horizon commodity price forecasting. Day-ahead (EPF) = secondary.**

| Priority | Architecture | Rationale |
|---|---|---|
| 1 (start here) | NBEATSx | MLP + exo concatenation; EPF SOTA (~20% over N-BEATS); interpretable decomposition; simplest real-benchmark–proven covariate model. **Frequency caveat**: EPF is day-ahead; validate separately on weekly/monthly data. |
| 2 (long-horizon; no exo needed) | N-HiTS | Hierarchical multi-rate pooling + interpolation; designed for long-horizon; M4 monthly SOTA (frequency-matched proxy); 50× faster than Transformers. More appropriate than NBEATSx for weekly/monthly horizons without large exo effect. |
| 3 (when exo drives the series) | TimeXer | Patch-attn + cross-attn; SOTA on 5 EPF datasets (avg MSE 0.307 vs DLinear 0.366); asymmetric endo/exo split validated. **Frequency caveat**: EPF is day-ahead. |
| 4 (correlated price series) | iTransformer | Channel-wise attention; good for correlated commodity complex (energy, metals); no exo natively |
| 5 (simplicity baseline with RevIN) | GLinear | Gaussian-activated linear + RevIN; data-efficient for smaller weekly/monthly datasets; outperforms DLinear/NLinear; no exo natively. Validated on academic LTSF only (ETTh1, Electricity, Weather, Traffic). |
| 6 (ablation) | DLinear | Minimal linear baseline to isolate covariate contribution |
| 7 (academic LTSF frontier) | TimeKAN | 2025 SOTA on ETT/Weather only; no EPF/commodity evaluation; complex; KAN complicates AttGrad |
| Avoid for temporal backbone | Autoformer, Informer, FEDformer | Outperformed by DLinear; complexity not justified |

**Key caveat**: TimeKAN/iTransformer/TimeMixer SOTA is measured on academic LTSF benchmarks (ETT×4, Weather, Electricity), which are self-dependent and stationary. None have published results on EPF or commodity prices. **For P1's price/commodity focus, NBEATSx and TimeXer are the architectures with evidence on real benchmarks (EPF) — but EPF is day-ahead, not the weekly/monthly horizon that is P1's primary target.** N-HiTS is the best frequency-matched backbone (M4 monthly), but lacks covariate support.

## SSM and linear-RNN landscape (background)

State space models and linear RNNs (Mamba, RWKV, xLSTM, HGRN, GLA, etc.) represent a class of subquadratic alternatives to Transformers designed primarily for language modelling. Their applicability to multivariate TSF is limited: [Wang et al. (2024)](../../sources/src-2026-06-wang-mamba-tsf.md) find that Mamba-based S-Mamba is competitive on high-variate periodic datasets (Traffic, Electricity) but shows suboptimal results on low-variate aperiodic benchmarks (ETT, Exchange) where DLinear is competitive or better — consistent with the DLinear finding that architectural complexity does not guarantee TSF gains in the regimes most analogous to retail SKU forecasting. The majority of SSM/linear-RNN papers (Mamba-2, RWKV, Eagle/Finch, HGRN, HGRN2, GLA, Gated Delta Networks, Longhorn, TTT, GSA, Jamba) report no TSF evaluation at all, with benchmarks focused exclusively on language modeling. P1 uses a compact MLP or linear backbone rather than SSMs for three reasons: (1) no demonstrated TSF accuracy advantage over DLinear in low-variate aperiodic regimes; (2) SSM hidden states are opaque to the AttGrad attribution protocol; (3) MLP/linear models have better serialization and integration properties with the forecast\_pipeline library.

Sources: [src-2026-06-wang-mamba-tsf](../../sources/src-2026-06-wang-mamba-tsf.md), [src-2026-06-gu-mamba](../../sources/src-2026-06-gu-mamba.md), [src-2026-06-dao-mamba2](../../sources/src-2026-06-dao-mamba2.md).

## Literature to integrate

External gaps not yet in the wiki — all `[gap]`:

- **EPF survey** (Weron 2014 or equivalent) — canonical review of electricity price forecasting methods, datasets, and evaluation conventions. `[gap]`
- **LEAR model** (Lago et al. 2018) — statistical EPF baseline that NBEATSx reports beating by 20%. Required to validate NBEATSx's EPF claim chain. `[gap]`
- **GARCH / GARCH-X** — established volatility model family; P1 success criterion references "outperform GARCH" but zero GARCH literature is in the wiki. At minimum: Bollerslev 1986 (GARCH), Engle 2002 (DCC-GARCH), or GARCH-X survey. `[gap]`
- **Commodity price forecasting survey** — no standardized commodity price benchmark (crude oil, metals, agricultural) in the wiki; EPF covers only electricity. `[gap]`
- **Structural break / change-point detection for price series** — methods like Bai-Perron test or PELT; required to validate the "explicit regime detection" branch. `[gap]`

## Sources & related

- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../../sources/src-2026-06-p1-cluster-pretrained-deep-models.md), [sources/src-2026-06-tsf-literature-review](../../sources/src-2026-06-tsf-literature-review.md)
- [sources/src-2026-06-zeng-dlinear](../../sources/src-2026-06-zeng-dlinear.md) — DLinear evidence for compact backbone
- [sources/src-2026-06-wang-timexer](../../sources/src-2026-06-wang-timexer.md) — TimeXer endo/exo split
- [sources/src-2026-06-arango-chronosx](../../sources/src-2026-06-arango-chronosx.md), [sources/src-2026-06-han-unica](../../sources/src-2026-06-han-unica.md), [sources/src-2026-06-potapczinski-apollopfn](../../sources/src-2026-06-potapczinski-apollopfn.md) — covariate gap evidence
- [comparisons/tsf-backbone-comparison](../../comparisons/tsf-backbone-comparison.md)
- Project: [projects/p1-cluster-pretrained-deep-models](../../projects/p1-cluster-pretrained-deep-models.md)
