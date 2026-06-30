---
type: shared
domain: shared
project: shared
status: active
stage: seed
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-px-cross-project-strategy
- src-2026-06-p4-availability-nowcasting
- src-2026-06-embedding-model-v1
tags:
- open-questions
---

# Open questions

## P1

**Architecture / design:**
- Do v1 embeddings separate commodity price regimes well enough for covariate selection? Gold and oil may look structurally similar in the Soft-DTW space but have opposite macro sensitivities — empirical validation required before Phase 0 ships.
- Is a learned projection (W_q, W_k: 128 → d_sel) needed on top of v1 embeddings, or is cosine similarity over unit-norm vectors sufficient? Ablation required.
- Can the backbone be as shallow as 2 layers with v1 embeddings in the selection layer, or does temporal complexity of price data require more capacity?

**Experiment / ownership:**
- Who owns the cluster-quality experiment (volatility regime vs shape cluster overlap)?
- Should NBEATSx and TimeXer both be prototyped on a single cluster before choosing?
- Are M5 and VN2 in scope or validation-only (day-ahead EPF is already secondary)?

**Evaluation:**
- Do EPF-validated backbone architectures (NBEATSx, TimeXer) transfer to weekly/monthly commodity price forecasting?
- Does AttGrad remain faithful (low polarity-violation rate) on volatile price data, or do attribution gradients degrade under distributional shift?

## P2

- Is there a dedicated researcher for the asymmetric embedding objective?
- Which TE/Granger estimator and lag selection method to use on the distillation subset?
- What pairwise-label sampling strategy produces reliable soft labels at tractable scale?
- Which P1 task should be the first downstream validation target for P2?
- Which asymmetric geometry: source/target two-head architecture, order embeddings, or hyperbolic?
- With P1 Phase 0 using v1 symmetric embeddings, is P2 still a timeline priority, or can it run as a lower-urgency research track?

## P3

- Does Bayesian uncertainty ship in v1 or v2? (Source-internal deck contradiction — held open; see [projects/p3-scenario-engine](../projects/p3-scenario-engine.md).)
- What customer-facing confidence format is trusted but not overcomplicated?
- Which commodity pair should anchor the first CPCV-validated scenario backtest?

## P4

- Which vertical should be first: components, chemicals/materials, or food/agri?
- Which public source connector should anchor the first validation set (SEC EDGAR, TED/SAM.gov, GDELT)?
- What is the minimum viable evidence schema (entity types, relation types, confidence attributes)?
- When, if ever, should graph completion (hidden-edge inference) enter the product?

## Cross-project

- With P1 now using v1 for Phase 0 covariate selection, what is the correct sequencing between P1 Phase 0 validation and P2 research? Does P1 ship Phase 0 as production first?
- P4 moat: is the moat the evidence-ledger/provenance discipline, or the nowcast model itself?
