---
type: concept
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-jain-attention-not-explanation-2019
- src-2026-06-wiegreffe-attention-not-not-2019
- src-2026-06-liu-rethinking-attention-explainability-2022
- src-2026-06-bastings-elephant-interpretability-2020
- src-2026-06-bibal-attention-explanation-survey-2022
tags:
- concept
- attention-faithfulness
---

# Attention Faithfulness

## Definition

Faithfulness is the property that an explanation correctly identifies the features causally responsible for a model's prediction — specifically that the direction (polarity) and magnitude of attributed importance match the actual effect of that feature on the output. A faithful explanation points to the true computational mechanism, not merely features that correlate with correct predictions. Distinct from *plausibility* (whether the explanation looks reasonable to domain experts).

## The debate: 2019–2022

### Negative result (Jain & Wallace 2019)

Raw attention weights in BiLSTM models correlate only weakly with gradient-based and leave-one-out feature importance (Kendall τ ~0.3–0.5). Adversarial attention exists: alternative attention distributions with Jensen-Shannon divergence ~0.69 from the learned weights that produce identical model predictions. Random permutation of attention weights causes minimal output change. Conclusion: raw attention is not explanation. See [sources/src-2026-06-jain-attention-not-explanation-2019](../sources/src-2026-06-jain-attention-not-explanation-2019.md).

### Positive counterpoint (Wiegreffe & Pinter 2019)

Four tests (uniform baseline, variance calibration, diagnostic MLP, model-consistent adversarial training) show that trained attention weights carry genuine information: they outperform adversarial alternatives on a diagnostic classifier. However, faithfulness is task- and dataset-dependent — on SST sentiment, uniform attention performs comparably. Existence of adversarial attention does not categorically disqualify attention as explanation; the correct criterion is empirical validation per task. See [sources/src-2026-06-wiegreffe-attention-not-not-2019](../sources/src-2026-06-wiegreffe-attention-not-not-2019.md).

### Quantitative resolution (Liu et al. 2022)

Introduces the faithfulness violation test: checks whether the *polarity* of attributed importance matches the actual effect of the feature on model output (positive vs negative attribution vs actual marginal contribution direction). Finds:
- Raw attention (RawAtt) violation ratio: ~0.31–0.40
- Attention ⊗ Gradient (AttGrad): violation ratio ~0.02–0.06 (approximately 10× improvement)
- Violation rate increases with model depth (more Transformer layers → more violations)
- No tested method achieves zero violations

**Practical recommendation**: use AttGrad (α ⊗ ∇α) as the default explanation measure; raw attention is unreliable. See [sources/src-2026-06-liu-rethinking-attention-explainability-2022](../sources/src-2026-06-liu-rethinking-attention-explainability-2022.md).

### Position paper (Bastings & Filippova 2020)

Attention operates on intermediate contextual representations, not original inputs — so high attention on a representation does not imply the original token was important. Gradient-based saliency requires only one additional backward pass and is systematically preferable for input-level attribution. The computational cost argument for preferring attention over saliency is largely unfounded. See [sources/src-2026-06-bastings-elephant-interpretability-2020](../sources/src-2026-06-bastings-elephant-interpretability-2020.md).

### Survey synthesis (Bibal et al. 2022)

The debate converges on: (1) raw attention alone is insufficient; (2) AttGrad substantially improves faithfulness across tasks and domains; (3) much apparent disagreement dissolves once faithfulness vs plausibility is distinguished; (4) practitioners must validate per task. See [sources/src-2026-06-bibal-attention-explanation-survey-2022](../sources/src-2026-06-bibal-attention-explanation-survey-2022.md).

## Practical consensus (as of 2022)

| Method | Violation Ratio | Gradient Needed | Notes |
|---|---|---|---|
| Raw attention | ~0.31–0.40 | No | Unreliable; do not use alone |
| Attention ⊗ Gradient (AttGrad) | ~0.02–0.06 | Yes (1 backward pass) | **Recommended** |
| Gradient saliency | ~0.02–0.08 | Yes | Equally good; input-level |
| Integrated Gradients | Lowest | Yes (20–300 passes) | Best axioms; expensive |

## Implications for P1

For hierarchical entmax covariate selection:

1. **Report AttGrad, not raw entmax weights**: cluster-level entmax mass is a routing signal; polarity-consistent importance requires α ⊗ ∇α.
2. **Faithfulness must be empirically validated**: the Liu et al. polarity consistency test should be applied to P1's covariate selection on the actual forecasting datasets, not assumed.
3. **Faithfulness ≠ plausibility**: the P1 interpretability claim is faithfulness-based (mechanistic accuracy of which covariates drive the forecast). Expert agreement alone is insufficient.
4. **Context representation gap**: entmax cluster routing operates on cluster prototype representations (contextual), not raw covariate values — Bastings & Filippova's argument applies, reinforcing the need for gradient-based attribution at the input level.
5. **Validation protocol**: combine AttGrad (primary), polarity consistency test (Liu et al.), and SHAP on a held-out set (external baseline). Agreement across methods strengthens the interpretability claim.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](hierarchical-entmax-covariate-selection.md)
- [sources/src-2026-06-jain-attention-not-explanation-2019](../sources/src-2026-06-jain-attention-not-explanation-2019.md)
- [sources/src-2026-06-wiegreffe-attention-not-not-2019](../sources/src-2026-06-wiegreffe-attention-not-not-2019.md)
- [sources/src-2026-06-liu-rethinking-attention-explainability-2022](../sources/src-2026-06-liu-rethinking-attention-explainability-2022.md)
- [sources/src-2026-06-bastings-elephant-interpretability-2020](../sources/src-2026-06-bastings-elephant-interpretability-2020.md)
- [sources/src-2026-06-bibal-attention-explanation-survey-2022](../sources/src-2026-06-bibal-attention-explanation-survey-2022.md)
