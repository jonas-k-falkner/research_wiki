---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p1-cluster-pretrained-deep-models
tags:
- cluster-models
- covariate-selection
- entmax
- feature-importance
- forecasting
---

# Source: P1 — Cluster-pretrained deep models

## Metadata

- Source ID: `src-2026-06-p1-cluster-pretrained-deep-models`
- Raw path: `raw/seed/p1_cluster-pretrained_deep-models.md`
- Source type: consolidated seed note (system design + covariate-selection design)
- Date: June 2026
- Upstream origin: [src-2026-05-sybilion-ai-projects-review](src-2026-05-sybilion-ai-projects-review.md) (deck Slides 2–3) + the "gaze" covariate-selection note
- Relevant projects: P1 (covariate layer relevant to P2)

## One-line takeaway

Train a lightweight deep model per cluster of similar series and route new SKUs by embedding; inside each model, select covariates with a query-dependent hierarchical cluster→feature α-entmax selector, reporting importance via weight × gradient and cluster-level stability rather than raw attention weights.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| Cluster-pretrained models can eliminate per-SKU analyst tuning at scale. | Hand-tuning is manageable at 10–20 SKUs but breaks at 500–1000; cluster models give each new series a pre-fitted inductive bias. | Judge P1 partly on analyst-time elimination, not only raw accuracy. | medium |
| Shape clusters may mix regimes. | Shape-similar series can have different stationarity/seasonality/heteroscedasticity, which a single model could underfit. | Run the cluster-quality gate before full build; sub-cluster by regime if needed. | high |
| PyTorch integration must respect library invariants. | `forecast_pipeline` uses strict layering, determinism, and serialization; a deep model must extend the `Model` ABC without breaking them. | Implement `ClusterDeepModel` as a first-class `Model` ABC subclass; FAISS routing index via `save_state_dict`; deep model optional dependency. | medium |
| Attention weights are routing signals, not faithful explanations. | The note warns attention can vary while preserving output. | P1 importance reporting must not rely on raw attention weights alone. | high |
| α-entmax preferred over hard L0 gates for stable training. | Hard gates give stronger interpretability but need temperature scheduling and risk collapse. | First productionizable P1 selector. | medium |
| Hierarchical cluster→feature selection improves robustness to correlated covariates. | Cluster mass + within-cluster selection reduce arbitrary choice among redundant macro series. | Relevant when covariates are independent macro series. | high |
| Weight × gradient and MC-dropout stability are cheap importance/uncertainty estimates. | One forward/backward pass beats ablation/SHAP; stochastic passes estimate cluster activation frequency/variance. | Online explanation and stability reporting; still approximate. MC-dropout implies a determinism carve-out. | medium |

## Product implications

- Separate routing/selection from explanation.
- Prefer cluster-level importance narratives over single-covariate rankings when covariates are correlated.
- P2 causal embeddings can feed the selector; the explanation layer still uses sensitivity/stability diagnostics.
- Avoid residual paths that bypass selection if interpretability is required.

## Open questions

- D-Linear vs MLP backbone — prototype both on one cluster, or commit upfront?
- M5/VN2 — part of P1 scope or validation-only?
- Pre-registered threshold for the cluster-quality gate (low vs high within-cluster variance).

## Updated pages

- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md)
- [domains/timeseries-forecasting/thesis](../domains/timeseries-forecasting/thesis.md)
