---
type: project
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
  - src-2026-06-p1-cluster-pretrained-deep-models
  - src-2026-06-tsf-literature-review
  - src-2026-06-chen-channel-clustering
  - src-2026-06-qiu-duet-clustering
  - src-2026-06-aghabozorgi-ts-clustering-survey
  - src-2026-06-sen-global-local-forecasting
  - src-2026-06-peters-sparse-seq2seq-2019
  - src-2026-06-lim-tft-2021
  - src-2026-06-jain-attention-not-explanation-2019
  - src-2026-06-wiegreffe-attention-not-not-2019
  - src-2026-06-liu-rethinking-attention-explainability-2022
  - src-2026-06-zeng-dlinear
  - src-2026-06-chen-closer-look-transformers
  - src-2026-06-wang-timexer
  - src-2026-06-arango-chronosx
  - src-2026-06-han-unica
  - src-2026-06-potapczinski-apollopfn
  - src-2026-06-lu-cats-ats
  - src-2026-06-challu-nhits
  - src-2026-06-oreshkin-nbeats
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
  - src-2026-06-beck-xlstm
  - src-2026-06-tan-ts-indexing
  - src-2026-06-ates-counterfactual-ts
  - src-2026-06-zhang-tem-topology
  - src-2026-06-kadra-mesomorphic
  - src-2026-06-embedding-model-v1
tags:
  - forecasting
  - deep-learning
  - scalability
---

# P1 — Cluster-pretrained deep models

## Purpose

Train cluster-routed deep forecasting models on commodity, energy, and price time series — the **input/procurement side** of the supply chain. Target: volatile, non-stationary price data (commodity prices, electricity prices, energy futures, FX) rather than demand/sales series. **Primary forecast horizon: weekly/monthly long-horizon** (weeks to 1+ year ahead commodity prices); day-ahead scenarios (e.g., power markets) are a secondary use case. Core value: **robust price forecasts with interpretable attribution** — surfacing which macro, weather, or supply indicators drove a given price movement, to support procurement and hedging decisions.

## Current thesis

P1 is the attribution + robust forecasting layer for procurement-side intelligence. The cluster approach routes price series by market type and volatility regime (not by SKU demand patterns). The most important near-term question is whether volatility-regime clusters are stable enough for shared models, or whether explicit regime detection and regime sub-clustering is required. The architecture investment priority is the **covariate attribution layer** (sparse hierarchical α-entmax + AttGrad), not the backbone — the backbone needs only to match established EPF/commodity baselines.

## Candidate architecture

Two-stream design: v1 pre-computed embeddings supply rich representation to the selection layer for free; a shallow backbone handles temporal resolution for the forecast.

```text
Portfolio of commodity / energy / price series
  ↓
  ┌─ [offline] precompute v1 embeddings ──────────────────────────────────────┐
  │   z_target = v1.transform(target)                 (128-dim, unit-norm)    │
  │   z_cov_k  = v1.transform(cov_k) for k=1..N      (128-dim, unit-norm)    │
  └────────────────────────────────────────────────────────────────────────────┘
  ↓
  FAISS cluster routing on z_target
    (clusters = energy complex / metals / agricultural / FX / other)
    → optional regime sub-clustering (high-vol vs low-vol; structural breaks)
  ↓
  ┌─ covariate selection (Stream 1 — embedding-based) ────────────────────────┐
  │   query = W_q · z_target  (learned projection 128 → d_sel)               │
  │   keys  = W_k · z_cov_k   (same projection)                              │
  │   scores = query^T key_k / sqrt(d_sel)                                   │
  │   → α-entmax over scores → sparse selection weights                       │
  │       (exact-zero weights = hard covariate gate)                          │
  │   top-k covariates selected for Stream 2                                  │
  │   Phase 0: W_q, W_k learned; v1 embeddings frozen symmetric              │
  │   Phase 1: upgrade z_cov to P2 directed embeddings (no other change)     │
  └────────────────────────────────────────────────────────────────────────────┘
  ↓
  ┌─ temporal re-embedding (Stream 2 — raw series) ───────────────────────────┐
  │   target raw series + top-k covariate raw series                          │
  │   → shallow encoder (1-2 layer TCN or patch encoder)                      │
  │     captures full temporal resolution the 128-dim embedding compresses    │
  └────────────────────────────────────────────────────────────────────────────┘
  ↓
  cluster-specific forecasting backbone (shallow, 2-4 layers):
    NBEATSx (MLP + exo; EPF SOTA; start here)
    or TimeXer (patch-attn + cross-attn; large exo set)
    or iTransformer (channel-wise attn; correlated price complex)
    | DLinear = ablation baseline only |
  ↓
  AttGrad attribution
    (weight × gradient over selection weights + backbone)
  ↓
  price forecast + attribution report
```

