---
type: project
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
- supply-chain
- nowcasting
- graph
- evidence-ledger
---

# P4 — Availability nowcasting graph

## Purpose

Build a high-rigor MVP for industrial B2B supply availability nowcasting across components, chemicals/materials, and food/agri. Outputs are product/category × region availability and supplier/company × category availability.

## Current thesis

The right MVP is a hybrid nowcast plus evidence ledger, not a full reconstructed global supply-chain graph. The graph should be a provenance-backed view over evidence, not a speculative hidden-edge generator.

## Recommended architecture

```text
official structured sources + public text + optional expanded data
  → entity normalization
  → taxonomy alignment
  → event and relation extraction
  → evidence ledger
  → explicit evidence graph
  → mixed-frequency signal fusion
  → availability scores
  → explainable alerts
```

## MVP boundary

| Include in MVP | Defer |
|---|---|
| Category × region availability nowcast | Full global supply-chain reconstruction |
| Supplier × category estimates where evidence exists | Aggressive hidden-edge completion |
| Provenance-backed relation edges | GNN/link prediction as operational truth |
| Mixed-frequency score fusion | Heavy black-box nowcast models |
| Public-first data sources | Expensive licensed data before coverage gaps are measured |

## Source strategy

Public-first sources include SEC EDGAR, GLEIF, TED, SAM.gov, GDELT, Common Crawl / first-party web crawling, FAO statistics, and derived trade access layers. Expanded tier can later add customs/BOL, AIS, and vertical distributor APIs.

## Key design principle

The evidence ledger is the system of record. The graph is a query and propagation view over the ledger.

## Main risks

| Risk | Mitigation |
|---|---|
| Supplier-depth coverage is uneven | Separate coverage confidence from availability score |
| Graph reconstruction becomes unverifiable | Store only provenance-backed edges in MVP |
| Public text creates false positives | Use evidence types, source reliability, and confidence scoring |
| Data licenses constrain downstream use | Prefer official/public connectors first and isolate expanded-tier sources |

## Secondary literature (I-P4-A MEDIUM, 2026-06-30)

**Schema-driven disruption/event extraction:**
- **SHIELD** ([src-2026-06-cheng-shield](../sources/src-2026-06-cheng-shield.md), CMU 2024): LLM schema induction (GPT-4o from 239 sources) produces 11 event categories × 27 subcategories for EV battery SC disruption prediction; fine-tuned RoBERTa event detection + GCN impact scoring outperform baseline GCN and GPT-4o prompting. Human-in-the-loop curation is non-negotiable. P4 design input: LLM schema induction is viable for generating P4's disruption event taxonomy from unstructured sources.
- **MARE** ([src-2026-06-ramzy-mare](../sources/src-2026-06-ramzy-mare.md), Infineon + TIB 2022): Disruption Ontology (hasCause, hasScope, hasSeverity, hasLocation, hasBeginDate/hasEndDate) + SPARQL DMP pipeline covers all 4 phases (Monitor, Assess, Recover, Evaluate). P4 design input: MARE's 6-attribute Disruption Ontology is the reference schema for P4's disruption event entity type in the evidence ledger.

**Graph DB infrastructure:**
- **Besta et al.** ([src-2026-06-besta-graph-databases](../sources/src-2026-06-besta-graph-databases.md), ETH Zurich 2023, ACM CSUR): survey of 51 graph DB systems; LPG (Neo4j) is better than RDF for property-rich heterogeneous SC graphs (O(1) property storage vs RDF's O(n) triples). Cypher MATCH is more natural for SC pattern queries than SPARQL. Decision: Neo4j is confirmed as the correct MVP graph store for P4's explicit evidence graph.

## Literature support (I-P4-A, 2026-06-30)

Three primary papers now support the P4 architecture:
- **SC KG construction + RotatE completion** ([src-2026-06-liu-sc-kg](../sources/src-2026-06-liu-sc-kg.md)): MRR 0.4377 on curated 3-tier SC KG confirms the MVP's rejection of aggressive hidden-edge completion. SC KG schema (8 entity types, 11 relation types) is a concrete starting template.
- **Agentic SC monitoring** ([src-2026-06-almahri-agentic-sc](../sources/src-2026-06-almahri-agentic-sc.md)): F1 0.962–0.991 on 7-agent pipeline built on pre-existing SC KG. Validates evidence ledger → graph → agent pipeline. Three required mitigations: RAG, deterministic tool calls, human-in-the-loop.
- **GCN + FL for SC link prediction** ([src-2026-06-zheng-sc-gcn-fl](../sources/src-2026-06-zheng-sc-gcn-fl.md)): GraphSAGE inductive learning is required for live SC graph with evolving entity set. FL enables multi-organization data integration without raw data sharing (relevant for GDPR-constrained onboarding).

## Sources

- [sources/src-2026-06-p4-availability-nowcasting.md](../sources/src-2026-06-p4-availability-nowcasting.md) — full MVP report; rejects full graph reconstruction.
- [sources/src-2026-06-liu-sc-kg.md](../sources/src-2026-06-liu-sc-kg.md) — SC KG construction and RotatE KG completion (ESWC 2023)
- [sources/src-2026-06-almahri-agentic-sc.md](../sources/src-2026-06-almahri-agentic-sc.md) — agentic SC disruption monitoring (arXiv 2026)
- [sources/src-2026-06-zheng-sc-gcn-fl.md](../sources/src-2026-06-zheng-sc-gcn-fl.md) — GCN + federated learning for SC link prediction (Cambridge, 2025)
- [sources/src-2026-06-cheng-shield.md](../sources/src-2026-06-cheng-shield.md) — SHIELD: LLM schema induction for EV battery SC disruption prediction (CMU 2024)
- [sources/src-2026-06-ramzy-mare.md](../sources/src-2026-06-ramzy-mare.md) — MARE: semantic SC disruption ontology + SPARQL DMP framework (Infineon, 2022)
- [sources/src-2026-06-besta-graph-databases.md](../sources/src-2026-06-besta-graph-databases.md) — graph DB taxonomy: LPG (Neo4j) vs RDF, infrastructure choice for P4 (ETH 2023)
- [sources/src-2026-06-minder-data2neo.md](../sources/src-2026-06-minder-data2neo.md) — Data2Neo (ETH 2024): open-source Python ETL for relational → Neo4j; recommended ETL tool for P4's evidence ledger → graph construction

## Related pages

- [domains/nowcasting-graph/thesis](../domains/nowcasting-graph/thesis.md)
- [concepts/evidence-ledger](../concepts/evidence-ledger.md)
- [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md)
- [concepts/mixed-frequency-nowcasting](../concepts/mixed-frequency-nowcasting.md)
- [entities/p4-public-data-sources](../entities/p4-public-data-sources.md)
- [experiments/exp-p4-public-first-nowcast-mvp](../experiments/exp-p4-public-first-nowcast-mvp.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
