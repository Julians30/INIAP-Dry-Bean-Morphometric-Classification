# INIAP Dry Bean Morphometric Classification

Reproducibility repository for the manuscript:

**Comparative Evaluation of Dimensionality Reduction, Machine Learning, and Deep Tabular Models for Morphometric Classification of INIAP Dry Bean Cultivars**

## Overview

This repository contains the computational workflow, analysis notebooks, derived results, publication figures, tables, and reproducibility documentation for morphometric classification of four certified INIAP dry bean cultivars.

The study evaluates classical machine-learning models, dimensionality-reduction pipelines, deep tabular models, and pretrained TabPFN under leakage-safe repeated nested stratified cross-validation.

## Study design

- **Biological unit:** one individual dry bean grain per row.
- **Sample size:** 4,000 grains.
- **Cultivars:** four INIAP dry bean cultivars, 1,000 grains per cultivar.
- **Primary representation:** 11 image-derived morphometric descriptors (`FULL_11`).
- **Redundancy analysis:** reduced seven-descriptor representation (`REDUCED_7`).
- **Repeated outer evaluation:** 3 seeds (2026, 2027, 2028) × 5 outer folds.
- **Inner model selection:** 3 inner folds where applicable.
- **Primary performance metric:** macro-F1.
- **Additional analyses:** calibration, equivalence testing, corrected inference, selective prediction, redundancy ablation, and learning curves.

## Cultivars

1. INIAP 420 Canario del Chota
2. INIAP 425 Blanco Fanesquero
3. INIAP 481 Rojo del Valle
4. INIAP 485 Urcuquí

## Repository organization

```text
.
├── README.md
├── .gitignore
├── requirements.txt
├── notebooks/
│   └── README.md
├── results/
│   └── README.md
├── figures/
│   └── README.md
├── tables/
│   └── README.md
└── docs/
    ├── DATA_AVAILABILITY.md
    ├── REPRODUCIBILITY.md
    └── VALIDATION_PROTOCOL.md
```

The analysis notebooks and selected derived outputs are added only after they have been audited for obsolete versions, embedded credentials, raw-data leakage, and manuscript consistency.

## Data availability

The original morphometric dataset and raw grain photographs are **not distributed in this repository**. The dataset may be made available to qualified researchers upon reasonable request to the corresponding author, subject to the applicable authorization conditions.

See [docs/DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md).

## Reproducibility

The notebooks follow the original Google Colab workflow and preserve the study's repeated nested stratified cross-validation design. The recommended execution sequence and expected outputs are documented in [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).

## Main reported results

Using the full 11-descriptor representation:

- **TabPFN:** mean macro-F1 = **0.9866**
- **LDA-XGBoost:** mean macro-F1 = **0.9797**
- **LDA-SVM:** mean macro-F1 = **0.9792**

TabPFN also achieved a Brier score of **0.0206** and a 10-bin expected calibration error (ECE) of **0.0023**.

These values are reported as study results; the original observations required to rerun the complete analysis are subject to the data-availability conditions above.

## Important reproducibility note

Repeated seeds are repeated evaluations of the same 4,000 physical grains. They are **not** treated as independent biological observations. Outer-test predictions are kept strictly separate from model selection and training.

## Software

Core dependencies are listed in [requirements.txt](requirements.txt). Exact package versions used in individual experimental runs are also recorded by the notebooks where available.

## Authors

- Bryan Iván Barahona-Montalván
- Julián Coronel-Reyes
- Bryan Orlando Vélez-San Martin
- Dara Castro-Chancay
- Ericka Yolanda Tacuri Armijos

See [AUTHORS.md](AUTHORS.md) for the manuscript author order.

## Citation

Machine-readable citation metadata are provided in [CITATION.cff](CITATION.cff). GitHub can use this file to display the repository's **Cite this repository** option.

## License

A repository license will be added after the final code/data-sharing license is confirmed. Until then, no license is implied.
