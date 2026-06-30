---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-jain-attention-not-explanation-2019
tags:
- source
- attention-faithfulness
- interpretability
citekey: jainAttentionNotExplanation
source_hash: 3750735a8bfd5f7d960a7cdb1bbdf6e16ac34cf0d449cf5c4bc45e3c3549e607
author: Jain, Sarthak; Wallace, Byron C.
year: 2019
title: Attention Is Not Explanation
venue: NAACL 2019
zotero: jainAttentionNotExplanation
---

# Jain & Wallace (2019) — Attention Is Not Explanation

## Summary

Empirically tests whether attention weights can serve as explanations in BiLSTM text classification and question answering models. Finds that attention weights correlate only weakly with gradient-based and leave-one-out (LOO) feature importance measures (Kendall τ ~0.3–0.5). Demonstrates the existence of adversarial attention: alternative attention distributions with high Jensen-Shannon divergence (~0.69) from the original that produce identical model predictions. Concludes that raw attention weights do not identify features responsible for model outputs.

## Key claims

1. Attention weights in BiLSTM models correlate weakly with gradient and LOO feature importance measures (Kendall τ ~0.3–0.5), indicating that high-attention tokens are not necessarily the causal drivers of predictions.
2. Adversarial attention distributions exist: one can find attention weights that are maximally different from the learned weights (JSD ~0.69) while producing identical model predictions, demonstrating attention is not a unique explanation.
3. Randomly permuting attention weights causes minimal change in model output, confirming that learned attention patterns are not the mechanism by which predictions are computed.

## Relevance to P1

Establishes the negative result: raw attention weights from a selection mechanism cannot be used directly as explanations without additional validation. Motivates the weight×gradient approach and stability diagnostics for hierarchical entmax covariate selection. The adversarial attention finding directly implies that reporting entmax weights alone is insufficient for interpretability claims.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/attention-faithfulness](../concepts/attention-faithfulness.md)
