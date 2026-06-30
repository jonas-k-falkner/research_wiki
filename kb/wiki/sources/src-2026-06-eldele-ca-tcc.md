---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-eldele-ca-tcc
tags:
- ssl
- self-supervised
- semi-supervised
- contrastive
- time-series
zotero: eldeleSelfsupervisedContrastiveRepresentation2023
source_hash: 35b085f23d057a49e2eed9c9eb56fdfc6c128b3b65acf232ef5aab7bb0c49993
---

# Self-supervised Contrastive Representation Learning for Semi-supervised Time-Series Classification (CA-TCC)

**Eldele et al. (2023) — IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)**

## Summary

Journal extension of TS-TCC (IJCAI 2021). Adds a semi-supervised variant, CA-TCC (ClassAware TS-TCC), that builds on the pretrained TS-TCC encoder with a 4-phase semi-supervised training pipeline: (1) pretrain with TS-TCC on all unlabeled data; (2) fine-tune encoder on few labeled samples; (3) generate pseudo labels for unlabeled data; (4) class-aware contrastive loss using pseudo labels. Also adds a systematic study of TS augmentation selection for contrastive learning. Shows that CA-TCC matches fully supervised training with as few as 1% of labels on multiple benchmark datasets.

## Key results

- CA-TCC with 1% labels matches fully supervised training on HAR dataset
- 10% labels: CA-TCC performance within 1-2% of 100% supervised fine-tuning across all 10 test datasets
- Linear evaluation of TS-TCC encoder (unchanged from IJCAI 2021): HAR 90.37%, Epilepsy 97.23%
- Strong augmentation (permutation+jitter) + temporal contrasting = best combination for TS
- Cross-view prediction (strong→predicts weak future, weak→predicts strong future) is the key tough-task component

## Architecture details

- 3-block CNN encoder (same as IJCAI 2021 version)
- Temporal contrasting: Transformer autoregressive model predicts future timesteps of one augmented view using context of the other (cross-view)
- Contextual contrasting: SimCLR loss on context tokens across views and instances
- CA-TCC extension: class-aware contrastive loss treats same-pseudo-label instances as additional positives, different-label as negatives
- Four-phase semi-supervised: pretrain → fine-tune → pseudo-label → class-aware contrastive

## Claims

**Claim:** CA-TCC semi-supervised training (4-phase: TS-TCC pretrain + pseudo-label + class-aware contrastive) matches fully supervised performance with only 1% of labels on HAR, and is within 1-2% at 10% labels across 10 datasets.
**Evidence:** Eldele et al. 2023 (TPAMI), Table 3-5. CA-TCC with 1% labels vs. fully supervised baseline.
**Applicability:** Any TS domain with abundant unlabeled data and expensive annotation — especially industrial sensor/IoT applications. P2 training scenario matches: abundant unlabeled TS, sparse TE/Granger scores as weak labels.
**Limitations:** Requires a good pretrained encoder first (TS-TCC quality as baseline). Pseudo-labels may reinforce encoder errors in early rounds.
**Contradictions:** TimeMAE (2023) achieves 91.31% linear eval on HAR vs TS-TCC 90.37%, so TS-TCC is no longer SOTA on classification; but CA-TCC's semi-supervised story is different and not directly replicated by TimeMAE.
**Decision impact:** The CA-TCC 4-phase semi-supervised pattern (pretrain on unlabeled → use sparse labels to generate pseudo-labels → class-aware contrastive) maps directly to P2's training scenario. P2 has abundant TS but expensive TE/Granger labels — this phased approach is a reference architecture.
**Confidence:** high

## Applicability to P2

High. The CA-TCC phased semi-supervised framework maps directly to P2's constraint: abundant unlabeled series, expensive pairwise TE/Granger labels, and a need for an encoder that generalises to unlabeled pairs. Replacing class-aware contrastive with a directed asymmetric loss head is the P2 extension.

## Related

- [src-2026-06-eldele-ts-tcc](src-2026-06-eldele-ts-tcc.md) — original IJCAI 2021 version
- [src-2026-06-cheng-timemae](src-2026-06-cheng-timemae.md) — stronger classification encoder
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
