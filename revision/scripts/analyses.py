import sys, os, numpy as np, pandas as pd, warnings, time
warnings.filterwarnings('ignore')
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import f1_score
REPO, DATA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
A = pd.read_csv(f'{REPO}/results/model_performance/all_metrics_harmonized.csv')
F = A[A.feature_set == 'FULL_11']
A8 = pd.read_csv(f'{REPO}/tables/supplementary/S8_MCC_Kappa_FoldLevel.csv')
F8 = A8[A8.feature_set == 'FULL_11']

def corrected(a, b):
    """Nadeau-Bengio corrected resampled t-test, 15 pairs, test/train = 1/4."""
    m = F.pivot_table(index=['seed', 'outer_fold'], columns='model', values='f1_macro')
    d = (m[a] - m[b]).values; J = len(d)
    se = np.sqrt((1 / J + 0.25)) * d.std(ddof=1)
    t = d.mean() / se; p = 2 * stats.t.sf(abs(t), J - 1)
    h = stats.t.ppf(0.975, J - 1) * se
    return d.mean(), d.mean() - h, d.mean() + h, t, p, (d > 0).sum(), J

# 1) hybrid vs direct contrasts (R1-4)
pairs = [('LDA_XGBoost', 'XGBoost'), ('LDA_SVM', 'SVM_RBF'), ('LDA_MLP', 'MLP'),
         ('PCA_XGBoost', 'XGBoost'), ('PCA_SVM', 'SVM_RBF'), ('PCA_MLP', 'MLP')]
rows = []
for a, b in pairs:
    m, lo, hi, t, p, wins, J = corrected(a, b)
    rows.append(dict(hybrid=a, direct=b, mean_delta=m, ci_low=lo, ci_high=hi, t=t, p=p, folds_hybrid_better=f'{wins}/{J}'))
H = pd.DataFrame(rows); H['p_holm'] = multipletests(H.p, method='holm')[1]
H.to_csv(f'{OUT}/T_hybrid_vs_direct_corrected.csv', index=False); print(H.round(5).to_string())

# 2) TabPFN rank stability (R2 selection bias)
m = F.pivot_table(index=['seed', 'outer_fold'], columns='model', values='f1_macro')
rk = m.rank(axis=1, ascending=False, method='min')
print('TabPFN rank per fold:', rk['TabPFN'].values, ' first in', (rk['TabPFN'] == 1).sum(), 'of', len(rk))
seedmean = F.groupby(['seed', 'model']).f1_macro.mean().unstack()
print('rank by seed:\n', seedmean.rank(axis=1, ascending=False)['TabPFN'])
second = m.drop(columns='TabPFN').max(axis=1)
print('TabPFN minus best other per fold: mean', (m['TabPFN'] - second).mean(), 'min', (m['TabPFN'] - second).min())
pd.DataFrame({'tabpfn_rank': rk['TabPFN'], 'tabpfn_minus_best_other': m['TabPFN'] - second}).to_csv(f'{OUT}/T_tabpfn_rank_stability.csv')

# 3) timing (R3-5, R3-9)
T = F8.groupby('model')[['fit_search_seconds', 'refit_seconds', 'predict_seconds', 'predict_proba_seconds', 'n_test']].mean()
T['ms_per_1000_grains_proba'] = T.predict_proba_seconds / T.n_test * 1000 * 1000
T.sort_values('fit_search_seconds').to_csv(f'{OUT}/T_timing.csv'); print(T.round(4).to_string())

# 4) per-cultivar review burden and errors in rejected set (R2, R3-8)
C = pd.read_csv(f'{REPO}/results/selective_prediction/strict_rejected_composition_by_cultivar.csv')
S = pd.read_csv(f'{REPO}/results/selective_prediction/strict_selective_prediction_by_seed.csv')
print(S.columns.tolist())
C = C[C.target_coverage.isin([0.8, 0.9])].copy()
C['accept_rate'] = C.accepted_n / (C.accepted_n + C.rejected_n)
B = C.groupby(['model', 'target_coverage', 'cultivar']).agg(accepted_mean=('accepted_n', 'mean'), rejected_mean=('rejected_n', 'mean'),
       accept_rate_mean=('accept_rate', 'mean'), accept_rate_min=('accept_rate', 'min'), accept_rate_max=('accept_rate', 'max')).reset_index()
