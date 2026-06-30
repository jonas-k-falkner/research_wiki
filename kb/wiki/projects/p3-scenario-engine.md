---
type: project
domain: scenario-engine
project: P3
status: active
stage: seed
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-p3-scenario-engine
tags:
- scenario-analysis
- procurement
- forecasting
---

# P3 — Scenario engine

## Purpose

Ship interpretable if-then scenario queries for procurement and cost forecasting. Example: if cotton futures rise 15%, estimate impact on yarn procurement cost with confidence bounds and named drivers.

## Current thesis

P3 should start now because it has the shortest time-to-value, the clearest customer evidence, low team cost, and direct linkage to CPO priority product work.

## Customer evidence from deck

| Pain statement | Mentions |
|---|---:|
| We negotiate blind against our suppliers | 17/20 |
| Our forecasts are not trusted enough to act on | 14/20 |
| By the time we were sure, the window was closed | 12/20 |
| We see the signal but do not know what to do with it | 10/20 |

## MVP scope

- Granger/TE feature selection.
- CPCV validation.
- Interpretable linear model per commodity pair.
- Scenario re-run API.
- Forecast impact with confidence bounds (OLS standard errors; conformal CQR deferred to v2).
- Explainability layer showing drivers, direction, and magnitude.

## V1 scope decision (2026-06-30)

**Decided:** P3 v1 ships linear model + CPCV only. Bayesian/variational layer and conformalized quantile regression (CQR) are explicitly deferred to v2.

V1 delivers: Granger/TE feature selection → CPCV-validated linear model per commodity pair → scenario re-run API → OLS-based confidence intervals. The goal is a trusted, interpretable, shippable product without uncertainty-layer complexity.

V2 adds: Bayesian/variational posterior (calibrated uncertainty), conformalized CQR (distribution-free prediction intervals), and optional nonlinear models if the linear ceiling is hit in production.

> **Source-internal contradiction resolved `[decided 2026-06-30]`.** Deck Slide 5 listed the Bayesian/variational layer under "What ships" (v1); Slide 8 listed it as an open question. Decision: defer to v2. The contradiction is recorded here per wiki policy rather than silently erased.

## Main risk

The linear model may hit a ceiling on nonlinear or complex relationships. This is acceptable for v1 if the product goal is trusted, interpretable scenario reasoning rather than maximum predictive accuracy.

## Sources

- [sources/src-2026-06-p3-scenario-engine](../sources/src-2026-06-p3-scenario-engine.md) — customer evidence, MVP scope, Bayesian open question.

## Related pages

- [concepts/scenario-re-run-api](../concepts/scenario-re-run-api.md)
- [concepts/cpcv-validation](../concepts/cpcv-validation.md)
- [experiments/exp-p3-scenario-engine-mvp](../experiments/exp-p3-scenario-engine-mvp.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [domains/scenario-engine/thesis](../domains/scenario-engine/thesis.md)
- [decisions/adr-0001-project-sequencing](../decisions/adr-0001-project-sequencing.md)
