---
type: source
domain: nowcasting-graph
project: P4
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-liu-sc-kg
tags:
- supply-chain
- knowledge-graph
- link-prediction
- graph-embedding
zotero: liuKnowledgeGraphPerspective2023
source_hash: 67e78b4710c9ee04e857efae1acd89316ac79858e480a20cda04bd7b619116da
---

# Supply Chain Knowledge Graph Completion with Relation Learning

**Liu et al. (2023) — ESWC 2023**

## Summary

Constructs and evaluates knowledge graph completion methods on a real Siemens industrial supply chain KG spanning 3 tiers of suppliers (tier-1, tier-2, tier-3). The KG contains 65K nodes, 311K edges, 8 entity types (component, supplier, manufacturer, customer, location, category, standard, process), and 11 relation types (supplies, manufactures, locatedIn, categorizedAs, etc.). Evaluates TransE, DistMult, ComplEx, RotatE, and Tucker on KG completion; RotatE achieves best MRR. Also computes centrality-based supplier criticality metrics for risk management.

## Key results

- RotatE: MRR 0.4377 — best KG embedding method on this SC benchmark
- TransE: MRR ~0.32, DistMult ~0.35, ComplEx ~0.37, Tucker comparable to RotatE
- 65K nodes, 311K edges across 3 supplier tiers
- Centrality metrics (betweenness, closeness, degree centrality) identify critical supplier nodes
- KG constructed from structured Siemens supplier database, not text extraction

## Architecture details

- RotatE represents relations as rotations in complex space: $h \circ r = t$, modelling symmetry and antisymmetry
- Entity types: component, supplier, manufacturer, customer, location, category, standard, process
- Relation types: supplies, manufactures, locatedIn, categorizedAs, conformsTo, requires, alternativeTo, plus tier-specific relations
- KG completion formulated as link prediction (head or tail prediction given other two elements of triple)
- Centrality computed on projected single-relation subgraphs

## Claims

**Claim:** RotatE achieves MRR 0.4377 on a 3-tier industrial supply chain KG (65K nodes, 311K edges), the best among TransE, DistMult, ComplEx, and Tucker.
**Evidence:** Experimental results table, ESWC 2023 paper. MRR 0.4377 for RotatE vs TransE ~0.32, DistMult ~0.35.
**Applicability:** Industrial manufacturing SC KGs with well-structured, curated entity/relation schemas. Performance on noisier, text-extracted SC KGs is unknown.
**Limitations:** KG constructed from structured database — not from text extraction. Real-world SC KGs from public sources would be noisier. Results on a single proprietary SC dataset.
**Contradictions:** None.
**Decision impact:** RotatE is the reference KG embedding baseline for P4. MRR ~0.44 on curated data confirms KG completion is feasible but imperfect — supports P4's evidence-ledger-first approach over aggressive hidden-edge completion.
**Confidence:** high

**Claim:** Node centrality metrics (betweenness, closeness, degree) on supply chain KGs identify supplier criticality and concentration risk without requiring predictive models.
**Evidence:** Liu et al. 2023 Section 4: centrality analysis identifies a small set of high-betweenness tier-2 suppliers whose failure would disconnect large graph components.
**Applicability:** Any structured SC graph with multi-tier topology.
**Limitations:** Centrality is a static structural metric — does not capture dynamic availability or event-based disruptions.
**Contradictions:** None.
**Decision impact:** Centrality-based criticality is a simple, interpretable baseline for P4's supplier risk scores. Should be included as a fallback heuristic alongside evidence-based scoring.
**Confidence:** high

## Applicability to P4

High. This paper directly informs P4's SC graph schema and KG completion choices:
- RotatE MRR 0.4377 confirms the formerly unverified MRR ~0.44 claim in `explicit-evidence-graph.md`
- 8 entity types / 11 relation types gives a concrete starting schema for P4's SC KG
- MRR <0.5 on curated data reinforces why P4's MVP rejects aggressive hidden-edge completion (provenance-backed edges only)
- Centrality criticality metrics are a viable P4 risk heuristic

## Related

- [src-2026-06-almahri-agentic-sc](src-2026-06-almahri-agentic-sc.md) — agentic monitoring built on top of such a KG
- [src-2026-06-zheng-sc-gcn-fl](src-2026-06-zheng-sc-gcn-fl.md) — GCN+FL for link prediction on SC KGs
- [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md)
- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
