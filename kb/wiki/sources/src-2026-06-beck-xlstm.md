---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-beck-xlstm
tags:
- ssm
- lstm
- timeseries-forecasting
- embedding-architecture
zotero: beckXLSTMExtendedLong2024
source_hash: 8cfe1b57d0ab668a7ea82d05e1ce0d962cbf19cf9f05f3b440510555dc3370e6
---

# Source: xLSTM: Extended Long Short-Term Memory (2024)

## Metadata
- **Citekey:** `beckXLSTMExtendedLong2024`
- **Authors:** Beck, Pöppel, Spanring, Auer, Prudnikova, Kopp, Klambauer, Brandstetter, Hochreiter
- **Venue:** NeurIPS 2024 (ELLIS Unit / JKU Linz)
- **Relevant projects:** P1 (backbone candidate), P2 (architecture input)

## One-line takeaway

xLSTM's mLSTM cell uses a matrix memory with a key–value covariance update rule — making it a fully parallelizable associative memory that is directly architecturally relevant to P2's directed embedding design, and a viable future P1 backbone for non-stationary price series.

## Key claims

- xLSTM introduces two new cells: **sLSTM** (scalar memory, exponential gating, memory mixing) and **mLSTM** (matrix memory C ∈ ℝ^{d×d}, fully parallelizable covariance update C_t = f_t · C_{t-1} + i_t · v_t · k_t^T, output h_t = o_t ⊙ (C_t · q_t / max(|n_t^T · q_t|, 1))).
- mLSTM maps input to query q, key k, value v — forming an explicit key–value associative recall mechanism. Benchmark: multi-query associative recall (256 KV pairs, context 2048), xLSTM[1:1] outperforms all non-Transformer models including Mamba, RWKV-5/6.
- xLSTM performs "favorably when compared to state-of-the-art Transformers and State Space Models, both in performance and scaling" on language modeling (15B and 300B token SlimPajama runs, up to 1.3B params).
- Linear computation + constant memory complexity w.r.t. sequence length (unlike quadratic attention). "xLSTM has the potential to considerably impact other deep learning fields like Reinforcement Learning, **Time Series Prediction**, or the modeling of physical systems."
- No direct TSF evaluation in this paper; derivative work TiRex (Auer et al. 2025, citekey: `auerTiRexZeroShotForecasting2025`) demonstrates xLSTM-backed zero-shot TSF beating Chronos, TimesFM, Moirai.

## Relevance to P1

mLSTM is a competitive alternative backbone for P1's price series encoder: linear complexity (vs quadratic attention), state-tracking capability that Transformers lack (Merrill et al. 2024), and non-stationary sequence handling. Current P1 architecture uses NBEATSx/TimeXer (MLP/attention); xLSTM could become a drop-in encoder for the cluster-routing preprocessing step or replace the backbone in the high-volatility cluster where regime-switching matters. Block to adopt: start with TiRex benchmark on EPF/commodity data before replacing the P1 backbone.

## Relevance to P2

mLSTM's explicit key–value associative memory (q, k, v projection → matrix memory retrieval) is architecturally analogous to the directed embedding P2 requires: a query series retrieves high-influence key–value pairs. Design input: mLSTM's covariance update C_t = f_t · C_{t-1} + i_t · v_t · k_t^T is a sequential version of the bilinear similarity P2 needs for A→B ≠ B→A objectives. The mLSTM mechanism confirms that asymmetric key–value memories can be trained end-to-end with gradient descent.