**Why the backbone can be shallow:** v1 embeddings supply deep representational signal (shape, volatility structure, Soft-DTW similarity) before the backbone sees anything. The backbone's only remaining job is temporal dynamics at the forecast resolution — no need for deep feature learning. Consistent with TEM topology findings: 2–4 layer Transformer backbones avoid topology degradation ([src-2026-06-zhang-tem-topology](../sources/src-2026-06-zhang-tem-topology.md)).

**Why no projection may even be needed:** v1 has L2 norm regularization pushing embeddings toward unit-norm, so cosine similarity between `z_target` and `z_cov_k` is directly interpretable as structural similarity without any learned projection. A projection is optional and should be evaluated empirically.

## V1 embeddings as covariate selection input (2026-06-30)

The v1 production embedding model ([src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md)) provides P1 with strong covariate representations at zero additional training cost.

**What v1 captures that matters for covariate selection:**
- SL head (Soft-DTW, weight 0.7): shape and structural similarity across variable-length series; DTW-invariant temporal alignment
- GL head (masked MSE, weight 0.3): reconstruction-based regularity; series that share recoverable structure
- MeanMax pooling: both average trend and peak/spike characteristics in a single 128-dim vector

**How it plugs into P1:**

| P1 component | What v1 provides |
|---|---|
| FAISS cluster routing | `z_target` directly routes to nearest cluster prototype |
| Covariate selection query | `z_target` (projected) as the selection query — no re-training needed |
| Covariate selection keys | `z_cov_k` (projected) as per-covariate key — offline precomputed |
| Selection semantics (Phase 0) | Shape/structural similarity (symmetric): "series that look like the target" |
| Selection semantics (Phase 1) | Directed influence (asymmetric): "series that causally drive the target" (P2 upgrade) |

**What v1 does NOT capture for P1:**
- Fine temporal resolution at the forecast horizon (e.g. recent 2-week momentum) — Stream 2 handles this
- Target-specific causal direction (v1 is symmetric by construction) — P2 upgrade path handles this
- Cross-series interaction at training time — backbone handles this

**Phase 0 → Phase 1 upgrade path:** The covariate selection layer's interface is `z_cov_k ∈ ℝ^128`. When P2 is ready, replace v1 embeddings with P2's directed embeddings at this interface. The rest of P1's architecture — projection, α-entmax weights, backbone, AttGrad — requires no modification. This makes P2 a surgical plug-in upgrade to P1's covariate layer.

## Important design update from `p1_cluster-pretrained_deep-models.md`

Source: [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md). The "shared encoder for target and covariate series" described in this note is now identified as **v1** (`ConvAttnEncoder`). For covariate selection, the preferred direction is:

- v1 embeddings as precomputed keys and query (no shared encoder re-training required)
- optional learned projection (128 → d_sel) to adapt embedding space to selection task
- target-query-dependent hierarchical cluster→feature α-entmax
- no residual path bypassing selection
- feature importance by weight × gradient (AttGrad) and cluster sensitivity
- MC-dropout stability checks for confidence

This makes the explanation layer more robust than raw attention weights, especially when covariates are highly correlated.

## Success criteria

| Criterion | Target |
|---|---|
| Forecast accuracy | Match or exceed GARCH/ARIMAX and LGBM on internal weekly/monthly commodity/price data; use EPF benchmarks as secondary (day-ahead) validation for architecture sanity-check |
| Attribution quality | AttGrad identifies top-k macro/supply covariates that align with known market drivers; polarity consistency test (Liu et al. 2022) passes |
| Cluster quality | Low within-cluster variance for volatility regime, seasonality, structural behavior; within-cluster model outperforms global model |
| Robustness | Forecast accuracy degrades gracefully under price spikes and volatility regime shifts, not catastrophically |
| Integration | `ClusterDeepModel` fits forecast pipeline Model ABC and serialization constraints |
| New series onboarding | New commodity / contract routed to cluster and forecast with zero or minimal fold-in |

## Main risks

| Risk | Mitigation |
|---|---|
| Price volatility regime shifts invalidate cluster models faster than demand patterns | Implement explicit regime detection; trigger re-clustering and/or re-routing on structural break signals |
| Non-stationarity of price data makes long-horizon forecasting harder than for stationary demand | Focus on weekly/monthly horizons with RevIN normalization and probabilistic intervals; track calibration not just point accuracy |
| AttGrad attribution is unstable under price spikes (extreme inputs stress the gradient path) | Run MC-dropout stability checks; test attribution consistency under perturbed inputs |
| Covariate selection is unstable under correlated macro inputs | Hierarchical entmax, cluster-level importance, diversity regularization, stability diagnostics |
| PyTorch integration violates library layering/determinism | Implement first-class optional `ClusterDeepModel`; persist routing index and state dict cleanly |
| EPF benchmark does not fully represent commodity (non-electricity) price dynamics | Validate on at least one additional benchmark (e.g., commodity futures) once data is sourced |

