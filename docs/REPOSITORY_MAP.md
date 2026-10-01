# Repository Map

```text
INIAP-Dry-Bean-Morphometric-Classification/
├── README.md
├── AUTHORS.md
├── CITATION.cff
├── LICENSE
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
│   ├── NB14_Final_PCA_LDA_Calibration_Publication.ipynb
│   ├── NB16_Strict_Calibration_Selective_Reviewer_Audit.ipynb
│   ├── NB17_STRICT6_Descriptive_Reviewer_Audit.ipynb
│   └── NB99_Package_All_Results_UPDATED.ipynb
│
├── environment/
│   ├── ENVIRONMENT.md
│   └── exact_versions.json
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
│
├── tables/
│   ├── README.md
│   ├── analysis_summaries/
│   └── supplementary/
│
└── docs/
    ├── DATA_AVAILABILITY.md
    ├── SOFTWARE_AVAILABILITY.md
    ├── REPRODUCIBILITY.md
    ├── VALIDATION_PROTOCOL.md
    └── REPOSITORY_MAP.md
```

## Superseded workflow elements

NB15 and the earlier fixed-width calibration-gap visualization were superseded by the strict outer-training-only calibration workflow in NB16 and are not part of the final manuscript analysis.

## Excluded by design

The public repository does not contain:

- the original morphometric dataset;
- private TabPFN access credentials;
- pretrained model checkpoint files;
- Colab user identifiers;
- obsolete temporary notebooks or intermediate execution artifacts.

## Public-release principle

The repository separates restricted source observations from public computational reproducibility materials. Code, validation design, derived outputs, statistical summaries, final figures, and machine-readable supplementary tables are public; the morphometric source dataset remains subject to the manuscript's Data Availability Statement.
