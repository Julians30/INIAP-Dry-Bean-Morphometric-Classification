# Figures

This directory contains the publication figures and figure-generation outputs aligned with the current manuscript.

## Current manuscript figure map

1. **Figure 1 — Analytical workflow:** includes FULL_11, REDUCED_7, and STRICT_6, repeated nested validation, OOF predictions, robustness analyses, and strict reliability assessment.
2. **Figure 2 — Correlation matrix:** 11 morphometric descriptors.
3. **Figure 3 — PCA/LDA projection:** combined unsupervised PCA and supervised LDA descriptive projection.
4. **Figure 4 — FULL_11 benchmark:** comparative macro-F1 performance across the complete model benchmark.
5. **Figure 5 — Confusion matrices:** TabPFN and LDA-XGBoost.
6. **Figure 6 — ROC comparison:** TabPFN and LDA-XGBoost one-vs-rest ROC curves.
7. **Figure 7 — Strict adaptive calibration:** outer-training-only adaptive equal-mass calibration curves.
8. **Figure 8 — Strict accuracy-coverage:** selective-prediction curves using thresholds estimated only within each outer-training partition.
9. **Figure 9 — Learning curves:** TabPFN and LDA-XGBoost diagnostic learning curves.

Vector SVG files are provided where the final source figure is vector-based; high-resolution PNG is retained for figures exported from the final NB14/NB16 workflows. Captions are maintained in the manuscript.

## Revision (first round of peer review)

Figures 1, 2, 3, 6, 7, and 8 were updated for the revised manuscript. Figures 1–3 were regenerated at 600 dpi with
[`revision/scripts/regenerate_figures_1_3.py`](../revision/scripts/regenerate_figures_1_3.py) (Figure 1 adds the
revision analyses; Figure 2 uses the true minus sign; values are unchanged). Panel labels (A, B) were added to Figure 6,
and in Figures 7 and 8 the in-figure titles were removed and the colours harmonized with Figure 4 (TabPFN orange,
LDA-XGBoost blue); the plotted values are unchanged. Figures 1 and 2 are now provided as 600 dpi PNG files.
