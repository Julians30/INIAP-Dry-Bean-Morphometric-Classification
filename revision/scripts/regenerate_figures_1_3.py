"""Regenerate Figures 1-3 at publication resolution (true minus signs, no thousands comma).

Usage: python regenerate_figures_1_3.py <INIAP_Dataset.xlsx> <output_dir>
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.unicode_minus': True})
import sys
OUT = sys.argv[2] if len(sys.argv) > 2 else '.'
df = pd.read_excel(sys.argv[1]).rename(columns={'AspectRation': 'AspectRatio'})
X = df.drop(columns='Class'); y = df['Class']

# ---------------- Figure 2: correlation matrix
lab = ['Area', 'Perimeter', 'Major axis', 'Minor axis', 'Aspect ratio', 'Convex area', 'Equiv. diameter',
       'Extent', 'Solidity', 'Roundness', 'Compactness']
C = X.corr().values
fig, ax = plt.subplots(figsize=(11.2, 9.6))
im = ax.imshow(C, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
for i in range(11):
    for j in range(11):
        v = C[i, j]
        ax.text(j, i, f'{v:.2f}'.replace('-', '−'), ha='center', va='center', fontsize=10.5,
                color='white' if abs(v) > 0.8 else 'black')
ax.set_xticks(range(11)); ax.set_xticklabels(lab, rotation=45, ha='right', fontsize=11)
ax.set_yticks(range(11)); ax.set_yticklabels(lab, fontsize=11)
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03); cb.set_label('Pearson correlation (r)', fontsize=11)
cb.ax.set_yticklabels([t.get_text() for t in cb.ax.get_yticklabels()])
fig.tight_layout(); fig.savefig(f'{OUT}/Figure2.png', dpi=600); plt.close(fig)

# ---------------- Figure 3: PCA and LDA projections
Z = StandardScaler().fit_transform(X)
P = PCA(n_components=2).fit(Z); Zp = P.transform(Z)
L = LDA(n_components=2).fit(Z, y); Zl = L.transform(Z)
# orientation as in the original figure: INIAP 485 at positive LD1, INIAP 425 at positive LD2, INIAP 485 at negative PC1
if Zl[y == 'INIAP 485', 0].mean() < 0: Zl[:, 0] *= -1
if Zl[y == 'INIAP 425', 1].mean() < 0: Zl[:, 1] *= -1
if Zp[y == 'INIAP 485', 0].mean() > 0: Zp[:, 0] *= -1
if Zp[y == 'INIAP 425', 1].mean() < 0: Zp[:, 1] *= -1
ev, el = P.explained_variance_ratio_ * 100, L.explained_variance_ratio_ * 100
cols = {'INIAP 420': '#1f77b4', 'INIAP 425': '#ff7f0e', 'INIAP 481': '#2ca02c', 'INIAP 485': '#d62728'}
fig, axs = plt.subplots(1, 2, figsize=(13, 5.4))
for k, c in cols.items():
    m = (y == k).values
    axs[0].scatter(Zp[m, 0], Zp[m, 1], s=14, alpha=.5, color=c, edgecolors='none', label=k)
    axs[1].scatter(Zl[m, 0], Zl[m, 1], s=14, alpha=.5, color=c, edgecolors='none', label=k)
axs[0].set_title('(a) Principal component analysis', fontsize=12)
axs[0].set_xlabel(f'PC1 ({ev[0]:.1f}% variance)'); axs[0].set_ylabel(f'PC2 ({ev[1]:.1f}% variance)')
axs[1].set_title('(b) Linear discriminant analysis', fontsize=12)
axs[1].set_xlabel(f'LD1 ({el[0]:.1f}% discriminant variance)'); axs[1].set_ylabel(f'LD2 ({el[1]:.1f}% discriminant variance)')
for a in axs: a.grid(alpha=.2)
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, loc='lower center', ncol=4, frameon=False, markerscale=2, fontsize=11)
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(f'{OUT}/Figure3.png', dpi=600); plt.close(fig)
print('PCA', ev.round(2), 'LDA', el.round(2))

# ---------------- Figure 1: analytical workflow
fig, ax = plt.subplots(figsize=(13.5, 7.6)); ax.set_xlim(-1, 139); ax.set_ylim(0, 76); ax.axis('off')
def box(x, y, w, h, title, lines, fill='#f4f2ec', tsize=12.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.3,rounding_size=0.8', fc=fill, ec='#333333', lw=1.3))
    ax.text(x + w / 2, y + h - 2.0, title, ha='center', va='top', fontsize=tsize, fontweight='bold')
    for i, t in enumerate(lines):
        ax.text(x + w / 2, y + h - 6.4 - 2.9 * i, t, ha='center', va='top', fontsize=10)
def arrow(x0, y0, x1, y1):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle='-|>', lw=1.3, color='#222222'))
W, G = 42, 4.5; X0 = [2, 2 + W + G, 2 + 2 * (W + G)]; XC = [x + W / 2 for x in X0]
box(XC[1] - 45.5, 65, 91, 9, 'Morphometric classification dataset', ['4000 individual grains · 4 INIAP cultivars · 11 quantitative descriptors'], fill='#e3e0d8', tsize=14)
box(X0[0], 43, W, 15, 'Morphometric representation', ['FULL_11 primary representation', 'REDUCED_7 redundancy ablation', 'STRICT_6 strict sensitivity analysis'])
box(X0[1], 43, W, 15, 'Repeated nested validation', ['3 seeds × 5 outer folds', '3 inner folds for model selection', 'Identical partitions for all models'])
box(X0[2], 43, W, 15, 'AI and ML model families', ['Direct classifiers · PCA/LDA hybrids', 'Deep tabular models · TabPFN', '19 models in total'])
box(XC[1] - 45.5, 27, 91, 9, 'Outer-fold out-of-fold predictions', ['One aligned prediction per grain, model, and seed'], fill='#e3e0d8')
box(X0[0], 1.5, W, 18, 'Predictive performance', ['Macro-F1 · accuracy · balanced accuracy', 'ROC and class-specific diagnostics', 'FULL_11 vs. REDUCED_7 vs. STRICT_6', 'Simple-feature baselines'])
box(X0[1], 1.5, W, 18, 'Robustness and inference', ['Corrected resampled t-tests · TOST/ROPE', 'Paired bootstrap · McNemar', 'Hybrid vs. direct contrasts', 'Budget-matched deep tabular search'])
box(X0[2], 1.5, W, 18, 'Reliability and decision support', ['NLL · Brier · adaptive ECE · AURC', 'Selective prediction · Clopper–Pearson', 'Cultivar-specific review burden', 'Learning curves · computing time'])
for xc in XC: arrow(XC[1], 64.6, xc, 58.6)
for xc in XC: arrow(xc, 42.6, XC[1], 36.4)
for xc in XC: arrow(XC[1], 26.6, xc, 19.9)
fig.savefig(f'{OUT}/Figure1.png', dpi=600, bbox_inches='tight', pad_inches=0.05); plt.close(fig)
