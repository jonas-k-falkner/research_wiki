---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-ericsson-ssl-survey
tags:
- ssl
- survey
- contrastive-learning
zotero: ericssonSelfSupervisedRepresentationLearning2022
source_hash: b8d47c7b8086371c4145a53f822f760cd3ea21623f9b14ed1736670aed9af49a
---

# Source: Self-Supervised Representation Learning: Introduction, Advances and Challenges (2022)

## Metadata
- **Citekey:** `ericssonSelfSupervisedRepresentationLearning2022`
- **Authors:** Ericsson, Gouk, Loy, Hospedales
- **Venue:** IEEE Signal Processing Magazine 2022
- **Relevant projects:** P2 (SSL landscape reference)

## One-line takeaway

Comprehensive survey of discriminative SSL across image, video, speech, text, and graph modalities — four families of approach (contrastive instance discrimination, predictive/masked modeling, multi-view/multi-modal, clustering-based) — with practical guidance on transfer, compute, and deployment.

## Key claims

- Covers SimCLR, MoCo, BYOL, DINO, BERT, MAE, wav2vec, and graph SSL in a unified framework.
- SSL performance follows a log-scaling law with unlabeled pretraining dataset size — suggests larger unlabeled TS corpora will improve P2 representations for free as data accumulates.
- Four SSL families: (1) contrastive instance discrimination (SimCLR, MoCo), (2) self-distillation / no-negatives (BYOL, DINO), (3) predictive/masked modeling (BERT, MAE), (4) clustering (SwAV, DeepCluster).
- Practical finding: representation transferability is higher when pretraining domain matches downstream domain (in-domain > cross-domain for most modalities).
- Augmentation design is the most critical factor for contrastive methods; the invariances encoded by augmentations determine what the encoder learns.

## Relevance to P2

Reference survey for P2's SSL pretraining design. Key takeaway: (1) in-domain pretraining corpus is essential (confirmed for TS by Eldele 2024 survey); (2) augmentation design is the most impactful design choice — P2 should develop TS-specific augmentations that preserve directional signal (e.g., phase shifts, amplitude scaling) without destroying the TE/Granger label ordering; (3) no-negatives methods (BYOL/DINO) as an alternative when constructing large negative queues is difficult. The survey does not cover asymmetric/directed objectives.
