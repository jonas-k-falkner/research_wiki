---
type: shared
domain: shared
project: shared
status: active
confidence: medium
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-px-cross-project-strategy
  - src-2026-06-p1-cluster-pretrained-deep-models
  - src-2026-06-p4-availability-nowcasting
tags:
  - overview
---

# Overview

> **Stage: seed.** This wiki is built from three starting sources only (one strategy deck, two design/technical notes). It is a scaffold for research that will be executed later, not the full scope. See [shared/research-backlog](shared/research-backlog.md) for what is planned, and `CLAUDE.md` → Maturity model for what `seed`/`researched`/`validated` mean.

## Numbering crosswalk (read if you also use the wider project's file numbering)

The wider Sybilion project numbers files `p1…p4`; this wiki numbers projects `P1…P4`. They are **not** a clean 1:1 map:

| Wider project file | This wiki |
|---|---|
| `p1_pre-trained-deep-forecasting-model` (the "gaze" note) | split across **P1** (cluster routing + entmax selection) and **P2** (causal embedding objective) |
| `p4_availability_nowcasting` | **P4** (1:1) |
| (deck, not separately numbered in the wider project) | source for **P1, P2, P3** |

So "P1" here is the cluster-deep-models *project*, while the wider project's "p1" file is the covariate-selection *method note* — which lives partly in P1 and partly in P2.

## What the wiki tracks

The wiki currently tracks four AI-heavy project directions.

P1, P2, and P3 are an integrated forecasting/scenario stack. P3 is the near-term commercial product, P2 is the research moat around causal covariate retrieval, and P1 is the scalability unlock once SKU counts grow beyond analyst-tunable scope.

P4 is adjacent but distinct: a B2B supply-availability nowcasting and evidence-ledger system. It shares concepts with the other tracks — causal evidence, graph memory, entity normalization, confidence scoring, explainable alerts, mixed-frequency signals — but should not be collapsed into P1–P3.

## System-level thesis

The strongest portfolio shape is:

1. Ship P3 first to capture immediate customer value and validate scenario UX.
2. Run the P1 cluster-quality gate immediately to avoid committing to a bad clustering assumption.
3. Run P2 as a parallel research track because P2 upgrades P1's covariate layer and creates defensible retrieval infrastructure.
4. Treat P4 as a separate evidence-ledger/nowcasting product path whose MVP should not attempt full supply-chain graph reconstruction.

## Main coupling points

| Coupling | Interpretation |
|---|---|
| P3 → P1 | P3 proves value at 10–20 SKUs; larger enterprise deployments expose the analyst bottleneck that P1 addresses. |
| P2 → P1 | P2's causal covariate embeddings can replace or augment shape-similarity embeddings in P1's attention layer. |
| P1 → P2 | P1 provides a downstream forecasting validation task for P2 beyond retrieval-ranking metrics. |
| P3 ↔ P4 | Both need evidence-backed explanations, scenario logic, and confidence communication. |
| P2 ↔ P4 | Directed relation embeddings and entity-linked evidence can inform candidate relation retrieval, but P4 must preserve auditable provenance. |
| P1 ↔ P4 | Both involve time-sensitive nowcasting/forecasting, but P1 is SKU-level forecasting while P4 is availability state estimation over entities, categories, and regions. |

## See also

- [shared/evaluation-strategy](shared/evaluation-strategy.md) — per-project evaluation metrics
- [shared/risks-and-caveats](shared/risks-and-caveats.md) — consolidated risk register
- [shared/research-backlog](shared/research-backlog.md) — what to ingest next
