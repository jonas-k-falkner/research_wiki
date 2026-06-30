---
type: source
domain: nowcasting-graph
project: P4
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-cheng-shield
tags:
- supply-chain
- schema-induction
- llm
- knowledge-graph
- event-extraction
- ev-battery
zotero: chengSHIELDLLMDrivenSchema2024
source_hash: 47746e3192cd16e4c046a1156ca298a66d0cb50cc76d02e14367e51da52240c4
---

# SHIELD: LLM-Driven Schema Induction for Predictive Analytics in EV Battery Supply Chain Disruptions

**Cheng et al. (2024) — Carnegie Mellon University (arXiv / conference)**

## Summary

Two-stage system for EV battery SC disruption prediction. Stage 1: LLM-driven schema learning — uses GPT-4o and Llama3 to extract hierarchical event schemas (main events + sub-events + relations) from 239 sources (200 academic papers, 22 industry reports, 17 Wikipedia entries). Expert feedback refines into 11 main categories × 27 subcategories. Stage 2: Disruption analysis — fine-tuned RoBERTa for multi-sentence event detection, BERT for contextual enrichment, CRF for parameter extraction, GCN for impact scoring (centrality × magnitude). Evaluated on 12,070 paragraphs from 365 sources (2022-2023 EV SC news + enterprise reports). Outperforms baseline GCN and GPT-4o prompting.

## Key results

- LLM schema induction + GCN outperforms baseline GCN and GPT-4o prompt-only on disruption prediction
- 12,070 paragraphs from 365 sources (Jan 2022–Dec 2023), ~660K words
- Schema covers 6 EV battery raw materials (Li, Co, Ni, Mn, graphite, rare earths), 8 → 11 event categories (with expert feedback), 27 subcategories
- Event impact score: centrality (graph network position) + magnitude (severity); GCN models cascading effects
- Human-in-the-loop schema curation is essential: LLM alone produces schemas requiring expert correction

## Architecture details

- Schema extraction: GPT-4o / Llama3-3b / Llama3-70b with chain-of-thought prompts; hierarchical structure H = (E_main, E_sub, R)
- Schema merging: union of event sets and relation sets across individual source schemas
- Event detection: fine-tuned RoBERTa for cross-sentence event span detection
- Contextual enrichment: BERT embeddings for extracted events
- Event linking: coreference resolution across documents
- Parameter extraction: CRF on linked events
- Impact scoring: ImpactScore(e_i) = Centrality(e_i) + Magnitude(e_i)
- Event matching: composite similarity = α × SemSim (BERT cosine) + β × StrSim (Jaccard on parameter sets)

## Claims

**Claim:** LLM-driven schema induction from academic/industry documents (GPT-4o + human curation) produces event schemas that improve SC disruption prediction accuracy over both manual GCN and GPT-4o prompting baselines.
**Evidence:** Cheng et al. 2024, main results section. SHIELD outperforms baseline GCN and LLM+prompt (GPT-4o) on EV battery SC disruption prediction.
**Applicability:** Any SC domain where disruption event types are semi-structured and documentable — EV battery SC is an extreme case (geopolitical concentration, mineral dependencies). Applicable to P4 where schema-driven event extraction is needed from public news and filings.
**Limitations:** Heavy on infrastructure: requires fine-tuned RoBERTa, BERT, CRF, GCN. Expert curation is a bottleneck. Focused on EV battery SC — schema generalization to other SC domains not validated. GCN assumes a fixed event graph topology.
**Contradictions:** AlMahri et al. 2026 achieves high F1 with simpler agentic approach (RAG + Cypher queries) — may be sufficient for P4's monitoring use case without full schema induction infrastructure.
**Decision impact:** Schema induction via LLM is the reference approach for P4's event extraction component. However, SHIELD's full pipeline (schema + RoBERTa + CRF + GCN) is MVP-heavy. P4's MVP can start with LLM-based schema induction (event types, attributes) and simpler extraction, deferring GCN impact scoring. Key insight: human-in-the-loop schema curation is required — purely automated LLM schemas need expert validation.
**Confidence:** high

## Applicability to P4

Medium-high. SHIELD directly addresses P4's open question about "schema-driven disruption/event extraction frameworks." Key takeaways:
- LLM schema induction is a viable alternative to manual ontology design (MARE approach)
- Event impact scoring via GCN (centrality + magnitude) is a reference for P4's disruption propagation
- Human-in-the-loop curation is non-negotiable for production quality
- SHIELD's evaluation data (12K paragraphs from 365 sources) gives a concrete benchmark scale for P4's corpus

## Related

- [src-2026-06-ramzy-mare](src-2026-06-ramzy-mare.md) — ontology-based alternative for SC disruption modelling
- [src-2026-06-almahri-agentic-sc](src-2026-06-almahri-agentic-sc.md) — agentic approach that uses pre-existing KG
- [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md)
- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
