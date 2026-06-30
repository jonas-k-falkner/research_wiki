---
type: source
domain: nowcasting-graph
project: P4
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p4-availability-nowcasting
tags:
- nowcasting
- supply-chain
- evidence-ledger
- graph
---

# Source: B2B SCM availability nowcasting report

## Metadata

- Source ID: `src-2026-06-p4-availability-nowcasting`
- Raw path: `raw/seed/p4_availability_nowcasting.md`
- Date: June 2026
- Source type: technical report
- Relevant project: P4

## One-line takeaway

The best MVP is not full global supply-chain graph reconstruction; it is a hybrid nowcast plus evidence ledger using structured public data, high-frequency public text, relation extraction, and a lightweight provenance-backed graph.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| Public-only data can support useful category × region availability nowcasts. | Official data, procurement, public web, and event streams are enough for early-warning signals. | P4 MVP can start public-first. | medium |
| Public-only supplier × category estimates are possible but uneven. | Coverage is stronger for listed, procurement-active, and public-catalog firms; weaker for private deep-tier suppliers. | P4 should expose confidence and coverage limitations. | high |
| Full graph reconstruction is rejected for MVP. | Input sparsity, entity-resolution burden, hidden-edge uncertainty, and benchmarking difficulty dominate. | P4 should build an explicit evidence graph first. | high |
| Expanded data improves the same architecture rather than replacing it. | Customs, AIS, and distributor APIs improve coverage/freshness but do not change the ledger-centered design. | Buy data later when coverage gaps are visible. | medium |
| Evidence ledger is the center of gravity. | The graph should be a view over provenance-backed claims, not the source of truth. | Architecture should favor auditability over speculative graph completion. | high |

## Recommended MVP layers

1. Source ingestion.
2. Entity normalization.
3. Taxonomy alignment.
4. Event and relation extraction.
5. Evidence ledger.
6. Mixed-frequency signal fusion.
7. Availability scoring.
8. Explainable alerting.
9. Explicit evidence graph as a structured memory and propagation layer.

## Updated pages

- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
- [domains/nowcasting-graph/thesis](../domains/nowcasting-graph/thesis.md)
- [concepts/evidence-ledger](../concepts/evidence-ledger.md)
- [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md)
- [concepts/mixed-frequency-nowcasting](../concepts/mixed-frequency-nowcasting.md)
- [experiments/exp-p4-public-first-nowcast-mvp](../experiments/exp-p4-public-first-nowcast-mvp.md)
