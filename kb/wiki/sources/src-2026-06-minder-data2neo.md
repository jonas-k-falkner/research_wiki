---
type: source
domain: nowcasting-graph
project: P4
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-minder-data2neo
tags:
- neo4j
- etl
- graph-databases
- tooling
zotero: minderData2NeoToolComplex2024
source_hash: aceaa155c47e1921eb5dd8529f423e715825c363d3de7994a68b7690ad665706
---

# Source: Data2Neo — A Tool for Complex Neo4j Data Integration (2024)

## Metadata
- **Citekey:** `minderData2NeoToolComplex2024`
- **Authors:** Minder, Salamanca, Brandenberger, Schweitzer (ETH Zürich)
- **Venue:** arXiv / ICAIF 2024
- **Relevant projects:** P4 (ETL tooling for evidence graph)

## One-line takeaway

Data2Neo is an open-source Python library (YAML-based conversion recipes, custom Python pre/post-processors, parallel streaming from any data source) for building production-grade ETL pipelines from relational data into Neo4j knowledge graphs.

## Key claims

- YAML-based "Conversion Schema" declaratively maps relational entities and join-tables to Neo4j nodes and relationships; Python hooks for arbitrary data cleaning.
- Supports continuous online data integration (streaming, not just batch), with node merging across multiple data sources via shared key attributes.
- Parallelized processing for large datasets; designed to scale beyond what native Neo4j CSV import or APOC plugins handle ergonomically.
- Better than: native Neo4j CSV DI (no custom cleaning), APOC plugin (CYPHER complexity for complex transformations), Apache Hop/Neo4j ETL Tool (GUI-based, limited Python integration).
- Code: github.com/jkminder/data2neo.

## Relevance to P4

P4's evidence ledger → explicit evidence graph pipeline requires exactly this: (1) structured relational data (evidence rows with entity IDs, relation types, timestamps) → Neo4j nodes/relationships; (2) custom Python steps to normalize entity names, resolve duplicates, and validate confidence scores; (3) continuous streaming as new evidence arrives. Data2Neo is the recommended ETL library for P4's graph construction pipeline. Its YAML schema maps cleanly onto P4's evidence entity types (disruption events, suppliers, products, regions) and the LPG property graph model confirmed optimal by Besta et al.
