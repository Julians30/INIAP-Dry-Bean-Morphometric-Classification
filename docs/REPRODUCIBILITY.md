# Reproducibility Guide

## Intended environment

The original analysis was developed and executed in **Google Colab** with Google Drive used for persistent project storage. GPU acceleration is useful for the deep-tabular and TabPFN stages.

## Recommended notebook order

Only the audited/final notebook version for each stage should be used.

| Order | Notebook | Purpose |
|---|---|---|
| 00 | `NB00_Project_Setup.ipynb` | Project structure, paths, seeds, feature definitions |
| 01 | `NB01_Data_Audit_EDA.ipynb` | Data audit and exploratory analysis |
| 02 | `NB02_Dimensionality_Reduction.ipynb` | PCA/LDA dimensionality analysis |
| 03 | `NB03_Baseline_Models_FIXED.ipynb` | Baseline machine-learning benchmark |
| 04 | `NB04_Hybrid_Models_FIXED.ipynb` | PCA/LDA hybrid pipelines |
| 05 | `NB05_Deep_Tabular_Models_FIXED.ipynb` | TabNet and FT-Transformer |
| 06 | `NB06_Statistical_Comparison_Interpretability_FIXED.ipynb` | Statistical comparison and interpretation |
| 07 | `NB07_ROC_Learning_Curves.ipynb` | ROC analysis and initial diagnostic learning curves |
| 08 | `NB08_Extended_Baselines_Redundancy_Ablation.ipynb` | Extended baselines, FULL_11 vs REDUCED_7, TabPFN |
| 09 | `NB09_Statistical_Robustness_Calibration_Selective_R2.ipynb` | Corrected inference, calibration, equivalence, selective prediction |
| 10 | `NB10_Publication_Quality_Figures_MDPI_FINAL_R13.ipynb` | Main publication figures |
| 12 | `NB12_Top2_Confusion_and_Learning_Curves_FIXED.ipynb` | Final TabPFN/LDA-XGBoost confusion matrices and learning curves |
| 13 | `NB13_Final_Publication_Figure_Polish.ipynb` | Final figure-only polish; no model retraining |
| 99 | `NB99_Package_All_Results_UPDATED.ipynb` | Packaging/audit of final outputs |

Notebook 11 was a local housekeeping/cleanup utility and is intentionally not part of the scientific execution chain.

## Dataset placement

The notebooks were originally run with the dataset stored in the project Drive workspace. The raw dataset is not included in this public repository.

Authorized users should place the dataset at the path expected by the notebooks or adapt the path configuration in NB00.

## Reproducibility boundaries

Because the source dataset is not publicly redistributed, a public user can audit the code, experimental design, derived outputs, figures, and statistical workflow but cannot rerun the full study without authorized access to the source data.

## TabPFN

TabPFN requires the applicable Prior Labs model access in a fresh runtime. Credentials must be entered securely at runtime and must never be committed to the repository.

## Checkpoints

Long-running stages write checkpoints so an interrupted Colab session can resume without repeating completed fits.

## Final-figure workflow

NB13 regenerates the final publication versions of Figures 1, 4, and 8 from already-computed data/results and does not retrain TabPFN.
