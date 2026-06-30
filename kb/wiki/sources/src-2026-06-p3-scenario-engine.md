---
type: source
domain: scenario-engine
project: P3
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p3-scenario-engine
tags:
- scenario
- cpcv
- linear-models
- explainability
---

# Source: P3 — Scenario engine

## Metadata

- Source ID: `src-2026-06-p3-scenario-engine`
- Raw path: `raw/seed/p3_forecast_scenario_engine.md`
- Source type: seed design note (grounded in the `forecast_pipeline` repo)
- Date: June 2026
- Upstream origin: [src-2026-05-sybilion-ai-projects-review](src-2026-05-sybilion-ai-projects-review.md) (deck Slide 5; Bayesian scope from Slide 8)
- Relevant projects: P3

## One-line takeaway

CPCV-validated interpretable linear models with Granger/TE feature selection power "if-then" scenario queries returning impact + confidence interval + named drivers; mostly assembly of existing `forecast_pipeline` modules, with a Bayesian posterior layer deferred pending validation of the deterministic path.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| Scenario engine has shortest time-to-value and strongest near-term pull. | Customer interviews: negotiate blind (17/20), forecasts not trusted (14/20), window closed (12/20), see-signal-don't-act (10/20). | Start P3 first. | high |
| It is "mostly wiring" over existing modules. | `CPCVSplitter`, `GrangerSelector`/`TransferEntropySelector`, `LinearForecaster`, `ConformalIntervalWrapper`, `dm_test` already exist. | Low execution risk / low cost. | medium |
| Conformal intervals give calibrated bounds without Bayesian machinery. | `ConformalIntervalWrapper` is deterministic and present. | Ship deterministic uncertainty first. | medium |
| Linear-per-pair has a ceiling on nonlinear/interacting dynamics. | Deck names this the key risk. | Consider limited interaction terms on high-value pairs. | medium |

## Contradictions

- **Bayesian layer scope (source-internal).** Deck Slide 5 lists the Bayesian/variational layer under "what ships"; Slide 8 lists it as an open v1-or-v2 question. Held as **open**; validate deterministic scenario re-run first.

## Product implications

- Directly enables the Cost Model Forecast PRD (CPO priority) and Buy Window visualisation.
- Scenario re-run must handle correlated-driver perturbation honestly (naive ceteris-paribus can mislead).
- P3 proves value at 10–20 SKUs and creates the commercial pressure that justifies P1.

## Updated pages

- [projects/p3-scenario-engine](../projects/p3-scenario-engine.md)
- [concepts/cpcv-validation](../concepts/cpcv-validation.md)
- [concepts/scenario-re-run-api](../concepts/scenario-re-run-api.md)
- [domains/scenario-engine/thesis](../domains/scenario-engine/thesis.md)
- [experiments/exp-p3-scenario-engine-mvp](../experiments/exp-p3-scenario-engine-mvp.md)
