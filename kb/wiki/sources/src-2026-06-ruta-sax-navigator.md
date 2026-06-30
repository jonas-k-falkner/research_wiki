---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-ruta-sax-navigator
tags:
- clustering
- sax
- hierarchical-clustering
- timeseries
zotero: rutaSAXNavigatorTime2019
source_hash: 8bbb0a1cdbc0f90b4df965a339b1d7caec1a4ccfe9d9782135e42909dfd79a2f
---

# Source: SAX Navigator: Time Series Exploration through Hierarchical Clustering (2019)

## Metadata

- **Citekey:** `rutaSAXNavigatorTime2019`
- **Authors:** Ruta et al.
- **Venue:** 2019 (IEEE VAST)
- **Relevant projects:** P1

## One-line takeaway

SAX Navigator uses symbolic representation (SAX) + hierarchical clustering for exploratory visual analysis of large TS corpora — demonstrates that symbolization + hierarchy enables human-navigable clustering without per-series tuning.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| SAX (Symbolic Aggregate Approximation) enables fast approximate clustering of large TS corpora through compression and string distance | System demonstration on real TS datasets | Applicable for P1's offline cluster formation when computational budget is limited | medium |
| Hierarchical clustering of SAX-encoded series reveals multi-resolution cluster structure useful for navigation and anomaly detection | Visual analysis tool demonstration | P1 could use hierarchical structure to set cluster granularity adaptively | low |
| SAX loses shape information at high compression ratios — cluster quality degrades with aggressive quantization | Known limitation of SAX; cited in Aghabozorgi 2015 survey | At full P1 scale, SAX is a trade-off between speed and cluster accuracy | medium |

## Limitations & caveats

- SAX is lossy; regime-level patterns may survive compression but fine-grained shape patterns are lost.
- Primarily a visualization/exploration tool — not designed for production-scale forecasting pipelines.

## Decision impact for P1

- Low direct impact; confirms SAX is viable for exploratory cluster analysis but not for production clustering where routing accuracy matters.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
