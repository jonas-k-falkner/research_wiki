---
type: source
domain: nowcasting-graph
project: P4
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-ramzy-mare
tags:
- supply-chain
- ontology
- knowledge-graph
- disruption-management
- sparql
- semantic
zotero: ramzyMARESemanticSupply2022
source_hash: d81ce6814b1f63442b0a562c2a08c79db6ae9b4c0effe31dc32b44deec201fb371f
---

# MARE: Semantic Supply Chain Disruption Management and Resilience Evaluation Framework

**Ramzy, Auer, Ehm & Chamanara (2022) — Infineon Technologies + TIB Hannover**

## Summary

MARE is a semantic framework covering all four phases of Supply Chain Disruption Management Process (DMP): **Monitor/Model**, **Assess**, **Recover**, **Evaluate**. Existing approaches address DMP phases in isolation; MARE integrates them via ontologies, knowledge graphs, and SPARQL queries. A Disruption Ontology models event attributes (cause, scope, severity, location, begin/end dates). A Disruption KG instantiates specific events. SPARQL queries cross-reference the Disruption KG with production scheduling data (Supply Plan) to identify affected SC partners, find alternative allocations, and evaluate recovery cost/delay. Demonstrated on a synthetic semiconductor SC scenario (Infineon domain).

## Key results

- First framework (per authors) to integrate all 4 DMP phases via semantic technologies
- Disruption Ontology: 6 key attributes — hasCause, hasScope, hasSeverity, hasLocation, hasBeginDate, hasEndDate
- Assessment SPARQL: identifies affected SC partners by geospatial + temporal cross-reference with Supply Plan
- Recovery SPARQL: finds alternative supplier allocations from inventory + order management data
- Evaluation: SC resilience metric = cost of recovery + delay to return to pre-disruption state
- Examples: COVID warehouse shutdown, Philips semiconductor fire, Suez Canal blockage, BMW chip shortage — all modelled with same ontology

## Architecture details

- **Disruption Ontology** (RDF triples): Disruption hasCause Cause; Cause hasScope xsd:string; Disruption hasSeverity xsd:string; Disruption hasBeginDate/hasEndDate xsd:date; Disruption hasLocation Location (lat/long)
- **Supply Plan representation** (prior work, Ramzy 2021): Customer makes Order; Order hasProduct/hasDeliveryTime/hasQuantity; Plan needsPartner Partner; partner hasLongitude/hasLatitude
- **Assessment SPARQL**: WHERE clause cross-references disruption location/time with supply plan partner location/time; marks affected plans as isDisrupted 'True'
- **Recovery SPARQL**: finds alternative partners from inventory/order management for disrupted plans; quantifies toRecover amount
- **Evaluation framework**: resilience = time + cost to return to pre-disruption state; compares multiple recovery strategies

## Claims

**Claim:** A semantic ontology + SPARQL query approach (MARE) can cover all 4 DMP phases (Monitor, Assess, Recover, Evaluate) by cross-referencing a Disruption KG with structured SC planning data, without requiring a predictive model.
**Evidence:** Ramzy et al. 2022, Sections 4-6. SPARQL queries in Listings 1-2 demonstrate geospatial + temporal matching for disruption assessment. Synthetic Infineon SC scenario in Section 6 validates all four phases.
**Applicability:** SC with structured, machine-readable Supply Plan data (production scheduling, inventory, order management). P4's evidence ledger + explicit evidence graph is a direct analogue: disruption events are modelled as instances of the Disruption Ontology, and SPARQL over the evidence graph identifies affected supplier routes.
**Limitations:** Requires structured SC planning data — MARE's assessment SPARQL assumes exact geospatial coordinates for SC partners. P4's public-first evidence graph has lower entity resolution (many suppliers known at city/region level, not exact location). Recovery phase requires integration with live inventory/order management systems — not available for P4's public-first MVP.
**Contradictions:** SHIELD (LLM-based) uses event extraction from unstructured text — more scalable for public-first data. MARE assumes structured internal SC data. For P4, MARE's ontology is a reference design but extraction will be LLM-based.
**Decision impact:** MARE's Disruption Ontology is a reference schema for P4's event types. The 6 attributes (cause, scope, severity, location, begin/end dates) map directly to P4's disruption event columns in the evidence ledger. The Monitor→Assess→Recover→Evaluate pipeline matches P4's intended product workflow.
**Confidence:** high

## Applicability to P4

High for ontology design; Medium for full pipeline. Key takeaways:
- MARE's Disruption Ontology is a validated reference schema for P4's event entity type
- The SPARQL assessment pattern (cross-reference disruption location/time with SC plan) maps to P4's propagation logic
- Recovery phase (alternative supplier lookup) is a future P4 feature, not MVP scope
- MARE confirms that ontology + query approach is sufficient for assessment and planning — no ML required for the assessment phase

## Related

- [src-2026-06-cheng-shield](src-2026-06-cheng-shield.md) — LLM-based event schema induction (complements MARE's manual ontology)
- [src-2026-06-almahri-agentic-sc](src-2026-06-almahri-agentic-sc.md) — agentic monitoring that builds on similar KG infrastructure
- [src-2026-06-besta-graph-databases](src-2026-06-besta-graph-databases.md) — graph DB choice (SPARQL/RDF vs LPG/Cypher)
- [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md)
- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
