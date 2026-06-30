# Literature Ingest Plan

Source of truth for moving `kb/wiki/` pages from `seed → researched`. Work tasks in priority
order; P1 first, then P2, then P4. Each task = one topic cluster = one reviewable commit.

**Ingest protocol (mandatory for every task):**
1. `wiki check source --citekey <KEY> --json` — skip if `unchanged`; update hash if `changed`.
2. Create/update `wiki/sources/src-<YYYY-MM>-<slug>.md` with `zotero: <KEY>` + `source_hash:`.
3. Before each claim: `wiki check claim "TEXT" --citekey <KEY>` — skip `duplicate`; merge
   `additional-support` onto existing page; write only `new` hits.
4. Extract claims with Evidence / Applicability / Limitations / Contradictions / Decision impact.
5. Update the target wiki pages listed in the task scope.
6. Run `wiki toc build` after adding any new page.
7. Run `wiki lint` — fix errors before committing.
8. Append one entry to `wiki/log.md`.
9. One commit per task.

**Search first.** Before reading a full paper, run:
```
wiki search "<topic>" --mode hybrid --scope literature
wiki search "<citekey>" --mode lexical
```
Use the returned snippets to prioritise which sections to read deeply.

**Confidence rule.** A paper that directly experiments on the claim → `high`. A paper that
discusses or surveys the claim → `medium`. A secondary synthesis or analogy → `low`.
Never promote a page past `seed` without at least one `high`-confidence primary citation.

---

## P1 — Cluster-pretrained deep models (PRIMARY FOCUS)

P1 pages currently at `seed` stage with `[verify]` markers. Goal: attach primary citations
and promote to `researched` where the evidence supports it.

Key P1 concept pages to update:
- `kb/wiki/concepts/cluster-pretrained-deep-models.md`
- `kb/wiki/concepts/hierarchical-entmax-covariate-selection.md`
- `kb/wiki/projects/p1-cluster-pretrained-deep-models.md`
- `kb/wiki/domains/timeseries-forecasting/thesis.md`

---

### Task I-P1-A — Clustering methods: routing feasibility

**Goal:** Verify whether shape/regime clustering is a viable routing mechanism at scale, and
what the literature says about cluster quality, DTW-based methods, and channel clustering in
deep forecasting. This directly confirms or undermines P1's core architectural bet.

**Papers to ingest (priority order):**

| Citekey | Title (short) | Priority |
|---|---|---|
| `chenSimilaritySuperiorityChannel` | Channel Clustering "From Similarity to Superiority" | HIGH — P1 named primary |
| `qiuDUETDualClustering2025` | DUET: Dual Clustering Enhanced Multivariate TSF | HIGH — P1 named primary |
| `aghabozorgiTimeseriesClusteringDecade2015` | Time-series clustering: a decade review | HIGH — survey anchor |
| `petitjeanGlobalAveragingMethod2011` | DTW barycenter averaging | MEDIUM — foundational method |
| `petitjeanFasterMoreAccurate2016` | Faster DTW classification | MEDIUM — used in routing |
| `bagnallGreatTimeSeries2017` | Great TS classification bake-off | MEDIUM — benchmark reference |
| `rutaSAXNavigatorTime2019` | SAX Navigator: hierarchical clustering | LOW — SAX baseline |
| `keoghParameterfreeDataMining2004` | Parameter-free TS data mining | LOW — older baseline |
| `tanIndexingClassifyingGigabytes2017` | Indexing gigabytes under warping | LOW — scalability baseline |
| `lucasProximityForestEffective2019` | Proximity Forest | LOW — classifier alternative |

**Research questions to answer:**
- Does Channel Clustering / DUET show that clustering channels improves forecasting accuracy?
  What clustering criterion do they use (shape, regime, covariate correlation)?
- Does DUET separate clustering from routing, and does it report attribution at the cluster
  level (not just per-channel)?
- What cluster-quality metrics are standard in the literature? Can they be applied to P1's
  shape-based clusters to validate the quality gate?
- Is there evidence that shape similarity implies regime consistency, or does the literature
  caution against this assumption?

**`[verify]` claims to confirm or refute on target pages:**
- "Channel Clustering (NeurIPS 2024) validates cluster-first routing" — confirm with primary.
- "DUET (KDD 2025) combines clustering and sparsification" — confirm; does it do attribution?
- "Shape-based clusters may not be regime-consistent" — what does the literature say?

