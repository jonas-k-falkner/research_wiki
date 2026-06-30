---
type: source
domain: nowcasting-graph
project: P4
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-besta-graph-databases
tags:
- graph-database
- neo4j
- rdf
- labeled-property-graph
- infrastructure
- survey
zotero: bestaDemystifyingGraphDatabases2023
source_hash: 5ee58f1d5162fa8f6624d58c0072737a6f7d850e37bc9325e3d83b2fec06d976
---

# Demystifying Graph Databases: Analysis and Taxonomy of Data Organization, System Designs, and Graph Queries

**Besta et al. (2023) — ETH Zurich / ACM Computing Surveys**

## Summary

First comprehensive taxonomy and survey of 51 graph database systems. Covers four design axes: graph data models (RDF, LPG, hypergraph, etc.), data organisation (storage layout, indexing), data distribution (sharding, federation), and query execution (ACID transactions, OLTP vs OLAP). The two dominant paradigms are RDF/triple stores (W3C semantic web standard, SPARQL query language, e.g. Virtuoso, Stardog) and Labeled Property Graph databases (Neo4j, OrientDB; property-rich vertices and edges, Cypher/GQL query language). This is a survey paper — confidence medium (no experimental claims).

## Key findings from taxonomy

**Two primary paradigms:**
- **RDF triple stores** (subject–predicate–object): W3C standard; SPARQL query language; strong for semantic web inference (OWL ontologies), linked data interoperability; poor for property-rich entities (each property = new triple); used by: Virtuoso, Stardog, GraphDB, Blazegraph
- **Labeled Property Graph (LPG)**: vertices and edges carry arbitrary key-value properties and type labels; Cypher (Neo4j) / Gremlin query language; efficient for pattern matching on heterogeneous graphs; no global schema required; used by: Neo4j, OrientDB, TigerGraph, Amazon Neptune (supports both)

**Key design tradeoffs:**

| Dimension | RDF / Triple store | LPG (Neo4j) |
|---|---|---|
| Data model | Subject-predicate-object triples | Vertices + edges with labels and properties |
| Query language | SPARQL | Cypher / GQL |
| Schema flexibility | Schema-free (but verbose for properties) | Flexible labels + properties |
| Inference | OWL reasoning, RDFS entailment | No native inference |
| Pattern matching | Moderate (SPARQL graph patterns) | Strong (Cypher MATCH clause) |
| Property richness | O(n) triples per property per entity | O(1) property per entity |
| Ecosystem | Linked Data, knowledge graphs | Graph analytics, recommendation, SC networks |

**ACID and distribution:** Most GDBs support ACID. Sharding is hard for irregular graph topology — edge cuts produce frequent cross-partition traversals. Neo4j Fabric supports fabric sharding; fully distributed GDBs (TigerGraph, JanusGraph) trade ACID for scalability.

## Claims

**Claim:** For property-rich, heterogeneous SC graphs with multi-type entities (supplier, product, location, event) and multi-type relations, LPG (Neo4j) is architecturally superior to RDF triple stores because it stores arbitrary entity properties natively without exploding triple counts.
**Evidence:** Besta et al. 2023, Section 3.3.2 (LPG) vs 3.3.4 (RDF). RDF requires one triple per property per entity (e.g., Supplier hasSIC_code 3714 requires a separate triple); LPG stores all supplier properties in a single vertex record.
**Applicability:** Directly resolves P4's open question "relational store choice: do relational joins / materialized views suffice for the MVP before a property graph (Neo4j) is justified?" Answer: for multi-tier SC graphs with heterogeneous entity types and ad-hoc pattern queries, LPG wins over both RDF and relational.
**Limitations:** LPG lacks native inference (can't use OWL ontology to infer new relations — must be done in application layer). No semantic interoperability standard like SPARQL/RDF. Survey reflects state as of ~2023; newer systems (Amazon Neptune Analytics) support both paradigms.
**Contradictions:** MARE (Ramzy et al. 2022) uses RDF/SPARQL and achieves the same SC disruption assessment functionality — RDF works, it's just more verbose for property-rich schemas. AlMahri et al. 2026 uses Neo4j (LPG) in production; F1 0.962-0.991 confirms LPG is production-viable for SC monitoring.
**Decision impact:** Resolves P4's relational vs property graph question: Neo4j (LPG) is the right MVP choice. Rationale: (1) 8 entity types with many properties → LPG is O(1) per property vs RDF's O(n) triples; (2) Cypher MATCH is more natural for SC pattern queries than SPARQL; (3) AlMahri 2026 already validates Neo4j for SC monitoring at production F1; (4) MARE's SPARQL/RDF approach is usable but more complex for P4's heterogeneous schema.
**Confidence:** medium

## Applicability to P4

High for infrastructure decision. Confirms Neo4j (LPG) as the right graph database choice for P4's explicit evidence graph over RDF triple stores. The remaining open question (relational joins vs property graph for MVP scale) is answered: start with Neo4j, not a relational DB with graph joins, because SC pattern queries (multi-hop supplier path queries) are fundamentally graph operations.

## Related

- [src-2026-06-almahri-agentic-sc](src-2026-06-almahri-agentic-sc.md) — uses Neo4j in production (confirms LPG choice)
- [src-2026-06-ramzy-mare](src-2026-06-ramzy-mare.md) — uses RDF/SPARQL (alternative approach)
- [src-2026-06-liu-sc-kg](src-2026-06-liu-sc-kg.md) — SC KG schema reference
- [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md)
