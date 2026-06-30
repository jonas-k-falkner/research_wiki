---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-zhang-tem-topology
tags:
- transformers
- timeseries-forecasting
- interpretability
- topology
zotero: zhangUnderstandingTokenlevelTopological2025
source_hash: 58821f5063aa17023fde11cc91d2f2ed643c260ab1217403e2a8e331f1e0c1ab
---

# Source: Understanding Token-level Topological Structures in Transformer-based Time Series Forecasting (2025)

## Metadata
- **Citekey:** `zhangUnderstandingTokenlevelTopological2025`
- **Authors:** Zhang, Qiang, Wang, Zhou, Zheng, Xiong (CAS / Peking U / HKUST)
- **Venue:** arXiv 2025
- **Relevant projects:** P1 (backbone interpretability)

## One-line takeaway

Transformer-based TSF models progressively degrade both positional and semantic token topology as depth increases; TEM (Topology Enhancement Method) explicitly preserves both via learnable positional constraints + similarity matrix, improving forecasting accuracy and tightening generalization bounds.

## Key claims

- Empirical finding: positional topology (temporal order of patches) and semantic topology (similarity between patches) both degrade monotonically with Transformer depth — this explains why deeper Transformers don't always improve TSF.
- **TEM** = plug-in module for any Transformer-based TSF model: PTEM (Positional Topology Enhancement Module) injects learnable positional constraints at each intermediate layer; STEM (Semantic Topology Enhancement Module) injects a learnable similarity matrix.
- Theoretical: TEM provably tightens the model's generalization bound (PAC-Bayes bound analysis).
- Plug-and-play: integrating TEM into PatchTST, iTransformer, and other baselines consistently improves MSE/MAE on ETTh1, ETTm1, Weather, Traffic datasets.

## Relevance to P1

P1 uses patch-based Transformer models (TimeXer, iTransformer as candidates). TEM is a drop-in improvement that specifically targets the topology degradation problem in deep Transformers — relevant if P1 uses a deep Transformer backbone. More directly: TEM's finding that Transformers degrade temporal structure at depth is an argument for shallow patch-based models (2–4 layers), consistent with P1's preference for interpretable, compact architectures. Background for P1 backbone selection; not a required implementation.
