---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-bibal-attention-explanation-survey-2022
tags:
- source
- attention-faithfulness
- survey
- interpretability
citekey: bibalAttentionExplanationIntroduction2022
source_hash: f81bf7f058a9bd30fba4bfaa860fd005b4127fe419cc58dac8d5ac1004e6f988
author: Bibal, Adrien; Cardon, Rémi; Alfter, David; Watrin, Patrick; Liechi, Philippe;
  Frenay, Benoît
year: 2022
title: Is Attention Explanation? An Introduction to the Debate
venue: ACL 2022
zotero: bibalAttentionExplanationIntroduction2022
---

# Bibal et al. (2022) — Is Attention Explanation? An Introduction to the Debate

## Summary

Survey synthesizing the attention-as-explanation debate from Jain & Wallace (2019) through subsequent rebuttals and empirical studies. Covers NLP, computer vision, and other domains. Identifies convergences (attention alone is insufficient; gradient-based methods add necessary information) and persistent disagreements (what "explanation" means, how to evaluate faithfulness). Provides a structured taxonomy of the debate positions and a reading guide for practitioners entering the field.

## Key claims

1. The debate converges on a practical consensus: raw attention weights alone are insufficient for explanation, but attention combined with gradient information (e.g., AttGrad) substantially improves faithfulness across tasks and domains.
2. The definition of "explanation" varies across papers — some require faithfulness (mechanistic accuracy), others require plausibility (human-aligned) — and much apparent disagreement dissolves once the evaluation criterion is specified.
3. Evidence across NLP and CV supports that attention faithfulness is task- and architecture-dependent; no universal answer exists, and practitioners must validate per task.

## Relevance to P1

Provides the survey-level synthesis that contextualizes the Jain/Wiegreffe debate for P1. The practical consensus (AttGrad > raw attention) aligns with Liu et al.'s quantitative recommendation. The faithfulness vs. plausibility distinction is directly relevant: P1's interpretability claim is faithfulness-based (the selected covariates must be the causal drivers), not merely plausibility-based (the selection must look reasonable to domain experts). This distinction should be explicitly stated when reporting P1 results.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/attention-faithfulness](../concepts/attention-faithfulness.md)
