---
type: domain
domain: scenario-engine
project: P3
status: active
confidence: high
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-p3-scenario-engine
tags:
  - thesis
  - scenario-engine
---

# Domain thesis: Scenario engine

## Current thesis

The scenario engine is the fastest route to customer-visible value because it translates forecasts and causal feature selection into interpretable procurement actions.

## Product thesis

Customers do not only need a forecast; they need an actionable answer to what happens under a plausible market movement, with confidence bounds and named drivers.

## MVP stance

Ship deterministic CPCV-validated scenario logic first unless the Bayesian layer is necessary for user trust or enterprise positioning. Add posterior uncertainty after the deterministic workflow is validated.

## Main failure mode

If linear models are too weak for important relationships, the product may remain interpretable but underpowered. This risk should be tested through scenario backtests and customer review, not assumed away.

## Sources & related

- [sources/src-2026-06-p3-scenario-engine](../../sources/src-2026-06-p3-scenario-engine.md)
- Project: [projects/p3-scenario-engine](../../projects/p3-scenario-engine.md)