## Dependencies

- **v1 embedding model (now):** P1 uses v1 pre-computed embeddings directly for FAISS cluster routing and covariate selection. No P2 needed for Phase 0.
- **P2 (upgrade):** When P2's directed embeddings are ready, they replace v1 embeddings at the covariate selection interface only — surgical, no other architectural changes.
- **P3:** Creates commercial pressure for P1 by surfacing SKU-scaling bottlenecks.

## Contradictions & tensions

- **Determinism vs MC-dropout `[cross-layer, unresolved]`.** `p1_cluster-pretrained_deep-models.md` recommends MC-dropout (multiple stochastic passes) for importance stability, but the `forecast_pipeline` library is deterministic-by-default with explicitly seeded randomness. A `ClusterDeepModel` will need a documented stochasticity carve-out for uncertainty/importance estimation. Cannot be fully resolved until the `forecast_pipeline` repo context is ingested — tracked in [shared/research-backlog](../shared/research-backlog.md).
- **Moat rating — individual components now primary-confirmed; combination remains unmatched.** A primary-source literature pass (I-P1-A/B/C, 2026-06-29) confirms each P1 component has precedent: cluster-first channel routing (CCM, DUET), α-entmax sparse selection (Peters et al. 2019), AttGrad faithful attribution (Liu et al. 2022), and endo/exo backbone split (TimeXer). However, no 2024–2026 paper combines all of these — query-dependent sparse hierarchical gating + cluster-level AttGrad attribution + diversity regularization + MC-dropout stability — in one system. The combination remains a distinct direction. Confidence upgraded from "self-assessed" to "primary-supported" for the component claims; the full-combination novelty is still an inference from coverage gaps, not a direct experimental comparison. Medium confidence. Tracked on [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md).

## Open research questions

- See [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md) (global-vs-clustered-vs-local) and [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md) (entmax vs hard gates).
- **Volatility regime clustering**: do shape-based embeddings separate high/low vol periods, or is an explicit volatility-regime detector required before clustering?
- **Backbone for price spikes**: do MLP-based models (NBEATSx) handle price spike distributions robustly, or is a heavier backbone needed for tail events?
- **Attribution under non-stationarity**: does AttGrad remain faithful (low polarity violation rate) on volatile price data, or do attention gradient paths degrade under distributional shift?
- **Frequency mismatch gap**: EPF (the primary validated benchmark for NBEATSx/TimeXer) is day-ahead. P1's primary use case is weekly/monthly long-horizon. Do EPF-validated architectures transfer to weekly/monthly price forecasting? M4 monthly is the best frequency-matched public proxy but covers demand/macro, not commodity prices.
- **Commodity benchmarks beyond EPF**: EPF is well-studied; comparable open benchmarks for crude oil, metals, or agricultural commodity prices are less standardized. What is the best available public benchmark for non-electricity commodity price forecasting? `[gap]`

## External literature positioning

A deep-research synthesis ([sources/src-2026-06-tsf-literature-review](../sources/src-2026-06-tsf-literature-review.md)) finds adjacent validators for the parts of P1 — TimeXer (asymmetric target/covariate), Channel Clustering → DUET (cluster-first) — while TS foundation models are background, not blueprints, for sparse covariate selection. It also supports a compact backbone (spend the budget on the selector) and no residual bypass.

