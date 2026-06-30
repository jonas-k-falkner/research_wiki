---
type: shared
domain: shared
project: shared
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-px-cross-project-strategy
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-p4-availability-nowcasting
tags:
- risks
---

# Risks and caveats

| Area | Risk | Current mitigation |
|---|---|---|
| P1 | Shape clusters mix incompatible regimes | Gate experiment and regime sub-clustering |
| P1 | Deep models do not outperform tuned LGBM | Treat analyst-time elimination as first-class value |
| P1 | Attention weights misread as explanations | Use weight × gradient, cluster sensitivity, and stability diagnostics |
| P2 | Asymmetric embedding geometry fails to converge | Validate directional retrieval and downstream forecast lift |
| P2 | Retrieved covariates are correlated but not causal | Label as candidate causal drivers until validated |
| P3 | Linear models miss nonlinear dynamics | Backtest scenario accuracy and consider v2 models if needed |
| P3 | Bayesian layer slows MVP | Explicitly decide v1 scope boundary |
| P4 | Public-only supplier coverage is uneven | Report coverage and confidence separately |
| P4 | Full graph reconstruction becomes speculative | Keep ledger as source of truth and graph as evidence-backed view |