**Target pages to update:**
- `wiki/concepts/cluster-pretrained-deep-models.md` — promote to `researched` if evidence
  supports; attach citations; fill in cluster-quality metric section.
- `wiki/projects/p1-cluster-pretrained-deep-models.md` — update "External literature
  positioning" with confirmed citations.
- `wiki/domains/timeseries-forecasting/thesis.md` — update "Most important unresolved question"
  section with what the clustering literature actually shows.
- Create `wiki/sources/src-<date>-channel-clustering.md` and
  `wiki/sources/src-<date>-duet-clustering.md` (one source page per paper ingested).

**DoD:**
- Source pages created for all HIGH-priority papers; MEDIUM/LOW at discretion.
- `concepts/cluster-pretrained-deep-models.md` updated with ≥1 primary citation; `[verify]`
  markers removed where confirmed; stage promoted to `researched` if warranted.
- No `duplicate` claims written (all passed through `wiki check claim`).
- `wiki lint` clean; `wiki toc build` run; `wiki/log.md` entry appended.

---

### Task I-P1-B — Covariate selection & attention faithfulness

**Goal:** Verify the entmax/sparsemax covariate selection approach against primaries and
settle the attention-as-explanation debate, which directly affects the interpretability claims
in P1's covariate explanation layer.

**Papers to ingest (priority order):**

| Citekey | Title (short) | Priority |
|---|---|---|
| `petersSparseSequencetoSequenceModels2019` | Sparse Seq2Seq Models (sparsemax/α-entmax) | HIGH — foundational method |
| `limTemporalFusionTransformers2021` | Temporal Fusion Transformers | HIGH — comparison baseline |
| `jainAttentionNotExplanation` | Attention is not Explanation | HIGH — faithfulness debate |
| `wiegreffeAttentionNotNot2019` | Attention is not not Explanation | HIGH — faithfulness debate |
| `lundbergUnifiedApproachInterpreting2017` | SHAP (Unified Attribution) | HIGH — attribution baseline |
| `sundararajanAxiomaticAttributionDeep2017` | Integrated Gradients | HIGH — axiomatic attribution |
| `bibalAttentionExplanationIntroduction2022` | Attention Debate intro | MEDIUM — survey |
| `bastingsElephantInterpretabilityRoom2020` | Elephant in interpretability room | MEDIUM — why not attention |
| `liuRethinkingAttentionModelExplainability2022` | Faithfulness Violation Test | MEDIUM — empirical test |
| `rojatExplainableArtificialIntelligence2021` | XAI on Time Series Survey | MEDIUM — TSF-specific survey |
| `atashgahiQuickRobustFeature2022` | Energy-efficient sparse feature selection | LOW |
| `louSparserFasterLess2024` | Sparser is Faster (sparse attention) | LOW — architecture ref |
| `taySparseSinkhornAttention2020` | Sparse Sinkhorn Attention | LOW — sparse attn variant |
| `zhaoetal.SparseTransformerConcentrated2019` | Sparse Transformer | LOW — sparse attn baseline |

**Research questions to answer:**
- What does Jain & Wallace (2019) vs Wiegreffe & Pinter (2019) settle about attention weights
  as explanations? Is weight × gradient the recommended solution, or does the debate remain open?
- Does TFT's variable selection network use sparsemax or softmax gating? How does it compare
  to α-entmax for covariate selection stability?
- Do SHAP / Integrated Gradients apply to the hierarchical entmax mechanism? If so, can P1
  use gradient-based attribution to complement cluster-level importance?
- Is there empirical evidence that α-entmax gates are more stable than soft-attention under
  correlated inputs?

**`[verify]` claims to confirm or refute:**
- "sparsemax / α-entmax from Martins & Astudillo / Peters, Niculae & Martins" — confirm the
  primary paper and what it demonstrates for selection stability.
- "Attention faithfulness debate supports weight×gradient + stability diagnostics as the
  recommended approach" — summarise consensus after both sides.
- "TFT variable selection is the main comparison baseline for covariate selection in TSF" —
  confirm from the primary.

**Target pages to update:**
- `wiki/concepts/hierarchical-entmax-covariate-selection.md` — attach primaries; remove
  `[verify]` markers; promote to `researched` where evidence supports.
