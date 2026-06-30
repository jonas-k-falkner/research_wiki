---
type: domain
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
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
tags:
- thesis
- forecasting
---

# Domain thesis: Time-series forecasting

## Current thesis

The portfolio needs a scalable forecasting layer that can move from analyst-tuned SKU workflows to cluster-routed, low-touch global models. P1 is the main architecture for this transition.

## Most important unresolved question

Do shape-based clusters provide sufficiently consistent regimes for a shared model, or must clusters be split by stationarity, seasonality, heteroscedasticity, and related detector flags?

## Preferred near-term path

1. Run the P1 cluster-quality gate.
2. Prototype a single cluster with D-Linear and MLP if the gate passes or after regime sub-clustering.
3. Integrate sparse hierarchical covariate selection (NBEATSx concatenation or TimeXer cross-attention).
4. Validate against LGBM and existing forecasting baselines on data with real covariate effects (not just standard benchmarks).
5. Track analyst-time elimination as a first-class success metric.

## Key assumptions

| Assumption | Status | Decision impact |
|---|---|---|
| 200M series provide enough training diversity | unvalidated in current wiki | Determines whether P1 can generalize zero-shot |
| Shape + regime clusters are learnable and useful | testing required | Determines P1 viability |
| Compact backbone (DLinear/N-BEATS) suffices for temporal modeling | **evidence-backed** ([Zeng 2023](../../sources/src-2026-06-zeng-dlinear.md), [Chen 2025](../../sources/src-2026-06-chen-closer-look-transformers.md)): linear outperforms Transformers on standard benchmarks | Supports investing in covariate architecture, not backbone complexity |
| Hierarchical entmax can stabilize covariate selection | plausible | Influences P1 model architecture |
| P2 embeddings improve covariate layer | unvalidated | Influences sequencing of full P1 build |
| Standard benchmark results transfer to retail demand with real covariates | **not confirmed** ([Chen 2025](../../sources/src-2026-06-chen-closer-look-transformers.md) warns benchmarks are self-dependent/stationary) | Requires P1 validation on covariate-rich data |

## External literature positioning

A deep-research synthesis of 2024–2026 TSF ([sources/src-2026-06-tsf-literature-review](../../sources/src-2026-06-tsf-literature-review.md)) splits the field into two streams: stronger general backbones and a covariate-adapter stream. This is now verified against named primaries (I-P1-C ingest, 2026-06-29). Key confirmed findings:

**1. Compact backbone sufficiency — confirmed.**
Zeng et al. 2023 ([src-2026-06-zeng-dlinear](../../sources/src-2026-06-zeng-dlinear.md)) demonstrates that a one-layer linear model (DLinear) outperforms all tested Transformer-based LTSF models by **20–50% MSE** on 9 standard benchmarks (ETT, Electricity, Traffic, Weather, ILI, Exchange-Rate). Chen et al. 2025 ([src-2026-06-chen-closer-look-transformers](../../sources/src-2026-06-chen-closer-look-transformers.md)) explains the mechanism: standard benchmarks are self-dependent and stationary, so intra-variate temporal modeling (captured perfectly by a linear layer) dominates. This supports the P1 design preference for a compact backbone. **Caveat**: real demand data with promotional drivers may require cross-attention for exogenous covariates (TimeXer shows this on EPF datasets with genuine covariate effect).

**2. Covariate gap in TSFMs — confirmed across four papers.**
ChronosX ([src-2026-06-arango-chronosx](../../sources/src-2026-06-arango-chronosx.md)), UNICA ([src-2026-06-han-unica](../../sources/src-2026-06-han-unica.md)), ApolloPFN ([src-2026-06-potapczinski-apollopfn](../../sources/src-2026-06-potapczinski-apollopfn.md)), and CATS-ATS ([src-2026-06-lu-cats-ats](../../sources/src-2026-06-lu-cats-ats.md)) each explicitly identify that leading TSFMs — Chronos, TimesFM, MOMENT, Sundial, TimeMoE, LagLlama — ignore exogenous covariates. Only Moirai partially handles homogeneous covariates. This confirms that the covariate-adapter research stream exists precisely because the dominant TSFMs have this gap.

