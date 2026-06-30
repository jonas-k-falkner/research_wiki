---
type: experiment
domain: nowcasting-graph
project: P4
status: draft
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p4-availability-nowcasting
tags:
- experiment
---

# Experiment: P4 public-first nowcast MVP

## Status

Designed-from-source, not yet run. Report frames a ~6–8 week compressed plan; the correct first cut is **category × region for one vertical**, building the ledger so supplier × category can follow.

## Hypothesis

Public-first sources (official structured data + high-frequency public text) are sufficient to produce a useful, calibrated, explainable category × region availability nowcast for one vertical — without licensed data and without full graph reconstruction.

## Protocol (seed — from report MVP plan)

1. Lock scope + category taxonomy for one vertical (which vertical is an open question — see below).
2. Build a public validation set (SEC supplier/customer mentions, TED/SAM awards, known disruption windows, lagged FAO/trade directionality).
3. Stand up official connectors ([entities/p4-public-data-sources](../entities/p4-public-data-sources.md)) + a thin public-web crawl.
4. Event/relation extraction → write into a minimal [concepts/evidence-ledger](../concepts/evidence-ledger.md).
5. [concepts/mixed-frequency-nowcasting](../concepts/mixed-frequency-nowcasting.md) scoring → availability score + confidence.
6. Explainable alerts with provenance trace; backtest calibration.

## Metrics

- Entity-resolution accuracy.
- Event/relation extraction precision & recall.
- Alert lead time vs known disruptions.
- Availability-score calibration.
- Explanation completeness.
- **Coverage separation**: publicly-observable truth vs unobservable hidden-edge truth (do not penalise the system for the latter).

## To specify before running `[seed gaps]`

- First vertical: components vs chemicals/materials vs food/agri (open question — public-data quality differs sharply).
- Anchor source connector for the first validation set.
- Minimum viable evidence schema.

## Literature to integrate `[verify]`

- Entity resolution (Fellegi-Sunter; Splink/Dedupe-class methods) `[verify]`
- Event/relation extraction from news + filings; GDELT GKG usage `[verify]`
- Mixed-frequency nowcasting (MIDAS, dynamic factor) `[verify]`
- Supply-chain disruption monitoring frameworks cited in the report `[verify]`

## Expected failure modes (project-specific)

- Supplier-depth coverage too sparse for the chosen vertical → category×region works, supplier×category does not.
- Public-text extraction false-positive rate too high → noisy alerts erode trust.
- No clean public ground truth for the vertical → calibration unmeasurable.

## Decision impact

Go / modify / defer on the public-first thesis, and selection of the first production vertical.

## Related pages

- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
- [entities/p4-public-data-sources](../entities/p4-public-data-sources.md)
- [concepts/evidence-ledger](../concepts/evidence-ledger.md)
