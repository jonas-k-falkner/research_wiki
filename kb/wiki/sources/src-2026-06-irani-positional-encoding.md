---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-irani-positional-encoding
tags:
- timeseries-forecasting
- transformer
- positional-encoding
zotero: iraniPositionalEncodingTransformerBased2025
source_hash: e283fa26eed4aaf8eebeb9cbe23e72bbd7867dd680e92bfcd9016fb5522ee6f0
---

# Positional Encoding Survey for Transformer-Based Time Series Forecasting

**Irani et al. (2025)**

## Summary (3 bullets)

- Surveys positional encoding strategies for Transformer-based time series models, analyzing their impact on temporal ordering preservation and forecasting accuracy.
- Identifies that RoPE and learnable positional encodings outperform fixed sinusoidal encodings in time series settings.
- **Applicability to P1**: low priority; relevant if P1 uses a Transformer backbone (less likely given DLinear/MLP evidence). Directly confirms ApolloPFN's design choice to use RoPE for temporal ordering in the PFN setting.
