# Repository Map

```text
INIAP-Dry-Bean-Morphometric-Classification/
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   ├── README.md
│   ├── NB00_Project_Setup.ipynb
│   ├── NB01_Data_Audit_EDA.ipynb
│   ├── NB02_Dimensionality_Reduction.ipynb
│   ├── NB03_Baseline_Models_FIXED.ipynb
│   ├── NB04_Hybrid_Models_FIXED.ipynb
│   ├── NB05_Deep_Tabular_Models_FIXED.ipynb
│   ├── NB06_Statistical_Comparison_Interpretability_FIXED.ipynb
│   ├── NB07_ROC_Learning_Curves.ipynb
│   ├── NB08_Extended_Baselines_Redundancy_Ablation.ipynb
│   ├── NB09_Statistical_Robustness_Calibration_Selective_R2.ipynb
│   ├── NB10_Publication_Quality_Figures_MDPI_FINAL_R13.ipynb
│   ├── NB12_Top2_Confusion_and_Learning_Curves_FIXED.ipynb
│   ├── NB13_Final_Publication_Figure_Polish.ipynb
│   └── NB99_Package_All_Results_UPDATED.ipynb
│
├── results/
│   ├── README.md
│   ├── model_performance/
│   ├── redundancy/
│   ├── calibration/
│   ├── selective_prediction/
│   ├── learning_curves/
│   └── statistical_tests/
│
├── figures/
│   ├── README.md
│   └── final_publication/
│       ├── Figure1_...svg
│       ├── Figure2_...svg
│       ├── Figure3_...svg
│       ├── Figure4_...svg
│       ├── Figure5_...svg
│       ├── Figure6_...svg
│       ├── Figure7_...svg
│       └── Figure8_...svg
│
├── tables/
│   ├── README.md
│   └── analysis_summaries/
│
└── docs/
    ├── DATA_AVAILABILITY.md
    ├── REPRODUCIBILITY.md
    ├── VALIDATION_PROTOCOL.md
    └── REPOSITORY_MAP.md
```

## Excluded by design

The public repository does not contain:

- `INIAP_Dataset.xlsx` or any other raw morphometric data file;
- raw grain photographs;
- raw image-acquisition metadata;
- TabPFN access credentials;
- pretrained model checkpoints;
- Colab user identifiers or execution outputs;
- obsolete `OLD_DO_NOT_RUN`, archived, or temporary notebooks.

## Public-release principle

The repository separates **source data** from **computational reproducibility materials**. Code, validation design, selected derived outputs, statistical summaries, and final figures are public; restricted source observations remain subject to the manuscript's data-availability statement.
