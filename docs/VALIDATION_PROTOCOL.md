# Validation Protocol

## Unit of analysis

Each row corresponds to one distinct physical dry bean grain. There are no repeated measurements of the same grain across rows.

No plant-, pod-, lot-, or acquisition-event grouping identifier is available in the analytical modeling table. Consequently, the inferential scope is grain-level classification under repeated stratified cross-validation.

## Repeated nested stratified cross-validation

The primary evaluation design uses:

- seeds: **2026, 2027, 2028**;
- outer folds: **5**;
- inner folds: **3** where model selection is required;
- primary discrimination metric: **macro-F1**.

All fitted preprocessing, dimensionality reduction, hyperparameter selection, and model selection are restricted to outer-training data. The outer-test fold is reserved for evaluation.

## Feature representations

### FULL_11

The full representation contains 11 morphometric descriptors.

### REDUCED_7

The prespecified redundancy ablation removes `AspectRatio`, `Solidity`, `roundness`, and `Compactness`.

### STRICT_6

The strict sensitivity representation additionally removes `EquivDiameter` because it is exactly determined by `Area`:

`EquivDiameter = sqrt(4*Area/pi)`.

STRICT_6 is a sensitivity analysis and does not replace the primary FULL_11 versus REDUCED_7 ablation.

## Model families

The benchmark includes:

- direct classical machine learning models;
- PCA-based pipelines;
- LDA-based pipelines;
- TabNet;
- FT-Transformer-style model;
- pretrained TabPFN.

TabPFN is run locally in the Colab runtime when the required Prior Labs model access is available. No private access token or pretrained checkpoint file is stored in the repository.

## Corrected inference and equivalence

Repeated outer-fold comparisons use the Nadeau-Bengio corrected resampled t framework. The primary practical-equivalence margin is **±0.010 macro-F1**. Margins of **±0.005** and **±0.015** are retained as sensitivity analyses.

## Final strict probability-reliability protocol

The final calibration and selective-prediction analysis is outer-test external by construction.

For every seed and outer fold:

1. internal three-fold stratified cross-validation is performed **inside the outer-training partition**;
2. internal OOF probabilities are generated from models trained only on subsets of that outer-training partition;
3. the scalar temperature is estimated from these internal OOF probabilities;
4. confidence thresholds for target coverages of 100%, 95%, 90%, 80%, 70%, 60%, and 50% are estimated from the same outer-training-only calibrated OOF predictions;
5. the temperature and threshold are applied to the untouched outer-test probabilities.

The final probability-quality summaries include NLL, multiclass Brier score, equal-width ECE, adaptive equal-mass ECE, class-conditional ECE, fine high-confidence bins from 0.99 to 1.00, and AURC. NLL and Brier score are accompanied by grain-cluster bootstrap 95% confidence intervals. Accepted-case accuracy is accompanied by exact Clopper-Pearson 95% confidence intervals.

## Repeated-seed interpretation

The same 4,000 grains are evaluated under three random seeds. These repeated evaluations are **not** treated as 12,000 independent biological observations.
