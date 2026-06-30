---
type: comparison
domain: shared
project: shared
status: active
stage: seed
confidence: medium
updated: 2026-06-27
sources:
- src-2026-06-px-cross-project-strategy
- src-2026-06-p4-availability-nowcasting
- src-2026-06-tsf-literature-review
tags:
- comparison
- portfolio
---

# Portfolio evaluation matrix

Reconstructs the deck's "At a Glance" comparison (Slide 6) as a first-class decision artifact, and adds P4 from the nowcasting report. P1–P3 rows are quoted from [sources/src-2026-06-px-cross-project-strategy](../sources/src-2026-06-px-cross-project-strategy.md); the P4 row is derived from [sources/src-2026-06-p4-availability-nowcasting.md](../sources/src-2026-06-p4-availability-nowcasting.md) and is lower-confidence because it comes from a different source with a different framing.

| Dimension | P1 — Deep cluster models | P2 — Causal embedding | P3 — Scenario engine | P4 — Availability nowcast |
|---|---|---|---|---|
| Technical moat | Very high | Very high | Medium | Medium–high `[derived]` |
| Time to value | 6–10 months | 6–9 months | 2–4 months | ~6–8 week MVP hypothesis |
| Execution risk | Medium | Medium–high | Low | Medium `[derived]` |
| Team cost | High (1 FTE lead) | Medium (research track) | Low (mostly wiring) | Medium `[derived]` |
| Scalability unlock | Core unlock | Enabler | Indirect | New product path `[derived]` |
| Benchmark / proof | M5, VN2 + 200M TS | TE retrieval accuracy | CPCV scenario backtests | Public observable truth (procurement, filings, disruption windows) `[derived]` |

`[derived]` = not in the original six-dimension deck table; inferred from the P4 report and must be revisited when P4 is researched.

## Reading

- P3 is the low-risk, fast, revenue-facing start. P1 is the high-cost core scalability unlock gated on a cheap experiment. P2 is the highest-uncertainty, highest-moat enabler. P4 sits on a different axis — a separate product path, not a rung on the P1–P3 ladder.
- Moat for P1/P2 is rated "very high" **by the deck, which is the proposer** — treat as an interested estimate until externally checked.

## Open research questions

- Are the P1/P2 moat ratings defensible against the current state of pretrained time-series models and causal-discovery tooling? **Partial answer `[verify]`:** a deep-research synthesis ([sources/src-2026-06-tsf-literature-review](../sources/src-2026-06-tsf-literature-review.md)) finds no 2024–2026 paper solves P1's exact combination, giving the first external support for "very high" — but it's a sympathetic secondary synthesis, not a systematic survey, and it notes TSFMs are background rather than a compressor of *this* (covariate-selection) moat. Verify against the named primaries.
- Is P4's "medium–high" moat real, or is the moat actually the evidence-ledger/provenance discipline rather than the nowcast itself?

## Related pages

- [decisions/adr-0001-project-sequencing](../decisions/adr-0001-project-sequencing.md)
- [overview](../overview.md)
