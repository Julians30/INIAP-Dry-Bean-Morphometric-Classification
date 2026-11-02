"""Summarize the budget-matched deep tabular search and compare it with the fixed configurations and TabPFN.

usage: python compare_deep.py <repo_root> <deep_dir>
"""
import sys, glob, numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

REPO, D = sys.argv[1], sys.argv[2]
A = pd.read_csv(f'{REPO}/results/model_performance/all_metrics_harmonized.csv')
A = A[A.feature_set == 'FULL_11']
T = pd.concat([pd.read_csv(f) for f in glob.glob(f'{D}/*_tuned_outer.csv')], ignore_index=True)
T['model'] = T['model'].map({'tabnet_tuned': 'TabNet_tuned', 'ft_tuned': 'FTTransformer_tuned'})
T = T.drop_duplicates(['model', 'seed', 'outer_fold'])
F = pd.concat([A[['model', 'seed', 'outer_fold', 'f1_macro', 'log_loss']],
               T[['model', 'seed', 'outer_fold', 'f1_macro', 'log_loss']]], ignore_index=True)
W = F.pivot_table(index=['seed', 'outer_fold'], columns='model', values='f1_macro')


def corrected(a, b, ratio=0.25):
    d = (W[a] - W[b]).dropna().values; J = len(d)
    se = np.sqrt(1 / J + ratio) * d.std(ddof=1)
    t = d.mean() / se; p = 2 * stats.t.sf(abs(t), J - 1); h = stats.t.ppf(.975, J - 1) * se
    return dict(contrast=f'{a} vs. {b}', mean_delta=d.mean(), ci_low=d.mean() - h, ci_high=d.mean() + h,
                t=t, p=p, folds_a_better=f'{int((d > 0).sum())}/{J}', n=J)


summ = (F.groupby('model').agg(f1_mean=('f1_macro', 'mean'), f1_sd=('f1_macro', 'std'),
                               logloss_mean=('log_loss', 'mean'), n=('f1_macro', 'size'))
        .loc[lambda s: s.index.isin(['TabNet', 'TabNet_tuned', 'FTTransformer', 'FTTransformer_tuned', 'TabPFN',
                                     'LDA_XGBoost', 'LogisticRegression', 'SVM_RBF'])]
        .sort_values('f1_mean', ascending=False))
summ.to_csv(f'{D}/T_deep_tuned_summary.csv'); print(summ.round(4).to_string())

rows = []
for tuned, fixed in (('TabNet_tuned', 'TabNet'), ('FTTransformer_tuned', 'FTTransformer')):
    if tuned in W:
        rows += [corrected(tuned, fixed), corrected(tuned, 'TabPFN'), corrected(tuned, 'LDA_XGBoost'),
                 corrected(tuned, 'LogisticRegression')]
C = pd.DataFrame(rows)
C['family'] = C.contrast.str.split(' vs. ').str[1].map(
    lambda b: 'tuned vs. fixed' if b in ('TabNet', 'FTTransformer') else ('vs. TabPFN' if b == 'TabPFN' else 'vs. conventional'))
C['p_holm'] = C.groupby('family').p.transform(lambda p: multipletests(p, method='holm')[1])  # Holm within each family
C.to_csv(f'{D}/T_deep_tuned_tests.csv', index=False); print(C.round(4).to_string())

cfg = T.groupby('model').best_config.value_counts().rename('n_folds').reset_index()
cfg.to_csv(f'{D}/T_deep_tuned_selected_configs.csv', index=False); print(cfg.to_string())
tim = T.groupby('model').agg(fold_minutes=('fold_seconds', lambda s: s.mean() / 60), refit_s=('refit_seconds', 'mean'),
                             epochs=('epochs', 'mean'))
tim.to_csv(f'{D}/T_deep_tuned_timing.csv'); print(tim.round(2).to_string())
