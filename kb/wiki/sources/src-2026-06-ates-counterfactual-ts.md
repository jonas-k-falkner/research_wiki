---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-ates-counterfactual-ts
tags:
- explainability
- counterfactual
- timeseries
- multivariate
source_hash: 689f97d624027736ea4e9b3cc5162dc176e3c608975beaabd9384b39a5589467
---

# Source: Counterfactual Explanations for Machine Learning on Multivariate Time Series Data (2021)

## Metadata
- **Citekey:** `atesCounterfactualExplanationsMachine2021` (no Zotero library entry)
- **Authors:** Ates, Aksar, Leung, Coskun (Boston University / Sandia National Labs)
- **Venue:** IEEE ICMLA 2021 / arXiv
- **Relevant projects:** P1 (attribution layer), P3 (what-if analysis)

## One-line takeaway

Counterfactual explanations for multivariate TS classifiers: find the minimal subset of time series (from a distractor sample) that, when substituted into the query sample, flips the classifier prediction — providing a "what would have to be different" explanation in the original data format.

## Key claims

- **Problem formulation (NP-hard):** given sample x classified as c, find a distractor sample x' (class c') and a minimal substitution set S ⊆ {1,…,M} such that the classifier predicts c' on x with the substituted metrics. The explanation is the set of metrics replaced from x'.
- **Heuristic algorithm:** greedy substitution search — iteratively add the metric from x' that most increases classifier confidence in c', stop when prediction flips. Outperforms LIME and SHAP on faithfulness (fraction of correct explanations) and robustness (consistency across runs) on 4 multivariate TS datasets (HPC telemetry, human activity recognition, CMU motion capture, MIT-BIH ECG).
- Explanation format is identical to training data (replaced time series segments), making it interpretable by domain users without feature-level knowledge.
- Validated on ML frameworks for HPC system telemetry (199-metric multivariate TS), demonstrating practical usability.

## Relevance to P1

P1's attribution layer (AttGrad: weight × gradient) explains which covariates drove a price forecast. Counterfactual explanations complement this: instead of "these covariates had high gradient-weighted attention," a counterfactual says "if the wheat futures curve had looked like this other period's curve, the forecast would have been X% lower." P1 should support both attribution modes. Ates provides the algorithmic template for the counterfactual mode; the substitution search is directly applicable to P1's multivariate covariate input.

## Relevance to P3

P3's scenario/what-if analysis is essentially a counterfactual generation problem: "what input conditions would lead to a different output?" Ates's framework is a validated, model-agnostic starting point for P3's scenario generation layer.
