# Results

This directory contains selected derived outputs required to audit the results reported in the manuscript.

## Contents

- `model_performance/` — harmonized fold-level discrimination metrics.
- `redundancy/` — FULL_11 versus REDUCED_7 outputs plus STRICT_6 sensitivity results.
- `calibration/` — final strict outer-training-only calibration metrics and confidence-interval summaries.
- `selective_prediction/` — strict selective-prediction counts, exact accuracy intervals, and rejected-set cultivar composition.
- `learning_curves/` — final TabPFN and LDA-XGBoost learning-curve summaries.
- `statistical_tests/` — corrected repeated-CV tests, equivalence sensitivity, paired bootstrap, and McNemar outputs.

The original morphometric observations are not included. Large intermediate checkpoints are deliberately excluded.