- `wiki/projects/p1-cluster-pretrained-deep-models.md` — update covariate explanation section;
  resolve or deepen the MC-dropout + determinism tension with primary evidence.
- Possibly create `wiki/concepts/attention-faithfulness.md` if the debate warrants a
  standalone concept page (reused across P1/P2).

**DoD:** Same as I-P1-A.

---

### Task I-P1-C — TSF backbone landscape (compact model sufficiency)

**Goal:** Establish the TSF backbone landscape so the thesis "a compact backbone with the
right covariate inductive bias suffices" is backed by named primaries, and the "backbone
choice (D-Linear vs MLP) is an open question" is answered or scoped.

**Papers to ingest (priority order):**

| Citekey | Title (short) | Priority |
|---|---|---|
| `zengAreTransformersEffective2022` | Are Transformers Effective? (DLinear) | HIGH — compact-wins anchor |
| `wangTimeXerEmpoweringTransformers` | TimeXer (endo/exo split) | HIGH — covariate architecture |
| `challuNHiTSNeuralHierarchical2022` | N-HiTS | HIGH — strong compact baseline |
| `oreshkinNBEATSNeuralBasis2020` | N-BEATS | HIGH — strong compact baseline |
| `limTemporalFusionTransformers2021` | TFT (if not done in I-P1-B) | HIGH |
| `wangTimeMixerGeneralTime2024` | TimeMixer++ | MEDIUM — recent compact SOTA |
| `ekambaramTinyTimeMixers2024` | Tiny Time Mixers (TTMs, zero-shot) | MEDIUM — TSFM adapter |
| `arangoChronosXAdaptingPretrained2025` | ChronosX (exogenous adapter) | MEDIUM — named primary |
| `hanUNICAUNIFIEDCOVARIATE2026` | UNICA (unified covariate adaptation) | MEDIUM — named primary |
| `potapczynskiTimeAwarePriorFitted2026` | ApolloPFN (zero-shot + exogenous) | MEDIUM — named primary |
| `luCATSEnhancingMultivariate2026` | CATS-ATS | MEDIUM — named primary |
| `heGeneralTimeseriesModel2025` | General TSM | LOW |
| `olivaresNeuralBasisExpansion2023` | NBEATSx (exogenous N-BEATS) | LOW — exo extension |
| `cortesWinnertakesallMultivariateProbabilistic2025` | Winner-takes-all multivariate | LOW |
| `wuAutoformerDecompositionTransformers2021` | Autoformer | LOW — background |
| `wuTimesNetTemporal2DVariation2023` | TimesNet | LOW — background |
| `zanottiRetrainingFrequencyGlobal2025` | Retraining frequency of global models | LOW |
| `chenCloserLookTransformers` | Closer Look at Transformers for TSF | MEDIUM — directly cited |
| `auerTiRexZeroShotForecasting2025` | TiRex zero-shot | LOW |
| `iraniPositionalEncodingTransformerBased2025` | Positional encoding survey | LOW — background |
| `huangTimeKANKANbasedFrequency2025` | TimeKAN | LOW — background |
| `liangITFKANInterpretableTime2025` | iTFKAN | LOW — background |
| `rizviBridgingSimplicitySophistication2025` | GLinear | LOW |
| `kumarMixBEATSMixerenhancedBasis2025` | Mix-BEATS | LOW |
| `wangRDLinearNovelTime2024` | RDLinear | LOW |
| `zhangLongRangeSwitching2024` | Long Range Switching | LOW |
| `zhangUnderstandingTokenlevelTopological2025` | Token-level topological structures | LOW |
| `fein-ashleySPECTREFFTBasedEfficient2025` | SPECTRE FFT attention | LOW |
| `bytez.comAreSelfAttentionsEffective2024` | Are Self-Attentions Effective? (web) | LOW |

**Research questions to answer:**
- Does the literature support "D-Linear or MLP suffices for the backbone when the covariate
  selector is the key component"? What accuracy gap (if any) remains vs transformer backbones?
- What do the covariate adapter papers (TimeXer, ChronosX, UNICA, ApolloPFN, CATS-ATS) say
  about architecture choice for the backbone? Do any recommend MLP over attention?
- Do TSFMs (Chronos, Moirai, TimesFM etc.) address exogenous covariates, or is that the gap
  the adapter papers fill? How does this frame P1's architecture bet?
