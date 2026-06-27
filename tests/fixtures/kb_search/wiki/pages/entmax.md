---
type: concept
domain: timeseries-forecasting
project: P1
status: active
stage: seed
confidence: medium
updated: 2026-06-01
sources: []
tags: []
---

## Overview

Entmax is a sparse probability mapping that generalises softmax by concentrating mass on a subset of inputs. It produces genuinely sparse attention distributions, where most weights are exactly zero.

## Properties

Entmax-alpha controls sparsity: alpha=1 recovers softmax; alpha=2 gives sparsemax. Higher alpha → sparser outputs.

## Applications

Used in attention mechanisms to enforce sparse covariate selection in transformer-based time series models.
