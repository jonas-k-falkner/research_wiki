---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-zanotti-retraining-frequency
tags:
- timeseries-forecasting
- global-models
- retraining
zotero: zanottiRetrainingFrequencyGlobal2025
source_hash: 89c3e5ad92975d6301cb10ac39c7b832c657cb90da5d76afb85dd9e4c22eed3f
---

# Retraining Frequency of Global Models

**Zanotti et al. (2025)**

## Summary (3 bullets)

- Studies how often global forecasting models need to be retrained to maintain accuracy as distribution shifts occur, finding that retraining frequency depends on the strength and frequency of distribution shifts.
- Global models (trained on many series) are more robust to distributional shifts than local models, requiring less frequent retraining.
- **Applicability to P1**: directly relevant to P1's operational cadence question — how often cluster-pretrained models need full retraining vs. lightweight adaptation. Supports the global/cluster-pretrained model design direction.