- What benchmark results should P1 target (M5, ETTh/m, Traffic, Exchange) based on what
  comparable methods report?

**`[verify]` claims to confirm or refute:**
- "Compact backbone (spend the budget on the selector)" — confirmed by which papers?
- "TS foundation models are background, not blueprints, for sparse covariate selection" —
  does the adapter literature confirm this gap?
- "TimeXer, ChronosX, UNICA, ApolloPFN, CATS-ATS validate the exo-covariate gap" — confirm
  each paper's specific contribution.

**Target pages to update:**
- `wiki/domains/timeseries-forecasting/thesis.md` — fill backbone-choice section with
  primary evidence; remove `[verify]`; promote where warranted.
- `wiki/projects/p1-cluster-pretrained-deep-models.md` — add "Backbone choice" subsection
  with the evidence summary; update benchmarks table.
- Possibly create `wiki/comparisons/tsf-backbone-comparison.md` if a structured table of
  backbones is useful for P1 design decisions.
- Source pages for all HIGH/MEDIUM papers.

**DoD:** Same as I-P1-A. `domains/timeseries-forecasting/thesis.md` promoted to `researched`
if the backbone question is settled.

---

### Task I-P1-D — SSM / alternative architecture survey (background, brief)

**Goal:** Establish that Mamba, RWKV, linear RNNs, etc. are architectural background for P1
but not the right backbone choice. Produce concise source pages; do not over-invest.

**Papers to ingest (LOW priority — skim and summarise, no deep claim extraction):**

`guMambaLinearTimeSequence2024`, `wangMambaEffectiveTime2024`, `patroSiMBASimplifiedMambaBased2024`,
`daoTransformersAreSSMs2024`, `beckXLSTMExtendedLong2024`, `pengRWKVReinventingRNNs2023`,
`pengEagleFinchRWKV2024`, `qinHierarchicallyGatedRecurrent2023`, `qinHGRN2GatedLinear2024`,
`yangGatedLinearAttention2024`, `yangGatedDeltaNetworks2025`, `liuLonghornStateSpace2024`,
`sunLearningLearnTest2024`, `zhangGatedSlotAttention2024`, `lieberJambaHybridTransformerMamba2024`

**Approach:** One short source page per paper (metadata + 2–3 bullet claims max). Update
`domains/timeseries-forecasting/thesis.md` with a single "SSM/linear-RNN landscape" paragraph
citing these as background. Do NOT create individual concept pages for each architecture.

**Research question:** Does `wangMambaEffectiveTime2024` show Mamba underperforms simple
linear models on TSF? If yes, note on the thesis page as empirical backing for the compact
backbone choice.

**DoD:** Source pages created (brief). Domain thesis updated. One commit.

---

## P2 — Causal embedding model (SECONDARY)

Work these after all P1 tasks are complete or in parallel if bandwidth allows.

---

### Task I-P2-A — Self-supervised / contrastive TS representation learning

**Goal:** Build the literature foundation for P2's SSL encoder (Ti-MAE GL, ConvAttn, Soft-DTW
SL) by ingesting the core SSL/contrastive representation learning papers.

**Papers to ingest (priority order):**

