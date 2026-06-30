---
type: domain
domain: nowcasting-graph
project: P4
status: active
stage: seed
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-p4-availability-nowcasting
- src-2026-06-liu-sc-kg
- src-2026-06-almahri-agentic-sc
- src-2026-06-zheng-sc-gcn-fl
- src-2026-06-cheng-shield
- src-2026-06-ramzy-mare
- src-2026-06-besta-graph-databases
- src-2026-06-minder-data2neo
tags:
- thesis
- nowcasting
- graph
- supply-chain
---

# Domain thesis: Nowcasting graph

## Current thesis

The best MVP is a public-first, evidence-ledger-centered nowcast system. It should estimate availability for category × region and supplier × category views using provenance-backed evidence and mixed-frequency signal fusion.

## Rejected MVP thesis

A full reconstructed global supply-chain graph is not the right first build. The binding constraints are public input sparsity, hidden-edge uncertainty, entity resolution, and benchmark construction rather than graph-model sophistication.

## Architecture principle

The evidence ledger is the source of truth. The graph is a structured view used for propagation, explanation, and analyst queries.

## Validation stance

The system should be evaluated against public observable truth: procurement awards, SEC supplier/customer mentions, public company pages, known disruption windows, and lagged official data. It should not be penalized for hidden private-tier relationships that are not publicly observable.

## SC KG literature (I-P4-A, 2026-06-30)

Three primary papers confirm the thesis and provide concrete architecture inputs:
- **Liu et al. 2023** (ESWC) — RotatE MRR 0.4377 on industrial SC KG confirms link completion alone is insufficient; evidence-first approach is correct. SC KG schema (8 entity types, 11 relation types) as starting template.
- **AlMahri et al. 2026** — 7-agent SC monitoring pipeline built on pre-existing KG (F1 0.962–0.991). Evidence ledger → graph → agentic monitoring is now validated at production scale. Mandatory mitigations: RAG, deterministic tool calls, human-in-the-loop.
- **Zheng & Brintrup 2025** — GraphSAGE inductive learning for live SC graphs; FL for multi-org integration. Inductive embedding is a hard requirement for P4.

## MEDIUM literature (I-P4-A, 2026-06-30)

Three additional papers resolve previously open design questions:
- **SHIELD** (Cheng et al. 2024, CMU) — LLM schema induction from unstructured sources for EV battery SC disruption prediction. Confirms schema-driven event extraction is viable; human-in-the-loop curation required.
- **MARE** (Ramzy et al. 2022, Infineon + TIB) — Disruption Ontology (hasCause, hasScope, hasSeverity, hasLocation, hasBeginDate/hasEndDate) + SPARQL DMP pipeline. Reference disruption event schema for P4's evidence ledger.
- **Besta et al.** (ETH Zurich 2023, ACM CSUR) — survey of 51 graph DB systems; LPG (Neo4j) is better than RDF for property-rich SC graphs. Confirms Neo4j as the correct MVP graph store.

## Sources & related

- [sources/src-2026-06-p4-availability-nowcasting.md](../../sources/src-2026-06-p4-availability-nowcasting.md)
- [sources/src-2026-06-liu-sc-kg.md](../../sources/src-2026-06-liu-sc-kg.md), [sources/src-2026-06-almahri-agentic-sc.md](../../sources/src-2026-06-almahri-agentic-sc.md), [sources/src-2026-06-zheng-sc-gcn-fl.md](../../sources/src-2026-06-zheng-sc-gcn-fl.md)
- [sources/src-2026-06-cheng-shield.md](../../sources/src-2026-06-cheng-shield.md), [sources/src-2026-06-ramzy-mare.md](../../sources/src-2026-06-ramzy-mare.md), [sources/src-2026-06-besta-graph-databases.md](../../sources/src-2026-06-besta-graph-databases.md)
- Project: [projects/p4-availability-nowcasting-graph](../../projects/p4-availability-nowcasting-graph.md)
