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
| 09 | `NB09_Statistical_Robustness_Equivalence.ipynb` | Corrected inference and equivalence sensitivity |
| 10 | `NB10_Publication_Quality_Figures_MDPI_FINAL_R13.ipynb` | Publication-quality benchmark figures |
| 12 | `NB12_Top2_Confusion_and_Learning_Curves_FIXED.ipynb` | TabPFN/LDA-XGBoost confusion matrices and learning curves |
| 13 | `NB13_Final_Publication_Figure_Polish.ipynb` | Figure-only polish |
| 14 | `NB14_Final_PCA_LDA_Publication.ipynb` | Combined PCA/LDA descriptive projection |
| 16 | `NB16_Strict_Calibration_Selective_Prediction.ipynb` | Final strict outer-training-only calibration, adaptive ECE, NLL/Brier CIs, AURC, Clopper-Pearson intervals, selective prediction, rejected-set composition, and TabPFN/LDA-XGBoost ROC comparison |
| 17 | `NB17_STRICT6_Descriptive_Sensitivity.ipynb` | STRICT_6 sensitivity analysis and cultivar-wise descriptive morphometry |
| 99 | `NB99_Package_All_Results_UPDATED.ipynb` | Packaging/audit of derived outputs; use together with final NB16/NB17 exports |

Notebook 11 was a housekeeping utility and is not part of the scientific workflow.

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

For computational efficiency and exact continuity with the primary benchmark, NB16 reuses the already saved leakage-safe outer-test OOF probabilities from the completed benchmark. It does **not** use those outer-test predictions to estimate calibration parameters. New calibration probabilities are generated separately through three-fold internal OOF prediction inside each outer-training partition, and only those internal predictions are used to fit the temperature and confidence threshold.

## STRICT_6

NB17 defines the strict six-descriptor representation by removing `EquivDiameter` from REDUCED_7 because `EquivDiameter = sqrt(4*Area/pi)`. STRICT_6 is an additional sensitivity analysis and does not replace the prespecified FULL_11 versus REDUCED_7 comparison.

## Reproducibility boundaries

Because the source dataset is not publicly redistributed, public users can audit the code, experimental design, derived outputs, figures, statistical workflow, and calibration logic but cannot rerun the entire study without authorized access to the source data.

## Exact fold generation

All models, including the revision analyses, use identical partitions generated with scikit-learn 1.6.1:

```python
from sklearn.model_selection import StratifiedKFold
for seed in (2026, 2027, 2028):
    outer = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    for fold, (tr, te) in enumerate(outer.split(X, y), start=1):
        inner = StratifiedKFold(n_splits=3, shuffle=True, random_state=seed + fold)
```

Rows are used in the original order of the dataset table, `y` is the label-encoded `Class` column
(`INIAP 420`, `INIAP 425`, `INIAP 481`, `INIAP 485`), and the column `AspectRation` is renamed `AspectRatio`.
Inner model selection uses `GridSearchCV(scoring="f1_macro")`. Deep tabular models additionally take a stratified
15% early-stopping subset from the training part only (`train_test_split(..., test_size=0.15, random_state=seed + fold)`).

## Image acquisition and feature extraction (upstream of this repository)

The morphometric table was produced by an upstream imaging workflow and is the starting point of this repository.
Certified seed of each cultivar was obtained from INIAP and kept in separate cultivar-labeled bags; 1000 grains per
cultivar were photographed individually (one grain per image) in 2026 inside a light box with a black background,
LED illumination and a fixed vertical support (photographic area about 15 × 19 cm; camera about 15 cm above the
background), using a single Xiaomi Redmi Note 15 smartphone (main rear camera, 3060 × 4080 pixels). Each image was
converted to grayscale, thresholded with Otsu's method, cleaned with a morphological opening, and segmented by
contour detection; the 11 descriptors were computed from the grain contour with standard OpenCV geometric
functions and the derived ratios defined in the manuscript (Section 2.1). All descriptors are in pixel units; no pixel-to-millimetre calibration was applied.
Seed-lot identifiers, production sites, harvest seasons and per-grain acquisition dates were not recorded.

## TabPFN

TabPFN requires applicable Prior Labs model access in a fresh runtime. Authentication is provided securely at runtime and must never be committed to the repository. The pretrained checkpoint itself is not redistributed.

Procedure used to obtain a compatible checkpoint:

1. Install the recorded version: `pip install tabpfn==9.0.0` (see `environment/exact_versions.json`).
2. Create a Prior Labs account and accept the TabPFN model license.
3. Provide the access token at runtime only (for example, through an environment variable or the Colab secrets
   manager); never write it into a notebook cell that is saved or committed.
4. Instantiate `TabPFNClassifier()` with default settings; on first use the package downloads the pretrained
   checkpoint recorded in the manuscript (`tabpfn-v3.5-20260909.safetensors`). No weights are fine-tuned on the
   present data.

## Revision analyses (first round of peer review)

The `revision/` directory contains the scripts and outputs added in response to the reviewers
(see `revision/README.md`).

## Checkpoints

NB16 and NB17 write restart-safe checkpoints so interrupted Colab sessions can resume without repeating completed model-fold combinations.
