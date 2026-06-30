---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-yasuda-sequential-attention-2023
tags:
- source
- feature-selection
- sequential-attention
- greedy-selection
citekey: yasudaSequentialAttentionFeature2023
source_hash: b33dcbaabb97d6272e9a5109b51b7107e76130016531a71a10531d2ca478f97c
author: Yasuda, Taisuke; Bateni, MohammadHossein; Chen, Lin; Fahrbach, Matthew; Fu,
  Gang; Mirrokni, Vahab
year: 2023
title: Sequential Attention for Feature Selection
venue: ICLR 2023
zotero: yasudaSequentialAttentionFeature2023
---

# Yasuda et al. (2023) — Sequential Attention for Feature Selection

## Summary

Proposes Sequential Attention: a feature selection algorithm based on efficient one-pass greedy forward selection using attention weights as proxy for marginal feature importance. At each step, selected features are passed directly to the model; unselected features are downscaled by their softmax attention weight. The algorithm selects one feature per step (k total steps for k features), capturing residual/marginal value — the contribution of each feature given previously-selected features. Theoretical result: for linear regression, the algorithm is equivalent to Orthogonal Matching Pursuit (OMP) and inherits its guarantees. Achieves state-of-the-art empirical results on neural network feature selection benchmarks.

## Key claims

1. Sequential Attention addresses the redundancy failure mode of flat attention-based feature selection: by selecting features one at a time and conditioning each step on already-selected features, it captures marginal (residual) value rather than raw importance.
2. For linear regression, Sequential Attention is equivalent to Orthogonal Matching Pursuit (OMP), inheriting provable near-optimal subset selection guarantees without requiring O(kd) model trainings.
3. Sequential Attention uses a single global feature mask (not instance-wise masks), simplifying training, reducing hyperparameter overhead, and enabling direct application to any differentiable model architecture.

## Relevance to P1

Directly relevant to hierarchical entmax covariate selection: Sequential Attention is an alternative that explicitly accounts for feature redundancy through greedy marginal selection. P1's flat entmax may select correlated covariates together (all receiving high mass) without the redundancy check. The Sequential Attention approach could be incorporated as a post-hoc selection refinement step or as an alternative training procedure. The OMP equivalence provides a theoretical baseline for assessing what any feature selection mechanism needs to match.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
