"""Budget-matched nested hyperparameter search for TabNet and the FT-Transformer-style network (Reviewer 3, comment 4).

Outer folds: StratifiedKFold(5, shuffle=True, random_state=seed), seeds 2026-2028 (identical to the main benchmark).
Inner folds: StratifiedKFold(3, shuffle=True, random_state=seed + fold), selection by mean inner macro-F1.
Search: the same 12 randomly sampled configurations (sampler seed 20261102) are evaluated in every outer fold.
Early stopping: 15% stratified validation subset taken from the training part only (patience 20, max 200 epochs).
Refit: best configuration refitted on the outer-training partition (same 85/15 split as NB05) and scored on the
untouched outer-test fold.

usage: python deep_tuning.py {tabnet|ft} <INIAP_Dataset.xlsx> <out_dir> [n_threads] [seeds, e.g. 2026,2027]
"""
import sys, os, json, time, random, itertools
import numpy as np, pandas as pd
import torch, torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import f1_score, accuracy_score, balanced_accuracy_score, log_loss

MODEL, DATA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
torch.set_num_threads(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
os.makedirs(OUT, exist_ok=True)
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
SEEDS = tuple(int(v) for v in sys.argv[5].split(',')) if len(sys.argv) > 5 else (2026, 2027, 2028)
TAG = MODEL + ('_' + '_'.join(map(str, SEEDS)) if len(sys.argv) > 5 else '')
N_CONF, MAX_EP, PAT = 12, 200, 20


def seed_everything(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)


# ------------------------------------------------------------------ search spaces
SPACE = {
    'tabnet': dict(n_da=[8, 16, 24, 32, 64], n_steps=[3, 4, 5, 7], gamma=[1.0, 1.3, 1.5, 2.0],
                   lambda_sparse=[1e-5, 1e-4, 1e-3], lr=[0.005, 0.01, 0.02, 0.05]),
    'ft': dict(d_token=[32, 64, 128], n_layers=[1, 2, 3], n_heads=[4, 8], dropout=[0.0, 0.1, 0.2],
               lr=[3e-4, 1e-3, 3e-3], weight_decay=[1e-5, 1e-4, 1e-3]),
}[MODEL]
rng = random.Random(20261102)
grid = [dict(zip(SPACE, v)) for v in itertools.product(*SPACE.values())]
CONFS = rng.sample(grid, N_CONF)
DEFAULT = (dict(n_da=8, n_steps=3, gamma=1.3, lambda_sparse=1e-3, lr=0.02) if MODEL == 'tabnet'
           else dict(d_token=64, n_layers=2, n_heads=4, dropout=0.1, lr=1e-3, weight_decay=1e-4))
if DEFAULT not in CONFS:
    CONFS[-1] = DEFAULT          # the original fixed configuration is always one of the candidates
json.dump(CONFS, open(f'{OUT}/{MODEL}_configurations.json', 'w'), indent=1)


# ------------------------------------------------------------------ models
class FTTransformer(nn.Module):  # identical architecture to NB05, with tunable size
    def __init__(self, n_features, n_classes, d_token=64, n_heads=4, n_layers=2, dropout=0.1):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(n_features, d_token) * 0.02)
        self.bias = nn.Parameter(torch.zeros(n_features, d_token))
        self.cls = nn.Parameter(torch.zeros(1, 1, d_token))
        layer = nn.TransformerEncoderLayer(d_model=d_token, nhead=n_heads, dim_feedforward=d_token * 4,
                                           dropout=dropout, batch_first=True, activation='gelu', norm_first=True)
        self.encoder = nn.TransformerEncoder(layer, num_layers=n_layers)
        self.head = nn.Sequential(nn.LayerNorm(d_token), nn.Linear(d_token, n_classes))

    def forward(self, x):
        tok = x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)
        z = self.encoder(torch.cat([self.cls.expand(x.size(0), -1, -1), tok], dim=1))
        return self.head(z[:, 0])


class DS(Dataset):
    def __init__(self, X, y): self.X, self.y = torch.tensor(X), torch.tensor(y, dtype=torch.long)
    def __len__(self): return len(self.X)
    def __getitem__(self, i): return self.X[i], self.y[i]


