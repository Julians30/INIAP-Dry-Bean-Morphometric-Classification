# Validation Protocol

## Unit of analysis

Each row corresponds to one distinct physical dry bean grain. There are no repeated measurements of the same grain across rows.

No plant-, pod-, lot-, or image-acquisition-event grouping identifier was available for the modeling dataset. Consequently, the inferential scope is grain-level classification under repeated stratified cross-validation.

## Repeated nested stratified cross-validation

The primary evaluation design uses:

- seeds: **2026, 2027, 2028**;
- outer folds: **5**;
- inner folds: **3** where model selection is required;
- primary metric: **macro-F1**.

All preprocessing, dimensionality reduction, model selection, and hyperparameter selection are restricted to the outer-training data. The outer-test fold is reserved for evaluation.

## Feature representations

### FULL_11

The full representation contains 11 image-derived morphometric descriptors.

### REDUCED_7

The reduced representation removes four algebraically derived/redundant descriptors for the prespecified redundancy ablation.

## Model families

The computational benchmark includes:

- direct classical machine-learning models;
- PCA-based pipelines;
- LDA-based pipelines;
- TabNet;
- FT-Transformer;
- pretrained TabPFN.

TabPFN is used locally in the Colab runtime when the required model access is available; the repository does not contain private access tokens or pretrained checkpoint files.

## Statistical and probabilistic analyses

The workflow includes:

- repeated outer-fold model comparisons;
- corrected inference;
- paired comparisons;
- equivalence testing;
- calibration assessment;
- temperature scaling using fold-external information;
- selective classification;
- feature-redundancy ablation;
- diagnostic learning curves.

The prespecified primary equivalence margin is **±0.010**. Margins of **±0.005** and **±0.015** are sensitivity analyses only.

## Repeated-seed interpretation

The same 4,000 grains are evaluated under three random seeds. These repeated evaluations are not interpreted as 12,000 independent biological observations.

For confusion matrices and related summaries, seed-specific outer-test results are calculated first and then summarized across seeds where appropriate.
