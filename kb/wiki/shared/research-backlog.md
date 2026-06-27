---
type: shared
domain: shared
project: shared
status: active
confidence: high
stage: seed
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

| Internal source | Why it matters | Resolves |
|---|---|---|
| `forecast_pipeline` repo context | Confirms Model ABC, serialization, determinism constraints P1 must satisfy | P1 PyTorch-integration risk; the determinism contradiction below |
| `embedding_model` repo context | The actual SSL encoder (ConvAttn, Soft-DTW SL, Ti-MAE GL) that P1 routing and P2 retraining build on | P1/P2 encoder assumptions; "200M series" provenance |
| Deployment / ops-api context | How forecasts ship (Temporal, driver search, artifacts) — where P3/P4 outputs would live | P3 scenario-API surface; P4 delivery |
| Product / company context | Customer outcomes, GTM, the Cost Model Forecast PRD P3 enables | P3 commercial framing; P4 positioning |

## Known tensions to resolve during research

- **Determinism vs MC-dropout.** `forecast_pipeline` is deterministic-by-default (seeded); the gaze method uses MC-dropout for importance stability. P1 needs an explicit, documented stochasticity carve-out. Cannot be resolved until the repo context is ingested. (Flagged on [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md).)
- **P3 Bayesian layer v1-or-v2.** Source is internally inconsistent (deck Slide 5 lists it under "what ships"; Slide 8 lists it as an open question). Held as open. (Flagged on [projects/p3-scenario-engine](../projects/p3-scenario-engine.md).)
- **Numbering crosswalk.** The "gaze" note is the wider project's `p1` file but is split here across wiki-P1 and wiki-P2; wider-project `p4` == wiki-P4. (See [overview](../overview.md).)

## Cross-source contradictions

None between the three current sources — they cover non-overlapping scope (deck = P1–P3 strategy; gaze = P1/P2 method; report = P4). The contradiction machinery in the claim format is therefore currently exercised only on **source-internal** and **cross-layer** tensions (above). Re-check after each ingest.

## Related pages

- [overview](../overview.md)
- [shared/open-questions](open-questions.md)
- [decisions/adr-0001-project-sequencing](../decisions/adr-0001-project-sequencing.md)
