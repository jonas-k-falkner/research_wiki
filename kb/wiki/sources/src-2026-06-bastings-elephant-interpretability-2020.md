---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-bastings-elephant-interpretability-2020
tags:
- source
- attention-faithfulness
- saliency
- interpretability
citekey: bastingsElephantInterpretabilityRoom2020
source_hash: 3603438177146935ba9064689eeca1be5ed59092214971bbc57da697c8dde838
author: Bastings, Jasmijn; Filippova, Katja
year: 2020
title: 'The Elephant in the Interpretability Room: Why Use Attention as Explanation
  When We Have Saliency Methods?'
venue: BlackboxNLP @ EMNLP 2020
zotero: bastingsElephantInterpretabilityRoom2020
---

# Bastings & Filippova (2020) — The Elephant in the Interpretability Room

## Summary

Position paper arguing that saliency methods (gradient-based) are preferable to attention weights for identifying important input tokens. Key argument: attention operates on intermediate contextual representations, not original inputs, so high attention on a token's representation does not imply that original token was important. Gradient computation requires only one additional backward pass (one line of code in TensorFlow/PyTorch). Recommends practitioners default to gradient saliency rather than attention for explanation.

## Key claims

1. Attention reflects intermediate (contextual) representations, not original input tokens — attention weights measure importance of encoder states, which have already mixed information across all positions, making them unreliable as input-level explanations.
2. Gradient-based saliency requires only one additional backward pass (a single TF/PyTorch line) — the computational cost argument for preferring attention over saliency is largely unfounded.
3. For identifying important input features, saliency methods are systematically preferable to raw attention; this position is consistent with the Jain & Wallace empirical findings and the Liu et al. violation test results.

## Relevance to P1

Reinforces that the P1 explanation protocol must not rely solely on entmax weights. The contextual-representation argument applies directly: cluster-level entmax weights route over cluster prototype representations, not original covariate values, so weight×gradient (saliency at the input level) is required for faithful feature attribution. The one-backward-pass cost argument supports practical deployment of AttGrad in P1's inference pipeline.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/attention-faithfulness](../concepts/attention-faithfulness.md)
