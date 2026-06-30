---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-um-wearable-augmentation
tags:
- data-augmentation
- ssl
- timeseries
zotero: umDataAugmentationWearable2017
source_hash: 16da48ca4aecba78c4ea55cfc62adc8e5b5658f178088bcd43cba0d2b3d0f72e
---

# Source: Data Augmentation of Wearable Sensor Data for Parkinson's Disease Monitoring (2017)

## Metadata
- **Citekey:** `umDataAugmentationWearable2017`
- **Authors:** Um, Pfister, Pichler, Endo, Lang, Hirche, Fietzek, Kulić
- **Venue:** ICMI 2017
- **Relevant projects:** P2 (augmentation catalog)

## One-line takeaway

Foundational paper for TS data augmentation: systematic comparison of jitter, scaling, magnitude warping, time warping, rotation, permutation, and window slicing/cropping on wearable sensor TS — jitter + scaling are the most reliable; rotation is domain-specific (sensor orientation).

## Key claims

- **Augmentation catalog:** jitter (Gaussian noise), scaling (global amplitude), magnitude warping (smooth random scaling per-timestep), time warping (smooth random time axis distortion), rotation (multiply by random rotation matrix), permutation (shuffle equal-length segments), window slicing (crop random subsequence).
- On Parkinson's disease gait telemetry, jitter + scaling + magnitude warping improve classification accuracy most reliably; permutation and rotation are more dataset-specific.
- First systematic comparison of TS augmentations for health sensor data; became the standard reference for TS contrastive learning augmentation design (cited by TS-TCC, TimeCLR, and virtually all TS SSL papers).

## Relevance to P2

Canonical augmentation reference for P2's positive-pair construction. Safe augmentations for P2 (preserve TE/Granger directional signal): jitter, scaling, magnitude warping, window slicing. Dangerous augmentations for P2 (may destroy causal direction): permutation (shuffles temporal order), rotation (for multivariate TS with correlated channels). P2 should use jitter + scaling + window slicing as the baseline augmentation set and ablate magnitude warping.
