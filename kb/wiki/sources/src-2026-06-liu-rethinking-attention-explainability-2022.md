---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-liu-rethinking-attention-explainability-2022
tags:
- source
- attention-faithfulness
- interpretability
- faithfulness-violation
citekey: liuRethinkingAttentionModelExplainability2022
source_hash: 13a3f2ec814cca0601d72710bad70e20d1bb84fc518b5a89a772e8e38b25fa97
author: Liu, Xing; Zhu, Zhenglin; Yu, Haoyuan; Chen, Yubo; Liu, Kang; Zhao, Jun
year: 2022
title: Rethinking Attention-Model Explainability through Faithfulness Violation Test
venue: ICML 2022
zotero: liuRethinkingAttentionModelExplainability2022
---

# Liu et al. (2022) — Rethinking Attention-Model Explainability

## Summary

Introduces a faithfulness violation test that checks polarity consistency: whether the direction of a feature's attribution (positive/negative) matches the actual effect of that feature on model output. Prior work only checked importance correlation, missing this dimension. Evaluates raw attention (RawAtt), attention×gradient (AttGrad), and other methods. Finds raw attention has violation ratios of ~0.31–0.40, while AttGrad reduces this to ~0.02–0.06. Deeper model architectures increase violation rates. Recommends Attention ⊗ Gradient (α ⊗ ∇α) as the practical choice.

## Key claims

1. Raw attention weights have faithfulness violation ratios of ~0.31–0.40 (polarity inconsistency with actual feature effects), whereas Attention ⊗ Gradient (AttGrad) reduces violations to ~0.02–0.06 — a factor of ~10 improvement.
2. Deeper model architectures produce more faithfulness violations: violation rate is positively correlated with layer count, meaning raw attention is especially unreliable in deep Transformer models.
3. No tested method achieves zero faithfulness violations; AttGrad is the practical recommendation but remains imperfect, supporting the use of multiple attribution methods in combination.

## Relevance to P1

Provides the empirical protocol for validating entmax covariate selection faithfulness. The polarity consistency test is directly applicable: after training, check that covariates with high entmax weight also have positive gradient with respect to the output, and vice versa. AttGrad (entmax weight × gradient of output w.r.t. entmax weight) is the recommended explanation measure for P1, superseding raw entmax weights alone. The violation ratio metric can serve as a model evaluation criterion alongside forecasting loss.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/attention-faithfulness](../concepts/attention-faithfulness.md)
