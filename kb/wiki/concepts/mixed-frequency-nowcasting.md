---
type: concept
domain: nowcasting-graph
project: P4
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p4-availability-nowcasting
tags:
- concept
---

# Mixed-frequency nowcasting

## Definition

A signal-fusion layer that combines inputs arriving at different cadences — slow official statistics, high-frequency event streams, procurement signals, public-text evidence, and structural priors — into a current-state availability score with confidence, using decay and reliability weighting. The report recommends starting with transparent weighted/dynamic-factor scoring before heavy black-box models. See [sources/src-2026-06-p4-availability-nowcasting.md](../sources/src-2026-06-p4-availability-nowcasting.md).

## Why it matters

Availability changes faster than official data is released, so the value is in fusing lagged, irregular, and partially-missing streams in real time — and doing it transparently enough to explain an alert.

## Open research questions

- Weighted scalar score vs dynamic-factor/Kalman state-space — what is the right MVP complexity under tight compute?
- How are reliability weights and decay rates set per source, and how are they calibrated?
- How is score calibration validated against lagged official ground truth without overfitting to known disruption windows?

## Literature to integrate `[verify]`

- MIDAS regressions for mixed-frequency data (Ghysels et al.) `[verify]`
- Dynamic factor models / Kalman-filter nowcasting (Giannone, Reichlin & Small) `[verify]`
- Real-time data and ragged-edge handling in nowcasting `[verify]`

## Cross-project relevance

- Consumes [concepts/evidence-ledger](evidence-ledger.md) signals; calibration methodology shared with [concepts/cpcv-validation](cpcv-validation.md) (P3).

## Related pages

- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
- [domains/nowcasting-graph/thesis](../domains/nowcasting-graph/thesis.md)
