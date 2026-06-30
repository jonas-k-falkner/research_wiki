---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-fraikin-trep
tags:
- ssl
- self-supervised
- time-embeddings
- contrastive
- forecasting
- time-series
zotero: fraikinTRepRepresentationLearning2024
source_hash: 65772fe729aadb12b9a4c1d6a7e0c4904117fb5f9c8a86040c15afe785ad0a08
---

# T-Rep: Representation Learning for Time Series Using Time-Embeddings

**Fraikin, Allassonnière & Bennetot (2024) — ICLR 2024**

## Summary

T-Rep extends TS2Vec by adding a learned **time-embedding module** that produces vector embeddings of timestep indices (not the raw signal). These time-embeddings are incorporated into two novel pretext tasks, enabling the model to learn a continuous notion of temporal distance instead of the binary positive/negative signal of contrastive learning. Built on TS2Vec's dilated TCN encoder and hierarchical loss framework. Evaluated on anomaly detection, classification, and forecasting; outperforms TS2Vec, TS-TCC, and BTSF on all tasks. Notably more robust to missing data.

## Key results

- Outperforms TS2Vec, TS-TCC, BTSF on anomaly detection (Yahoo + Sepsis), classification (UCR), and forecasting
- Strong robustness to missing data: performs well when 20–50% of timesteps are missing
- Same or smaller latent dimension than baselines, yet higher performance
- Time-embeddings are interpretable: latent space visualisation shows continuous temporal structure
- Evaluated on real-world Sepsis ICU dataset (40,336 patients) — significant practical validation

## Architecture details

- **Time-embedding module** h_ψ: learns τ_t ∈ ℝ^K from timestep index t; output normalised to probability simplex (sigmoid + L1-norm). Architecture: Time2Vec (or MLP) recommended; learned jointly with encoder.
- **Encoder**: dilated TCN (same as TS2Vec); linear projection → time-embedding concat → dilated CNN
- **Pretext task 1 — Time-embedding Divergence Prediction**: given two representations z_{i,t} and z_{j,t'} from different contexts, predict JSD(τ_t || τ_{t'}) — Jensen-Shannon divergence between time-embeddings. Replaces binary contrastive signal with continuous temporal distance.
- **Pretext task 2 — Time-embedding-conditioned Forecasting**: given z_{i,t} and τ_{t+Δ}, predict z_{i,t+Δ} (representation at nearby timestep). Δ ∈ [-Δ_max, Δ_max]; short-range (Δ_max ≤ 20). Backwards + forwards predictions.
- Total loss: linear combination of TS2Vec hierarchical loss + divergence prediction loss + forecasting loss

## Claims

**Claim:** T-Rep is the first SSL method for time series to incorporate learned time-embeddings (from timestep indices) in pretext tasks, producing a continuous notion of temporal distance that replaces the binary positive/negative signal of contrastive learning.
**Evidence:** Fraikin et al. 2024 (ICLR), Section 2 related work: "existing methods have made tremendous progress in extracting spatial features from time series, but temporal feature learning is still limited... not suited to handling recurring patterns (periodic or irregular), and struggle to learn fine-grained temporal dependencies, because of the binary signal and sampling bias of contrastive tasks." T-Rep's divergence prediction task directly addresses this.
**Applicability:** Any TS application where fine-grained temporal structure matters — periodic signals, irregular recurring patterns, finite-state systems. Directly relevant to commodity/energy price TS with seasonal patterns and regime shifts.
**Limitations:** Time-embedding module adds parameters; Time2Vec works well for periodic signals but may not capture all relevant temporal patterns in commodity TS.
**Contradictions:** None identified among current baselines.
**Decision impact:** T-Rep's time-embedding approach is directly applicable to P2. A learnable time-embedding that encodes temporal context (trend, seasonality, regime position) could be incorporated into P2's directed pretext task — the TE/Granger asymmetric objective could be conditioned on time-embeddings to make it regime-aware.
**Confidence:** high

**Claim:** T-Rep's time-embedding-conditioned pretext task produces representations that are significantly more robust to missing data than TS2Vec and TS-TCC, because time-embeddings provide temporal context even when data is absent.
**Evidence:** Fraikin et al. 2024, Table 1 (anomaly detection on Sepsis with missing data); ablation studies in appendix show degradation rate with increasing missingness.
**Applicability:** Industrial TS with sensor dropouts or irregular sampling — common in P4 supply chain event data and P1 commodity data with reporting gaps.
**Limitations:** Only tested up to 50% missingness; above that, time-embeddings alone may not be sufficient.
**Contradictions:** None.
**Decision impact:** P2 and P1 both operate on real-world commodity/price TS with irregular reporting — incorporating time-embeddings for robustness to missing data is a concrete design improvement.
**Confidence:** high

## Applicability to P2

High. T-Rep is still symmetric, but its core innovation — learnable time-embeddings that encode temporal structure in pretext tasks — is directly applicable to P2. Key transfer:
1. Time-embeddings add a continuous temporal context that P2's directed pretext task could condition on (regime-aware TE/Granger labels)
2. JSD divergence prediction is a continuous-signal alternative to binary contrastive loss — the same pattern applies to directed asymmetric signals

## Related

- [src-2026-06-yue-ts2vec](src-2026-06-yue-ts2vec.md) — T-Rep's base architecture
- [src-2026-06-cheng-timemae](src-2026-06-cheng-timemae.md) — alternative encoder for P2 baseline
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
