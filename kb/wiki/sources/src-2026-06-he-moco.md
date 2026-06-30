---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-he-moco
tags:
- contrastive-learning
- ssl
- momentum-contrast
zotero: heMomentumContrastUnsupervised2020
source_hash: 52030a3c7f0781e86b419c9ee2282168c6507e6dface349b80a9441e35cd0c6d
---

# Source: Momentum Contrast for Unsupervised Visual Representation Learning (2020)

## Metadata
- **Citekey:** `heMomentumContrastUnsupervised2020`
- **Authors:** He, Fan, Wu, Xie, Girshick (Facebook AI Research)
- **Venue:** CVPR 2020
- **Relevant projects:** P2 (foundational SSL mechanism)

## One-line takeaway

MoCo frames contrastive learning as dictionary look-up with a large dynamic queue + momentum-updated key encoder (m = 0.999 EMA), enabling large and consistent negative dictionaries on 8 GPUs — directly foundational to all TS contrastive SSL methods.

## Key claims

- **Core mechanism:** maintain a FIFO queue of encoded keys (size 65,536 — far larger than any in-batch negative set); key encoder θ_k is updated by momentum: θ_k ← m·θ_k + (1−m)·θ_q (m = 0.999), not by gradient. Current mini-batch is enqueued; oldest is dequeued.
- **Loss:** InfoNCE L_q = −log[exp(q·k₊/τ) / Σᵢ exp(q·kᵢ/τ)] over K+1 keys (1 positive, K negatives from queue).
- **Results:** ImageNet linear classification 60.6% top-1 (vs SimCLR at similar scale needing 256 TPU cores vs MoCo's 8 GPUs). Outperforms supervised ImageNet pretraining on 7/7 downstream detection/segmentation tasks on PASCAL VOC, COCO.
- Queue decouples dictionary size from mini-batch size. Moving-averaged encoder keeps key representations consistent across iterations — the key innovation.
- Directly adopted/adapted by TS-TCC, CA-TCC, Series2Vec, TimeCLR and most TS contrastive methods reviewed in I-P2-A.

## Relevance to P2

MoCo is the standard large-scale contrastive pretraining mechanism behind all TS SSL methods in the P2 baseline set. Two architectural lessons for P2's directed objective: (1) the moving-averaged key encoder (EMA update) is the most stable way to maintain consistent negative representations during training — P2 should use a momentum encoder for the "source" encoder and a gradient-updated encoder for the "target" encoder; (2) queue-based negatives allow a much larger effective batch size, critical when sampling directed (A→B) pairs where positives are sparse (high TE/Granger score) and the negative set must be large to prevent degenerate solutions.
