---
type: shared
domain: shared
project: shared
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-px-cross-project-strategy
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-p4-availability-nowcasting
tags:
- index
---

# Sybilion AI Research Wiki

> **Stage: seed.** Built from five seed notes (P1–P4 + cross-project), consolidated from an internal deck and two technical notes; a scaffold for later literature/topic research, not the full scope. Start at [shared/research-backlog](shared/research-backlog.md) to see what is planned. See `CLAUDE.md` → Maturity model.

## Project tracks

| Project | Page                                                                                            | Purpose | Current stance |
|---|-------------------------------------------------------------------------------------------------|---|---|
| P1 | [projects/p1-cluster-pretrained-deep-models](projects/p1-cluster-pretrained-deep-models.md) | Scalable zero-shot or low-touch SKU forecasting through cluster-routed deep models | Run gate experiment before full build |
| P2 | [projects/p2-causal-embedding-v2](projects/p2-causal-embedding-v2.md)                                                             | Directed causal covariate retrieval via asymmetric embedding space | Start as research thread |
| P3 | [projects/p3-scenario-engine](projects/p3-scenario-engine.md)                                                                 | Interpretable if-then scenario queries for procurement/cost decisions | Start now |
| P4 | [projects/p4-availability-nowcasting-graph](projects/p4-availability-nowcasting-graph.md)                                                   | Hybrid supply-availability nowcast with evidence ledger and explicit graph | Build public-first evidence-ledger MVP; defer full graph reconstruction |

## Domain thesis pages

- [domains/timeseries-forecasting/thesis](domains/timeseries-forecasting/thesis.md)
- [domains/embedding-models/thesis](domains/embedding-models/thesis.md)
- [domains/scenario-engine/thesis](domains/scenario-engine/thesis.md)
- [domains/nowcasting-graph/thesis](domains/nowcasting-graph/thesis.md)

## Shared pages

- [shared/evaluation-strategy](shared/evaluation-strategy.md)
- [shared/risks-and-caveats](shared/risks-and-caveats.md)
- [shared/open-questions](shared/open-questions.md)
- [shared/research-backlog](shared/research-backlog.md) — planned literature + internal sources to ingest (seed-stage roadmap)

## Comparisons

- [comparisons/portfolio-evaluation](comparisons/portfolio-evaluation.md) — P1–P4 across moat / time-to-value / risk / cost / scalability / proof

## Entities

- [entities/p4-public-data-sources](entities/p4-public-data-sources.md) — P4 public-first and expanded-tier data sources

## Important concepts

- [concepts/cluster-pretrained-deep-models](concepts/cluster-pretrained-deep-models.md)
- [concepts/causal-covariate-embeddings](concepts/causal-covariate-embeddings.md)
- [concepts/hierarchical-entmax-covariate-selection](concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/evidence-ledger](concepts/evidence-ledger.md)
- [concepts/explicit-evidence-graph](concepts/explicit-evidence-graph.md)
- [concepts/mixed-frequency-nowcasting](concepts/mixed-frequency-nowcasting.md)
- [concepts/scenario-re-run-api](concepts/scenario-re-run-api.md)
- [concepts/cpcv-validation](concepts/cpcv-validation.md)

## Decisions

- [decisions/adr-0001-project-sequencing](decisions/adr-0001-project-sequencing.md)

## Experiments

- [experiments/exp-p1-cluster-quality-gate](experiments/exp-p1-cluster-quality-gate.md)
- [experiments/exp-p2-causal-retrieval-validation](experiments/exp-p2-causal-retrieval-validation.md)
- [experiments/exp-p3-scenario-engine-mvp](experiments/exp-p3-scenario-engine-mvp.md)
- [experiments/exp-p4-public-first-nowcast-mvp](experiments/exp-p4-public-first-nowcast-mvp.md)

## Source summaries

Seed notes (cited by content pages):

- [P1 — Cluster-pretrained deep models](sources/src-2026-06-p1-cluster-pretrained-deep-models.md)
- [P2 — Causal embedding model v2](sources/src-2026-06-p2-causal-embedding-model.md)
- [P3 — Scenario engine](sources/src-2026-06-p3-scenario-engine.md)
- [P4 — Availability nowcasting](sources/src-2026-06-p4-availability-nowcasting.md)
- [PX — Cross-project strategy](sources/src-2026-06-px-cross-project-strategy.md)

Deep-research synthesis (secondary, `[verify]`):

- [TSF literature review (Jan 2024–mid 2026)](sources/src-2026-06-tsf-literature-review.md)

Upstream origin (consolidated, not cited directly):

- [Sybilion AI projects review (deck, May 2026)](sources/src-2026-05-sybilion-ai-projects-review.md)

<!-- AUTO:start -->
## Domain indexes

| Domain | Pages | Stages |
|---|---|---|
| [Embedding models](domains/embedding-models/index.md) | 5 | 5 seed |
| [Nowcasting graph](domains/nowcasting-graph/index.md) | 8 | 8 seed |
| [Scenario engine](domains/scenario-engine/index.md) | 6 | 6 seed |
| [Time-series forecasting](domains/timeseries-forecasting/index.md) | 71 | 68 researched, 3 seed |

## Shared pages

- [Portfolio evaluation matrix](comparisons/portfolio-evaluation.md)
- [ADR-0001: Project sequencing](decisions/adr-0001-project-sequencing.md)
- [Source: PX — Cross-project portfolio & strategy](sources/src-2026-06-px-cross-project-strategy.md)
- [Source: Sybilion AI projects review](sources/src-2026-05-sybilion-ai-projects-review.md)
- [Evaluation strategy](shared/evaluation-strategy.md)
- [Open questions](shared/open-questions.md)
- [Research backlog](shared/research-backlog.md)
- [Risks and caveats](shared/risks-and-caveats.md)

_98 total pages across 4 domain(s) + shared._
<!-- AUTO:end -->
