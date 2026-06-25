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
  - project-map
---

# Project map

| Project | Domain | Primary value | Horizon | Team cost | Main dependency |
|---|---|---|---|---|---|
| P1 | Time-series forecasting | Scalability | 6–10 months | High | P1 gate, then P2 covariate retrieval |
| P2 | Embedding models | Speed + moat | 6–9 months | Medium | Research owner and asymmetric-objective validation |
| P3 | Scenario engine | Revenue + retention | 2–4 months | Low | CPCV scenario MVP scope |
| P4 | Nowcasting graph | New evidence-ledger product path | 6–8 week MVP hypothesis | Medium | Public-first source connectors and evidence schema |

## Integration view

P1–P3 form a relatively coherent forecasting/scenario stack. P4 is adjacent and may reuse concepts, but it should remain architecturally separate because its source landscape, graph/evidence model, and validation logic are different.
