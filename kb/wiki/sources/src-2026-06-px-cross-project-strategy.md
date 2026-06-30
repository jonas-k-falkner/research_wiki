---
type: source
domain: shared
project: shared
status: active
stage: seed
confidence: high
updated: 2026-06-25
sources:
- src-2026-06-px-cross-project-strategy
tags:
- portfolio
- strategy
- sequencing
---

# Source: PX — Cross-project portfolio & strategy

## Metadata

- Source ID: `src-2026-06-px-cross-project-strategy`
- Raw path: `raw/seed/px_cross-project_strategy.md`
- Source type: seed strategy note (cross-project)
- Date: June 2026
- Upstream origin: [src-2026-05-sybilion-ai-projects-review](src-2026-05-sybilion-ai-projects-review.md) (deck Slides 1, 6, 7, 8)
- Relevant projects: shared (P1, P2, P3). P4 is a separate adjacent track, not part of this review.

## One-line takeaway

Start P3 now (fast, low-risk, revenue), run the P1 cluster-quality gate in parallel, launch P2 as a research thread, and begin the full P1 build (~month 4–5) once P3 ships and P2 covariate retrieval is validated.

## Comparison (deck Slide 6)

| Dimension | P1 | P2 | P3 |
|---|---|---|---|
| Technical moat | Very high | Very high | Medium |
| Time to value | 6–10 mo | 6–9 mo | 2–4 mo |
| Execution risk | Medium* | Medium–high | Low |
| Team cost | High | Medium | Low |
| Scalability unlock | Core unlock | Enabler | Indirect |
| Proof | M5, VN2 + 200M TS | TE retrieval accuracy | Client outcomes |

\* reduced by regime sub-clustering. Moat ratings are the proposer's estimate — treat as interested until externally checked.

## Key claims

| Claim | Evidence / rationale | Decision impact | Confidence |
|---|---|---|---|
| P3 should start first. | Shortest TTV, closes top customer pain, activates the CPO PRD. | Sequencing step 1. | high |
| P1 gate runs in parallel (2–3 weeks). | Validates cluster quality before committing engineering bandwidth. | Sequencing step 2. | high |
| P2 runs as a parallel research thread. | De-risks the novel embedding objective without blocking delivery. | Sequencing step 3. | medium |
| P1 full build starts ~month 4–5. | After P3 ships and P2 retrieval is validated. | Sequencing step 4. | medium |

## Coupling

- P3 → P1: surfaces the scaling need (10–20 → 100–1000 SKUs).
- P2 → P1: causal `z_cov` upgrades the covariate-attention layer.
- P1 → P2: cluster forecasting provides downstream validation beyond ranking.

## Open questions

- Gate ownership; P2 research allocation; D-Linear vs MLP; M5/VN2 scope; P3 Bayesian v1-or-v2.

## Updated pages

- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [decisions/adr-0001-project-sequencing](../decisions/adr-0001-project-sequencing.md)
- [overview](../overview.md)
