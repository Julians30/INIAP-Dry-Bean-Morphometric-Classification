# Revision analyses — first round of peer review (AgriEngineering, agriengineering-4634256)

Additional analyses requested by the reviewers. All of them use the **identical partitions** of the main
benchmark (see `docs/REPRODUCIBILITY.md`, *Exact fold generation*). The source dataset is not included;
it is available from the corresponding author upon reasonable request.

| Script | Outputs | Manuscript / Supplement |
|---|---|---|
| `scripts/analyses.py` | `results/T_hybrid_vs_direct_corrected.csv`, `T_tabpfn_rank_stability.csv`, `T_review_burden_by_cultivar.csv`, `T_rejected_errors_summary.csv`, `T_simple_baselines_*.csv`, `T_timing.csv` | Sections 3.2, 3.3, 3.5; Tables S6c, S9, S10, S11 |
| `scripts/cpu_timing.py` | `results/T_cpu_timing_local.csv` | Section 4.2; Table S11 |
| `scripts/deep_tuning.py` | `results/deep_tabular_tuning/{tabnet,ft}_tuned_{outer,inner}.csv`, `*_configurations.json` | Section 2.6; Tables S12a–S12b |
| `scripts/regenerate_figures_1_3.py` | `figures/final_publication/Figure1–3_*.png` | Figures 1–3 |
| `scripts/compare_deep.py` | `results/deep_tabular_tuning/T_deep_tuned_*.csv` | Sections 3.2, 4.2; Table S12a |

## Usage

```bash
python revision/scripts/analyses.py <repo_root> <INIAP_Dataset.xlsx> <output_dir>
python revision/scripts/cpu_timing.py <INIAP_Dataset.xlsx> <output_dir>/T_cpu_timing_local.csv
python revision/scripts/deep_tuning.py tabnet <INIAP_Dataset.xlsx> <deep_dir> [n_threads] [seeds]
python revision/scripts/deep_tuning.py ft     <INIAP_Dataset.xlsx> <deep_dir> [n_threads] [seeds]
python revision/scripts/compare_deep.py <repo_root> <deep_dir>
```

`deep_tuning.py` is restart-safe (JSON checkpoint per model/seed subset) and can be split by seed, e.g.
`... ft data.xlsx deep 1 2026`, to run several processes in parallel.

## Budget-matched deep tabular search (Reviewer 3, comment 4)

- Same 12 configurations per model in every outer fold, sampled without replacement from the full grid
  (sampler seed 20261102); the original fixed configuration of NB05 is always a candidate.
- Inner selection: `StratifiedKFold(3, shuffle=True, random_state=seed + fold)`, mean inner macro-F1.
- Early stopping: stratified 15% subset of each (inner- or outer-) training split, max 200 epochs, patience 20.
- Refit: selected configuration on the outer-training partition with the same 85/15 split as NB05.
- Environment: CPU, PyTorch 2.11.0, pytorch-tabnet 4.1.0, scikit-learn 1.9.1.

| Model | Macro-F1, mean (SD) |
|---|---|
| TabPFN (reference) | 0.9866 (0.0038) |
| FT-Transformer-style, budget-matched search | 0.9743 (0.0043) |
| FT-Transformer-style, fixed configuration | 0.9736 (0.0056) |
| TabNet, budget-matched search | 0.9723 (0.0079) |
| TabNet, fixed configuration | 0.9706 (0.0067) |

Tuned vs. fixed: TabNet +0.0017 (corrected p = 0.78), FT-Transformer-style +0.0008 (p = 0.85).
Tuned vs. TabPFN: −0.0143 (Holm p = 0.009) and −0.0123 (Holm p < 0.001); tuned models were below TabPFN in 15/15 folds.

## Statistical procedures

- Corrected resampled t-test (Nadeau and Bengio): variance factor (1/J + n_test/n_train), J = 15, n_test/n_train = 0.25, df = 14.
- Paired bootstrap and exact McNemar results: `results/statistical_tests/`.
