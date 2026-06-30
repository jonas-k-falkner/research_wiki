---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-kazemi-time2vec
tags:
- time-embedding
- ssl
- temporal-representation
source_hash: a3c19a2fae0092b47b7fcf3419e2e63881682538b63e99f840ca1f88ed66398a
---

# Source: Time2Vec: Learning a Vector Representation of Time (2019)

## Metadata
- **Citekey:** `kazemiTime2VecLearningVector2019` (no Zotero library entry)
- **Authors:** Kazemi, Goel, Eghbali, Ramanan, Sahota, Thakur, Wu, Smyth, Poupart, Brubaker (Borealis AI)
- **Venue:** arXiv 2019
- **Relevant projects:** P2 (foundational input), P1 (indirect)

## One-line takeaway

Time2Vec is a model-agnostic, learnable vector representation of time using sine functions with learned frequencies/phase-shifts — capturing periodic and non-periodic temporal patterns — that improves downstream task performance when substituted for raw time features across multiple architectures.

## Key claims

- **Formulation:** t2v(τ)[i] = ωᵢτ + φᵢ for i = 0 (linear); t2v(τ)[i] = F(ωᵢτ + φᵢ) for 1 ≤ i ≤ k, where F = sin, ωᵢ is the learned frequency, φᵢ is the learned phase shift. Period = 2π/ωᵢ.
- Three design properties: (1) captures both periodic and non-periodic patterns (linear + sinusoidal terms), (2) invariant to time rescaling (Proposition 1 proven), (3) simple vector form easily appended to any model input.
- Learning frequencies outperforms fixed frequencies (equal-spaced Fourier or Transformer-style positional encoding) — experiments on synthesized periodic data, Event-MNIST, N-TIDIGITS18, Stack Overflow, Last.FM, CiteULike datasets confirm improvement.
- Model-agnostic: validated by integrating into LSTM, TimeLSTM, and self-attention architectures with consistent performance gains.
- Direct precursor to T-Rep's time-embedding approach (Fraikin et al. 2024), which extends Time2Vec into a divergence-prediction pretext task for TS SSL.

## Relevance to P2

Time2Vec is the foundational architecture behind T-Rep's learned temporal conditioning. P2's directed embedding objective could use a Time2Vec-style component to condition the asymmetric similarity on regime/seasonality — for example, making the TE/Granger label distillation aware of the time epoch (commodity supercycle phase, harvest season, central bank cycle). This is directly applicable to P2's pretext task design: replace raw timestep with t2v(τ) as an auxiliary input to the directed similarity head. See [sources/src-2026-06-fraikin-trep](src-2026-06-fraikin-trep.md) for the T-Rep extension.

## Relevance to P1

Indirect: Time2Vec-style temporal conditioning could enrich P1's cluster-routing step by encoding seasonality and cyclicality directly in the cluster-assignment embedding, rather than relying on raw lag features.
