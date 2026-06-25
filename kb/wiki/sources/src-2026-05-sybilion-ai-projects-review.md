---
type: source
domain: shared
project: shared
status: active
confidence: high
stage: seed
updated: 2026-06-25
sources:
  - src-2026-05-sybilion-ai-projects-review
tags:
  - portfolio
  - strategy
  - p1
  - p2
  - p3
---

# Source: Sybilion AI projects review

> **Upstream origin (consolidated).** This May-2026 deck is the origin of the P1/P2/P3 per-project seed notes and the PX cross-project note. Content pages cite those consolidated notes, not this deck directly; it is retained as the dated origin artifact. P4 has a separate origin (the availability nowcasting report).

Consolidated into: [P1](src-2026-06-p1-cluster-pretrained-deep-models.md) · [P2](src-2026-06-p2-causal-embedding-model.md) · [P3](src-2026-06-p3-scenario-engine.md) · [PX](src-2026-06-px-cross-project-strategy.md).

## Metadata

- Source ID: `src-2026-05-sybilion-ai-projects-review`
- Raw path: `raw/seed/sybilion_ai_projects_review.pptx`
- Source type: strategic project deck
- Date: May 2026
- Relevant projects: P1, P2, P3

## One-line takeaway

The recommended sequencing is to start P3 now, run the P1 cluster-quality gate in parallel, launch P2 as a research thread, and start the full P1 build only after P3 ships and P2 covariate retrieval is validated.

## Project claims

| Project | Claim | Evidence / rationale | Decision impact | Confidence |
|---|---|---|---|---|
| P1 | Cluster-pretrained deep models can eliminate per-SKU analyst tuning at enterprise scale. | The deck frames current hand-tuning as manageable at 10–20 SKUs but breaking at 500–1000 SKUs. | P1 should be judged partly on analyst-time elimination, not only raw accuracy. | medium |
| P1 | Shape clusters may mix different regimes. | The deck names stationarity, seasonality, and heteroscedasticity variance as a core risk. | Run cluster QA before full build. | high |
| P2 | Directed causal embeddings could retrieve high-impact covariates much faster than explicit Granger/TE search. | The deck frames exhaustive TE over 200M series as intractable and proposes distillation into an asymmetric embedding space. | P2 should be run as a research thread with retrieval and downstream validation. | medium |
| P3 | Scenario engine has shortest time-to-value and strongest near-term commercial pull. | Customer interview evidence highlights supplier negotiation blindness, lack of forecast trust, and missed timing windows. | P3 should start first. | high |

## Risks

- P1: cluster quality, PyTorch integration, and uncertain accuracy gain over tuned LGBM.
- P2: asymmetric geometry convergence.
- P3: linear-model ceiling on nonlinear dynamics.

## Open questions

- Who owns the P1 2–3 week cluster-quality experiment?
- Does P2 have a dedicated research owner?
- Should P1 prototype D-Linear and MLP, or commit to one backbone?
- Should M5 and VN2 be part of P1 scope or validation-only?
- Should P3 include Bayesian uncertainty in v1 or defer it?

## Updated pages

- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
- [projects/p3-scenario-engine](../projects/p3-scenario-engine.md)
- [decisions/adr-0001-project-sequencing](../decisions/adr-0001-project-sequencing.md)
- [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md)
