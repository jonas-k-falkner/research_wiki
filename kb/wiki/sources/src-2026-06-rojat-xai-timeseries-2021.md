---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-rojat-xai-timeseries-2021
tags:
- source
- xai
- timeseries
- survey
- interpretability
citekey: rojatExplainableArtificialIntelligence2021
source_hash: c86a846d9185f07d96ed2e08762fd0be05cd443ad764bd7dfd1763aa19b70c76
author: Rojat, Thomas; Puget, Raphaël; Filliat, David; Del Ser, Javier; Gelin, Rodolphe;
  Díaz-Rodríguez, Natalia
year: 2021
title: 'Explainable Artificial Intelligence (XAI) on TimeSeries Data: A Survey'
venue: arXiv 2021
zotero: rojatExplainableArtificialIntelligence2021
---

# Rojat et al. (2021) — XAI on Time Series Data

## Summary

Survey of explainability methods applied to time-series deep learning models. Covers attribution methods (gradient-based, perturbation-based, attention-based), concept-level explanations, and model-specific approaches. Identifies key challenges for time-series XAI: temporal dependencies between features, multiple time scales, and the need for explanations that are stable and robust across similar inputs. Notes that most deep learning time-series models lack built-in interpretability.

## Key claims

1. Temporal ordering of features is a fundamental challenge for time-series XAI: methods that treat features independently (such as vanilla SHAP) miss lagged dependencies and causal temporal structure that are central to time-series interpretation.
2. Stability and robustness of explanations across similar inputs are underexplored evaluation criteria in time-series XAI; explanation methods that are sensitive to small input perturbations provide unreliable covariate importance signals.
3. Deep learning time-series models generally lack built-in interpretability; post-hoc methods dominate the field but introduce a gap between the explanation and the model's actual computation.

## Relevance to P1

Provides the survey-level context for why hierarchical entmax selection is architecturally preferable to post-hoc attribution: the selection is built-in (intrinsic), not post-hoc, which closes the gap Rojat et al. identify. The temporal ordering limitation of SHAP reinforces that SHAP alone is insufficient for covariate explanation in P1. The stability criterion aligns with the weight×gradient + stability diagnostic design in the P1 explanation protocol.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
