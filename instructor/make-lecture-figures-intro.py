"""Rebuild the figures for the course-opening lecture (lectures/00-course-intro)."""

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lecture_svg import Drawing, INK, TEAL, PURPLE, RED, BLUE, PALE, GREY

OUT = ROOT / "lectures" / "00-course-intro"
OUT.mkdir(exist_ok=True)
matplotlib.rcParams.update({"svg.fonttype": "none", "font.size": 16,
                            "axes.spines.top": False, "axes.spines.right": False,
                            "axes.labelsize": 17, "figure.facecolor": "white"})


def cell(d, x, y, w, text, fill="#f8fafc", colour=INK, bold=False):
    d.rect(x, y, w, 56, fill=fill, stroke="#cbd5e1", radius=0)
    d.text(x + 16, y + 37, text, size=24, fill=colour, weight="bold" if bold else "normal")


# Gene symbols typed into a spreadsheet become dates.
d = Drawing(title="A spreadsheet converts gene symbols into dates")
d.text(110, 60, "You type", size=26, weight="bold")
d.text(690, 60, "The spreadsheet stores", size=26, weight="bold")
for i, (gene, date) in enumerate([("SEPT2", "2-Sep"), ("MARCH1", "1-Mar"), ("DEC1", "1-Dec"), ("TP53", "TP53")]):
    y = 90 + 66 * i
    cell(d, 110, y, 300, gene)
    changed = gene != date
    cell(d, 690, y, 300, date, fill="#fbe9ec" if changed else "#f8fafc",
         colour=RED if changed else INK, bold=changed)
    d.arrow(430, y + 28, 670, y + 28, stroke=RED if changed else GREY)
d.text(550, 400, "The gene name is gone; the date cannot be turned back reliably.", size=24, anchor="middle")
d.text(550, 445, "Gene lists in published supplementary files were affected.", size=24, anchor="middle", fill=GREY)
d.save(OUT / "gene-dates.svg")

# Old .xls row limit silently drops records.
d = Drawing(title="An old spreadsheet format stops at 65,536 rows")
for i, label in enumerate(["lab A.csv", "lab B.csv", "lab C.csv"]):
    d.file(60, 20 + 140 * i, "", width=110, height=80)
    d.text(190, 68 + 140 * i, label, size=22)
    d.arrow(300, 60 + 140 * i, 390, 225)
d.rect(400, 60, 300, 330, fill="#eef6f7", stroke=TEAL)
d.text(550, 105, "template.xls", size=26, anchor="middle", weight="bold")
for i in range(6):
    d.line(425, 140 + 34 * i, 675, 140 + 34 * i, stroke="#9fb7c0", width=2)
d.text(550, 365, "row 65,536 (last)", size=22, anchor="middle", fill=TEAL)
d.arrow(720, 160, 860, 160, stroke=TEAL)
d.text(880, 168, "reported", size=26, fill=TEAL, weight="bold")
d.arrow(720, 340, 860, 340, stroke=RED)
d.text(880, 330, "rows after the", size=24, fill=RED)
d.text(880, 362, "limit: dropped", size=24, fill=RED, weight="bold")
d.text(550, 455, "No error message. The missing results were simply not there.", size=24, anchor="middle")
d.save(OUT / "xls-row-limit.svg")

# From raw data to a report that re-runs.
d = Drawing(title="A reproducible analysis from raw file to report")
steps = [("raw data", "seedlings.csv", BLUE), ("code", "analysis.Rmd", PURPLE),
         ("checks", "counts, units", TEAL), ("results", "plot + test", TEAL), ("report", "report.html", BLUE)]
for i, (head, sub, colour) in enumerate(steps):
    x = 20 + 218 * i
    d.rect(x, 150, 180, 130, fill="#f8fafc", stroke=colour)
    d.text(x + 90, 205, head, size=27, anchor="middle", weight="bold", fill=colour)
    d.text(x + 90, 245, sub, size=21, anchor="middle")
    if i < len(steps) - 1:
        d.arrow(x + 184, 215, x + 214, 215)
d.path("M 1000 290 C 1000 420, 110 420, 110 290", stroke=GREY, width=3)
d.text(550, 455, "Change the data or a decision, re-run, and every number and figure updates.", size=24, anchor="middle")
d.text(550, 100, "Every step is written down, so anyone can repeat it.", size=26, anchor="middle")
d.save(OUT / "workflow.svg")

# How big biological data get, compared with spreadsheet limits.
items = [("Seedlings in this course (plants)", 24),
         ("96-well plate, 100 time points (readings)", 9_600),
         ("Single-cell experiment (cells)", 100_000),
         ("Microscopy image, 2048 × 2048 (pixels)", 4_194_304),
         ("One sequencing run (reads, approx.)", 1_000_000_000),
         ("Human genome (DNA letters)", 3_100_000_000)]
fig, ax = plt.subplots(figsize=(11, 4.6))
labels = [a for a, _ in items][::-1]
values = [b for _, b in items][::-1]
ax.barh(labels, values, color=TEAL)
ax.set_xscale("log")
ax.set_xlim(10, 2e10)
for limit, text, colour, y in [(65_536, "old .xls limit: 65,536 rows", RED, 5.3), (1_048_576, ".xlsx limit: 1,048,576 rows", PURPLE, 4.3)]:
    ax.axvline(limit, color=colour, linestyle="--", linewidth=2)
    ax.text(limit * 1.2, y, text, color=colour, fontsize=14, va="center",
            bbox=dict(facecolor="white", edgecolor="none", pad=1))
ax.set_xlabel("Number of rows needed (log scale)")
fig.tight_layout()
fig.savefig(OUT / "data-scale.svg", format="svg", bbox_inches="tight")
plt.close(fig)
print("Wrote course-intro figures to", OUT)
