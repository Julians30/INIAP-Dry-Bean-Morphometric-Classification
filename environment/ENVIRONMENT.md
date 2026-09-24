# Computational Environment

This file records the software environment captured during the final experimental workflow. It is provided for archival reproducibility and should be read together with the notebook-specific configuration.

## Captured environment

| Component | Version / value |
|---|---|
| Python | 3.13.15 |
| NumPy | 2.1.3 |
| pandas | 2.2.3 |
| scikit-learn | 1.6.1 |
| SciPy | 1.16.3 |
| statsmodels | 0.15.0 |
| XGBoost | 3.4.1 |
| CatBoost | 1.2.10 |
| TabPFN | 9.0.0 |
| PyTorch | 2.11.0+cu128 |
| GPU used for GPU-oriented stages | NVIDIA L4 |
| TabPFN device | CUDA |

The main repeated-CV seeds were **2026, 2027, and 2028**. The primary evaluation used five outer folds and, where model selection was required, three inner folds.

## Reproducibility note

The root `requirements.txt` lists the packages required by the public notebooks. This environment record reports versions actually captured during the completed workflow. Some utility-package versions were not preserved in the final run logs and are therefore not invented here.

TabPFN access may require authorization for the applicable pretrained checkpoint in a fresh runtime. No access token, private checkpoint, or credential is distributed in this repository.

## Hardware note

GPU-oriented deep-tabular and TabPFN stages were executed with CUDA available; the captured run information identifies an NVIDIA L4 GPU for the deep-tabular stage.

## Data boundary

The original morphometric dataset and raw images are not covered by the repository's MIT software license because they are not distributed in this repository. See `docs/DATA_AVAILABILITY.md`.
