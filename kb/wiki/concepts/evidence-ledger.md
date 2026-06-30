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
- src-2026-06-almahri-agentic-sc
tags:
- concept
- evidence
- provenance
- supply-chain
---

# Evidence ledger

## Definition

An append-only, provenance-backed store of extracted claims — each row carrying source, observed/published timestamps, linked entities/categories/regions, evidence type, confidence, and document reference. It is P4's system of record; the graph is a view over it. See [sources/src-2026-06-p4-availability-nowcasting.md](../sources/src-2026-06-p4-availability-nowcasting.md).

## Why it matters

It keeps availability nowcasts auditable and stops the graph from drifting into unverifiable hidden-edge generation — which is the report's central design choice and aligns with Sybilion's "explainable / decision-history" positioning.

## Open research questions

- What is the minimum viable evidence schema for an MVP vertical? (Open question in [shared/open-questions](../shared/open-questions.md).)
- How are conflicting claims about the same entity/category reconciled (recency, source reliability, weighting)?
- How is stale evidence retired without losing the audit trail (validity intervals on edges)?

## Primary literature (I-P4-A, 2026-06-30)

**Agentic SC monitoring confirms architecture** ([src-2026-06-almahri-agentic-sc](../sources/src-2026-06-almahri-agentic-sc.md), AlMahri et al. 2026):
- The best-performing agentic SC pipeline (F1 0.962–0.991) stores all SC entity knowledge in an evidence-backed Neo4j KG and queries it via Cypher for every factual lookup. This matches the evidence ledger as system-of-record design.
- Three hallucination mitigations required for production F1 > 0.95: (1) RAG over the evidence ledger, (2) deterministic tool calls for all factual lookups (no LLM hallucination on entity facts), (3) human-in-the-loop escalation for low-confidence alerts.
- The evidence-first architecture is validated at production scale.

## Open questions (unresolved)

- Provenance / claim-tracking data models; bitemporal modelling (valid-time vs transaction-time)
- Truth discovery / source-reliability weighting across conflicting sources

## Cross-project relevance

- Pairs with [concepts/explicit-evidence-graph](explicit-evidence-graph.md) (view over ledger) and feeds [concepts/mixed-frequency-nowcasting](mixed-frequency-nowcasting.md) (scored signals). Auditability principle overlaps with P3's explainability story.

## Related pages

- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
- [domains/nowcasting-graph/thesis](../domains/nowcasting-graph/thesis.md)
