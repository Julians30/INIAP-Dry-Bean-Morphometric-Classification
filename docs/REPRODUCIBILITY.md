# Reproducibility Guide

## Intended environment

The analysis was developed and executed in **Google Colab**, with Google Drive used for persistent project storage. GPU acceleration is useful for deep tabular models and TabPFN.

## Captured environment

Software versions from the completed workflow are documented in [../environment/ENVIRONMENT.md](../environment/ENVIRONMENT.md) and [../environment/exact_versions.json](../environment/exact_versions.json).

## Recommended scientific notebook order

| Order | Notebook | Purpose |
|---|---|---|
| 00 | `NB00_Project_Setup.ipynb` | Project structure, paths, seeds, feature definitions |
| 01 | `NB01_Data_Audit_EDA.ipynb` | Data audit and exploratory analysis |
| 02 | `NB02_Dimensionality_Reduction.ipynb` | PCA/LDA dimensionality analysis |
| 03 | `NB03_Baseline_Models_FIXED.ipynb` | Baseline machine learning benchmark |
| 04 | `NB04_Hybrid_Models_FIXED.ipynb` | PCA/LDA hybrid pipelines |
| 05 | `NB05_Deep_Tabular_Models_FIXED.ipynb` | TabNet and FT-Transformer |
| 06 | `NB06_Statistical_Comparison_Interpretability_FIXED.ipynb` | Statistical comparison and interpretation |
| 07 | `NB07_ROC_Learning_Curves.ipynb` | ROC analysis and diagnostic learning curves |
| 08 | `NB08_Extended_Baselines_Redundancy_Ablation.ipynb` | Extended baselines, FULL_11 vs REDUCED_7, TabPFN |
| 09 | `NB09_Statistical_Robustness_Calibration_Selective_R2.ipynb` | Corrected inference, equivalence, and preliminary probability analyses |
| 10 | `NB10_Publication_Quality_Figures_MDPI_FINAL_R13.ipynb` | Publication-quality benchmark figures |
| 12 | `NB12_Top2_Confusion_and_Learning_Curves_FIXED.ipynb` | TabPFN/LDA-XGBoost confusion matrices and learning curves |
| 13 | `NB13_Final_Publication_Figure_Polish.ipynb` | Figure-only polish |
| 14 | `NB14_Final_PCA_LDA_Calibration_Publication.ipynb` | Combined PCA/LDA descriptive projection; its older calibration helper outputs are superseded by NB16 |
| 16 | `NB16_Strict_Calibration_Selective_Reviewer_Audit.ipynb` | Final strict outer-training-only calibration, adaptive ECE, NLL/Brier CIs, AURC, Clopper-Pearson intervals, selective prediction, rejected-set composition, and TabPFN/LDA-XGBoost ROC comparison |
| 17 | `NB17_STRICT6_Descriptive_Reviewer_Audit.ipynb` | STRICT_6 sensitivity analysis and cultivar-wise descriptive morphometry |
| 99 | `NB99_Package_All_Results_UPDATED.ipynb` | Packaging/audit of derived outputs; use together with final NB16/NB17 exports |

Notebook 11 was a housekeeping utility and is not part of the scientific workflow. NB15 generated an earlier fixed-width calibration-gap visualization and is **superseded by NB16**; it is not part of the final manuscript workflow.

## Dataset placement

The notebooks were originally run with the dataset stored in the project Google Drive workspace. The raw dataset is not included in this public repository.

Authorized users should place the dataset at the path expected by the notebooks or adapt the path configuration in NB00.

## Strict calibration design

The final probability-reliability analysis is implemented in NB16.

For each outer-test fold:

1. only the corresponding outer-training partition is used to generate three-fold internal OOF probabilities;
2. temperature scaling is estimated from those internal OOF predictions;
3. selective-prediction thresholds are also estimated from those internal OOF predictions;
4. the resulting temperature and thresholds are applied to the untouched outer-test predictions.

Therefore, the evaluated outer-test fold does not contribute labels or predictions to estimation of its own temperature or rejection threshold.

## STRICT_6

NB17 defines the strict six-descriptor representation by removing `EquivDiameter` from REDUCED_7 because `EquivDiameter = sqrt(4*Area/pi)`. STRICT_6 is an additional sensitivity analysis and does not replace the prespecified FULL_11 versus REDUCED_7 comparison.

## Reproducibility boundaries

Because the source dataset is not publicly redistributed, public users can audit the code, experimental design, derived outputs, figures, statistical workflow, and calibration logic but cannot rerun the entire study without authorized access to the source data.

## TabPFN

TabPFN requires applicable Prior Labs model access in a fresh runtime. Authentication is provided securely at runtime and must never be committed to the repository. The pretrained checkpoint itself is not redistributed.

## Checkpoints

NB16 and NB17 write restart-safe checkpoints so interrupted Colab sessions can resume without repeating completed model-fold combinations.