**Updated with primary-source verification (I-P1-C, 2026-06-29; re-evaluated 2026-06-30):**
- Compact backbone preference is evidence-backed. On academic LTSF benchmarks (ETT, Weather, Electricity), the frontier has moved: DLinear → PatchTST → iTransformer → TimeMixer++ → TimeKAN, with TimeKAN explicitly noting a "significant gap" over DLinear. Chen et al. 2025 explains this: all succeed because benchmarks are self-dependent/stationary. **For P1's price/commodity/energy focus, EPF (electricity price forecasting) is the primary real benchmark** — it features genuine non-stationarity, price spikes, and informative exogenous covariates (load, gas prices, weather). On EPF: NBEATSx ([src-2026-06-olivares-nbeatsx](../sources/src-2026-06-olivares-nbeatsx.md)) and TimeXer ([src-2026-06-wang-timexer](../sources/src-2026-06-wang-timexer.md)) are directly validated. TimeKAN/iTransformer/TimeMixer have **no published EPF or commodity price evaluation** — their SOTA is academic LTSF only. For M5/retail demand (Zanotti 2025, [src-2026-06-zanotti-retraining-frequency](../sources/src-2026-06-zanotti-retraining-frequency.md)), N-BEATS/N-HiTS are DL SOTA — less relevant to P1's new domain focus but useful as methodological background.
- Covariate gap is confirmed: four 2025–2026 papers (ChronosX, UNICA, ApolloPFN, CATS-ATS) independently identify that Chronos, TimesFM, MOMENT, and other leading TSFMs do not support exogenous covariates; TimeXer ([src-2026-06-wang-timexer](../sources/src-2026-06-wang-timexer.md)) provides the strongest validated endo/exo cross-attention template; iTransformer and TimeMixer++ also lack native exo support. See [comparisons/tsf-backbone-comparison](../comparisons/tsf-backbone-comparison.md) for full model table.

## Supplementary literature (ingest 2026-06-30)

**Backbone extension — xLSTM:**
- **xLSTM** ([src-2026-06-beck-xlstm](../sources/src-2026-06-beck-xlstm.md), Beck et al. 2024, NeurIPS): mLSTM matrix memory with linear sequence complexity. P1 assessment: current P1 backbone (NBEATSx/TimeXer) is correct for now — no published EPF or commodity price evaluation for xLSTM yet. TiRex (Auer et al. 2025) demonstrates xLSTM zero-shot TSF beating Chronos/TimesFM but has not been evaluated on EPF. xLSTM is a candidate future backbone replacement for the high-volatility/non-stationary regime cluster; evaluate once TiRex benchmarks on EPF become available.

**Scalable cluster routing — TSI:**
- **TSI** ([src-2026-06-tan-ts-indexing](../sources/src-2026-06-tan-ts-indexing.md), Tan et al. 2017): hierarchical K-means + DTW lower-bounding for gigabyte-scale TS classification. At P1 scale (millions of price series), TSI's K-means tree enables O(log K) cluster routing instead of O(K·L²) brute force DTW. The FAISS index used for P2's embedding-based routing is complementary — P2's vector routing is faster; TSI's DTW routing is more accurate for temporal structure.

**Attribution — counterfactual explanations:**
- **Ates et al. 2021** ([src-2026-06-ates-counterfactual-ts](../sources/src-2026-06-ates-counterfactual-ts.md)): greedy substitution algorithm for counterfactual explanations of multivariate TS classifiers. P1 attribution currently uses AttGrad; counterfactual mode ("if crude oil futures had looked like 2020, the copper price would have been X% lower") is a second explanation surface. Algorithm is model-agnostic and directly applicable to P1's multivariate covariate inputs. Implement as optional secondary attribution alongside AttGrad.

**Backbone interpretability — TEM:**
- **TEM** ([src-2026-06-zhang-tem-topology](../sources/src-2026-06-zhang-tem-topology.md), Zhang et al. 2025): Transformers degrade token topology (positional + semantic) with depth; TEM plug-in preserves both, tightening generalization bounds and improving forecasting. P1 implication: shallow Transformer backbones (2–4 layers) are preferred to avoid topology degradation — consistent with current P1 preference for compact architectures.

**Tabular attribution — IMN:**
- **IMN** ([src-2026-06-kadra-mesomorphic](../sources/src-2026-06-kadra-mesomorphic.md), Kadra et al. 2024): hypernetworks generate instance-specific linear models for tabular data, providing per-sample feature importances by design (no post-hoc SHAP). P1 consideration: could replace AttGrad for the tabular covariate feature-importance layer if the TS backbone is separated from the covariate head; requires adapting IMN to TS-derived feature vectors.

## Literature to integrate

The following gaps exist in the current wiki. Each is required to properly validate P1's claims. All are `[gap]` — no citation attached yet.

