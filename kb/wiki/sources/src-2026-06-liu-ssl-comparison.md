---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-liu-ssl-comparison
tags:
- ssl
- contrastive-learning
- masked-autoencoder
- timeseries
zotero: liuSelfSupervisedLearningTime2024
source_hash: 9969ab07aad2cd21d680600f38e4cca9811769c959d4b1c93a8c49500e70c41e
---

# Source: Self-Supervised Learning for Time Series: Contrastive or Generative? (2024)

## Metadata
- **Citekey:** `liuSelfSupervisedLearningTime2024`
- **Authors:** Liu, Hu, Liu, Zheng, Ma, Shu (DL4mHealth group)
- **Venue:** arXiv 2024
- **Relevant projects:** P2 (pretraining objective selection)

## One-line takeaway

In a controlled SimCLR vs MAE comparison on TS classification, contrastive (SimCLR) wins when label ratio > 0.5 and MAE wins in the very sparse label regime (< 100 samples/class, ratio < 0.1); MAE is also 25.6% faster to pretrain.

## Key claims

- Both pretraining methods consistently improve over no pretraining by ~2% F1 at label ratio 0.1, regardless of method.
- **SimCLR vs MAE crossover:** MAE outperforms SimCLR at label ratio ≤ 0.1 (e.g., 5.53% F1 gap at label ratio 0.01); SimCLR outperforms MAE at label ratio ≥ 0.5.
- Convergence: SimCLR converges faster (>60% F1 in first few epochs at label ratio 0.1); MAE eventually matches or surpasses.
- Pretraining time at HAR dataset: MAE = 754s, SimCLR = 1016s — MAE is ~25.6% faster.
- Practical recommendation from paper: "if dataset is substantial and performance comparable, recommend generative (MAE) to save time without compromising performance."
- Code/data public: github.com/DL4mHealth/SSL_Comparison.

## Relevance to P2

Directly answers the P2 pretraining objective question. P2's TE/Granger labels are expensive → sparse label scenario → MAE-style generative pretraining is the preferred backbone. Specifically: (1) pretrain a MAE encoder on the full unlabeled TS corpus; (2) fine-tune the directed asymmetric head using sparse TE/Granger labels. The crossover at label ratio 0.5 means if P2 can annotate >50% of pairs with TE scores (unlikely at 200M scale), switch to SimCLR. At realistic annotation budgets (<<10%), MAE is the right pretraining stage. This paper does not evaluate an asymmetric/directed objective; P2 novelty gap remains confirmed.
