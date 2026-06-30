---
type: source
domain: nowcasting-graph
project: P4
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-zheng-sc-gcn-fl
tags:
- supply-chain
- knowledge-graph
- graph-neural-network
- federated-learning
- link-prediction
zotero: zhengAnalyticsDrivenApproachEnhancing2025
source_hash: bfe94707151e39285bea4b6a6c3c4845a8f801e4a8b0a9f0ab24bf0c0694fb7a
---

# An Analytics-Driven Approach to Enhancing Supply Chain Visibility with Graph Neural Networks and Federated Learning

**Zheng & Brintrup (2025) — Cambridge / Alan Turing Institute**

## Summary

Proposes a Federated Learning (FL) + GraphSAGE framework for supply chain knowledge graph link prediction across multiple countries without raw data sharing. Each country trains a local GraphSAGE encoder on its SC KG; only the parameters of a shared NN module are aggregated (FedAvg). An adaptive variant (AdapFLavg) groups countries by data similarity before aggregation. Evaluated on Marklines automotive dataset: 10 countries, 5 entity types (company, customer, country, certificate, product), 4 relation types (supplies to, buys, made by, has cert). AdapFLavg consistently outperforms both local and standard FL models, especially on the sparse `has cert` relationship (<5% of edges).

## Key results

- AdapFLavg: best ROC-AUC on `has cert` across all 10 countries (e.g., Brazil 0.8576, Japan 0.8770)
- Local model competitive on large datasets (China: 191K edges, Japan: 122K edges)
- FL-based models outperform local on small countries (Brazil, Taiwan, UK) for most relations
- `has cert` (compliance certification) is the hardest to predict — lowest ROC-AUC for all models due to <5% edge proportion
- `buys` (product purchase) is easiest — highest edge proportion → best model performance
- GraphSAGE supports inductive learning: new company/product nodes can be embedded without retraining

## Architecture details

- SC KG: 5 entity types (company, customer, country, certificate, product) + 4 relation types
- GraphSAGE: mean aggregator over sampled neighbors; k aggregation hops
- NN module: 3 FC layers + ReLU (shared across countries in FL)
- Link prediction: dot product + sigmoid over node pair embeddings
- FedAvg: average NN parameters across all countries; GraphSAGE layers kept local
- AdapFLavg: group countries by mutual model performance before averaging
- Train/val/test: 70%/10%/20% split per country; negative triplets sampled 1:1

## Claims

**Claim:** GraphSAGE + Federated Learning with adaptive country grouping (AdapFLavg) outperforms both local-only training and standard FedAvg for predicting rare relationship types (has cert, <5% of edges) in multi-country SC KGs.
**Evidence:** Tables 4 and 5: AdapFLavg achieves highest ROC-AUC for has cert in 8/10 countries; e.g., Brazil 0.8604 vs local 0.6534, FLavg 0.7486.
**Applicability:** SC KGs with heterogeneous country-level data distributions where rare relationship types must be predicted across multiple jurisdictions.
**Limitations:** Requires all countries to agree on a shared entity/relation schema. FL aggregation adds communication overhead. Marklines is automotive-sector-only; SC graph structure in food/agri or chemicals may differ significantly.
**Contradictions:** For large countries (China, Japan), local model is competitive on the three high-frequency relation types; FL adds noise. No clear win across all conditions.
**Decision impact:** FL-style approach is relevant for P4 if cross-jurisdictional SC data must be integrated without raw data sharing. GraphSAGE's inductive learning (new nodes without retraining) is directly relevant for P4's continuously expanding evidence graph.
**Confidence:** high

**Claim:** GraphSAGE inductive learning enables embedding new supply chain entities (companies, products) as they appear without retraining the full model.
**Evidence:** Zheng & Brintrup 2025, Section 3.3: "GraphSAGE supports inductive learning, enabling generation of embeddings for nodes not present in training data. This is especially relevant in SCKGs, where entities such as new companies or products frequently emerge."
**Applicability:** Any dynamic SC KG where the entity set changes over time (new suppliers, new products, company mergers).
**Limitations:** GraphSAGE inductive embeddings depend on the quality of node features — if features are sparse (no initial attributes), quality degrades. Comparative evaluation against transductive GCNs not provided.
**Contradictions:** None.
**Decision impact:** Inductive embedding is a hard requirement for P4's evidence graph (suppliers are continuously added/removed). GraphSAGE or equivalent inductive GNN is the baseline recommendation over transductive methods.
**Confidence:** high

## Applicability to P4

Medium-high. Key insights for P4:
- GraphSAGE inductive learning is required (not optional) for a live SC graph — supports P4's design
- SC entity schema (5 types, 4 relations) is a concrete starting template; P4 needs to extend for availability signals and events
- FL is relevant if P4 ingests data from multiple organizations under GDPR constraints
- The paper confirms link prediction alone is insufficient for a live availability signal — visibility ≠ availability, and GCN can only predict structural relationships, not dynamic states (disruptions, out-of-stock)
- Certification (compliance) relationship is hardest to predict — reinforces P4's public-first strategy where compliance data is sparse

## Related

- [src-2026-06-liu-sc-kg](src-2026-06-liu-sc-kg.md) — SC KG with RotatE completion (different embedding approach)
- [src-2026-06-almahri-agentic-sc](src-2026-06-almahri-agentic-sc.md) — agentic disruption monitoring on SC KG
- [concepts/explicit-evidence-graph](../concepts/explicit-evidence-graph.md)
- [projects/p4-availability-nowcasting-graph](../projects/p4-availability-nowcasting-graph.md)