B.to_csv(f'{OUT}/T_review_burden_by_cultivar.csv', index=False); print(B.round(3).to_string())
S.to_csv(f'{OUT}/S_selective_raw.csv', index=False)
# 4b) rejected-set errors, computed separately per seed before averaging.
# A target_coverage=1.0 row contains the total errors for that seed/model.
totals = (S.loc[S.target_coverage == 1.0, ['model', 'seed', 'accepted_errors']]
          .rename(columns={'accepted_errors': 'total_errors'}))
q = S.loc[S.target_coverage.isin([0.8, 0.9, 0.95])].merge(
    totals, on=['model', 'seed'], how='inner', validate='many_to_one')
q['errors_in_rejected'] = q['total_errors'] - q['accepted_errors']
q['rejected_error_rate'] = q['errors_in_rejected'] / q['n_rejected']
q['share_errors_captured'] = q['errors_in_rejected'] / q['total_errors']
reject = q.groupby(['model', 'target_coverage'], as_index=False)[
    ['n_rejected', 'total_errors', 'accepted_errors', 'errors_in_rejected',
     'rejected_error_rate', 'share_errors_captured']].mean()
reject.to_csv(f'{OUT}/T_rejected_errors_summary.csv', index=False)

import os
if not os.path.exists(DATA): sys.exit("NO DATA")
# 5) simple-feature baselines with the same outer folds (R2)
df = pd.read_excel(DATA)
df = df.rename(columns={'AspectRation': 'AspectRatio'})
y = LabelEncoder().fit_transform(df['Class']); Xall = df.drop(columns='Class')
sets = {'FULL_11 (check)': list(Xall.columns), 'Area only': ['Area'], 'MajorAxisLength only': ['MajorAxisLength'],
        'Major + Minor axis': ['MajorAxisLength', 'MinorAxisLength'], 'Area + AspectRatio': ['Area', 'AspectRatio'],
        'Major + Minor + Extent': ['MajorAxisLength', 'MinorAxisLength', 'Extent']}
models = {'LogisticRegression': (Pipeline([('s', StandardScaler()), ('m', LogisticRegression(max_iter=5000))]), {'m__C': [0.1, 1, 10]}),
          'LDA': (Pipeline([('s', StandardScaler()), ('m', LinearDiscriminantAnalysis())]), {})}
res = []
for sname, cols in sets.items():
    X = Xall[cols].values
    for mname, (est, grid) in models.items():
        for seed in (2026, 2027, 2028):
            outer = StratifiedKFold(5, shuffle=True, random_state=seed)
            for fold, (tr, te) in enumerate(outer.split(X, y), start=1):
                inner = StratifiedKFold(3, shuffle=True, random_state=seed + fold)
                g = GridSearchCV(est, grid or {'s__with_mean': [True]}, scoring='f1_macro', cv=inner).fit(X[tr], y[tr])
                t0 = time.perf_counter(); pr = g.predict(X[te]); dt = time.perf_counter() - t0
                res.append(dict(feature_set=sname, n_features=len(cols), model=mname, seed=seed, outer_fold=fold,
                                f1_macro=f1_score(y[te], pr, average='macro'), predict_seconds=dt))
R = pd.DataFrame(res); R.to_csv(f'{OUT}/T_simple_baselines_by_fold.csv', index=False)
Rs = R.groupby(['feature_set', 'n_features', 'model']).f1_macro.agg(['mean', 'std']).reset_index().sort_values('mean', ascending=False)
Rs.to_csv(f'{OUT}/T_simple_baselines_summary.csv', index=False); print(Rs.round(4).to_string())
# replication check against repository LogisticRegression / LDA FULL_11
chk = R[R.feature_set == 'FULL_11 (check)'].merge(F[['model', 'seed', 'outer_fold', 'f1_macro']].replace({'LogisticRegression': 'LogisticRegression'}),
        on=['model', 'seed', 'outer_fold'], suffixes=('_new', '_repo'))
print('replication max abs diff:', (chk.f1_macro_new - chk.f1_macro_repo).abs().groupby(chk.model).max().to_dict())
