---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-petitjean-faster-dtw
tags:
- classification
- dtw
- nearest-centroid
- timeseries
zotero: petitjeanFasterMoreAccurate2016
source_hash: 005a2b3ef0343325a2b6767abcd8b7b4c3492e30073c647b27a14eb54f4a589f
---

# Source: Faster and More Accurate Classification of Time Series by Exploiting a Novel DTW Averaging Algorithm (2016)

## Metadata

- **Citekey:** `petitjeanFasterMoreAccurate2016`
- **Authors:** François Petitjean, Germain Forestier, Geoffrey I. Webb, Ann E. Nicholson, Yanping Chen, Eamonn Keogh
- **Venue:** IEEE TKDE, 2016 (Monash University / UC Riverside)
- **Relevant projects:** P1

## One-line takeaway

Using DBA-computed cluster centroids in a Nearest Centroid Classifier achieves classification accuracy matching or exceeding 1-NN DTW at 100x lower runtime — prototype quality determines routing quality.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| Nearest Centroid Classifier (NCC) with DBA centroids matches or exceeds 1-NN DTW accuracy on UCR benchmarks while being 100x faster at classification time | Empirical results on UCR datasets; some datasets show higher accuracy for NCC than NN | When prototypes accurately represent cluster shape; degrades for multimodal clusters | high |
| The key insight is that the DBA average is more representative than any individual instance ("Galton effect") — averaging combines evidence to produce a Platonic ideal | Theoretical motivation Section II | Supports using cluster prototypes as routing targets rather than all training instances | medium |
| Standard Euclidean averaging of DTW-comparable series produces prototypes with artefactual features (extra peaks/modes) not present in any individual series | Figure 1: oil refinery daily pattern example; Euclidean centroid has spurious peak | P1: do not use Euclidean centroid for prototype-based routing if series have temporal shifts | high |

## Limitations & caveats

- Accuracy gains of NCC over NN are not universal — multimodal cluster distributions or very heterogeneous clusters will see NCC accuracy collapse (Japanese flag counterexample).
- Focused on classification (labelled data); the clustering quality needed to produce good prototypes is assumed, not measured here.
- UCR benchmarks are classification datasets, not forecasting datasets — results may not transfer directly to P1's forecasting context.

## Decision impact for P1

- Reinforces: prototype quality (via DBA) is the primary lever for routing accuracy in a cluster-then-route system.
- 100x speedup at routing time is directly relevant: P1 routing to prototypes is much cheaper than comparing to all training series.
- Sets expectation: routing accuracy can be as good as NN-DTW if prototypes are high quality; but poor prototypes (Euclidean centroids) can significantly degrade routing.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
