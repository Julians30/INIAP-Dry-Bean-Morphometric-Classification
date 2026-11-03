# Supplementary Tables

Machine-readable companions to the supplementary tables cited in the manuscript.

- **Table S1:** `S1_Descriptive_Morphometry.csv` — cultivar-wise mean, SD, median, Q1, and Q3 in the original analytical units.
- **Table S2:** `S2_Kruskal_Holm_Effect_Sizes.csv` — Kruskal-Wallis statistics, Holm-adjusted p-values, and epsilon-squared effect sizes.
- **Table S3:** `S3_STRICT6_Fold_Results.csv` — STRICT_6 model results by seed and outer fold.
- **Table S4:** `S4_Strict_Calibration_By_Seed.csv` — strict outer-training-only NLL, Brier, equal-width ECE, adaptive ECE, and AURC by seed.
- **Table S5:** `S5a_High_Confidence_099_100_Bins.csv` and `S5b_Classwise_Adaptive_ECE.csv` — high-confidence and class-conditional calibration diagnostics.
- **Table S6:** `S6a_Selective_Prediction_By_Seed.csv`, `S6b_Rejected_Composition_By_Cultivar.csv`, and `S6c_Review_Burden_By_Cultivar.csv` — selective-prediction counts, exact accuracy intervals, rejected-set cultivar composition, and cultivar-specific acceptance rates and errors captured in the referred set.
- **Table S7:** `S7a_TOST_Equivalence_Sensitivity.csv` and `S7b_CorrelatedT_ROPE_Sensitivity.csv` — equivalence-margin and ROPE sensitivity analyses.
- **Table S8:** `S8_MCC_Kappa_FoldLevel.csv` — fold-level metrics including MCC and Cohen's kappa.
- **Table S9:** `S9_Simple_Feature_Baselines.csv` — logistic regression and LDA with one to three primary measurements on the identical folds.
- **Table S10:** `S10_Hybrid_vs_Direct_Comparisons.csv` — hybrid-versus-direct corrected resampled t-tests, paired bootstrap, and exact McNemar results.
- **Table S11:** `S11_Computational_Time_Hardware.csv` — fitting and prediction times and hardware.
- **Table S12:** `S12a_Deep_Tabular_Budget_Matched_Summary.csv`, `S12a_Deep_Tabular_Budget_Matched_Tests.csv`, and `S12b_Deep_Tabular_Search_Configurations.csv` — budget-matched nested search of TabNet and the FT-Transformer-style model.

Tables S6c and S9–S12 were added during peer review; the scripts that generate them are in [`../../revision/scripts/`](../../revision/scripts/).

These files contain derived results only. The original morphometric observations are not redistributed.
