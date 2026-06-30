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
| P1 | v1 shape-similarity space does not separate commodity regimes (gold ≈ oil in Soft-DTW space but opposite macro drivers) | Empirical validation of v1 cluster routing on commodity price series before Phase 0 ships |
| P1 | Shape clusters mix incompatible volatility regimes | Cluster quality gate experiment; regime sub-clustering if needed |
| P1 | Deep models do not outperform tuned LGBM on price data | Treat analyst-time elimination as first-class value; use LGBM as baseline |
| P1 | AttGrad unstable under price spikes / distributional shift | MC-dropout stability checks; polarity-consistency test (Liu et al. 2022) |
| P1 | Determinism constraint: forecast_pipeline seeded; MC-dropout requires stochasticity carve-out | Explicit documented stochasticity carve-out in ClusterDeepModel; unresolved until repo context ingested |
| P2 | Asymmetric embedding geometry fails to converge | Validate directional retrieval and downstream forecast lift |
| P2 | Retrieved covariates are correlated but not causal | Label as candidate causal drivers until validated; require downstream forecast lift |
| P2 | P2 urgency reduced — P1 Phase 0 ships without P2 | P2 remains high-moat research track; Phase 1 upgrade is surgical (single interface swap) |
| P3 | Linear models miss nonlinear dynamics | Backtest scenario accuracy; consider v2 models if needed |
| P3 | Bayesian layer slows MVP — ship in v1 or defer? | Explicit scope decision required; hold as open until deterministic path validated |
| P4 | Public-only supplier coverage is uneven | Report coverage and confidence separately; do not penalize for unobservable hidden relationships |
| P4 | Full graph reconstruction becomes speculative | Evidence ledger as source of truth; graph as evidence-backed view only |
