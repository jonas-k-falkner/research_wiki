---
type: concept
domain: nowcasting-graph
project: P4
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p4-availability-nowcasting
tags:
- concept
---

# Explicit evidence graph

## Definition

A graph built only from provenance-backed, confidence-scored edges derived from the evidence ledger (company–produces–category, company–supplies–customer, company–operates–site, site–in–region, region–exposed-to–event). Used for reasoning and disruption propagation, explicitly *not* for speculative reconstruction of unknown links. See [sources/src-2026-06-p4-availability-nowcasting.md](../sources/src-2026-06-p4-availability-nowcasting.md).

## Why it matters

It gives structured propagation and analyst-traceable explanations while bounding ambition — the report rejects full graph reconstruction for the MVP because input sparsity, entity resolution, and benchmarking dominate over model sophistication.

## Open research questions

- When (if ever) does graph completion / link prediction earn its place, given the report cites a best MRR around 0.44 as informative-but-not-operational?
- Relational store choice: do relational joins / materialized views suffice for the MVP before a property graph (Neo4j) is justified?
- How is propagation confidence computed and decayed across multi-hop paths?

## Literature to integrate `[verify]`

- Supply-chain knowledge graphs and graph completion / GNN link prediction (the report's cited resilience-KG work — pull and verify) `[verify]`
- Schema-driven disruption/event extraction frameworks (the report references named systems — verify) `[verify]`
- Property-graph vs relational tradeoffs for evidence-scale graphs

## Cross-project relevance

- A view over [concepts/evidence-ledger](evidence-ledger.md); candidate relations could be informed by [concepts/causal-covariate-embeddings](causal-covariate-embeddings.md) retrieval, provided provenance is preserved.

## Related pages

- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
- [domains/nowcasting-graph/thesis](../domains/nowcasting-graph/thesis.md)
