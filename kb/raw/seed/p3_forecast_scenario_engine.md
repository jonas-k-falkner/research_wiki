# Scenario Engine — Interpretable If-Then Forecasting

*Seed source note for P3. Consolidates the project deck (Slide 5, plus the Bayesian-scope open
question from Slide 8) with grounding in the `forecast_pipeline` repo. Sections marked "Design
considerations", "Things to try", and "Open questions" are reasoning/options, not decided
facts.*

---

## Problem Setup — Customer Evidence (20 interviews)

| Pain | Count |
|---|---|
| "We negotiate blind against our suppliers" | 17/20 |
| "Our forecasts aren't trusted enough to act on" | 14/20 |
| "By the time we were sure, the window was closed" | 12/20 |
| "We see the signal — but don't know what to do with it" | 10/20 |

The throughline: customers don't lack forecasts, they lack a **trusted, explainable
if-then** they can take into a procurement decision.

---

## Core Idea (from deck)

CPCV-validated linear models with causal feature selection power interpretable **"if-then"
scenario queries**. Example: *if cotton futures rise 15%, what happens to yarn procurement
cost?* Output: **expected impact + confidence interval + named causal drivers**. Optionally
extended with Bayesian / variational posteriors for a full distribution over outcomes.

---

## What Ships (from deck)

1. **Granger/TE feature selection → CPCV validation → interpretable linear model per commodity
   pair.**
2. **Scenario re-run API**: change one input covariate, recompute forecast and confidence
   bounds.
3. **Bayesian linear model (variational inference)** for a full posterior over scenario
   outcomes — CFO/CPO-ready uncertainty. *(Scope-disputed — see Open questions.)*
4. **Explainability layer**: which drivers moved, by how much, in which direction.
5. Directly enables the **Cost Model Forecast PRD** (CPO top priority) and **Buy Window
   visualisation**.

---

## Why It's "Mostly Wiring" — Grounding in `forecast_pipeline`

Almost every component already exists in the library; P3 is largely composition:

- Feature selection: `GrangerSelector`, `TransferEntropySelector` (feature_selectors layer).
- Validation: `CPCVSplitter` (Combinatorial Purged CV) — leakage-controlled folds.
- Model: `LinearForecaster` (interpretable coefficients per pair).
- Intervals: `ConformalIntervalWrapper` — calibrated bounds **without** Bayesian machinery.
- Comparison: `dm_test` (Diebold-Mariano) for significance vs. baselines.

This is why the deck rates P3 low cost / low execution risk: the deterministic path is
assembly of existing, tested modules.

---

## Scenario Re-run Mechanics

- Perturb one covariate (e.g. cotton +15%), hold the model fixed, recompute the forecast and
  its interval; report the delta and the named drivers responsible.
- Per-pair interpretable linear coefficients make attribution direct.
- **Caveat (design):** naive ceteris-paribus perturbation can mislead when drivers are
  correlated — moving one input while freezing correlated ones is not a realistic joint move.
  Needs an explicit decision on whether/how co-movement is handled.

---

## Uncertainty: Two Paths

- **Deterministic (conformal)** — `ConformalIntervalWrapper` gives calibrated intervals now,
  no extra stochastic machinery; fits the library's determinism principle.
- **Bayesian / variational** — full posterior over outcomes; richer, but heavier and
  stochastic.

> **Open scope question (deck Slide 8).** Ship the Bayesian uncertainty layer in v1, or defer
> to v2 after validating the deterministic scenario re-run? Note the deck is internally
> inconsistent here: Slide 5 lists the Bayesian layer under "what ships", Slide 8 lists it as
> an open v1/v2 question. Treat as **open**; validate deterministic logic first.

---

## Validation

- CPCV-validated error **and interval calibration** (empirical coverage vs nominal).
- Scenario backtest: do historical analog moves reproduce the predicted impact?
- `dm_test` vs. established baselines for significance.
- Customer-facing: is the impact + interval + driver set *trusted and actionable* in
  design-partner review (the 14/20 trust pain)?

---

## Challenges

1. **Linear-model ceiling** (deck key risk) — nonlinear/interacting dynamics are
   interpretable but may be underpowered.
2. **Correlated-driver perturbation** — see re-run caveat above.
3. **Calibration vs. false trust** — an interval that is present but miscalibrated is worse
   than none for a CFO decision.
4. **No counterfactual ground truth** — scenario interventions can't be directly validated;
   only historical analogs and calibration stand in.

---

## Things to Try

- Conformalized quantile regression for sharper calibrated bounds while staying
  distribution-light.
- Limited interaction terms / piecewise-linear on the highest-value pairs to lift the linear
  ceiling without losing interpretability.
- Move from per-pair to **portfolio / bill-of-materials** scenarios to serve the Cost Model
  Forecast PRD (cost = weighted sum of input movements).

---

## Coupling

- **P3 → P1**: P3 proves value at 10–20 SKUs per client; as clients scale to 100–1000 SKUs the
  analyst bottleneck becomes the hard constraint, creating the commercial pressure that
  justifies P1.
- **P3 → product**: directly enables the Cost Model Forecast PRD and Buy Window visualisation.

---

## Deck Metadata

- Horizon: 2–4 months. Team cost: low (mostly wiring). Primary value: revenue + retention.
- Key risk: linear-model ceiling on nonlinear dynamics.
