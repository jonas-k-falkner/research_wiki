# PX — Cross-Project Portfolio & Strategy

*Seed source note consolidating the cross-project content of the project deck (Slides 1, 6, 7,
8): the comparison matrix, recommended sequencing, the decision/recommended path, and the
open questions. This is the portfolio-strategy layer that sits above the per-project notes
(P1 cluster models, P2 causal embedding, P3 scenario engine). Faithful to the deck;
"Sybilion · May 2026". P4 (availability nowcasting) is a separate adjacent track and is **not**
part of this three-project review.*

---

## Framing

Strategic Technology Investment Review — three projects evaluated across **scalability, moat,
and time-to-value**:

- **P1 — Cluster-pretrained deep models**
- **P2 — Causal embedding v2**
- **P3 — Mathematical scenario engine**

---

## At a Glance — Evaluation Across Six Dimensions (Slide 6)

| Dimension | P1 Deep cluster models | P2 Causal embedding | P3 Scenario engine |
|---|---|---|---|
| Technical moat | Very high | Very high | Medium |
| Time to value | 6–10 months | 6–9 months | 2–4 months |
| Execution risk | Medium* | Medium–high | Low |
| Team cost | High | Medium | Low |
| Scalability unlock | Core unlock | Enabler | Indirect |
| Benchmark / proof | M5, VN2 + 200M TS | TE retrieval accuracy | Client outcomes |

\* P1 execution risk reduced significantly: sub-clustering by regime handles the shape ≠ regime
cases, and the 200M series are the training pool.

Reading: P3 is the low-risk, fast, revenue-facing start; P1 is the high-cost **core
scalability unlock**; P2 is the highest-uncertainty, highest-moat **enabler**. Moat ratings
for P1/P2 are the proposer's estimate — treat as interested until externally checked.

---

## Recommended Sequencing (Slide 7)

Timeline (Now → ~M10):

- **P3 — Scenario engine**: starts now.
- **P2 — Causal embedding**: starts now as a *research thread*.
- **P1 — Gate experiment**: early, in parallel (2–3 weeks).
- **P1 — Cluster deep models (full build)**: starts ~M4–5, runs to ~M10.

How the three reinforce each other:

- **P3 → P1 (surfaces the scaling need).** P3 proves value at 10–20 SKUs per client. As clients
  grow to 100–1000 SKUs, the analyst bottleneck becomes the hard constraint — P1 is the
  answer. P3 creates the commercial pressure that justifies P1.
- **P2 → P1 (covariate layer upgrade).** P1 built with DTW-symmetric covariate embeddings is
  good; P1 built with P2's causal embeddings (where `z_cov` encodes directed influence) is
  materially better. P2 ships as a research thread first; P1's full build starts when P2's
  covariate retrieval is validated.
- **P1 → P2 (downstream validation).** P2 needs a forecasting task to evaluate against beyond
  ranking metrics. P1's cluster model provides exactly that: did causal covariate retrieval
  improve cluster-model accuracy on held-out series? Cleaner than ranking-only evaluation.

---

## Decision — Recommended Path (Slide 8)

1. **Start P3 now.** Ships in 2–4 months, closes top customer pain, activates the CPO's
   priority PRD (Cost Model Forecast).
2. **Run the P1 gate experiment in parallel** (2–3 weeks). Validates cluster quality before
   committing engineering bandwidth.
3. **Launch P2 as a research thread** alongside P3 — one researcher, distillation approach.
   De-risks the novel embedding objective without blocking delivery.
4. **P1 full build starts ~month 4–5**, once P3 ships and P2's covariate retrieval is
   validated. Launches with the full causal covariate mechanism.

---

## Open Questions for Discussion (Slide 8)

- **P1 cluster quality** — run the gate experiment before committing, or is discussion enough?
  Who owns the 2–3 week experiment?
- **P2 research allocation** — is there a dedicated researcher to own the causal embedding
  objective as a parallel track, or does it wait until P3 ships?
- **P1 architecture** — D-Linear vs MLP backbone: prototype both on a single cluster and
  compare, or commit to one upfront?
- **Benchmark strategy** — target M5 and VN2 as part of P1 scope, or treat as validation-only?
  A strong VN2 result would be a meaningful external signal.
- **P3 scope boundary** — ship the Bayesian uncertainty layer in v1, or defer to v2 after
  validating the deterministic scenario re-run first? *(Note: deck is internally inconsistent —
  Slide 5 lists Bayesian under "what ships", Slide 8 lists it as open. Treat as open.)*

---

## Coupling Summary

```
P3 (revenue, now) ──surfaces scaling need──▶ P1 (core unlock)
P2 (enabler) ──causal z_cov covariate layer──▶ P1
P1 ──downstream forecasting validation──▶ P2
```

P3 funds attention and proves the commercial case; P2 de-risks the covariate moat in parallel;
P1 is the capital-intensive core build that both lead into.
