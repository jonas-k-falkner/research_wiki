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

# Evidence ledger

## Definition

An append-only, provenance-backed store of extracted claims — each row carrying source, observed/published timestamps, linked entities/categories/regions, evidence type, confidence, and document reference. It is P4's system of record; the graph is a view over it. See [sources/src-2026-06-p4-availability-nowcasting.md](../sources/src-2026-06-p4-availability-nowcasting.md).

## Why it matters

It keeps availability nowcasts auditable and stops the graph from drifting into unverifiable hidden-edge generation — which is the report's central design choice and aligns with Sybilion's "explainable / decision-history" positioning.

## Open research questions

- What is the minimum viable evidence schema for an MVP vertical? (Open question in [shared/open-questions](../shared/open-questions.md).)
- How are conflicting claims about the same entity/category reconciled (recency, source reliability, weighting)?
- How is stale evidence retired without losing the audit trail (validity intervals on edges)?

## Literature to integrate `[verify]`

- Provenance / claim-tracking data models; bitemporal modelling (valid-time vs transaction-time) `[verify]`
- Truth discovery / source-reliability weighting across conflicting sources `[verify]`
- Evidence-based monitoring frameworks for supply-chain disruption (the report references semantic disruption frameworks — pull and verify) `[verify]`

## Cross-project relevance

- Pairs with [concepts/explicit-evidence-graph](explicit-evidence-graph.md) (view over ledger) and feeds [concepts/mixed-frequency-nowcasting](mixed-frequency-nowcasting.md) (scored signals). Auditability principle overlaps with P3's explainability story.

## Related pages

- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
- [domains/nowcasting-graph/thesis](../domains/nowcasting-graph/thesis.md)
