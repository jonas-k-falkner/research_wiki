---
type: shared
domain: shared
project: shared
status: active
stage: seed
confidence: high
updated: 2026-06-25
sources:
- src-2026-06-px-cross-project-strategy
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-p4-availability-nowcasting
tags:
- log
---

# Log

## 2026-06-22

- Ingested `raw/seed/sybilion_ai_projects_review.pptx` as P1–P3 strategic project source.
- Ingested `raw/seed/p1_cluster-pretrained_deep-models.md` as P1/P2 sparse covariate-selection design note.
- Ingested `raw/seed/p4_availability_nowcasting.md` as P4 nowcasting/evidence-ledger graph source.
- Created four project pages: P1, P2, P3, P4.
- Created four domain thesis pages.
- Created shared project map, evaluation strategy, risks/caveats, and open questions.
- Created ADR-0001 for project sequencing.
- Created initial experiment pages for P1–P4.
- Updated `CLAUDE.md` to reflect the four-project wiki structure.

### Needs review

- Confirm whether P4 should be a first-class project track or a research-adjacent domain.
- Confirm whether P3 Bayesian uncertainty is v1 or v2.
- Assign owners for P1 cluster-quality gate and P2 causal embedding research.

## 2026-06-22 (lint + seed-hardening pass)

Ran the `CLAUDE.md` lint workflow against the initial ingest and fixed structural/depth issues, keeping everything explicitly at **seed** stage (scaffold for later literature research, not final scope).

### Lint findings

