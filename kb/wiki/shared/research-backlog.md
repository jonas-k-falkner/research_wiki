---
type: shared
domain: shared
project: shared
status: active
stage: seed
confidence: high
updated: 2026-06-27
sources:
- src-2026-06-px-cross-project-strategy
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-p4-availability-nowcasting
- src-2026-06-tsf-literature-review
tags:
- backlog
- roadmap
- research
---

# Research backlog

This wiki is at **seed** stage (see `CLAUDE.md` → Maturity model). It was built from three starting sources. This page tracks what must be pulled in to move pages from `seed` → `researched` → `validated`. It is the single place where the current corpus gaps are made visible rather than left implicit.

## Planned external literature (by topic)

Each links the concept page that will host the citations once verified.

| Topic | Candidate directions to find & verify | Lands on |
|---|---|---|
| Global vs clustered vs local forecasting | Montero-Manso & Hyndman; **Channel Clustering / "From Similarity to Superiority" (NeurIPS 2024)**; **DUET (KDD 2025)**; backbone context: "A Closer Look at Transformers for TSF" (ICML 2025), iTransformer, TimeMixer; TSFM baselines (Chronos, Moirai, TimesFM, Time-MoE, Sundial, Timer) | [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md) |
| Sparse covariate selection | α-entmax/sparsemax (Martins, Peters); TFT variable selection (Lim); L0/hard-concrete (Louizos); attention-faithfulness (Jain & Wallace; Wiegreffe & Pinter). *Note: review finds entmax support in TSF is adjacent, not direct.* | [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md) |
| Causal / asymmetric embeddings | **TimeXer (NeurIPS 2024, endo/exo split)**; **ChronosX, UniCA, ApolloPFN** (covariate adapters); CATS-ATS; CauAir; order & hyperbolic embeddings (Nickel & Kiela); Transfer Entropy (Schreiber); Granger; distillation | [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md) |
| Validation & calibration | CPCV (López de Prado); conformal/CQR (Romano); Diebold-Mariano | [concepts/cpcv-validation](../concepts/cpcv-validation.md) |
| Scenario / counterfactual | stress-testing methodology; intervention under correlated inputs; uncertainty communication | [concepts/scenario-re-run-api](../concepts/scenario-re-run-api.md) |
| Mixed-frequency nowcasting | MIDAS (Ghysels); dynamic factor models (Giannone, Reichlin & Small) | [concepts/mixed-frequency-nowcasting](../concepts/mixed-frequency-nowcasting.md) |
| Evidence ledger / provenance | bitemporal modelling; truth discovery / source-reliability weighting | [concepts/evidence-ledger](../concepts/evidence-ledger.md) |
| Supply-chain graphs | KG completion / GNN link prediction; schema-driven disruption extraction | [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md) |

## Completed deep-research steps

- **2026-06-27 — TSF literature review** ([sources/src-2026-06-tsf-literature-review](../sources/src-2026-06-tsf-literature-review.md)). A deep-research synthesis of 2024–2026 TSF, read against P1. It **named** the primaries above (TimeXer, Channel Clustering, DUET, ChronosX, UniCA, ApolloPFN, CATS-ATS, CauAir, …) and positioned them, but **carries no resolvable citations** — so it is a `[verify]`-tier map, not verification. **Next:** export the named papers from Zotero into `raw/literature/`, then confirm each claim against the primary before promoting any P1 page `seed → researched`.

## Planned internal sources to ingest

The current corpus has the strategy/research layer but **not** the production-truth layer. Ingesting these would let architecture claims be checked rather than repeated, and would resolve several open questions.

| Internal source | Why it matters | Status |
|---|---|---|
| `forecast_pipeline` repo context | Confirms Model ABC, serialization, determinism constraints P1 must satisfy | **pending** |
| `embedding_model` repo context | Production SSL encoder (ConvAttn, Soft-DTW SL, masked GL); P1 routing and P2 build on it | **done** — `src-2026-06-embedding-model-v1` (2026-06-30) |
| Deployment / ops-api context | How forecasts ship (Temporal, driver search, artifacts) — P3/P4 output surface | **pending** |
| Product / company context | Customer outcomes, GTM, Cost Model Forecast PRD P3 enables | **pending** |

## Known tensions to resolve during research

- **Determinism vs MC-dropout.** `forecast_pipeline` is deterministic-by-default (seeded); the gaze method uses MC-dropout for importance stability. P1 needs an explicit, documented stochasticity carve-out. Cannot be resolved until the repo context is ingested. (Flagged on [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md).)
- **P3 Bayesian layer v1-or-v2.** Source is internally inconsistent (deck Slide 5 lists it under "what ships"; Slide 8 lists it as an open question). Held as open. (Flagged on [projects/p3-scenario-engine](../projects/p3-scenario-engine.md).)
- **P2's value to P1 is now narrower.** P1 Phase 0 uses v1 symmetric embeddings for covariate selection — shape-similarity selection works immediately without P2. P2's contribution to P1 is now specifically directional (A→B ≠ B→A), not general covariate retrieval. This weakens P2's urgency as a P1 enabler and changes P2's priority story: it is a research upgrade, not a P1 dependency. (New tension, 2026-06-30; see [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md) Dependencies.)
- **v1 embedding quality gate for P1.** P1 Phase 0 covariate selection quality is bounded by v1's shape-similarity space. If v1 does not separate commodity regimes well enough (e.g. gold and oil look structurally similar to v1 but have opposite macro sensitivities), Phase 0 will retrieve wrong covariates. This requires empirical validation before Phase 1 (P2) upgrade. New open item — no data yet.
- **Numbering crosswalk.** The "gaze" note is the wider project's `p1` file but is split here across wiki-P1 and wiki-P2; wider-project `p4` == wiki-P4. (See [overview](../overview.md).)

## Cross-source contradictions

None between the three current sources — they cover non-overlapping scope (deck = P1–P3 strategy; gaze = P1/P2 method; report = P4). The contradiction machinery in the claim format is therefore currently exercised only on **source-internal** and **cross-layer** tensions (above). Re-check after each ingest.

## Related pages

- [overview](../overview.md)
- [shared/open-questions](open-questions.md)
- [decisions/adr-0001-project-sequencing](../decisions/adr-0001-project-sequencing.md)
