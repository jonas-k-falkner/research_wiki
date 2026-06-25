---
type: project
domain: nowcasting-graph
project: P4
status: active
confidence: medium
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-p4-availability-nowcasting
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

## Sources

- [sources/src-2026-06-p4-availability-nowcasting.md](../sources/src-2026-06-p4-availability-nowcasting.md) — full MVP report; rejects full graph reconstruction.

## Related pages

- [domains/nowcasting-graph/thesis](../domains/nowcasting-graph/thesis.md)
- [concepts/evidence-ledger](../concepts/evidence-ledger.md)
- [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md)
- [concepts/mixed-frequency-nowcasting](../concepts/mixed-frequency-nowcasting.md)
- [entities/p4-public-data-sources](../entities/p4-public-data-sources.md)
- [experiments/exp-p4-public-first-nowcast-mvp](../experiments/exp-p4-public-first-nowcast-mvp.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