def fit_predict(c, Xtr, ytr, Xv, yv, Xte, n_classes, seed):
    """Train with early stopping on (Xv, yv); return class probabilities for Xte and epochs used."""
    seed_everything(seed)
    if MODEL == 'tabnet':
        from pytorch_tabnet.tab_model import TabNetClassifier
        m = TabNetClassifier(n_d=c['n_da'], n_a=c['n_da'], n_steps=c['n_steps'], gamma=c['gamma'],
                             lambda_sparse=c['lambda_sparse'], optimizer_params=dict(lr=c['lr']),
                             seed=seed, verbose=0, device_name=DEVICE)
        m.fit(Xtr, ytr, eval_set=[(Xv, yv)], eval_metric=['balanced_accuracy'], max_epochs=MAX_EP,
              patience=PAT, batch_size=256, virtual_batch_size=128)
        return m.predict_proba(Xte), int(m.best_epoch) + 1
    model = FTTransformer(Xtr.shape[1], n_classes, c['d_token'], c['n_heads'], c['n_layers'], c['dropout']).to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=c['lr'], weight_decay=c['weight_decay'])
    loss_fn = nn.CrossEntropyLoss()
    gen = torch.Generator(); gen.manual_seed(seed)
    dl = DataLoader(DS(Xtr, ytr), batch_size=128, shuffle=True, generator=gen)
    vX = torch.tensor(Xv, device=DEVICE)
    best, state, stale, ep = -1, None, 0, 0
    for ep in range(MAX_EP):
        model.train()
        for xb, yb in dl:
            opt.zero_grad(set_to_none=True)
            loss_fn(model(xb.to(DEVICE)), yb.to(DEVICE)).backward(); opt.step()
        model.eval()
        with torch.no_grad():
            s = f1_score(yv, model(vX).argmax(1).cpu().numpy(), average='macro')
        if s > best + 1e-5:
            best, stale = s, 0
            state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        else:
            stale += 1
        if stale >= PAT:
            break
    model.load_state_dict(state); model.eval()
    with torch.no_grad():
        return torch.softmax(model(torch.tensor(Xte, device=DEVICE)), 1).cpu().numpy(), ep + 1


def prep(Xa, ya, train_idx, extra, seed):
    """85/15 stratified split of train_idx; scaler fitted on the 85% part only."""
    tri, vi = train_test_split(train_idx, test_size=.15, stratify=ya[train_idx], random_state=seed)
    sc = StandardScaler().fit(Xa[tri])
    f = lambda a: sc.transform(a).astype(np.float32)
    return f(Xa[tri]), ya[tri], f(Xa[vi]), ya[vi], f(extra)


# ------------------------------------------------------------------ main loop (restart-safe)
df = pd.read_excel(DATA).rename(columns={'AspectRation': 'AspectRatio'})
X = df.drop(columns='Class').values.astype(np.float32)
le = LabelEncoder(); y = le.fit_transform(df['Class'].astype(str)); K = len(le.classes_)
CK = f'{OUT}/{TAG}_checkpoint.json'
done = json.load(open(CK)) if os.path.exists(CK) else {'outer': [], 'inner': [], 'oof': []}
fin = {(r['seed'], r['outer_fold']) for r in done['outer']}

for seed in SEEDS:
    outer = StratifiedKFold(5, shuffle=True, random_state=seed)
    for fold, (tr, te) in enumerate(outer.split(X, y), start=1):
        if (seed, fold) in fin:
            continue
        fs = seed + fold; t_fold = time.time()
        inner = list(StratifiedKFold(3, shuffle=True, random_state=fs).split(X[tr], y[tr]))
        scores = []
        for ci, c in enumerate(CONFS):
            f1s = []
            for k, (itr, ite) in enumerate(inner, start=1):
                Xa, ya = X[tr], y[tr]
                Xt, yt, Xv, yv, Xe = prep(Xa, ya, itr, Xa[ite], fs)
                p, ep = fit_predict(c, Xt, yt, Xv, yv, Xe, K, fs)
                f1s.append(f1_score(ya[ite], p.argmax(1), average='macro'))
                done['inner'].append(dict(seed=seed, outer_fold=fold, config=ci, inner_fold=k, f1_macro=f1s[-1], epochs=ep))
            scores.append(np.mean(f1s))
        best = int(np.argmax(scores))
        t0 = time.time()
        Xt, yt, Xv, yv, Xe = prep(X, y, tr, X[te], fs)        # same 85/15 split as NB05
        p, ep = fit_predict(CONFS[best], Xt, yt, Xv, yv, Xe, K, fs)
        pred = p.argmax(1)
        done['outer'].append(dict(model=f'{MODEL}_tuned', seed=seed, outer_fold=fold, best_config=best,
                                  best_inner_f1=float(scores[best]), f1_macro=f1_score(y[te], pred, average='macro'),
                                  accuracy=accuracy_score(y[te], pred), balanced_accuracy=balanced_accuracy_score(y[te], pred),
                                  log_loss=log_loss(y[te], np.clip(p, 1e-15, 1), labels=np.arange(K)),
                                  epochs=ep, refit_seconds=time.time() - t0, fold_seconds=time.time() - t_fold, **CONFS[best]))
        done['oof'] += [dict(seed=seed, outer_fold=fold, row_id=int(i), y_true=le.classes_[y[i]], y_pred=le.classes_[pred[j]],
                             **{f'prob_{c}': float(p[j, k]) for k, c in enumerate(le.classes_)}) for j, i in enumerate(te)]
        json.dump(done, open(CK, 'w'))
        r = done['outer'][-1]
        print(f'{MODEL} seed {seed} fold {fold}: best={best} inner={r["best_inner_f1"]:.4f} test={r["f1_macro"]:.4f} '
              f'({r["fold_seconds"]:.0f}s)', flush=True)

for key in ('outer', 'inner', 'oof'):
    pd.DataFrame(done[key]).to_csv(f'{OUT}/{TAG}_tuned_{key}.csv', index=False)
print('finished', TAG)
