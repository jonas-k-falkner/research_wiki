---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-fein-ashley-spectre
tags:
- attention
- efficiency
- fft
- transformer
zotero: fein-ashleySPECTREFFTBasedEfficient2025
source_hash: fe5d9a02fd9f17a15bcc80ee3a553983506117cfe1031ec8e9501b39b0746142
---

# SPECTRE: FFT-Based Drop-In Replacement for Self-Attention

**Fein-Ashley et al. (2025)**

## Summary

SPECTRE replaces multi-head self-attention with a content-adaptive FFT-based token mixer, reducing per-layer complexity from O(L²) to O(L log L). Each attention head is replaced by: (1) RFFT (real FFT) of the input tokens, (2) content-adaptive spectral gate (diagonal + optional low-rank), (3) IFFT back to token space. A Prefix-FFT cache enables streaming autoregressive generation analogous to the KV-cache.

Evaluated on **language modeling (PG19)** and **image classification (ImageNet-1k)**. Achieves up to 7× faster inference than FlashAttention-2 at 128k-token context while matching baseline accuracy.

## Claims

- **SPECTRE achieves O(L log L) per-layer complexity** by replacing attention with RFFT + content-adaptive spectral gates + IFFT — a drop-in replacement requiring only <6% additional parameters. [Evidence: Section 2, Figure 1]
- **7× faster than FlashAttention-2 at 128k-token context** on language modeling while matching or exceeding PG19 perplexity. [Evidence: Figure 1, Section 4]
- **Content-adaptive spectral gates** (learned per-token diagonal gates) preserve the context-sensitivity of attention; distinguishes SPECTRE from fixed-filter spectral methods (FNet). [Evidence: Section 3.1]
- **Prefix-FFT cache enables streaming generation** at O(n log n) memory without recomputing FFT at every decoding step. [Evidence: Section 3.3]

## Caveats

- No time series forecasting evaluation — tested only on NLP (PG19 language modeling) and vision (ImageNet).
- The efficiency gains are for **long-context language models** (tens of thousands of tokens); typical TSF lookback windows (96–720 steps) are short enough that quadratic attention is not a bottleneck.
- Drop-in compatibility requires Transformer-based backbone — not applicable to MLP/linear models (NBEATSx, N-HiTS, GLinear, DLinear).

## Applicability to P1

**Very low — infrastructure reference only.**

P1's preferred backbone family (NBEATSx, N-HiTS, DLinear, GLinear) does not use self-attention, so SPECTRE's efficiency improvement does not apply. If P1 ever uses a Transformer backbone at scale (TimeXer, iTransformer) with very long context windows, SPECTRE could reduce inference cost — but this scenario is not imminent given the weekly/monthly frequency context (short effective sequence lengths even over multi-year history).

Retain as **background reference** for attention efficiency when evaluating any Transformer-based TSF backbone.

## Related

- [src-2026-06-wang-timexer](src-2026-06-wang-timexer.md) — TimeXer: Transformer backbone that uses attention (candidate for SPECTRE replacement)
- [domains/timeseries-forecasting/thesis](../domains/timeseries-forecasting/thesis.md) — SSM and linear-RNN landscape section
