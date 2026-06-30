---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-tezekbayev-alpha-relu-2022
tags:
- source
- entmax
- alpha-relu
- sparse-attention
citekey: tezekbayevSpeedingEntmax2022
source_hash: 086b94587532db3c22a68c8997f5026e55d1fc3a3856b7b1f432f6d2d8a1c9c3
author: Tezekbayev, Maxat; Pak, Alexandr; Korobov, Mikhail; Kasymbekov, Zhenisbek;
  Perrault-Archambault, Ariel
year: 2022
title: Speeding Up Entmax
venue: arXiv 2022
zotero: tezekbayevSpeedingEntmax2022
---

# Tezekbayev et al. (2022) — Speeding Up Entmax

## Summary

Introduces α-ReLU as a faster alternative to α-entmax for neural machine translation output layers. α-ReLU is implemented as a shifted ReLU raised to the power 1/(α−1), producing the same sparsity properties as α-entmax without the iterative bisection algorithm. Training speed matches softmax. Evaluated on NMT tasks, showing comparable BLEU scores to α-entmax with substantially lower computational overhead.

## Key claims

1. α-ReLU (shifted ReLU^(1/(α−1))) achieves the same sparse output distribution properties as α-entmax while matching softmax training speed — eliminating the O(d log d) iterative bisection cost of exact α-entmax.
2. α-ReLU and α-entmax produce comparable NMT BLEU scores at the same α value, suggesting the exact normalization of entmax is not critical for the sparsity benefit in output distributions.
3. α-ReLU is evaluated on NMT output layers; its applicability to attention (not just output) layers is not directly demonstrated, leaving open whether it can replace entmax in covariate selection routing.

## Relevance to P1

Relevant if computational cost of α-entmax in the hierarchical routing mechanism becomes a bottleneck. α-ReLU provides a speed-matched alternative that may simplify deployment. However, the normalization guarantee of α-entmax (weights sum to 1, non-negative) is important for cluster-level mass interpretation; α-ReLU's unnormalized outputs may complicate the cluster attribution interpretation. Worth benchmarking against α-entmax in P1 ablations.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
