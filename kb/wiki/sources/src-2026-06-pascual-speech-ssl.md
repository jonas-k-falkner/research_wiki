---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-pascual-speech-ssl
tags:
- ssl
- multi-task
- speech
- background
zotero: pascualLearningProblemagnosticSpeech2019
source_hash: 786e5fa2387ab6e6039b7b0ea090743f2543731cfd6c6592d979f8d1c3f56c8c
---

# Source: Learning Problem-agnostic Speech Representations from Multiple Self-supervised Tasks (2019)

## Metadata
- **Citekey:** `pascualLearningProblemagnosticSpeech2019`
- **Authors:** Pascual, Ravanelli, Serrà, Bonafonte, Bengio
- **Venue:** Interspeech 2019
- **Relevant projects:** P2 (multi-task SSL architecture)

## One-line takeaway

PASE (Problem-Agnostic Speech Encoder): a single convolutional encoder trained simultaneously on multiple self-supervised regression/classification "worker" tasks (waveform autoencoding, MFCC prediction, MFSC prediction, AFDO, ZCR, log-energy, LSTM speech encoding) — foundational for multi-task SSL architectures.

## Key claims

- Architecture: one shared convolutional encoder → multiple task-specific "worker" heads, each predicting a different self-supervised target from the same representation.
- Workers include: waveform autoencoding, MFCC/MFSC prediction, power spectral density, zero-crossing rate, log-energy, and an LSTM-based speaker context predictor.
- Multi-task training learns more general speech representations than any single pretext task alone; evaluated on speaker identification, speech emotion recognition, and speaker verification.
- Precursor to Choi & Kang 2023's multi-task SSL for TS (multi-task SSL paper in I-P2-A MEDIUM batch).

## Relevance to P2

PASE is the speech-domain precursor to multi-task SSL for TS. P2 could adopt a PASE-style architecture: one shared TS encoder + multiple worker heads, where workers include: (1) symmetric reconstruction (MAE), (2) temporal distance prediction (T-Rep style), (3) directed asymmetric similarity prediction (the P2 novel head). Running all three simultaneously may improve encoder generalization compared to training the asymmetric head alone. Background reference; the TS-specific multi-task SSL paper (Choi & Kang 2023) is the more direct reference.
