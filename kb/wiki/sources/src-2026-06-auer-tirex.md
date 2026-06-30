---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-auer-tirex
tags:
- timeseries-forecasting
- tsfm
- zero-shot
- xlstm
zotero: auerTiRexZeroShotForecasting2025
source_hash: 6b055dd8f6b4e3831d98fed65203ae9acfb63672935d2fae59309eb32c3bdc9b
---

# TiRex: Zero-Shot Forecasting Across Long and Short Horizons with Enhanced In-Context Learning

**Auer et al. (NXAI/JKU Linz, 2025)**

## Summary

TiRex is a pretrained zero-shot forecasting model based on xLSTM (enhanced LSTM with competitive in-context learning). It introduces Contiguous Patch Masking (CPM) training strategy to preserve state-tracking across long horizons. Sets SOTA on GiftEval and Chronos-ZS benchmarks, outperforming larger Transformer-based TSFMs.

## Key points

- xLSTM backbone: recurrent state-tracking (unlike Transformer permutation-invariance) + in-context learning (unlike standard LSTM).
- CPM: masks contiguous patches during training to prevent autoregressive degradation over long horizons.
- No exogenous covariate support.
- Demonstrates that recurrent state-tracking matters for long-horizon zero-shot forecasting.

## Claims

- **xLSTM-based TiRex outperforms Transformer-based TSFMs (Chronos, TimesFM, Moirai) in zero-shot forecasting** on GiftEval and Chronos-ZS benchmarks. [Evidence: SOTA tables]
- **State-tracking (recurrence) is a critical property for long-horizon forecasting** that Transformers lack but LSTMs possess. [Evidence: Section 1 argument + results]

## Caveats / Applicability to P1

Background. TiRex demonstrates that LSTM-based models remain competitive for zero-shot TSFMs. No covariate support makes it less directly relevant to P1. Useful as a reference point for zero-shot forecasting benchmarks.
