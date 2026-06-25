---
type: decision
domain: shared
project: shared
status: active
confidence: high
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-px-cross-project-strategy
  - src-2026-06-p4-availability-nowcasting
tags:
  - adr
  - sequencing
---

# ADR-0001: Project sequencing

## Status

Proposed / active.

## Context

The portfolio contains three connected forecasting/scenario projects and one adjacent nowcasting/evidence-ledger graph project.

## Decision

1. Start P3 now.
2. Run the P1 cluster-quality gate immediately in parallel.
3. Launch P2 as a research thread alongside P3.
4. Start the full P1 build around month 4–5 only after P3 ships and P2 covariate retrieval has initial validation.
5. Treat P4 as a separate public-first evidence-ledger MVP, not as a full graph-reconstruction effort.

## Evidence

- P3 has the shortest time-to-value and customer evidence.
- P1 is high-value but needs cluster-quality validation before engineering commitment.
- P2 is strategically important but technically uncertain.
- P4 research rejects full graph reconstruction for MVP and recommends a hybrid nowcast plus evidence ledger.

## Consequences

- Near-term engineering effort concentrates on P3 and the P1 gate.
- P2 remains research-heavy and should have an explicit owner.
- P4 should be scoped separately to avoid contaminating P1–P3 with a broad graph-reconstruction project.

## What would change this decision

- P1 gate fails badly and sub-clustering does not fix cluster quality.
- P3 scenario engine fails user trust or actionability tests.
- P2 cannot produce usable directional retrieval.
- P4 identifies a narrow vertical where public-only evidence quality is much higher than expected.
