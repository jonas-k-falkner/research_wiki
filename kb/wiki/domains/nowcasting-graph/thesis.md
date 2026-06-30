---
type: domain
domain: nowcasting-graph
project: P4
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p4-availability-nowcasting
tags:
- thesis
- nowcasting
- graph
---

# Domain thesis: Nowcasting graph

## Current thesis

The best MVP is a public-first, evidence-ledger-centered nowcast system. It should estimate availability for category × region and supplier × category views using provenance-backed evidence and mixed-frequency signal fusion.

## Rejected MVP thesis

A full reconstructed global supply-chain graph is not the right first build. The binding constraints are public input sparsity, hidden-edge uncertainty, entity resolution, and benchmark construction rather than graph-model sophistication.

## Architecture principle

The evidence ledger is the source of truth. The graph is a structured view used for propagation, explanation, and analyst queries.

## Validation stance

The system should be evaluated against public observable truth: procurement awards, SEC supplier/customer mentions, public company pages, known disruption windows, and lagged official data. It should not be penalized for hidden private-tier relationships that are not publicly observable.

## Sources & related

- [sources/src-2026-06-p4-availability-nowcasting.md](../../sources/src-2026-06-p4-availability-nowcasting.md)
- Project: [projects/p4-availability-nowcasting-graph](../../projects/p4-availability-nowcasting-graph.md)
