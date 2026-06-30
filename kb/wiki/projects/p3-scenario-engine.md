---
type: project
domain: scenario-engine
project: P3
status: active
stage: seed
confidence: high
updated: 2026-06-25
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
- Forecast impact with confidence bounds.
- Explainability layer showing drivers, direction, and magnitude.

## Defer or decide

The Bayesian / variational posterior layer is valuable, but it should be explicitly scoped. The open question is whether to ship it in v1 or defer until deterministic scenario logic is validated.

> **Source-internal contradiction `[unresolved]`.** The deck is inconsistent about this: Slide 5 lists the Bayesian/variational layer under **"What ships"** (i.e. v1), while Slide 8 lists "ship Bayesian in v1 or defer to v2?" as an **open question**. The wiki holds it as *open* and validates deterministic logic first ([experiments/exp-p3-scenario-engine-mvp](../experiments/exp-p3-scenario-engine-mvp.md)); recorded rather than silently resolved.

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
