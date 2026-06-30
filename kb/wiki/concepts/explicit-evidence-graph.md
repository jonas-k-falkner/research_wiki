---
type: concept
domain: nowcasting-graph
project: P4
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-p4-availability-nowcasting
- src-2026-06-liu-sc-kg
- src-2026-06-almahri-agentic-sc
- src-2026-06-zheng-sc-gcn-fl
tags:
- concept
- knowledge-graph
- supply-chain
- link-prediction
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

## Primary literature (I-P4-A, 2026-06-30)

**SC KG completion** ([src-2026-06-liu-sc-kg](../sources/src-2026-06-liu-sc-kg.md), Liu et al. 2023, ESWC):
- RotatE achieves **MRR 0.4377** on 3-tier industrial SC KG (65K nodes, 311K edges) — this confirms the formerly unverified MRR ~0.44 claim from the P4 MVP report.
- SC KG schema: 8 entity types (component, supplier, manufacturer, customer, location, category, standard, process) and 11 relation types. Good starting template for P4.
- MRR <0.5 even on curated structured data reinforces P4's decision to reject aggressive hidden-edge completion in the MVP.
- Centrality metrics (betweenness, degree) on SC graph identify critical supplier nodes — usable as a simple risk heuristic.

**Agentic SC monitoring** ([src-2026-06-almahri-agentic-sc](../sources/src-2026-06-almahri-agentic-sc.md), AlMahri et al. 2026):
- 7-agent pipeline (CrewAI + GPT-4o) built **on top of** a Neo4j SC KG achieves F1 0.962–0.991.
- The KG is a prerequisite, not an output — it must be constructed before the pipeline runs. This matches P4's architecture: explicit evidence graph is built first, then queried by agents.
- Three required hallucination mitigations: RAG over evidence ledger, deterministic tool calls (Cypher), human-in-the-loop escalation.

**GCN + Federated Learning for SC link prediction** ([src-2026-06-zheng-sc-gcn-fl](../sources/src-2026-06-zheng-sc-gcn-fl.md), Zheng & Brintrup 2025):
- GraphSAGE inductive learning: new entities (companies, products) can be embedded without retraining the full model — a hard requirement for P4's live expanding graph.
- AdapFLavg (adaptive federated learning) is best for predicting sparse relationship types (compliance certifications <5% of edges) — relevant for rare event types in P4's evidence graph.
- SC KG entity/relation schema: company, customer, country, certificate, product; supplies to, buys, made by, has cert. More lightweight than Liu 2023 but maps the procurement layer well.

## Open research questions

- When (if ever) does graph completion / link prediction earn its place, given RotatE achieves MRR 0.4377 on curated data — informative but not reliable as ground truth?
- Relational store choice: do relational joins / materialized views suffice for the MVP before a property graph (Neo4j) is justified?
- How is propagation confidence computed and decayed across multi-hop paths?

## Open questions (unresolved)

- Schema-driven disruption/event extraction frameworks
- Property-graph vs relational tradeoffs for evidence-scale graphs

## Cross-project relevance

- A view over [concepts/evidence-ledger](evidence-ledger.md); candidate relations could be informed by [concepts/causal-covariate-embeddings](causal-covariate-embeddings.md) retrieval, provided provenance is preserved.

## Related pages

- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
- [domains/nowcasting-graph/thesis](../domains/nowcasting-graph/thesis.md)
