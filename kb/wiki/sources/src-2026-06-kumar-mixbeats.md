---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-kumar-mixbeats
tags:
- timeseries-forecasting
- backbone
- energy-forecasting
- load-forecasting
- n-beats
zotero: kumarMixBEATSMixerenhancedBasis2025
source_hash: 2fab6dc1fc049165506f38d9107107588472a6791a2593af7ce03590a99a0e67
---

# Mix-BEATS: Mixer-enhanced Basis Expansion for Short-Term Load Forecasting

**Kumar et al. (Indian Institute of Science, 2025)**

## Summary

Mix-BEATS is a lightweight hybrid architecture combining **N-BEATS** (residual basis expansion) with **TSMixer** (patch+time mixing MLP blocks) for short-term load forecasting (STLF) in smart buildings. Pre-trained on hourly energy data from 38,956 buildings, evaluated on 1,000 held-out buildings. Outperforms TSFM baselines (Chronos, Moirai, Lag-Llama, TTMs) in zero-shot and fine-tuned settings on NRMSE. Highly compute-efficient: 0.18M parameters, 0.18 seconds inference per building.

**Domain: building-level energy consumption forecasting** — hourly frequency, day-ahead (24-hour) horizon.

## Architecture

- **Outer structure**: N-BEATS stacks (M stacks × K blocks each); doubly residual; each block subtracts its backcast from the residual, adds its forecast.
- **Inner block**: TSMixer (from MLPMixer) — patches the input, applies patch-mixing MLP then time-mixing MLP with GELU activation and layer normalization.
- **No covariate support** — univariate forecasting only.
- **Hyperparameters**: 3 stacks × 3 blocks, patch size 8, hidden dim 256, input window 168 hours (7 days), horizon 24 hours (1 day).

## Key results

- Zero-shot: outperforms Moirai, Chronos, Lag-Llama, TTMs on NRMSE for commercial buildings.
- Fine-tuned: competitive with Moirai and Lag-Llama; best or second-best on commercial and residential buildings.
- 0.18M parameters vs 14M (Moirai), 46M (Chronos) — ~80–250× smaller; 0.18s inference vs 13–17s for large TSFMs.
- Training on 38,956 buildings from EnerNOC, I-Blend, CEEW, and other diverse real-world datasets demonstrates cross-building generalization.

## Claims

- **N-BEATS + TSMixer hybrid achieves better zero-shot STLF accuracy than large TSFMs** (Chronos, Moirai, Lag-Llama, TTMs) while being orders of magnitude smaller and faster. [Evidence: Table 1]
- **Large-scale domain-specific pretraining (38,956 buildings)** enables generalization to unseen buildings without task-specific fine-tuning — the real-world energy domain provides sufficient training diversity. [Evidence: Section 3.5.1]
- **Mix-BEATS performance may degrade in long-term forecasting** (authors' own caveat): it is optimized for STLF (day-ahead) and not validated beyond 24-hour horizons. [Evidence: Section 4, limitations]

## Caveats

- **Hourly STLF only** — no evaluation beyond 24-hour horizons; explicitly flagged as a limitation for long-term forecasting.
- Building energy consumption (load) ≠ commodity prices — different statistical properties: load has strong diurnal/weekly seasonality, prices have regime shifts and fat tails.
- No exogenous covariates — not validated with weather, occupancy, or price signals as inputs.
- Benchmark is NRMSE on proprietary building datasets — harder to compare externally.

## Applicability to P1

**Low-to-medium — relevant as methodological background, not a primary backbone candidate.**

Mix-BEATS demonstrates that the N-BEATS-family can be adapted for real-world energy domain data at scale (38,956 buildings) and outperform large TSFMs. This supports the general thesis that N-BEATS-style architectures are strong on real energy data — consistent with NBEATSx's EPF SOTA and N-HiTS's M4 performance.

Key takeaways for P1:
- The patch+mixing augmentation of N-BEATS is a valid path for improving pattern extraction without adding covariate complexity.
- Pretraining on a large number of diverse energy series enables zero-shot generalization — relevant for P1's cluster pretraining hypothesis.
- Frequency mismatch: Mix-BEATS is hourly/daily; P1's primary use case is weekly/monthly. Long-term performance is explicitly flagged as unvalidated.
- No covariate support limits direct use in P1's attribution pipeline.

## Related

- [src-2026-06-oreshkin-nbeats](src-2026-06-oreshkin-nbeats.md) — N-BEATS: parent architecture
- [src-2026-06-olivares-nbeatsx](src-2026-06-olivares-nbeatsx.md) — NBEATSx: exo extension of N-BEATS; P1 primary backbone
- [src-2026-06-challu-nhits](src-2026-06-challu-nhits.md) — N-HiTS: hierarchical extension; better for long-horizon
