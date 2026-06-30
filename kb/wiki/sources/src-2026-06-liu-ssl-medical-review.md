---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-liu-ssl-medical-review
tags:
- ssl
- contrastive-learning
- medical-ts
- survey
zotero: liuSelfSupervisedContrastiveLearning2023
source_hash: b9b895e6e5fd0a5d82f1873ec347e7b1c5870e26f597e85c0bf3c1289e626e85
---

# Source: Self-Supervised Contrastive Learning for Medical Time Series: A Systematic Review (2023)

## Metadata
- **Citekey:** `liuSelfSupervisedContrastiveLearning2023`
- **Authors:** Liu, Alavi, Li, Zhang (RMIT / UNC Charlotte)
- **Venue:** Sensors 2023
- **Relevant projects:** P2 (augmentation survey)

## One-line takeaway

Systematic review (PRISMA, 1908 papers screened → 43 reviewed) of contrastive SSL for medical TS (EEG, ECG, ICU vitals) covering augmentation strategies, encoder architectures, contrastive losses, and 51 public datasets.

## Key claims

- Augmentation catalog for dense TS (high-frequency physiological signals): jitter, scaling, permutation, time warping, window slicing, channel dropout, frequency domain perturbations (magnitude/phase), cross-subject mixing.
- Encoder backbone survey: most reviewed papers use Transformer or ResNet/TCN as encoder; recurrent (LSTM) encoders are declining.
- Loss function survey: InfoNCE/NT-Xent dominates; triplet and supervised contrastive losses also common.
- Open challenges: no standard augmentation protocol; domain shift between pretraining and clinical deployment; multi-modal fusion (EEG + ECG simultaneously) under-explored.
- 51 public datasets cataloged with size, sampling rate, and task type.

## Relevance to P2

Augmentation survey is directly transferable to P2's TS SSL design: jitter, scaling, and window slicing are safe augmentations that preserve causal direction (TE/Granger order); cross-subject mixing and permutation destroy temporal structure and should not be used as positive-pair augmentations for P2. Encoder backbone survey confirms Transformer/TCN > LSTM for dense TS — consistent with P2's preference for patch-based encoder (like TimeMAE or TS2Vec). Medical TS findings transfer reasonably well to financial TS (both are dense, multivariate, with temporal dependencies).