**3. TimeXer as endo/exo split template — confirmed.**
TimeXer ([src-2026-06-wang-timexer](../../sources/src-2026-06-wang-timexer.md)) demonstrates that separating endogenous (patch-level self-attention) from exogenous (variate-level cross-attention) through a learnable global token bridge achieves SOTA on electricity price forecasting benchmarks with covariates, outperforming DLinear by a significant margin when covariates are genuinely informative.

**4. TS foundation models are background, not blueprints.**
The TSFM wave (Chronos, TimesFM, Moirai, TTM, TiRex) is best understood as a zero-shot generalization paradigm without covariate support. For P1's cluster-pretrained + covariate design, the MLP/linear backbone family (N-BEATS, N-HiTS, NBEATSx, DLinear) is more directly relevant than large-scale TSFMs.

## Backbone landscape

See [comparisons/tsf-backbone-comparison](../../comparisons/tsf-backbone-comparison.md) for the full comparison table covering 15 models.

**Summary recommendation for P1 backbone**:

| Priority | Architecture | Rationale |
|---|---|---|
| 1 (start here) | DLinear or NBEATSx | Compact, fast, proven on benchmark + covariate tasks; DLinear for temporal baseline, NBEATSx for covariate-integrated variant |
| 2 (if covariate cross-attn needed) | TimeXer | Best endo/exo cross-attention architecture; heavier but validated on real covariate datasets |
| 3 (if multi-task needed) | TimeMixer++ | General-purpose pattern machine; no exogenous support |
| Avoid for temporal backbone | Autoformer, Informer, FEDformer | Outperformed by DLinear; complexity not justified |

## SSM and linear-RNN landscape (background)

State space models and linear RNNs (Mamba, RWKV, xLSTM, HGRN, GLA, etc.) represent a class of subquadratic alternatives to Transformers designed primarily for language modelling. Their applicability to multivariate TSF is limited: [Wang et al. (2024)](../../sources/src-2026-06-wang-mamba-tsf.md) find that Mamba-based S-Mamba is competitive on high-variate periodic datasets (Traffic, Electricity) but shows suboptimal results on low-variate aperiodic benchmarks (ETT, Exchange) where DLinear is competitive or better — consistent with the DLinear finding that architectural complexity does not guarantee TSF gains in the regimes most analogous to retail SKU forecasting. The majority of SSM/linear-RNN papers (Mamba-2, RWKV, Eagle/Finch, HGRN, HGRN2, GLA, Gated Delta Networks, Longhorn, TTT, GSA, Jamba) report no TSF evaluation at all, with benchmarks focused exclusively on language modeling. P1 uses a compact MLP or linear backbone rather than SSMs for three reasons: (1) no demonstrated TSF accuracy advantage over DLinear in low-variate aperiodic regimes; (2) SSM hidden states are opaque to the AttGrad attribution protocol; (3) MLP/linear models have better serialization and integration properties with the forecast\_pipeline library.

Sources: [src-2026-06-wang-mamba-tsf](../../sources/src-2026-06-wang-mamba-tsf.md), [src-2026-06-gu-mamba](../../sources/src-2026-06-gu-mamba.md), [src-2026-06-dao-mamba2](../../sources/src-2026-06-dao-mamba2.md).

## Sources & related

- [sources/src-2026-06-p1-cluster-pretrained-deep-models](../../sources/src-2026-06-p1-cluster-pretrained-deep-models.md), [sources/src-2026-06-tsf-literature-review](../../sources/src-2026-06-tsf-literature-review.md)
- [sources/src-2026-06-zeng-dlinear](../../sources/src-2026-06-zeng-dlinear.md) — DLinear evidence for compact backbone
- [sources/src-2026-06-wang-timexer](../../sources/src-2026-06-wang-timexer.md) — TimeXer endo/exo split
- [sources/src-2026-06-arango-chronosx](../../sources/src-2026-06-arango-chronosx.md), [sources/src-2026-06-han-unica](../../sources/src-2026-06-han-unica.md), [sources/src-2026-06-potapczinski-apollopfn](../../sources/src-2026-06-potapczinski-apollopfn.md) — covariate gap evidence
- [comparisons/tsf-backbone-comparison](../../comparisons/tsf-backbone-comparison.md)
- Project: [projects/p1-cluster-pretrained-deep-models](../../projects/p1-cluster-pretrained-deep-models.md)