| Gap | Why needed | Priority |
|---|---|---|
| EPF survey (e.g. Weron 2014 *Electricity price forecasting: A review*) | P1 references EPF as a benchmark domain; no EPF survey or taxonomy in the wiki. Need to understand EPF problem structure, forecasting horizons, and evaluation conventions. | `[gap]` High |
| LEAR model (Lago et al. 2018) | NBEATSx reports ~20% improvement over LEAR — the statistical benchmark it beats on EPF. P1's success criterion "outperform GARCH/ARIMAX" assumes these are competitive baselines. LEAR (Least-squares Estimation of AutoRegressive) is the EPF-specific statistical baseline, not generic ARIMA. | `[gap]` High |
| GARCH / GARCH-X literature | P1 success criterion: "outperform GARCH/ARIMAX." Zero GARCH literature in the wiki. For commodity price volatility modeling, GARCH-family models are the established baseline — need at least one survey or key reference. | `[gap]` High |
| Commodity price forecasting survey | EPF is well-studied; no comparable benchmark or literature exists in the wiki for crude oil, metals (copper, aluminium), or agricultural commodity price forecasting. What are the standard datasets, frequencies, and evaluation protocols? | `[gap]` Medium |
| Price regime / structural break detection | P1's open question: "do volatility-regime clusters separate regimes, or is explicit detection required?" [src-2026-06-zhang-switching-ssm](../sources/src-2026-06-zhang-switching-ssm.md) provides conceptual framing but no commodity price evidence. Need established methods for structural break tests (e.g. Bai-Perron) or change-point detection applied to price data. | `[gap]` Medium |
| Cross-commodity price dependency modeling | Commodity prices exhibit co-movement (energy complex, crack spreads, metal correlations). iTransformer is motivated partly for this use case but no commodity-specific cross-series literature in the wiki. | `[gap]` Low |
| Weekly/monthly long-horizon forecasting benchmark | No standardized public benchmark for weekly/monthly commodity price forecasting (EPF is day-ahead; M4 monthly is demand/macro). What is the appropriate evaluation protocol and dataset for P1's primary use case? | `[gap]` High |

## Sources

- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md) — cluster models, gate protocol, covariate-selection mechanism, risks.
- [sources/src-2026-06-tsf-literature-review](../sources/src-2026-06-tsf-literature-review.md) — external TSF literature positioning (secondary synthesis; key claims now verified against named primaries in I-P1-A/B/C).
- [sources/src-2026-06-rizvi-glinear](../sources/src-2026-06-rizvi-glinear.md) — GLinear: data-efficient simplicity baseline; RevIN for distribution shift; Priority 5 in backbone table.
- [sources/src-2026-06-pasche-extreme-conformal](../sources/src-2026-06-pasche-extreme-conformal.md) — GPD-extended conformal prediction for price spikes; addresses "forecast accuracy under price spikes" success criterion.
- [sources/src-2026-06-zhang-switching-ssm](../sources/src-2026-06-zhang-switching-ssm.md) — S4+SNLDS for regime detection; conceptual background for cluster re-routing on structural breaks.
- [sources/src-2026-06-kumar-mixbeats](../sources/src-2026-06-kumar-mixbeats.md) — Mix-BEATS: N-BEATS+TSMixer for STLF; supports N-BEATS-family on real energy data; frequency mismatch.
- [sources/src-2026-06-liang-itfkan](../sources/src-2026-06-liang-itfkan.md) — iTFKAN: interpretable KAN; complex; AttGrad incompatibility risk; academic LTSF only.
- [sources/src-2026-06-fein-ashley-spectre](../sources/src-2026-06-fein-ashley-spectre.md) — SPECTRE FFT attention; infrastructure reference; not directly applicable to MLP/linear P1 backbone.
- [sources/src-2026-06-tsitsulin-embedding-quality](../sources/src-2026-06-tsitsulin-embedding-quality.md) — unsupervised embedding quality metrics (coherence, stable rank, SelfCluster); directly applicable to P1 cluster quality gate.
- [sources/src-2026-06-beck-xlstm](../sources/src-2026-06-beck-xlstm.md) — xLSTM: mLSTM matrix memory; future backbone candidate for non-stationary price clusters
- [sources/src-2026-06-tan-ts-indexing](../sources/src-2026-06-tan-ts-indexing.md) — TSI (SDM 2017): hierarchical K-means + DTW lower-bound; scalable cluster routing at millions of series
- [sources/src-2026-06-ates-counterfactual-ts](../sources/src-2026-06-ates-counterfactual-ts.md) — counterfactual TS explanations; P1 secondary attribution surface
- [sources/src-2026-06-zhang-tem-topology](../sources/src-2026-06-zhang-tem-topology.md) — TEM (2025): topology preservation in Transformer TSF; supports shallow backbone preference
- [sources/src-2026-06-kadra-mesomorphic](../sources/src-2026-06-kadra-mesomorphic.md) — IMN (2024): interpretable mesomorphic networks; instance-specific linear attribution for tabular covariates
- [sources/src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md) — v1 production model; ConvAttnEncoder 128-dim embeddings used for P1 cluster routing and covariate selection

## Related pages

- [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md)
- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [domains/timeseries-forecasting/thesis](../domains/timeseries-forecasting/thesis.md)
