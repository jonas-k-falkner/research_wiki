---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-sundararajan-integrated-gradients-2017
tags:
- source
- integrated-gradients
- attribution
- interpretability
citekey: sundararajanAxiomaticAttributionDeep2017
source_hash: 4f9fad960c44b6873c93c9ac446ded589faa5e8ea3fc56681390352faac0f75d
author: Sundararajan, Mukund; Taly, Ankur; Yan, Qiqi
year: 2017
title: Axiomatic Attribution for Deep Networks
venue: ICML 2017
zotero: sundararajanAxiomaticAttributionDeep2017
---

# Sundararajan et al. (2017) — Integrated Gradients

## Summary

Introduces Integrated Gradients (IG), an attribution method for deep networks grounded in two axioms: Sensitivity(a) (attribution is non-zero when baseline and input differ in a way that affects the output) and Implementation Invariance (functionally identical networks receive identical attributions). IG computes a path integral of gradients from a baseline input x' to the actual input x, requiring 20–300 gradient evaluations per attribution. Attributions satisfy Completeness: they sum to F(x) - F(x').

## Key claims

1. Integrated Gradients requires gradient access and 20–300 gradient evaluations per attribution, making it computationally expensive at inference time; it is not tractable as a real-time explanation without caching.
2. The Completeness axiom guarantees that IG attributions sum to the output difference F(x) - F(x') between input and baseline, providing a ground-truth conservation property that raw attention weights lack.
3. IG satisfies Implementation Invariance — two networks with identical input-output mappings receive identical attributions — ensuring attributions reflect function behavior rather than implementation artifacts.

## Relevance to P1

Integrated Gradients provides the gold-standard gradient-based attribution baseline for validating entmax selection weights. The 20–300 gradient calls per attribution makes IG infeasible for real-time covariate explanation in a deployed forecasting system, but valuable for offline validation. If IG and entmax weights agree on which covariates matter, the entmax explanation is strengthened. The Completeness property is the axiom-based counterpart to the interpretability claim made by cluster-level entmax mass.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/attention-faithfulness](../concepts/attention-faithfulness.md)