| Citekey | Title (short) | Priority |
|---|---|---|
| `liTiMAESelfSupervisedMasked2023` | Ti-MAE | HIGH — P2 encoder named primary |
| `yueTS2VecUniversalRepresentation2022` | TS2Vec | HIGH — universal TS repr |
| `eldeleTimeSeriesRepresentationLearning2021` | TS repr via temporal/contextual contrast | HIGH |
| `chengTimeMAESelfSupervisedRepresentations2023` | TimeMAE | HIGH |
| `foumaniSeries2vecSimilaritybasedSelfsupervised2024` | Series2vec | MEDIUM |
| `choiMultiTaskSelfSupervisedTimeSeries2023` | Multi-task SSL for TS | MEDIUM |
| `eldeleSelfsupervisedContrastiveRepresentation2023` | SSL contrastive semi-supervised TS | MEDIUM |
| `eldeleLabelefficientTimeSeries2024` | Label-efficient TS repr review | MEDIUM |
| `jawedSelfsupervisedLearningSemisupervised2020` | SSL for semi-supervised TS classification | MEDIUM |
| `yangTimeCLRSelfsupervisedContrastive2022` | TimeCLR | MEDIUM |
| `fraikinTRepRepresentationLearning2024` | T-Rep (time embeddings) | MEDIUM |
| `talukderTOTEMTOkenizedTime2024` | TOTEM (tokenised TS embeddings) | MEDIUM |
| `heMomentumContrastUnsupervised2020` | MoCo | LOW — foundational contrastive |
| `ericssonSelfSupervisedRepresentationLearning2022` | SSL: intro, advances, challenges | LOW — survey |
| `liuSelfSupervisedContrastiveLearning2023` | SSL for medical TS (methodology review) | LOW |
| `liuSelfSupervisedLearningTime2024` | SSL: contrastive or generative? | LOW |
| `pascualLearningProblemagnosticSpeech2019` | Problem-agnostic speech repr (SSL analogy) | LOW |
| `musgraveMetricLearningReality` | Metric Learning Reality Check | LOW |
| `tsitsulinUnsupervisedEmbeddingQuality2023` | Unsupervised embedding quality eval | LOW |
| `umDataAugmentationWearable2017` | Data augmentation for TS (SSL contrast pairs) | LOW |
| `tranFastPreciseSinglecell2021` | Hierarchical autoencoder (method analogy) | LOW |

**Research questions to answer:**
- What pretraining objective does Ti-MAE use, and how does it relate to P2's masked
  autoencoder approach? Does it support directed/asymmetric embeddings or only symmetric?
- What does TS2Vec show about universal representation quality across tasks? Does it use
  contrastive or generative objectives?
- What augmentation strategies work for TS contrastive learning (TimeMAE, TimeCLR)?
  Which are appropriate for the 200M-series scale P2 operates at?
- How is embedding quality evaluated without labels? Does `tsitsulinUnsupervisedEmbeddingQuality2023`
  give a metric P2 can adopt?

**Target pages to update:**
- `wiki/projects/p2-causal-embedding-v2.md`
- `wiki/concepts/causal-covariate-embeddings.md`
- `wiki/domains/embedding-models/thesis.md`

**DoD:** Source pages for HIGH/MEDIUM papers. P2 project page updated with primary citations.
Concept page for causal embeddings promoted to `researched` where evidence supports.

---

## P4 — Availability nowcasting graph (TERTIARY)

Work these last, or in parallel once P1 is substantially complete.

---

### Task I-P4-A — Supply chain knowledge graphs and disruption monitoring

**Goal:** Ground the P4 KG/evidence-ledger architecture in primary literature on supply chain
graphs, entity extraction, and resilience frameworks.

**Papers to ingest:**

| Citekey | Title (short) | Priority |
|---|---|---|
| `liuKnowledgeGraphPerspective2023` | KG perspective on supply chain resilience | HIGH |
| `zhengAnalyticsDrivenApproachEnhancing2025` | Analytics-driven supply chain visibility (GNN) | HIGH |
| `almahriAutomatingSupplyChain2026` | Automating SC disruption monitoring (agentic AI) | HIGH |
| `chengSHIELDLLMDrivenSchema2024` | SHIELD: LLM schema induction for EV battery SC | MEDIUM |
| `ramzyMARESemanticSupply2022` | MARE: semantic SC disruption management | MEDIUM |
| `bestaDemystifyingGraphDatabases2023` | Demystifying graph databases | MEDIUM — architecture ref |
| `minderData2NeoToolComplex2024` | Data2Neo: Neo4j data integration | LOW — tooling ref |

**Research questions to answer:**
- What KG schema patterns does the literature recommend for supply chain entities and events?
  Does SHIELD or MARE provide a reusable schema P4 could adopt or adapt?
- What GNN approaches (link prediction, GCN, GAT) are applied to supply chain resilience?
  Do they achieve interpretable output or black-box scores?
- How does `almahriAutomatingSupplyChain2026` approach disruption detection with agentic AI?
  Does it maintain an evidence provenance chain?

**Target pages to update:**
- `wiki/projects/p4-availability-nowcasting-graph.md`
- `wiki/concepts/explicit-evidence-graph.md`
- `wiki/concepts/evidence-ledger.md`
- `wiki/domains/nowcasting-graph/thesis.md`

**DoD:** Same as I-P1-A.

---

## Appendix: papers not yet assigned

The following papers in `library.json` have no explicit task assignment above. Assign to
the closest task or create a new task if a theme emerges.

