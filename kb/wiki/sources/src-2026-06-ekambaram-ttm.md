---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-ekambaram-ttm
tags:
- timeseries-forecasting
- tsfm
- zero-shot
- mlp-mixer
zotero: ekambaramTinyTimeMixers2024
source_hash: 10f424ca02cf770d319c754eba6b597d0b8c8ae4ac0d15651e0df05cb982bffc
---

# Tiny Time Mixers (TTMs): Fast Pre-trained Models for Enhanced Zero/Few-shot Forecasting

**Ekambaram et al. (IBM Research, NeurIPS 2024)**

## Summary

TTM is a compact (1M+ parameter) pretrained TSFM based on the TSMixer (MLP-Mixer) architecture with adaptive patching, diverse resolution sampling, and resolution prefix tuning. It outperforms much larger TSFMs (Chronos, TimesFM, Moirai, MOMENT) in zero/few-shot forecasting while being runnable on CPU. Supports exogenous variables via an optional Exogenous Mixer block added during fine-tuning.

## Key design points

- **Backbone**: TSMixer (MLPMixer blocks with gated attention), not Transformer-based.
- **Multi-level**: backbone pretrained channel-independently → decoder fine-tuned with channel mixing → optional Exogenous Mixer for covariate integration.
- **Exogenous Mixer**: applies overlapped patching to forecast+exogenous channels, then TSMixer with channel mixing to learn lagged exogenous-to-target correlations.
- Pretrained on ~1B samples from Monash + LibCity; does not use ETT/Electricity/Weather (evaluation sets).

## Key results

- TTM outperforms Chronos, TimesFM, Moirai, MOMENT in zero-shot by 4–40% on standard benchmarks.
- Smallest model (1M params) vs. Chronos Large (710M params), TimesFM (200M params).
- CPU-runnable: significant deployment advantage.
- Exogenous Mixer (TTM-CM) integrates covariates during fine-tuning.

## Claims

- **Tiny pretrained MLP-Mixer models can match or outperform large Transformer-based TSFMs** in zero/few-shot forecasting, with dramatically lower compute. [Evidence: Table 1, Figure 1]
- **MLP-Mixer architecture is 2–3x more compute-efficient than Transformer equivalents** with comparable accuracy. [Evidence: Related work section]
- **Exogenous variable integration via a separate fine-tuning mixer module** is feasible without retraining the pretrained backbone. [Evidence: Section 3.2, Exogenous Mixer]

## Caveats / Applicability to P1

Background and adjacent. TTM demonstrates that the pretrained TSFM paradigm works at very small scales and that MLP-Mixer is a legitimate backbone for TSFMs. The Exogenous Mixer design (fine-tuning-time covariate integration) is a simpler variant of the ChronosX adapter pattern and relevant for P1's covariate integration strategy. No native exogenous support in zero-shot mode.
