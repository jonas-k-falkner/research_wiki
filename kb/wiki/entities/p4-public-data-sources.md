---
type: entity
domain: nowcasting-graph
project: P4
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p4-availability-nowcasting
tags:
- entity
- data-sources
- p4
---

# Entity set: P4 public data sources

Landing page for the data sources P4 depends on. Seeded from [sources/src-2026-06-p4-availability-nowcasting.md](../sources/src-2026-06-p4-availability-nowcasting.md); each row needs a dedicated entity page once the research/integration pass begins (access terms, rate limits, licensing, and coverage must be verified against current provider docs — they change).

## Public-first tier

| Source | Role in P4 | Most needed for | Cost | Verify before relying `[verify]` |
|---|---|---|---|---|
| SEC EDGAR | Filings; supplier/customer mentions; risk/facility disclosures | Supplier × category; validation | Free | Automated-access policy; coverage biased to filers |
| GLEIF (LEI) | Entity normalization; ownership links | All approaches | Free | LEI-centric coverage |
| GLEIF↔OpenCorporates map | LEI → registry identifiers | Cross-source joins | Free | Partial mapping coverage |
| TED | EU procurement demand/awards; CPV codes | Category × region; supplier × category | Free | Above-threshold procurement; fair-use policy |
| SAM.gov | US entity info; federal contracting | Supplier × category; validation | Free | Some views require sign-in |
| GDELT 2.0 | Global event/theme stream (~15-min) | Category × region nowcast; weak signals | Free | Event-extraction noise; media bias |
| Common Crawl + first-party crawl | Company sites, catalogs, supplier pages | Supplier × category | Free | Third-party site terms may still apply — legal caution |
| FAO / FAOSTAT | Agrifood production, trade, prices | Food/agri category × region | Free | Country reporting lags |
| OEC (Comtrade-derived) | Cleaned HS/SITC trade structures | Category × region | Free (site) | Derived, not primary authority |

## Expanded tier (deferred; licensing-gated)

| Source family | What it adds | Note `[verify]` |
|---|---|---|
| Customs / bills-of-lading | Biggest lift for supplier discovery & deep-tier inference | Quote-based pricing; redistribution limits |
| AIS / maritime intelligence | Vessel, port, congestion, delay signals | Freemium→commercial; coverage asymmetries |
| Electronics/industrial distributor APIs | Stock, lead-time, MOQ, alternates | High value for components, weak for bulk chemicals |

## Open research questions

- Which source anchors the first validation set, and for which vertical?
- Licensing isolation: how to keep expanded-tier data from contaminating public-only redistribution claims?

## Related pages

- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
- [experiments/exp-p4-public-first-nowcast-mvp](../experiments/exp-p4-public-first-nowcast-mvp.md)
- [concepts/evidence-ledger](../concepts/evidence-ledger.md)
