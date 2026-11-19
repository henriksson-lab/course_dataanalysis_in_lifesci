"""Extra figures for the 2026-11 makeover of lecture decks 03 and 06-10.

Run from the repository root:  python3 instructor/make-lecture-figures-makeover-a.py

Writes new SVG files only; it does not overwrite figures made by the other
generator scripts. The diagrams are schematic; numbers shown on them come from
the supplied CSV files or from the cited public incidents (old .xls row limit
of 65,536 rows; gene symbols such as SEPT2 converted to dates).
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lecture_svg import Drawing, INK, TEAL, RED, GREY, BLUE, PALE  # noqa: E402


def out(stem, name):
    return ROOT / "lectures" / stem / name


def cell_column(d, x, y, header, values, width=210, fill="white", stroke=GREY, colours=None):
    """A one-column table: header row plus value rows."""
    d.rect(x, y, width, 50, fill="#dbe8f3", stroke=stroke, radius=0)
    d.text(x + width / 2, y + 34, header, size=24, anchor="middle", weight="bold")
    for i, value in enumerate(values):
        yy = y + 50 + i * 50
        d.rect(x, yy, width, 50, fill=fill, stroke=stroke, radius=0)
        colour = colours[i] if colours else INK
        d.text(x + width / 2, yy + 34, value, size=24, anchor="middle", fill=colour)


# --- Day 7: an old spreadsheet format silently drops rows ------------------
# (Gene names turned into dates are taught on Day 1: lectures/01-files/gene-dates.svg.)
d = Drawing(1000, 520, "An old .xls sheet holds at most 65,536 rows; rows beyond the limit are not saved")
d.text(500, 45, "Rows beyond the limit vanish", size=30, anchor="middle", weight="bold")
d.text(140, 110, "rows in the", size=22, anchor="middle")
d.text(140, 140, "results file", size=22, anchor="middle")
d.rect(240, 70, 170, 300, fill=PALE, stroke=TEAL, radius=0)
d.text(325, 210, "rows 1 to", size=22, anchor="middle")
d.text(325, 242, "65,536", size=28, anchor="middle", weight="bold")
d.rect(240, 370, 170, 120, fill="#f9e3e8", stroke=RED, radius=0)
d.line(225, 370, 425, 370, stroke=RED, width=4, dashed=True)
d.text(325, 425, "more rows", size=22, anchor="middle", fill=RED)
d.text(325, 455, "not saved", size=22, anchor="middle", fill=RED)
d.text(450, 110, "Old .xls sheet: 65,536 rows at most.", size=24)
d.text(450, 145, "No error message, no warning.", size=24)
d.text(450, 400, "UK, October 2020: about 16,000", size=24, fill=RED)
d.text(450, 435, "positive COVID-19 tests were", size=24, fill=RED)
d.text(450, 470, "missed from the daily counts.", size=24, fill=RED)
d.save(out("07-import", "row-limit.svg"))

# --- Day 6: clicks are not recorded, a script is ----------------------------
d = Drawing(1200, 520, "A spreadsheet result hides how it was made; a script lists every step and can be run again")
d.text(290, 45, "Clicking in a spreadsheet", size=30, anchor="middle", weight="bold")
cols = ["A", "B", "C"]
for j, c in enumerate(cols):
    d.rect(80 + j * 140, 80, 140, 46, fill="#dbe8f3", stroke=GREY, radius=0)
    d.text(150 + j * 140, 112, c, size=22, anchor="middle", weight="bold")
rows = [["20", "37", "17"], ["22", "40", "18"], ["19", "34", "15"]]
for i, row in enumerate(rows):
    for j, v in enumerate(row):
        d.rect(80 + j * 140, 126 + i * 46, 140, 46, fill="white", stroke=GREY, radius=0)
        d.text(150 + j * 140, 158 + i * 46, v, size=22, anchor="middle")
d.text(290, 330, "Which cells? Typed or calculated?", size=23, anchor="middle", fill=RED)
d.text(290, 365, "Sorted, deleted, pasted?", size=23, anchor="middle", fill=RED)
d.text(290, 400, "The clicks were not recorded.", size=23, anchor="middle", fill=RED)

d.line(600, 30, 600, 490, stroke="#cbd5e1", width=2)

d.text(900, 45, "Writing a script", size=30, anchor="middle", weight="bold")
d.path("M640,80 h500 l30,30 v220 h-530 Z", fill="#eef2ff", stroke=BLUE, width=3)
lines = ["initial_mm <- c(20, 22, 19)", "final_mm <- c(37, 40, 34)",
         "growth_mm <- final_mm - initial_mm", "growth_mm"]
for i, s in enumerate(lines):
    d.parts.append(f'<text x="660" y="{140 + i * 44}" font-family="DejaVu Sans Mono, monospace" '
                   f'font-size="21" fill="{INK}">{s.replace("<", "&lt;")}</text>')
d.text(900, 365, "Every step is written down.", size=23, anchor="middle", fill=TEAL)
d.text(900, 400, "Run it again: 17 18 15, every time.", size=23, anchor="middle", fill=TEAL)
d.save(out("06-r-basics", "click-vs-script.svg"))

# --- Day 9: copy-pasted numbers go stale -------------------------------------
d = Drawing(1200, 540, "A hand-copied report keeps old numbers after the data change; a rendered report is rebuilt from the data")
d.text(30, 50, "Copy and paste", size=28, weight="bold", fill=RED)
d.file(40, 80, "data (corrected)", width=150, height=110)
d.file(330, 80, "script", width=150, height=110)
d.arrow(205, 135, 315, 135, stroke=GREY)
d.arrow(495, 135, 640, 135, stroke=GREY, )
d.text(568, 120, "copy by hand", size=20, anchor="middle", fill=GREY)
d.rect(660, 70, 480, 140, fill="#fbeff2", stroke=RED)
d.text(680, 115, "Word: \"24 plants; mean", size=23)
d.text(680, 148, "growth 18.4 mm\"  + old figure", size=23)
d.text(680, 185, "still the numbers from before", size=21, fill=RED)

d.line(30, 270, 1170, 270, stroke="#cbd5e1", width=2)

d.text(30, 320, "R Markdown", size=28, weight="bold", fill=TEAL)
d.file(40, 350, "data (corrected)", width=150, height=110)
d.file(330, 350, "report.Rmd", width=150, height=110)
d.arrow(205, 405, 315, 405, stroke=TEAL)
d.arrow(495, 405, 640, 405, stroke=TEAL)
d.text(568, 390, "render", size=20, anchor="middle", fill=TEAL)
d.rect(660, 340, 480, 140, fill=PALE, stroke=TEAL)
d.text(680, 385, "report.html: text, numbers and", size=23)
d.text(680, 418, "figure made from the data now", size=23)
d.text(680, 455, "change the data → render again", size=21, fill=TEAL)
d.save(out("09-rmarkdown", "copy-paste-stale.svg"))

print("wrote row-limit.svg, click-vs-script.svg, copy-paste-stale.svg")
