---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-lewis-bart
tags:
- masked-autoencoder
- ssl
- sequence-to-sequence
- background
zotero: lewisBARTDenoisingSequencetoSequence2019
source_hash: c884c393e817e408e581a3ac219263f54e086b0703e0b079e41c2f2e71f63195
---

# Source: BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension (2019)

## Metadata
- **Citekey:** `lewisBARTDenoisingSequencetoSequence2019`
- **Authors:** Lewis, Liu, Goyal, Ghazvininejad, Mohamed, Levy, Stoyanov, Zettlemoyer (Facebook AI)
- **Venue:** ACL 2020
- **Relevant projects:** P2 (generative SSL background)

## One-line takeaway

BART is a denoising seq2seq pretrained model (bidirectional encoder + autoregressive decoder) that generalizes BERT and GPT as special cases and achieves SOTA on text generation, translation, and comprehension — foundational architecture for MAE-style generative SSL in TS.

## Key claims

- Combines bidirectional encoder (like BERT) with autoregressive decoder (like GPT) in a single seq2seq pretraining framework.
- Corruption strategies: token masking (BERT-style), deletion, infilling (arbitrary spans masked to single token), sentence permutation, document rotation.
- Text infilling (mask arbitrary spans → predict) is the most effective single corruption strategy; combining strategies helps further.
- SOTA on summarization (CNN/DM, XSum), dialogue (ConvAI2), question answering (ELI5), and translation (RO-EN) at publication.
- Directly preceded by Ti-MAE and TimeMAE in TS: both adapt BART's masking/denoising pretraining to TS by masking random patches and reconstructing them via a seq2seq encoder–decoder architecture.

## Relevance to P2

Background for P2's generative pretraining stage (MAE backbone). BART establishes that seq2seq denoising pretraining transfers well from pretraining to downstream tasks. The TS adaptations (Ti-MAE, TimeMAE) inherit this design. P2's MAE pretraining stage (recommended by Liu SSL comparison paper) should follow the Ti-MAE/TimeMAE masking protocol (patch-level masking, 60–75% mask ratio), which derives from BART's infilling strategy.