- Concept pages carried identical boilerplate ("Current view" / "Decision impact") — violated the no-generic-summaries rule.
- Experiment pages were stubs ("Protocol: TBD", identical failure modes); the P1 gate protocol present in the source deck (Slide 3) was under-extracted.
- Source pages were dead-ends (0 inbound links) — provenance trail unwalkable.
- One concept page (`cluster-pretrained-deep-models`) was a true orphan, not linked from its own project.
- Contradiction/superseded machinery unused despite the schema; the P3 Bayesian v1/v2 source-internal inconsistency was silently smoothed.
- Missing structures the schema declares: no comparison page (despite the deck's six-dimension matrix), no entities, no research backlog.
- Corpus gap: production-repo context not ingested, so architecture claims (Model ABC, determinism) can't be checked.
- `confidence` near-uniform `medium` and decorative; B2B source page missing `Date`.

### Fixes applied

- Added a **maturity model** (`seed`/`researched`/`validated`) and a `stage:` frontmatter field on every page; all pages marked `stage: seed`.
- Rewrote all **8 concept pages**: real definitions, "Open research questions", "Literature to integrate" (candidate methods marked `[verify]`), cross-project relevance, inline source links.
- Rewrote all **4 experiment pages**: extracted real protocols (P1 gate now carries the full Slide-3 protocol + low/high-variance decision rule), project-specific failure modes, metrics, `[seed gaps]` to specify, research hooks.
- Fixed provenance: project/domain pages now link their **source pages inline** (sources went from 0 inbound to 11/7/5).
- Recorded contradictions: P3 Bayesian v1/v2 (source-internal); P1 determinism-vs-MC-dropout (cross-layer, pending repo ingest).
- Created `comparisons/portfolio-evaluation.md` (deck matrix + derived P4 row), `entities/p4-public-data-sources.md`, and `shared/research-backlog.md` (planned literature + internal sources + known tensions + contradiction status).
- Added numbering crosswalk to `overview.md`; seed banners on `index.md`/`overview.md`; added `Date` to the B2B source page.
- Verified: **0 broken wikilinks**; only `index.md`/`log.md` remain without inbound links (correct — they are nav roots).

### Still open (for the research pass, tracked in [shared/research-backlog](shared/research-backlog.md))

- Attach real citations to every `[verify]` item; promote pages `seed → researched`.
- Ingest `forecast_pipeline` / `embedding_model` / deployment / product context to ground architecture claims and resolve the determinism carve-out.
- Set numeric thresholds for the P1 gate; assign experiment owners.

## 2026-06-25 (finalize — source layer + ref sync)

Finalized the seed KB as a clean starting point for the research pass.

### Structure & sources
- Reconciled `wiki/sources/` with the five-note `raw/seed/` corpus. Source pages now: P1, P2,
  P3, P4, PX — one per seed note. Created P2, P3, PX; rewrote P1 (now consolidates the cluster
  models + the gaze covariate-selection content); renamed P4.
- The May-2026 deck is retained as the **upstream origin** (`src-2026-05-...`), consolidated
  into the five notes and no longer cited directly by content pages.
- Fixed the malformed `src-2026-06-p4.md` source ID (dropped the `.md`).

### Reference remap (deterministic, by project)
- `gaze` → P1 source (content folded into the P1 note).
- deck → per-project source (P1/P2/P3) or PX (shared); `src-2026-06-p4(.md)` → P4 source.
- Applied to frontmatter `sources:` and inline links; deduped sources lists.

### Verification
- 0 broken Markdown links; 0 orphan pages (only `index.md`/`log.md` nav roots lack inbound).
- Source IDs consistent across all pages; `updated` bumped to 2026-06-25.
- Added `raw/seed/README.md`; updated `CLAUDE.md` corpus + structure; updated `index.md`
  source summaries.

### Still seed-stage (for the research pass)
- All pages remain `stage: seed`; `[verify]` literature unattached; production-repo context
  (`forecast_pipeline`, `embedding_model`) not yet ingested — tracked in
  [shared/research-backlog](shared/research-backlog.md).

## 2026-06-27 (ingest — TSF literature review, deep-research synthesis)

Ingested a deep-research synthesis of 2024–2026 time-series forecasting literature, read against P1.

### Provenance call (important)
- Classified as a **secondary synthesis, `[verify]`-tier**: it names real primaries (TimeXer, Channel Clustering, DUET, ChronosX, UniCA, ApolloPFN, CATS-ATS, CauAir, …) but **carries no resolvable citations**. Ingest did **not** promote any page `seed → researched`. Pages remain `seed`; all added claims are attributed to the synthesis and marked `[verify]` against the named primaries.

### Added
- `raw/research/deep-forecaster-tsf-review-2026.md` (new `raw/research/` bucket).
- Source page `sources/src-2026-06-tsf-literature-review.md` with explicit evidence-tier framing.

### Distilled into
- `concepts/cluster-pretrained-deep-models` — Channel Clustering → DUET as best-supported lineage; "simple backbone, spend budget on selector"; no residual bypass.
- `concepts/hierarchical-entmax-covariate-selection` — calibration: entmax support in TSF is **adjacent, not direct** (seed note overstated it); cluster-level attribution is an open opportunity.
- `concepts/causal-covariate-embeddings` — TimeXer validates asymmetric target/covariate modeling; shared-encoder-for-target-conditioned-routing is unmatched (novelty point).
- `domains/timeseries-forecasting/thesis` — two-stream framing; TSFMs are background, not center. (Also fixed a duplicated source link.)
- `projects/p1-cluster-pretrained-deep-models` — external-literature positioning; **moat tension updated with first non-self-assessed support** (no 2024–2026 paper solves P1's exact combination), caveated as sympathetic secondary synthesis. (Also fixed a duplicated source link.)
- `comparisons/portfolio-evaluation` — partial answer to the P1/P2 moat question.
- `shared/research-backlog` — P1/P2 literature rows upgraded from vague areas to **named, venue-tagged primaries**; logged as a completed deep-research step.

### Next (tracked in research-backlog)
- Export the named primaries from Zotero into `raw/literature/`, then verify each claim against the primary source before any `seed → researched` promotion.

## 2026-06-29 (I-P1-A — P1 primary literature ingest, 12 papers)

Completed Task I-P1-A: ingested 12 academic papers on time-series clustering and forecasting into the wiki. All papers confirmed `state: new` (no pre-existing source pages). All 5 open research questions on `concepts/cluster-pretrained-deep-models` answered with high confidence from primaries; page promoted `seed → researched`.

### Source pages created (12)

| Source slug | Paper | Venue | Priority |
|---|---|---|---|
| `src-2026-06-chen-channel-clustering` | Chen et al., CCM | NeurIPS 2024 | HIGH |
| `src-2026-06-qiu-duet-clustering` | Qiu et al., DUET | KDD 2025 | HIGH |
| `src-2026-06-aghabozorgi-ts-clustering-survey` | Aghabozorgi et al., TS clustering survey | Inf. Systems 2015 | HIGH |
| `src-2026-06-petitjean-dtw-barycenter` | Petitjean et al., DBA | Pattern Recog. 2011 | MEDIUM |
| `src-2026-06-petitjean-faster-dtw` | Petitjean et al., NCC-DTW | IEEE TKDE 2016 | MEDIUM |
| `src-2026-06-bagnall-ts-bakeoff` | Bagnall et al., TS Bake-off | DAMI 2017 | MEDIUM |
| `src-2026-06-sen-global-local-forecasting` | Sen et al., DeepGLO | NeurIPS 2019 | MEDIUM |
| `src-2026-06-ruta-sax-navigator` | Ruta et al., SAX Navigator | — 2019 | LOW |
| `src-2026-06-keogh-parameter-free-ts` | Keogh et al., CDM | KDD 2004 | LOW |
| `src-2026-06-lucas-proximity-forest` | Lucas et al., Proximity Forest | DMKD 2019 | LOW |
| `src-2026-06-wang-ts-classification-cnn` | Wang et al., FCN/ResNet | IJCNN 2017 | LOW |
| `src-2026-06-ismail-benchmarking-dl-ts` | Ismail Fawaz et al., InceptionTime | NeurIPS — | LOW |

### Research questions answered

1. **Does CCM show clustering channels improves accuracy?** Yes — CCM: +2.4%/+7.2% MSE reduction (NeurIPS 2024); DUET: +7.1% over SOTA (KDD 2025). Clustering criterion: RBF on standardized values (CCM) / learnable Mahalanobis in frequency space (DUET).
2. **What does DUET add over CCM?** Temporal distribution clustering (TCM, MoE-style VAE gating) + channel soft-clustering via sparse binary mask matrix; clustering separated from routing via masked attention. No zero-shot capability (gap vs. CCM and P1).
3. **Shape similarity vs. regime consistency?** Literature treats them as distinct similarity types (Aghabozorgi 2015: time/shape/structural). DUET's TCM is closer to regime clustering; CCM/DBA are shape-based. Neither validates cross-overlap. Experiment required.
4. **Cluster quality metrics?** SSE and Silhouette index (internal); Petitjean 2011 uses WGSS (SSE under DTW) as DTW-native analog. Standard consensus from Aghabozorgi 2015.
5. **Global vs. local model debate?** DeepGLO (Sen 2019): hybrid global+local > either extreme on 115K-series dataset. Cluster model = global; few-shot fold-in = local. Pure per-series models not recommended at P1 scale.

### Concept page updated

- `concepts/cluster-pretrained-deep-models.md`: promoted `seed → researched`; confidence `medium → high`; 12 new source slugs added to frontmatter; all `[verify]` markers removed; full "Primary literature findings" section added with five research question answers.

### Claim deduplication

Ran `wiki check claim` on 5 key claims — all novel (no duplicates). DuckDB lock from background process caused graceful degradation to lexical fallback; no data loss.

### Next

- Verify `ismail-benchmarking-dl-ts` citekey against `library.json` (citekey mismatch warning).
- Run `exp-p1-cluster-quality-gate` experiment to test shape vs. regime cluster overlap on P1 demand data.
- Investigate DUET's zero-shot gap: can CCM's prototype routing be adapted for P1's new-SKU onboarding?

## 2026-06-29 (I-P1-B — sparse attention and faithfulness literature ingest, 16 papers)

Completed Task I-P1-B: ingested 16 academic papers on sparse attention (α-entmax), covariate selection, attention faithfulness, and post-hoc attribution methods. All 16 confirmed `state: new` before ingest. Concept page `hierarchical-entmax-covariate-selection` promoted `seed → researched`; new concept page `attention-faithfulness` created.

### Source pages created (16)

| Source slug | Paper | Venue | Priority |
|---|---|---|---|
| `src-2026-06-peters-sparse-seq2seq-2019` | Peters et al., Sparse Seq2Seq (α-entmax) | ACL 2019 | HIGH |
| `src-2026-06-jain-attention-not-explanation-2019` | Jain & Wallace, Attention is Not Explanation | NAACL 2019 | HIGH |
| `src-2026-06-wiegreffe-attention-not-not-2019` | Wiegreffe & Pinter, Attention is not not Explanation | EMNLP 2019 | HIGH |
| `src-2026-06-lim-tft-2021` | Lim et al., Temporal Fusion Transformers | Int. J. Forecasting 2021 | HIGH |
| `src-2026-06-lundberg-shap-2017` | Lundberg & Lee, SHAP | NeurIPS 2017 | HIGH |
| `src-2026-06-sundararajan-integrated-gradients-2017` | Sundararajan et al., Integrated Gradients | ICML 2017 | HIGH |
| `src-2026-06-liu-rethinking-attention-explainability-2022` | Liu et al., Faithfulness Violation Test | ICML 2022 | HIGH |
| `src-2026-06-bastings-elephant-interpretability-2020` | Bastings & Filippova, Elephant in Interpretability | BlackboxNLP 2020 | MEDIUM |
| `src-2026-06-bibal-attention-explanation-survey-2022` | Bibal et al., Is Attention Explanation? (survey) | ACL 2022 | MEDIUM |
| `src-2026-06-rojat-xai-timeseries-2021` | Rojat et al., XAI on Time Series (survey) | arXiv 2021 | MEDIUM |
| `src-2026-06-lou-sparsek-attention-2024` | Lou et al., SPARSEK Attention | arXiv 2024 | LOW |
| `src-2026-06-tay-sparse-sinkhorn-attention-2020` | Tay et al., Sparse Sinkhorn Attention | ICML 2020 | LOW |
| `src-2026-06-tezekbayev-alpha-relu-2022` | Tezekbayev et al., Speeding Up Entmax (α-ReLU) | arXiv 2022 | LOW |
| `src-2026-06-zhao-sparse-transformer-2019` | Zhao et al., Sparse Transformer (top-k) | arXiv 2019 | LOW |
| `src-2026-06-yasuda-sequential-attention-2023` | Yasuda et al., Sequential Attention | ICLR 2023 | LOW |
| `src-2026-06-sokar-wast-feature-selection-2022` | Sokar et al., WAST | NeurIPS 2022 | LOW |

### Research questions answered

1. **Peters et al. (1.5-entmax sweet spot):** 1.5-entmax outperforms softmax (BLEU 26.17 vs 25.70, DE→EN) and sparsemax (24.69); reduces average non-zero attention from 24.25 to 5.55. Exact O(d log d) bisection algorithm; near-softmax GPU speed.
2. **Jain/Wiegreffe faithfulness debate:** Practical consensus reached — raw attention weights are insufficient (violation ratios 0.31–0.40); AttGrad (attention × gradient) reduces violations to 0.02–0.06 (Liu et al. 2022). Task-dependent: Wiegreffe & Pinter show validation required per dataset.
3. **TFT variable selection:** Uses standard Softmax, not sparsemax. Removing VSN increases P90 loss by 4.1%. Shared-value multi-head attention for temporal interpretation. Direct comparison baseline for P1.
4. **SHAP vs Integrated Gradients:** Kernel SHAP — model-agnostic, no gradients, treats features independently (temporal ordering gap). IG — requires gradients, 20–300 evaluations, Completeness axiom. Both are offline validation tools, not real-time explanation. Neither handles temporal structure natively.
5. **Liu et al. faithfulness violation test:** Polarity consistency (not just importance correlation) is the key criterion. AttGrad recommended. Deeper architectures → more violations. Applicable as P1 model quality metric alongside forecasting loss.

### Concept pages updated/created

- `concepts/hierarchical-entmax-covariate-selection.md`: promoted `seed → researched`; confidence `medium → high`; 16 new source slugs added; all `[verify]` markers replaced with primary citations; full literature sections added (α-entmax mechanism, TFT baseline, faithfulness debate, post-hoc alternatives, Sequential Attention, open research questions updated).
- `concepts/attention-faithfulness.md`: **created** (new concept page); stage `researched`; documents the 2019–2022 debate arc, practical consensus table, and P1 implications. Referenced from hierarchical-entmax concept page and all 5 faithfulness source pages.

### Claim deduplication

All `wiki check claim` calls returned "no similar claims found" — all claims novel. DuckDB lock caused graceful degradation to lexical search; no data loss.

### Lint / TOC

- `uv run wiki lint`: 0 errors, 22 warnings (all pre-existing: library.json mismatches, near-duplicate titles from existing pages, stage/confidence sanity from pre-I-P1-B pages).
- `uv run wiki toc build`: indexes updated.

### Next

- Validate AttGrad polarity consistency on P1 pilot dataset once model training is running.
- Compare α-entmax vs α-ReLU speed on covariate routing layer in ablation.
- Consider Sequential Attention (Yasuda 2023) as redundancy-aware alternative to flat entmax routing.
- Add `yasudaSequentialAttentionFeature2023`, `tezekbayevSpeedingEntmax2022`, `sokarWherePayAttention2022` to `library.json` to resolve citekey warnings.

- **I-P1-D** (SSM background): Created 15 brief source pages for SSM/linear-RNN architectures (Mamba, S-Mamba, SiMBA, Mamba-2, xLSTM, RWKV, Eagle/Finch, HGRN, HGRN2, GLA, Gated Delta Networks, Longhorn, TTT, GSA, Jamba). Added background paragraph to timeseries-forecasting/thesis.md.

## 2026-06-29 (I-P1-C — TSF backbone landscape and covariate adapter ingest, 19 papers)

Completed Task I-P1-C: ingested 19 academic papers covering TSF backbone architectures (DLinear, N-BEATS, N-HiTS, NBEATSx, Autoformer, TimesNet, TimeMixer++, TTM, TiRex) and covariate adapter models (ChronosX, UNICA, ApolloPFN, CATS-ATS, TimeXer). All 19 confirmed `state: new` before ingest. All `wiki check claim` calls returned novel. `domains/timeseries-forecasting/thesis.md` promoted `seed → researched`.

### Source pages created (19)

| Source slug | Paper | Priority |
|---|---|---|
| `src-2026-06-zeng-dlinear` | Zeng et al., DLinear (AAAI 2023) | HIGH |
| `src-2026-06-oreshkin-nbeats` | Oreshkin et al., N-BEATS (ICLR 2020) | HIGH |
| `src-2026-06-challu-nhits` | Challu et al., N-HiTS (AAAI 2023) | HIGH |
| `src-2026-06-wang-timexer` | Wang et al., TimeXer (NeurIPS 2024) | HIGH |
| `src-2026-06-arango-chronosx` | Arango et al., ChronosX (2025) | HIGH |
| `src-2026-06-han-unica` | Han et al., UNICA (2026) | HIGH |
| `src-2026-06-potapczinski-apollopfn` | Potapczinski et al., ApolloPFN (2026) | HIGH |
| `src-2026-06-lu-cats-ats` | Lu et al., CATS-ATS (ICML 2024) | HIGH |
| `src-2026-06-chen-closer-look-transformers` | Chen et al., Closer Look (2025) | HIGH |
| `src-2026-06-wang-timemixer` | Wang et al., TimeMixer++ (2024) | MEDIUM |
| `src-2026-06-ekambaram-ttm` | Ekambaram et al., TTM (2024) | MEDIUM |
| `src-2026-06-olivares-nbeatsx` | Olivares et al., NBEATSx (2023) | MEDIUM |
| `src-2026-06-wu-autoformer` | Wu et al., Autoformer (NeurIPS 2021) | MEDIUM |
| `src-2026-06-auer-tirex` | Auer et al., TiRex (2025) | MEDIUM |
| `src-2026-06-wu-timesnet` | Wu et al., TimesNet (ICLR 2023) | LOW |
| `src-2026-06-cortes-winner-takes-all` | Cortes et al., WTA probabilistic (2025) | LOW |
| `src-2026-06-zanotti-retraining-frequency` | Zanotti et al., Retraining frequency (2025) | LOW |
| `src-2026-06-he-general-tsm` | He et al., General TSM (2025) | LOW |
| `src-2026-06-irani-positional-encoding` | Irani et al., Positional encoding survey (2025) | LOW |

### Comparison page created

- `comparisons/tsf-backbone-comparison.md`: Full 15-model comparison table (14 new + TFT from I-P1-B); three key findings sections; exogenous integration strategies ranked by complexity.

### Key findings

- **Compact backbone sufficiency confirmed**: DLinear (one-layer linear) outperforms all Transformer LTSF models by 20–50% MSE on 9 standard benchmarks (Zeng 2023). Chen 2025 explains the mechanism: benchmarks are self-dependent/stationary, so intra-variate temporal modeling dominates.
- **Covariate gap in TSFMs confirmed across four papers**: ChronosX, UNICA, ApolloPFN, CATS-ATS each independently identify Chronos, TimesFM, MOMENT, Sundial, TimeMoE, LagLlama as not supporting exogenous covariates.
- **P1 backbone recommendation**: DLinear or NBEATSx as starting point; TimeXer (endo/exo cross-attention) if covariates are genuinely informative on real demand data.

### Pages updated

- `domains/timeseries-forecasting/thesis.md`: promoted `seed → researched`; all `[verify]` markers removed; "External literature positioning" replaced with confirmed findings from primaries; "Backbone landscape" section added; "Key assumptions" table updated with two new evidence-backed rows.
- `projects/p1-cluster-pretrained-deep-models.md`: two bullets added under "External literature positioning" with primary citations.

### Lint / TOC

- `uv run wiki lint`: 0 errors, 36 warnings (all pre-existing: library.json mismatches, orphan LOW-priority source pages, near-duplicate titles, stage/confidence sanity from pre-I-P1-C pages).
- `uv run wiki toc build`: indexes updated.

## 2026-06-30

### DLinear re-evaluation against 2024–2025 architectures

**Triggered by**: user request to re-evaluate DLinear claims against newer 2024/2025/2026 architectures.

**Finding**: DLinear is no longer the performance frontier. The progression:
- 2023: PatchTST (ICLR) outperforms DLinear
- 2024: iTransformer (ICLR) = "current SOTA in TSF" per multiple 2024 papers; outperforms DLinear
- 2024: TimeMixer/TimeMixer++ further outperform iTransformer (7.3% on Electricity)
- 2025: TimeKAN = 2025 SOTA; explicitly states "DLinear already shows a significant gap"

The gap is NOT small. Chen et al. 2025 analysis still applies: all these models succeed on benchmarks because benchmarks are self-dependent/stationary. Core P1 implication — invest in covariate layer — unchanged. But starting baseline updated from DLinear to iTransformer/TimeMixer.

**New source page**: `sources/src-2026-06-huang-timekan.md` (TimeKAN, 2025 SOTA on most LT benchmarks).

### Pages updated

- `comparisons/tsf-backbone-comparison.md`: added iTransformer and PatchTST rows; added performance tier header; revised Key Finding #1 and backbone recommendation; DLinear demoted to "ablation baseline only."
- `domains/timeseries-forecasting/thesis.md`: key assumptions table updated; External literature positioning section revised; backbone recommendation table updated.
- `projects/p1-cluster-pretrained-deep-models.md`: External literature positioning updated; candidate architecture updated to iTransformer/TimeMixer as primary backbone.
- `sources/src-2026-06-zeng-dlinear.md`: caveat added noting PatchTST/iTransformer/TimeMixer/TimeKAN subsequently outperformed DLinear.

### Real-benchmark challenge: TimeKAN/iTransformer SOTA is academic-only

**Triggered by**: user challenge — TimeKAN is significantly more complex; what is the simplest architecture with acceptable performance on **real, useful benchmarks** (M5, retail demand, EPF)?

**Key finding**: TimeKAN, iTransformer, and TimeMixer have **no published evaluation on M5, VN1, or EPF**. Their SOTA claims are exclusively on academic LTSF benchmarks (ETT×4, Weather, Electricity) — the self-dependent/stationary datasets Chen et al. 2025 warns do not transfer to real retail demand.

On real benchmarks:
- **M5 / VN1 (real retail)**: Zanotti 2025 uses N-BEATS and N-HiTS as DL SOTA; LGBM/tree-based models win the competition.
- **EPF (real electricity price with exo)**: NBEATSx is SOTA with genuine exogenous covariates.
- **M5 zero-shot with exo**: ApolloPFN (native exo PFN) is SOTA with promotions/prices.

**TimeKAN complexity**: significantly more complex than N-HiTS. TimeKAN = CFD blocks + M-KAN polynomial basis + Frequency Mixing (KAN-based architecture). N-HiTS = MLP stacks + hierarchical interpolation + multi-rate pooling. N-HiTS is 50× faster than Transformers and scales linearly with input.

**Revised recommendation**: Start with N-HiTS (simplest + real-benchmark proof), add covariates via NBEATSx (simplest) or TimeXer (strongest). iTransformer/TimeKAN are academic comparisons, not the P1 starting point.

### Pages updated

- `sources/src-2026-06-zanotti-retraining-frequency.md`: expanded from stub to full source page; added key claims about N-BEATS/N-HiTS as M5/VN1 DL SOTA and LGBM as competition winner.
- `comparisons/tsf-backbone-comparison.md`: added real-benchmark tier header distinguishing academic LTSF from M5/VN1/EPF; revised backbone recommendation to N-HiTS → NBEATSx → TimeXer priority; added benchmark dependency caveat.
- `domains/timeseries-forecasting/thesis.md`: backbone priority table revised (N-HiTS to P1, N-HiTS/NBEATSx focus); near-term path updated; key assumption updated; real-benchmark update section added.
- `projects/p1-cluster-pretrained-deep-models.md`: candidate architecture updated to N-HiTS/NBEATSx/TimeXer; external positioning updated with real-benchmark evidence.
- Source added to frontmatter: `src-2026-06-zanotti-retraining-frequency` in thesis, comparison, and project pages.

## 2026-06-30 (P1 domain pivot: demand/SKU → price/commodity/energy)

**Triggered by**: user clarification that P1 targets the **input/procurement side** — commodity prices, energy futures, FX — not output/demand/sales. Focus is on non-stationary volatile price data, robust forecasting, and interpretable attribution (what drove the price move), not retail SKU scalability.

### Domain changes

| Before | After |
|---|---|
| Purpose | Retail SKU demand forecasting, analyst bottleneck removal | Commodity/energy/price forecasting, procurement-side attribution |
| Primary benchmark | M5, VN1 (real retail) | EPF — electricity price forecasting (genuinely non-stationary, spike-prone, exo-covariate-rich) |
| Backbone priority 1 | N-HiTS (M5/M4 proven) | NBEATSx (EPF SOTA, MLP + exo concatenation) |
| Backbone priority 2 | NBEATSx | TimeXer (SOTA on 5 EPF datasets, best endo/exo cross-attention) |
| Attribution priority | Supplementary | **Central** — identifying which macro/supply covariates drove a price move is the core business value |
| Cluster definition | Demand seasonality / SKU shape | Price series volatility regime / market type (energy complex, metals, agricultural, FX) |
| Accuracy baseline | LGBM (demand competition winner) | GARCH/ARIMAX + LGBM (price domain baselines) |
| Key risk | Shape ≠ regime in demand | Volatility regime shifts invalidate cluster models; price spikes stress AttGrad gradient path |

### Pages updated

- `kb/CLAUDE.md`: P1 project description updated; P1 tracking guidance updated (new domain tracking items, EPF benchmark, attribution quality)
- `projects/p1-cluster-pretrained-deep-models.md`: Purpose, Candidate architecture, Success criteria, Main risks, Open research questions, External literature positioning — all updated
- `domains/timeseries-forecasting/thesis.md`: Current thesis, Preferred near-term path, Key assumptions table, Backbone priority table, Real benchmark note
- `comparisons/tsf-backbone-comparison.md`: Real benchmarks tier header (EPF primary); backbone recommendation revised (NBEATSx → TimeXer → iTransformer → N-HiTS)
- `sources/src-2026-06-olivares-nbeatsx.md`: Applicability to P1 upgraded (now primary backbone candidate, EPF connection highlighted)
- `sources/src-2026-06-wang-timexer.md`: Applicability to P1 upgraded (Priority 2, EPF alignment)
- `sources/src-2026-06-challu-nhits.md`: Applicability to P1 downgraded (medium; demand-benchmark credentials; ablation baseline only for P1)
- `sources/src-2026-06-zanotti-retraining-frequency.md`: Applicability to P1 updated (indirect relevance; domain shifted; retraining-cadence finding still applicable)
