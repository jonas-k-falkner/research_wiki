---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-jawed-ssl-semisupervised
tags:
- ssl
- self-supervised
- semi-supervised
- multi-task
- forecasting
- time-series
zotero: jawedSelfsupervisedLearningSemisupervised2020
source_hash: 7b3bbdf50ceae4599eb4bdf8d85c8b7c73eda13159bb6371f99484ffc8ac7bff
---

# Self-supervised Learning for Semi-supervised Time Series Classification

**Jawed, Grabocka & Schmidt-Thieme (2020) — ECML PKDD 2020**

## Summary

One of the earliest papers to apply SSL to semi-supervised TS classification. Proposes a multi-task CNN that jointly trains a supervised classification head (on few labeled examples) and a self-supervised forecasting head (auxiliary task on unlabeled data). The forecasting task provides a "free" supervision signal — the model learns features that generalize from forecasting to classification. Evaluated on 13 UCR datasets with only 10% labeled data; outperforms all baselines including shapelet-based SSSL and Π-Model.

## Key results

- Outperforms state-of-the-art SSSL (shapelet-based) on 12/13 UCR datasets with 10% labels
- Hard-parameter sharing between classification and forecasting up to the last layer
- λ controls balance between classification and forecasting loss; needs tuning
- Transfer learning baseline (pretrain on forecasting → freeze → classify) performs worse than joint training
- Π-Model baseline (dropout ensembling) also underperforms the multi-task approach

## Architecture details

- Shared CNN backbone (from Fawaz et al. 2019): 3 conv blocks with batch norm
- Classification head: fully-connected layer → softmax
- Forecasting head: fully-connected layer → horizon h values (multi-step)
- Sliding window function generates forecasting samples with stride s and horizon h
- Joint loss: L_MTL = L_classification + λ × L_forecasting

## Claims

**Claim:** Forecasting-as-auxiliary-task multi-task learning with 10% labels outperforms semi-supervised shapelet learning and Π-Model on 13 UCR datasets (ECML PKDD 2020 baseline).
**Evidence:** Jawed et al. 2020, Table 2. Outperforms SSSL on 12/13 datasets; establishes the value of forecasting as a self-supervised signal for classification.
**Applicability:** Early-stage SSL baseline, circa 2020. Performance significantly exceeded by TS-TCC (2021), TS2Vec (2022), TimeMAE (2023). Still relevant as a design reference for forecasting-as-pretext approaches.
**Limitations:** Pre-contrastive, pre-transformer architecture. Single-task forecasting pretext is weaker than multi-view contrastive learning. Only univariate series.
**Contradictions:** TS-TCC, TS2Vec, TimeMAE all substantially outperform this approach on HAR and UCR benchmarks.
**Decision impact:** Historical baseline only. Confirms that an auxiliary task on unlabeled data (even simple forecasting) provides real signal for downstream classification. P2 is further along — directed TE/Granger distillation is a much stronger signal than next-step forecasting.
**Confidence:** high

## Applicability to P2

Low. 2020 method; outperformed by 2021-2023 SSL baselines. No directed/asymmetric content. Useful only as the earliest reference for using a related auxiliary task (forecasting) to leverage unlabeled TS.

## Related

- [src-2026-06-eldele-ts-tcc](src-2026-06-eldele-ts-tcc.md) — contrastive replacement for this approach
- [src-2026-06-choi-multitask-ssl](src-2026-06-choi-multitask-ssl.md) — modern multi-task SSL
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
