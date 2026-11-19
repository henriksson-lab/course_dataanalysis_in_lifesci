"""Extra figures for the 2026-11 makeover of the Day 18 and Day 25 decks.

Run from the repository root:  python3 instructor/make-lecture-figures-makeover-c.py

All plotted numbers come from the course CSVs in data/. The script writes new
files only; it does not overwrite figures made by the older generator scripts.
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
from scipy import stats  # noqa: E402

matplotlib.rcParams.update({'svg.fonttype': 'none', 'font.size': 16,
                            'axes.spines.top': False, 'axes.spines.right': False,
                            'axes.labelsize': 17, 'figure.facecolor': 'white'})


def records(name):
    with (ROOT / 'data' / name).open() as f:
        return list(csv.DictReader(f))


def save(fig, stem, name):
    fig.tight_layout()
    fig.savefig(ROOT / 'lectures' / stem / name, format='svg', bbox_inches='tight')
    plt.close(fig)


# Day 18: the same photosynthesis data analysed with and without the pairing.
paired = records('paired.csv')
before = [float(r['before_umol_m2_s']) for r in paired]
after = [float(r['after_umol_m2_s']) for r in paired]
change = [a - b for a, b in zip(after, before)]
n = len(change)
mean_change = statistics.mean(change)
paired_half = stats.t.ppf(.975, n - 1) * statistics.stdev(change) / n ** .5
va, vb = statistics.variance(after) / n, statistics.variance(before) / n
welch_df = (va + vb) ** 2 / (va ** 2 / (n - 1) + vb ** 2 / (n - 1))
welch_half = stats.t.ppf(.975, welch_df) * (va + vb) ** .5
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.axvline(0, color=GREY, ls='--', lw=1.5)
rows = [(1, 'paired: one change\nper plant (correct)', paired_half, TEAL),
        (0, 'two separate groups\n(ignores the pairing)', welch_half, RED)]
for y, label, half, colour in rows:
    lo, hi = mean_change - half, mean_change + half
    ax.plot([lo, hi], [y, y], color=colour, lw=6, solid_capstyle='butt')
    ax.scatter([mean_change], [y], marker='D', s=110, color=INK, zorder=5)
    ax.text(lo, y + .2, f'{lo:.2f}', ha='center', fontsize=15, color=colour)
    ax.text(hi, y + .2, f'{hi:.2f}', ha='center', fontsize=15, color=colour)
ax.set(yticks=[0, 1], yticklabels=[rows[1][1], rows[0][1]], ylim=(-.5, 1.6), xlim=(-.3, 3.8),
       xlabel='After − before, 95% interval for the mean (µmol m⁻² s⁻¹)')
save(fig, '18-paired', 'pairing-intervals.svg')

# Day 25: algae observations with A11 circled at its own plotted position.
algae = records('algae.csv')
fig, ax = plt.subplots(figsize=(9.2, 4.3))
for index, group in enumerate(['reference', 'supplement']):
    rows = [r for r in algae if r['treatment'] == group and r['biomass_mg']]
    xs = [index + ((j % 5) - 2) * .035 for j in range(len(rows))]
    ys = [float(r['biomass_mg']) for r in rows]
    ax.scatter(xs, ys, color=[TEAL, PURPLE][index], s=65)
    ax.scatter([index], [statistics.mean(ys)], marker='D', s=120, color=INK, zorder=4)
    for x, y, r in zip(xs, ys, rows):
        if r['culture_id'] == 'A11':
            ax.scatter([x], [y], s=320, facecolors='none', edgecolors=RED, lw=2.5, zorder=5)
            ax.annotate('A11: 41.7 mg, recorded value\n(no evidence of an error)', xy=(x, y),
                        xytext=(x + .2, y - 1.5), fontsize=14, color=RED,
                        arrowprops={'arrowstyle': '-', 'color': RED})
ax.set_xticks([0, 1], ['reference (12)', 'supplement (11 available)'])
ax.set_ylabel('Dry biomass (mg)')
ax.set_xlim(-.45, 1.55)
ax.set_ylim(10, 46)
ax.text(1.5, 12, 'diamonds: group means', ha='right', fontsize=13, color=INK)
save(fig, '25-consolidate', 'a11-highlight.svg')
print('Wrote pairing-intervals.svg and a11-highlight.svg')

# Day 23: the ggplot shown on the slide, made by exactly that R code.
import subprocess  # noqa: E402
r_code = r'''
suppressPackageStartupMessages({library(readr); library(dplyr); library(ggplot2)})
duckweed <- read_csv("data/duckweed.csv", show_col_types = FALSE)
available <- duckweed |> filter(!is.na(biomass_mg))
p <- ggplot(available, aes(x = treatment, y = biomass_mg)) +
  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 23)) +
  labs(x = "Treatment", y = "Dry biomass after seven days (mg)") +
  theme_minimal()
ggsave("lectures/23-mini-study/duckweed-ggplot.png", p, width = 5, height = 4, dpi = 150)
'''
subprocess.run(['Rscript', '-e', r_code], cwd=ROOT, check=True)
print('Wrote duckweed-ggplot.png')
