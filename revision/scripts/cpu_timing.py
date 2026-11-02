"""CPU timing (R3-5): largest XGBoost configuration of the search space (upper bound); single refit on an outer-training fold and prediction of the outer-test fold."""
import sys, time, numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
df = pd.read_excel(sys.argv[1]).rename(columns={'AspectRation': 'AspectRatio'})
y = LabelEncoder().fit_transform(df['Class']); X = df.drop(columns='Class').values
models = {
 'LDA-XGBoost': lambda: Pipeline([('s', StandardScaler()), ('l', LDA(n_components=3)),
     ('m', XGBClassifier(n_estimators=600, max_depth=5, learning_rate=0.1, subsample=1.0, colsample_bytree=1.0, n_jobs=2, tree_method='hist'))]),
 'LDA': lambda: Pipeline([('s', StandardScaler()), ('m', LDA())]),
 'Logistic regression': lambda: Pipeline([('s', StandardScaler()), ('m', LogisticRegression(C=10, max_iter=5000))]),
}
rows = []
for name, mk in models.items():
    fits, preds = [], []
    for seed in (2026, 2027, 2028):
        for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed).split(X, y):
            m = mk(); t0 = time.perf_counter(); m.fit(X[tr], y[tr]); fits.append(time.perf_counter() - t0)
            reps = []
            for _ in range(20):
                t0 = time.perf_counter(); m.predict_proba(X[te]); reps.append(time.perf_counter() - t0)
            preds.append(np.median(reps) / len(te) * 1000 * 1000)
    rows.append(dict(model=name, fit_s_median=np.median(fits), predict_ms_per_1000_median=np.median(preds)))
R = pd.DataFrame(rows); print(R.to_string()); R.to_csv(sys.argv[2], index=False)