- `atashgahiQuickRobustFeature2022` — feature selection (fits I-P1-B)
- `lewisBARTDenoisingSequencetoSequence2019` — NLP denoising pre-training (background; brief
  source page if referenced by any P1/P2 paper)
- `bytez.comAreSelfAttentionsEffective2024` — web page (no PDF); check if it has a primary
  paper equivalent in the library before ingesting

---

## Final ingest status (2026-06-30)

All tasks complete. All library papers with PDFs now have source pages.

**Ingested in supplementary pass (2026-06-30, priority-corrected):**

HIGH priority (priority label in plan was wrong):
- `beckXLSTMExtendedLong2024` — upgraded from background stub to full P1/P2 source page (mLSTM matrix memory)
- `kazemiTime2VecLearningVector2019` — not in original plan; created `src-2026-06-kazemi-time2vec`
- `heMomentumContrastUnsupervised2020` — was LOW in I-P2-A; created `src-2026-06-he-moco`
- `musgraveMetricLearningReality` — was LOW in I-P2-A; created `src-2026-06-musgrave-metric-learning-reality`
- `liuSelfSupervisedLearningTime2024` — was LOW in I-P2-A; created `src-2026-06-liu-ssl-comparison`
- `tanIndexingClassifyingGigabytes2017` — was LOW in I-P1-A; created `src-2026-06-tan-ts-indexing`
- `atesCounterfactualExplanationsMachine2021` — not in library, no citekey; created `src-2026-06-ates-counterfactual-ts`

MEDIUM/LOW (background and tooling):
- `ericssonSelfSupervisedRepresentationLearning2022` → `src-2026-06-ericsson-ssl-survey`
- `liuSelfSupervisedContrastiveLearning2023` → `src-2026-06-liu-ssl-medical-review`
- `umDataAugmentationWearable2017` → `src-2026-06-um-wearable-augmentation`
- `lewisBARTDenoisingSequencetoSequence2019` → `src-2026-06-lewis-bart`
- `pascualLearningProblemagnosticSpeech2019` → `src-2026-06-pascual-speech-ssl`
- `tranFastPreciseSinglecell2021` → `src-2026-06-tran-scrna-autoencoder`
- `minderData2NeoToolComplex2024` → `src-2026-06-minder-data2neo`
- `zhangUnderstandingTokenlevelTopological2025` → `src-2026-06-zhang-tem-topology`
- `kadraInterpretableMesomorphicNetworks2024` → `src-2026-06-kadra-mesomorphic` (no library entry)

**Papers that cannot be ingested (no PDF in library):**
- `atashgahiQuickRobustFeature2022` — library entry present, no PDF file. Skip.
- `wangRDLinearNovelTime2024` — library entry present, no PDF file. Skip.
- `bytez.comAreSelfAttentionsEffective2024` — web page entry, no PDF file. Skip.

---

## Execution order

```
I-P1-A  (clustering core)         ← start here
I-P1-B  (covariate selection)     ← can run in parallel with I-P1-A
I-P1-C  (backbone landscape)      ← after A and B; some papers overlap
I-P1-D  (SSM background)          ← low effort; batch at end of P1 sprint
I-P2-A  (SSL representation)      ← start after P1-A/B complete
I-P4-A  (supply chain KG)         ← independent; can run in parallel with P2
```

## Cross-cutting rules

- **One commit per task.** Do not mix papers from different tasks in a single commit.
- **Do not over-create pages.** A concept page is worth creating only if ≥2 tasks reference it
  and it carries reusable synthesis. Otherwise, fold into the project or domain page.
- **Search before reading.** `wiki search` the citekey and key terms before opening the full
  txt. Use snippets to identify which sections are decision-relevant.
- **PDF is the authority for exact math.** When a claim depends on a formula, re-read the PDF;
  do not rely on docling txt output alone.
- **Update `wiki/log.md`** at the end of every task with a concise entry (date, task ID, what
  was ingested, what was promoted, key finding).
- **Run `wiki toc build`** after any structural change (new source page, new concept page).
- **Run `wiki lint`** before every commit; fix all errors; flag warns.


## open gaps

- multi-frequency merging approaches for daily freq forecasts (needs a model that works with monthly, weekly and daily data and is able to fuse the information without leakage and without forward looking info.
