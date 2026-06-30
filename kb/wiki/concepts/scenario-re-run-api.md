---
type: concept
domain: scenario-engine
project: P3
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p3-scenario-engine
tags:
- concept
---

# Scenario re-run API

## Definition

An interface that perturbs one or more input covariates (e.g. "cotton futures +15%") and recomputes forecast impact, confidence bounds, and named driver attributions — the user-facing "if-then" surface of P3. See [sources/src-2026-06-p3-scenario-engine](../sources/src-2026-06-p3-scenario-engine.md).

## Why it matters

It converts a forecast into a procurement action, which is the customer value the deck's interviews point to ("we see the signal but don't know what to do with it", 10/20). The interpretable-linear-per-pair design is what makes attribution clean.

## Open research questions

- For correlated drivers, how does perturbing one covariate propagate — do we hold others fixed, or move them along an estimated joint structure? Naive ceteris-paribus may mislead.
- What confidence format is "trusted but not overcomplicated" for non-technical buyers? (Open question in [shared/open-questions](../shared/open-questions.md).)
- Does this stay linear-per-pair, or need interaction terms once portfolios/bills-of-materials are involved (links to the Cost Model Forecast PRD)?

## Literature to integrate `[verify]`

- Scenario analysis / stress testing methodology in econometrics `[verify]`
- Counterfactual reasoning under correlated inputs; structural vs reduced-form interventions `[verify]`
- Uncertainty communication / decision-maker trust in forecast intervals `[verify]`

## Cross-project relevance

- Depends on [concepts/cpcv-validation](cpcv-validation.md); explanation surface overlaps with P4 explainable alerts.

## Related pages

- [projects/p3-scenario-engine](../projects/p3-scenario-engine.md)
