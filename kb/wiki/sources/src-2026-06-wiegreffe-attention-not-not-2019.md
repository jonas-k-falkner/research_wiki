---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-wiegreffe-attention-not-not-2019
tags:
- source
- attention-faithfulness
- interpretability
citekey: wiegreffeAttentionNotNot2019
source_hash: 874e427b9a56ce57360ca360b1dbd07f35ca9d2aad49a39ac5dfb7828e54ffaf
author: Wiegreffe, Sarah; Pinter, Yuval
year: 2019
title: Attention is not not Explanation
venue: EMNLP 2019
zotero: wiegreffeAttentionNotNot2019
---

# Wiegreffe & Pinter (2019) — Attention is not not Explanation

## Summary

Rebuts Jain & Wallace (2019) using four tests: uniform baseline comparison, variance calibration, diagnostic MLP, and model-consistent adversarial training. Shows that trained LSTM attention weights outperform adversarially-trained alternatives on a diagnostic MLP classifier, suggesting they carry genuine information. However, on SST sentiment and some datasets, uniform attention performs similarly — indicating explanatory power is task- and dataset-dependent. Concludes that attention can serve as explanation but this requires empirical validation per task/dataset rather than being assumed or categorically denied.

## Key claims

1. Trained attention weights outperform adversarially-trained attention alternatives on a diagnostic MLP test, indicating they contain genuine predictive information beyond what Jain & Wallace's adversarial construction implies.
2. Attention's explanatory value is task- and dataset-dependent: on SST sentiment, uniform attention performs similarly to trained attention, showing that high attention correlates with output only in certain settings.
3. Existence of adversarial attention (Jain & Wallace) does not disqualify attention as explanation; the correct criterion is whether learned weights provide a faithful account of the model's computation, which requires empirical testing.

## Relevance to P1

Provides the positive counterpoint: attention can be faithful but requires validation. Supports the P1 design decision to pair entmax routing weights with weight×gradient diagnostics and stability tests rather than abandoning attention-based explanation entirely. The task-dependence finding motivates empirical validation of covariate selection faithfulness on the specific forecasting datasets used.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/attention-faithfulness](../concepts/attention-faithfulness.md)
