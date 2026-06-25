---
type: experiment
domain: scenario-engine
project: P3
status: draft
confidence: medium
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-p3-scenario-engine
tags:
  - experiment
---

# Experiment: P3 scenario engine MVP

## Status

Designed-from-source, not yet run. P3 is the start-now track (ADR-0001 step 1); deck horizon 2–4 months.

## Hypothesis

Deterministic, CPCV-validated, interpretable linear models over a small set of commodity pairs can deliver trusted "if-then" scenario answers (impact + confidence bounds + named drivers) that customers will act on — before any Bayesian/variational layer is added.

## Protocol (seed — from deck Slide 5)

1. Granger/TE feature selection per commodity pair.
2. CPCV validation ([concepts/cpcv-validation](../concepts/cpcv-validation.md)).
3. Fit interpretable linear model per pair.
4. Expose scenario re-run: perturb one covariate, recompute impact + confidence bounds ([concepts/scenario-re-run-api](../concepts/scenario-re-run-api.md)).
5. Explainability layer: which drivers moved, by how much, in which direction.
6. Backtest scenario accuracy and review with design-partner customers.

## Metrics

- CPCV-validated error and **interval calibration** (coverage vs nominal).
- Scenario backtest accuracy on historical analog moves.
- Customer-facing: trust and actionability in design-partner review.
- Driver-attribution usefulness.

## Open decision carried into this experiment

The Bayesian/variational posterior layer is a **v1-or-v2 decision** — see the source-internal contradiction noted in [projects/p3-scenario-engine](../projects/p3-scenario-engine.md). This experiment validates deterministic logic first so that decision can be made on evidence.

## Literature to integrate `[verify]`

- CPCV + purging/embargo (López de Prado) `[verify]`
- Conformalized quantile regression for calibrated bounds (Romano et al.) `[verify]`
- Variational/Bayesian linear models for posterior scenario distributions `[verify]`

## Expected failure modes (project-specific)

- Linear-per-pair ceiling: important relationships are nonlinear/interacting → interpretable but underpowered (the deck's named key risk).
- Ceteris-paribus perturbation misleads when drivers are correlated.
- Intervals present but not calibrated → false trust.

## Decision impact

Go / modify / defer for P3 v1, and the v1-vs-v2 scope boundary for the Bayesian layer.

## Related pages

- [projects/p3-scenario-engine](../projects/p3-scenario-engine.md)
- [concepts/scenario-re-run-api](../concepts/scenario-re-run-api.md)
- [concepts/cpcv-validation](../concepts/cpcv-validation.md)
