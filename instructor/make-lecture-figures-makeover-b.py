"""Extra figures for the 2026-11 makeover of lecture decks 11-16.

Run from the repository root:  python3 instructor/make-lecture-figures-makeover-b.py

Writes new SVG files only; it does not overwrite figures made by the other
generator scripts. All numbers are computed from the supplied CSV files.
"""
from pathlib import Path
import csv
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from lecture_svg import INK, TEAL, PURPLE, RED, GREY  # noqa: E402
import matplotlib  # noqa: E402
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

matplotlib.rcParams.update({'svg.fonttype': 'none', 'font.size': 16,
                            'axes.spines.top': False, 'axes.spines.right': False,
                            'axes.labelsize': 17, 'figure.facecolor': 'white'})


def save(fig, stem, name):
    path = ROOT / 'lectures' / stem / name
    fig.tight_layout()
    fig.savefig(path, format='svg', bbox_inches='tight')
    plt.close(fig)
    print('wrote', path.relative_to(ROOT))


def records(name):
    with (ROOT / 'data' / name).open() as f:
        return list(csv.DictReader(f))


plants = records('seedlings.csv')
growth = {r['plant_id']: float(r['final_mm']) - float(r['initial_mm']) for r in plants}
initial = {r['plant_id']: float(r['initial_mm']) for r in plants}
treated_ids = [r['plant_id'] for r in plants if r['treatment'] == 'treated']

# Day 11: one unit slip (P21 entered as 4.38 instead of 43.8 mm) moves the treated mean.
correct = [growth[i] for i in treated_ids]
slipped = [4.38 - initial[i] if i == 'P21' else growth[i] for i in treated_ids]
fig, ax = plt.subplots(figsize=(10, 4.6))
for x, values, label in [(0, slipped, 'P21 left as 4.38'), (1, correct, 'P21 corrected to 43.8 mm')]:
    jitter = np.linspace(-0.08, 0.08, len(values))
    colours = [RED if i == 'P21' else PURPLE for i in treated_ids]
    ax.scatter(np.full(len(values), x) + jitter, values, s=70, color=colours, alpha=0.9, zorder=3)
    m = statistics.mean(values)
    ax.hlines(m, x - 0.25, x + 0.25, color=INK, linewidth=3, zorder=2)
    ax.text(x + 0.28, m, f'mean {m:.2f} mm', va='center', fontsize=16, color=INK)
p21 = treated_ids.index('P21')
ax.annotate('P21: growth −19.2 mm', (0 + np.linspace(-0.08, 0.08, 12)[p21], slipped[p21]),
            xytext=(0.35, -14), fontsize=15, color=RED,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.axhline(0, color=GREY, linewidth=1, linestyle='--')
ax.set(xticks=[0, 1], xticklabels=['P21 left as 4.38', 'P21 corrected to 43.8 mm'],
       ylabel='Treated growth (mm)', xlim=(-0.45, 1.75), ylim=(-25, 35))
save(fig, '11-data-quality', 'unit-slip-effect.svg')

# Day 11: inventing a zero for the unknown P06 final length.
available = [g for i, g in growth.items() if i != 'P06']
invented = available + [0 - initial['P06']]
fig, ax = plt.subplots(figsize=(9, 4.4))
labels = ['P06 kept as NA\n23 available growths', 'P06 final set to 0\n24 values, one invented']
for x, values, colour in [(0, available, TEAL), (1, invented, RED)]:
    m = statistics.mean(values)
    ax.scatter([x], [m], s=160, color=colour, zorder=3)
    ax.text(x, m + 0.4, f'{m:.2f} mm', ha='center', fontsize=20)
ax.set(xticks=[0, 1], xticklabels=labels, ylabel='Mean growth, all plants (mm)',
       xlim=(-0.5, 1.5), ylim=(15, 20))
save(fig, '11-data-quality', 'zero-invented.svg')
