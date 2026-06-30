---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-kadra-mesomorphic
tags:
- interpretability
- tabular
- hypernetworks
source_hash: 0d307b2a602bc28be87939c35c08942425b5be5ba3b99ed5cbda270e5880da17
---

# Source: Interpretable Mesomorphic Neural Networks for Tabular Data (2024)

## Metadata
- **Citekey:** `kadraInterpretableMesomorphicNetworks2024` (no Zotero library entry)
- **Authors:** Kadra, Pineda Arango, Grabocka (University of Freiburg / UTN)
- **Venue:** arXiv 2024
- **Relevant projects:** P1 (interpretable attribution layer)

## One-line takeaway

IMN (Interpretable Mesomorphic Networks) trains deep hypernetworks to generate instance-specific linear models in the original feature space — achieving black-box accuracy with white-box, per-sample explanations for tabular data without post-hoc approximation.

## Key claims

- **Architecture:** hypernetwork θ maps each input xₙ to local linear weights w(xₙ;θ) ∈ ℝ^M; prediction = w(xₙ;θ)^T xₙ. The linear weights are the explanation: they are the input-feature importances for that specific sample.
- Achieves accuracy comparable to black-box classifiers (ResNet, FT-Transformer) on the AutoML benchmark (OpenML CC-18) while matching SHAP and LIME on the XAI interpretability benchmark.
- Outperforms other end-to-end explainable-by-design methods (e.g., NAM, NODE-GA2M) on accuracy.
- Per-instance linear weights provide free-lunch explainability: no post-hoc SHAP/LIME approximation, no separate explainability step.

## Relevance to P1

P1's attribution layer currently uses AttGrad (weight × gradient). IMN offers a complementary paradigm: instead of post-hoc gradient attribution on a fixed model, generate instance-specific linear models where the feature weights are the explanation by design. For P1's tabular covariate inputs (macro indicators, supply-chain signals, weather), IMN would produce per-forecast linear feature importance scores that are exact (not approximated). Implementation consideration: P1 uses multivariate TS as input (not flat tabular), requiring adaptation of IMN to time-window feature vectors extracted by the backbone encoder. Relevant but non-trivial to adapt.
