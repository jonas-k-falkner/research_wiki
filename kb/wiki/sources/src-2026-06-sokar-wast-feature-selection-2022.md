---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-sokar-wast-feature-selection-2022
tags:
- source
- feature-selection
- sparse-training
- autoencoder
- unsupervised
citekey: sokarWherePayAttention2022
source_hash: ca1529b531d66d52cf4e1260a9fe4a987a772039e8a842d497ced2447f1bbdf3
author: Sokar, Ghada; Atashgahi, Zahra; Pechenizkiy, Mykola; Mocanu, Decebal Constantin
year: 2022
title: Where to Pay Attention in Sparse Training for Feature Selection?
venue: NeurIPS 2022
zotero: sokarWherePayAttention2022
---

# Sokar et al. (2022) — WAST: Where to Pay Attention in Sparse Training

## Summary

Proposes WAST (Where to pay Attention during Sparse Training), an unsupervised feature selection method based on sparse autoencoders with dynamic sparse topology optimization. During training, WAST redistributes sparse connections to attend to informative input features quickly, guided by reconstruction loss and connection weight magnitudes. Outperforms state-of-the-art unsupervised feature selection methods on 10 benchmarks (image, speech, text, artificial, biological) while reducing training iterations and computational cost. Specifically handles very high-dimensional feature spaces and noisy environments.

## Key claims

1. WAST's attention-guided topology redistribution detects informative features after far fewer training iterations than random topology exploration (as in SET-based methods), demonstrating that directed sparse topology search is substantially more efficient than random search.
2. Unsupervised WAST matches or outperforms supervised neural-network feature selection methods on several benchmarks, suggesting that reconstruction-loss-guided sparse attention can identify globally informative features without label supervision.
3. WAST is designed for static tabular datasets and treats feature selection as input-node importance in an autoencoder — it does not model temporal structure or time-series-specific feature dynamics.

## Relevance to P1

Tangential: WAST's unsupervised approach could be relevant as a pre-screening step to identify which macro covariates are globally informative before applying the temporal supervised hierarchical entmax model. The lack of temporal structure modeling limits its direct applicability. The efficient sparse topology convergence concept is a useful design principle: prioritizing attention redistribution guided by loss signal rather than uniform exploration.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
