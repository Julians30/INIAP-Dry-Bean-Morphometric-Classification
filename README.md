# INIAP Dry Bean Morphometric Classification

Reproducibility repository for the manuscript:

**Reliable Morphometric Classification of INIAP Dry Bean Cultivars Using Artificial Intelligence: TabPFN, Calibration, Selective Prediction, and Redundancy Ablation**

## Overview

This repository contains the computational workflow, audited analysis notebooks, derived results, publication figures, tables, and reproducibility documentation for morphometric classification of four certified INIAP dry bean cultivars.

The study compares classical machine learning models, PCA- and LDA-based pipelines, deep tabular models, and pretrained TabPFN under repeated nested stratified cross-validation. The final reliability analysis additionally uses strict outer-training-only calibration and selective prediction.

## Study design

- **Biological unit:** one individual dry bean grain per row.
- **Sample size:** 4,000 grains.
- **Cultivars:** four INIAP dry bean cultivars, 1,000 grains per cultivar.
- **Primary representation:** 11 morphometric descriptors (`FULL_11`).
- **Primary redundancy ablation:** seven-descriptor representation (`REDUCED_7`).
- **Strict redundancy sensitivity analysis:** six-descriptor representation (`STRICT_6`), which additionally removes `EquivDiameter` because it is exactly determined by `Area`.
- **Repeated outer evaluation:** 3 seeds (2026, 2027, 2028) × 5 outer folds.
- **Inner model selection:** 3 inner folds where applicable.
- **Primary discrimination metric:** macro-F1.
- **Probability-quality metrics:** negative log-likelihood (NLL), multiclass Brier score, adaptive expected calibration error (ECE), and area under the risk-coverage curve (AURC).
- **Selective prediction:** confidence thresholds estimated only from internal OOF predictions generated inside each outer-training partition, with exact Clopper-Pearson intervals for accepted-case accuracy.

## Cultivars

1. INIAP 420 
2. INIAP 425 
3. INIAP 481 
4. INIAP 485 

## Feature representations

### FULL_11
`Area`, `Perimeter`, `MajorAxisLength`, `MinorAxisLength`, `AspectRatio`, `ConvexArea`, `EquivDiameter`, `Extent`, `Solidity`, `roundness`, and `Compactness`.

### REDUCED_7
`Area`, `Perimeter`, `MajorAxisLength`, `MinorAxisLength`, `ConvexArea`, `EquivDiameter`, and `Extent`.

### STRICT_6
`Area`, `Perimeter`, `MajorAxisLength`, `MinorAxisLength`, `ConvexArea`, and `Extent`.

`STRICT_6` is an additional sensitivity analysis. It does not replace the prespecified FULL_11 versus REDUCED_7 ablation.

## Repository organization

```text
.
├── README.md
├── AUTHORS.md
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── environment/
├── notebooks/
├── results/
├── figures/
├── tables/
│   ├── analysis_summaries/
│   └── supplementary/
└── docs/
```

Notebook outputs and personal Colab execution metadata are excluded from the public notebook copies. Scientific code, analysis logic, validation structure, and machine-readable derived summaries are retained.

## Data availability

The morphometric dataset analyzed in this study is not publicly deposited and is not included in this repository. It may be made available by the corresponding author upon reasonable request, subject to prior authorization and the applicable conditions governing its use.

The source code, notebooks, experimental configurations, derived numerical results, tables, figures, and reproducibility documentation are publicly available in this repository.

See [docs/DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md).

## Supplementary materials

The manuscript includes supplementary tables supporting the descriptive morphometry, complete nonparametric effect-size analysis, STRICT_6 sensitivity analysis, strict calibration, high-confidence calibration diagnostics, selective prediction, equivalence testing, and additional model metrics. Machine-readable counterparts are organized under `tables/supplementary/`.

## Main reported results

Using the FULL_11 representation:

- **TabPFN:** mean macro-F1 = **0.9866**
- **LDA-XGBoost:** mean macro-F1 = **0.9797**
- **LDA-SVM:** mean macro-F1 = **0.9792**
- **Logistic regression:** mean macro-F1 = **0.9754**
- **SVM-RBF:** mean macro-F1 = **0.9760**

Using STRICT_6:

- **TabPFN:** mean macro-F1 = **0.9854**
- **LDA-XGBoost:** mean macro-F1 = **0.9796**

Under strict outer-training-only calibration, TabPFN achieved:

- **NLL:** 0.03536 (95% CI: 0.02809–0.04301)
- **Multiclass Brier score:** 0.02063 (95% CI: 0.01619–0.02573)
- **Adaptive equal-mass ECE:** 0.00068
- **AURC:** 0.000395

At the nominal 90% selective-prediction operating point, mean realized coverage was approximately 0.906 and accepted-case accuracy was approximately 0.9994. At the nominal 80% operating point, no accepted errors occurred in any of the three seeds; exact Clopper-Pearson intervals are reported in the manuscript and public summary tables.

## Important reproducibility notes

1. Repeated seeds are repeated evaluations of the same 4,000 physical grains; they are **not** additional independent biological observations.
2. All model selection and fitted preprocessing are restricted to outer-training data.
3. In the final strict calibration analysis, temperature and rejection thresholds for an outer-test fold are estimated only from internal OOF predictions generated within that fold's outer-training partition.
4. TabPFN model weights are not redistributed in this repository. Access to the pretrained model is subject to Prior Labs authentication and licensing conditions.

## Software and environment

Core dependencies are listed in [requirements.txt](requirements.txt). The captured computational environment is documented under [environment/](environment/).

## Authors

- Bryan Iván Barahona-Montalván
- Julián Coronel-Reyes
- Bryan Orlando Vélez-SanMartín
- Ericka Yolanda Tacuri-Armijos

See [AUTHORS.md](AUTHORS.md) for the manuscript author order.

## Citation

Machine-readable citation metadata are provided in [CITATION.cff](CITATION.cff).

## License

The software, notebooks, documentation, and computational materials in this repository are released under the [MIT License](LICENSE). The original morphometric dataset is not distributed in this repository and is therefore not licensed under the MIT License.
