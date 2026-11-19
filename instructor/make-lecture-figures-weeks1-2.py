"""Rebuild the local SVG teaching diagrams for lecture days 1–10."""

from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lecture_svg import Drawing, INK, TEAL, PURPLE, RED, BLUE, PALE, GREY


def save(drawing, stem, name):
    drawing.save(ROOT / "lectures" / stem / name)


def label_box(d, x, y, w, h, label, fill=PALE, colour=TEAL, size=25):
    d.rect(x, y, w, h, fill=fill, stroke=colour)
    d.text(x + w / 2, y + h / 2 + 9, label, size=size, anchor="middle")


def table(d, x, y, headers, rows, widths, row_colours=None):
    for i, row in enumerate([headers] + rows):
        offset = x
        for j, cell in enumerate(row):
            fill = "#dceaf6" if i == 0 else (row_colours or {}).get(i, "#f8fafc")
            d.rect(offset, y + 52 * i, widths[j], 50, fill=fill, stroke="#cbd5e1", radius=0)
            d.text(offset + 12, y + 52 * i + 33, cell, size=21, weight="bold" if i == 0 else "normal")
            offset += widths[j]


def tree(stem, name, highlight="data"):
    d = Drawing(title="Project folders form a hierarchy")
    d.folder(425, 25, "course project", 250, 95)
    for x, label in [(60, "data"), (440, "output"), (820, "reports")]:
        d.line(550, 122, x + 110, 200, stroke=TEAL if label == highlight else GREY)
        d.folder(x, 200, label)
    d.file(80, 345, "seedlings.csv", width=180, height=85)
    d.file(460, 345, "growth.png", width=180, height=85)
    d.file(840, 345, "notes.txt", width=180, height=85)
    for x in [170, 550, 930]:
        d.line(x, 302, x, 340)
    save(d, stem, name)


# Day 1: files, applications, copies, and finding saved work.
stem = "01-files"
d = Drawing(title="One file can be read by different applications")
d.file(70, 150, "seedlings.csv", width=215, height=180)
d.arrow(315, 200, 590, 110)
d.arrow(315, 290, 590, 360)
d.rect(620, 50, 400, 125, fill="#f1f5f9", stroke=BLUE)
d.text(820, 95, "Text editor", anchor="middle", weight="bold")
d.text(650, 140, "P01,control,25.7,44.3", size=23)
d.rect(620, 295, 400, 125, fill="#f1f5f9", stroke=PURPLE)
table(d, 645, 310, ["ID", "initial", "final"], [["P01", "25.7", "44.3"]], [105, 120, 120])
d.text(430, 465, "The saved file is not the application window.", anchor="middle", size=27)
save(d, stem, "file-and-applications.svg")
tree(stem, "find-the-file.svg")
d = Drawing(title="A raw file and its separate practice copy")
d.folder(80, 40, "data")
d.file(100, 185, "seedlings.csv", width=190, height=150)
d.folder(780, 40, "output")
d.file(780, 185, "practice.csv", width=190, height=150)
d.arrow(335, 260, 725, 260)
d.text(530, 220, "copy", anchor="middle", weight="bold")
d.text(190, 430, "original retained", anchor="middle", fill=TEAL)
d.text(875, 430, "edit this copy", anchor="middle", fill=PURPLE)
save(d, stem, "copy-preserves-source.svg")
d = Drawing(title="Saving makes an edited note available after reopening")
for x, title in [(40, "Edit in memory"), (430, "Save to disk"), (810, "Reopen file")]:
    d.rect(x, 100, 250, 240, fill="#f1f5f9", stroke=BLUE)
    d.text(x + 125, 65, title, anchor="middle", size=25)
    for i, w in enumerate([160, 180, 130]):
        d.line(x + 35, 155 + i * 52, x + 35 + w, 155 + i * 52, stroke=TEAL, width=6)
d.arrow(310, 220, 410, 220)
d.arrow(700, 220, 790, 220)
d.text(550, 430, "Check the folder and filename, then close and reopen.", anchor="middle")
save(d, stem, "save-and-reopen.svg")

# Day 2: hierarchical locations and computer components.
stem = "02-folders-computers"
tree(stem, "project-tree.svg")
d = Drawing(title="A relative path depends on the starting folder")
d.folder(60, 70, "course project", width=265)
d.folder(60, 300, "reports", width=265)
d.folder(760, 70, "data", width=240)
d.file(790, 270, "seedlings.csv", width=180, height=105)
d.arrow(350, 125, 725, 125, stroke=TEAL)
d.text(540, 85, "data/seedlings.csv", anchor="middle", size=23)
d.arrow(350, 355, 725, 355, stroke=RED)
d.text(540, 320, "same words, wrong start", anchor="middle", size=23, fill=RED)
d.line(760, 390, 1000, 430, stroke=RED)
d.line(760, 430, 1000, 390, stroke=RED)
d.text(550, 475, "The file did not move; your starting point changed.", anchor="middle")
save(d, stem, "relative-start.svg")
d = Drawing(title="Storage, RAM, and CPU have different roles")
d.rect(60, 130, 270, 210, fill="#eef2ff", stroke=BLUE)
d.text(195, 190, "Storage", anchor="middle", weight="bold")
d.file(130, 225, "saved CSV", width=125, height=60)
d.rect(420, 130, 270, 210, fill=PALE)
d.text(555, 190, "RAM", anchor="middle", weight="bold")
for i, height in enumerate([45, 80, 60, 95]):
    d.rect(455 + i * 48, 310 - height, 30, height, fill=TEAL, stroke=TEAL, radius=0)
d.rect(810, 150, 190, 170, fill="#f4eefb", stroke=PURPLE)
d.text(905, 235, "CPU", anchor="middle", weight="bold", size=35)
d.arrow(340, 235, 405, 235)
d.arrow(700, 235, 795, 235)
d.text(195, 420, "saved between sessions", anchor="middle", size=23)
d.text(555, 420, "working information", anchor="middle", size=23)
d.text(905, 420, "instructions", anchor="middle", size=23)
save(d, stem, "computer-components.svg")
d = Drawing(title="Laptop, Ubuntu home, and remote storage are distinct locations")
for x, title, subtitle in [(20, "Windows / Mac", "laptop project"), (390, "Local Ubuntu", "Windows users' shell"), (760, "Remote Linux", "another computer")]:
    d.rect(x + 20, 100, 290, 180, fill="#f8fafc", stroke=BLUE)
    d.line(x + 165, 285, x + 165, 325, stroke=BLUE, width=6)
    d.line(x + 100, 325, x + 230, 325, stroke=BLUE, width=6)
    d.text(x + 165, 60, title, anchor="middle", weight="bold", size=26)
    d.folder(x + 70, 160, "home", width=190, height=90)
    d.text(x + 165, 390, subtitle, anchor="middle", size=23)
d.arrow(345, 195, 405, 195)
d.arrow(715, 195, 775, 195)
d.text(550, 465, "Moving a window is not transferring a file.", anchor="middle")
save(d, stem, "different-locations.svg")

# Day 3: the same directory through two interfaces, and navigation.
stem = "03-terminal"
d = Drawing(title="File manager and terminal refer to the same folder")
d.rect(40, 70, 450, 330, fill="#f8fafc", stroke=BLUE)
d.text(265, 115, "File manager", anchor="middle", weight="bold")
d.folder(100, 180, "practice", width=220)
d.rect(610, 70, 450, 330, fill="#203247", stroke=INK)
d.text(835, 115, "Terminal", anchor="middle", fill="white", weight="bold")
d.text(645, 205, "$ ls", fill="white", size=30)
d.text(645, 265, "practice", fill="#bce9d2", size=30)
d.line(500, 235, 600, 235, stroke=TEAL, width=5)
d.text(550, 465, "Two views, one saved folder; each window has its own location.", anchor="middle", size=24)
save(d, stem, "two-views.svg")
d = Drawing(title="A command follows the shell prompt")
d.rect(70, 140, 960, 130, fill="#203247", stroke=INK)
d.text(115, 225, "anna@laptop:~$", size=36, fill="#bce9d2")
d.text(470, 225, "cd", size=36, fill="white")
d.text(585, 225, "practice", size=36, fill="white")
for x, end, label in [(280, 280, "prompt: do not type"), (490, 505, "command"), (685, 840, "argument: destination")]:
    d.arrow(x, 280, end, 370)
    d.text(end, 425, label, anchor="middle", size=23)
save(d, stem, "command-anatomy.svg")
d = Drawing(title="Changing directory changes the starting location")
d.folder(60, 70, "home", 230)
d.folder(430, 70, "workspace", 230)
d.folder(800, 70, "practice", 230)
d.arrow(315, 120, 410, 120)
d.arrow(685, 120, 780, 120)
d.text(360, 65, "cd", anchor="middle")
d.text(730, 65, "cd", anchor="middle")
d.arrow(905, 260, 550, 260, stroke=PURPLE)
d.text(730, 310, "cd ..", anchor="middle", fill=PURPLE)
d.text(550, 430, "pwd reports the location; it does not move you.", anchor="middle")
save(d, stem, "navigate-tree.svg")
d = Drawing(title="An empty directory is a valid directory")
d.folder(60, 70, "observations", width=310, height=120)
d.rect(570, 85, 460, 290, fill="#203247", stroke=INK)
d.text(610, 155, "$ ls", fill="white", size=30)
d.text(610, 280, "$", fill="white", size=30)
d.text(250, 350, "No visible entries", anchor="middle", size=27)
d.arrow(390, 205, 545, 205)
d.text(550, 455, "No names printed is different from an error message.", anchor="middle")
save(d, stem, "empty-is-valid.svg")

# Day 4: archive versus files, headers, selection, and a pipe.
stem = "04-inspect-archive"
d = Drawing(title="Extraction creates ordinary files without deleting the archive")
d.file(70, 145, "lab-data.zip", width=200, height=170)
d.arrow(330, 230, 610, 230)
d.text(470, 185, "unzip", anchor="middle", weight="bold")
d.folder(690, 50, "lab-data", width=260)
d.file(630, 230, "README.txt", width=150, height=105)
d.file(850, 230, "samples.tsv", width=150, height=105)
d.text(550, 450, "Archive remains; extracted files can now be inspected.", anchor="middle")
save(d, stem, "extract-archive.svg")
headers = ["sample_id", "treatment", "file"]
rows = [["S01", "control", "measurements/S01.csv"], ["S02", "control", "measurements/S02.csv"], ["S03", "treated", "measurements/S03.csv"], ["S04", "treated", "measurements/S04.csv"]]
d = Drawing(title="One header and four biological sample records")
table(d, 140, 80, headers, rows, [170, 200, 430])
d.text(60, 115, "1", anchor="middle", fill=BLUE)
d.text(60, 245, "+4", anchor="middle", fill=TEAL)
d.text(550, 425, "wc -l counts 5 lines; the experiment has 4 sample records.", anchor="middle", size=25)
save(d, stem, "manifest-lines.svg")
d = Drawing(title="Literal text search selects the two treated records")
table(d, 140, 70, headers, rows, [170, 200, 430], row_colours={3: "#d7f1e7", 4: "#d7f1e7"})
d.text(550, 430, "grep -F treated samples.tsv", anchor="middle", size=29)
save(d, stem, "grep-selection.svg")
d = Drawing(title="A pipe sends selected lines to the next program")
for i in range(4):
    d.line(60, 120 + i * 58, 250, 120 + i * 58, stroke=TEAL if i >= 2 else GREY, width=9)
d.arrow(290, 220, 390, 220)
label_box(d, 410, 145, 220, 150, "grep", size=35)
d.arrow(650, 220, 745, 220)
for i in range(2):
    d.line(775, 185 + i * 65, 910, 185 + i * 65, stroke=TEAL, width=9)
d.arrow(930, 220, 1000, 220)
d.text(1040, 240, "2", anchor="middle", size=62, fill=BLUE)
d.text(550, 420, "Four records → matching lines → wc -l → count", anchor="middle")
save(d, stem, "pipe-stream.svg")

# Day 5: collection for sharing, copies, and local versus remote work.
stem = "05-lab-files"
d = Drawing(title="A report folder is packaged into a separate archive")
d.folder(70, 65, "report", width=260)
d.file(80, 230, "findings.txt", width=170, height=110)
d.file(320, 230, "selected.txt", width=170, height=110)
d.arrow(540, 230, 760, 230)
d.text(650, 175, "zip -r", anchor="middle")
d.file(820, 140, "report-bundle.zip", width=190, height=170)
d.text(550, 445, "Keep the ordinary folder; inspect and test the ZIP.", anchor="middle")
save(d, stem, "package-report.svg")
d = Drawing(title="Copy retains two files; rename changes a name")
d.file(50, 70, "source.txt", width=150, height=100)
d.arrow(230, 120, 380, 120)
d.file(430, 70, "copy.txt", width=150, height=100)
d.text(780, 135, "cp: source remains", anchor="middle", fill=TEAL)
d.file(50, 300, "copy.txt", width=150, height=100)
d.arrow(230, 350, 380, 350, stroke=PURPLE)
d.file(430, 300, "notes.txt", width=150, height=100)
d.text(800, 365, "mv: new name / location", anchor="middle", fill=PURPLE)
save(d, stem, "copy-and-rename.svg")
d = Drawing(title="A displayed remote session does not synchronise files")
d.rect(60, 75, 350, 240, fill="#eef2ff", stroke=BLUE)
d.text(235, 130, "Laptop", anchor="middle", size=32)
d.folder(120, 180, "local files", width=230)
d.rect(690, 75, 350, 240, fill=PALE)
d.text(865, 130, "Remote computer", anchor="middle", size=32)
d.folder(750, 180, "remote files", width=230)
d.arrow(440, 150, 660, 150)
d.text(550, 115, "SSH / desktop", anchor="middle", size=23)
d.arrow(440, 365, 660, 365, stroke=PURPLE)
d.text(550, 420, "Explicit file transfer is a separate action.", anchor="middle", size=25)
save(d, stem, "remote-and-transfer.svg")
d = Drawing(title="A shell and an R console interpret different languages")
for x, title, command, colour in [(40, "Shell", "grep -F treated samples.tsv", TEAL), (600, "R console", "44.3 - 25.7", PURPLE)]:
    d.rect(x, 100, 460, 240, fill="#f8fafc", stroke=colour)
    d.text(x + 230, 155, title, anchor="middle", size=34, weight="bold")
    d.text(x + 230, 245, command, anchor="middle", size=24)
d.text(550, 435, "Choose the interface before typing the instruction.", anchor="middle")
save(d, stem, "two-languages.svg")

# Day 6: quantities, assignments, vectors, and matched observations.
stem = "06-r-basics"
d = Drawing(title="Growth is final length minus initial length")
for y, value, label, colour in [(150, 20, "initial: 20 mm", TEAL), (290, 37, "final: 37 mm", PURPLE)]:
    d.line(150, y, 150 + value * 20, y, stroke=colour, width=18)
    d.text(145, y - 40, label, size=29)
    for tick in range(0, value + 1, 5):
        d.line(150 + tick * 20, y - 17, 150 + tick * 20, y + 17, stroke=INK, width=2)
d.line(550, 360, 890, 360, stroke=RED, width=6)
d.text(720, 425, "growth: 17 mm", anchor="middle", size=31, fill=RED)
save(d, stem, "growth-is-change.svg")
d = Drawing(title="An assigned name refers to a value in this R session")
d.text(150, 145, "37 − 20", size=40)
d.arrow(360, 135, 550, 135)
label_box(d, 600, 60, 350, 150, "growth_mm → 17", fill="#eef2ff", colour=PURPLE, size=33)
d.file(150, 310, "day06.R", width=190, height=110)
d.arrow(385, 360, 600, 360)
d.text(760, 370, "run saved instructions", anchor="middle", size=26)
d.text(550, 470, "Saving a script and running it are different actions.", anchor="middle", size=25)
save(d, stem, "named-object.svg")
d = Drawing(title="Vector subtraction must match the same plant at each position")
for index, (plant, initial, final, change) in enumerate([("P01", 20, 37, 17), ("P02", 22, 40, 18), ("P03", 19, 34, 15)]):
    x = 100 + 350 * index
    d.text(x + 100, 45, plant, anchor="middle", size=30, weight="bold")
    label_box(d, x, 80, 200, 80, str(final), fill="#f4eefb", colour=PURPLE)
    label_box(d, x, 220, 200, 80, str(initial))
    d.arrow(x + 100, 170, x + 100, 210)
    d.text(x + 100, 385, str(change) + " mm", anchor="middle", size=35, fill=BLUE)
    d.arrow(x + 100, 310, x + 100, 345)
d.text(550, 470, "Position-by-position arithmetic needs matched observations.", anchor="middle", size=25)
save(d, stem, "matched-vectors.svg")
d = Drawing(title="Percentage yield compares collected mass with a supplied maximum")
label_box(d, 70, 80, 390, 110, "supplied maximum: 1.00 g", size=28)
d.rect(70, 250, 800, 85, fill="#f1f5f9", stroke=GREY, radius=0)
d.rect(70, 250, 496, 85, fill="#bce9d2", stroke=TEAL, radius=0)
d.text(318, 305, "collected: 0.62 g", anchor="middle", size=29)
d.text(980, 310, "62%", anchor="middle", size=44, fill=TEAL)
d.text(550, 435, "100 × 0.62 / 1.00 = 62; masses use the same units.", anchor="middle", size=27)
save(d, stem, "yield-ratio.svg")

# Day 7: importing changes representation, not the source file.
stem = "07-import"
d = Drawing(title="Import reads a saved CSV into an R object")
d.file(80, 145, "data/seedlings.csv", width=210, height=170)
d.arrow(350, 225, 650, 225)
d.text(500, 170, "read_csv()", anchor="middle", size=29)
d.rect(730, 110, 280, 230, fill=PALE)
d.text(870, 165, "R memory", anchor="middle", weight="bold")
d.text(870, 240, "seedlings", anchor="middle", size=32)
d.text(870, 295, "24 rows × 4 columns", anchor="middle", size=22)
d.text(550, 440, "The file remains on disk; the object lives in this session.", anchor="middle", size=25)
save(d, stem, "file-to-object.svg")
d = Drawing(title="Identifiers and treatments are text; measurements are numeric")
table(d, 70, 80, ["plant_id", "treatment", "initial_mm", "final_mm"],
      [["P01", "control", "25.7", "44.3"], ["P02", "control", "24.3", "32.3"], ["P13", "treated", "24.0", "54.8"]], [180, 250, 250, 250])
d.text(285, 390, "labels / text", anchor="middle", fill=PURPLE)
d.text(785, 390, "lengths / numeric / mm", anchor="middle", fill=TEAL)
d.text(550, 460, "One row = one plant; two lengths do not create two plants.", anchor="middle", size=25)
save(d, stem, "column-roles.svg")
tree(stem, "project-relative-path.svg")
d = Drawing(title="Missing values are not measured zeros")
for x, label, height, colour in [(110, "12 mm", 180, TEAL), (470, "NA", 0, RED), (830, "18 mm", 270, TEAL)]:
    d.line(x, 360, x + 140, 360, stroke=INK)
    if height:
        d.rect(x + 25, 360 - height, 90, height, fill=colour, stroke=colour, radius=0)
    else:
        d.text(x + 70, 270, "?", size=90, fill=RED, anchor="middle")
    d.text(x + 70, 415, label, anchor="middle", size=30)
d.text(550, 475, "Available-value mean: 15 mm from two observed measurements.", anchor="middle", size=24)
save(d, stem, "missing-not-zero.svg")

# Day 8: selecting rows/columns and the same plant viewed as change.
stem = "08-transform-plot"
d = Drawing(title="A calculated column keeps its link to the input measurements")
table(d, 80, 90, ["plant_id", "initial_mm", "final_mm", "growth_mm"],
      [["P01", "25.7", "44.3", "18.6"], ["P02", "24.3", "32.3", "8.0"]], [180, 240, 240, 240])
d.arrow(520, 310, 845, 310)
d.text(550, 390, "final − initial", anchor="middle", size=31)
d.text(550, 455, "A derived column does not overwrite the raw CSV.", anchor="middle")
save(d, stem, "derived-column.svg")
d = Drawing(title="Filtering chooses rows; selecting chooses columns")
table(d, 35, 95, ["ID", "group", "growth"], [["P01", "control", "18.6"], ["P13", "treated", "30.8"], ["P14", "treated", "21.4"]], [110, 160, 130], row_colours={2: "#d7f1e7", 3: "#d7f1e7"})
d.arrow(450, 210, 570, 210)
table(d, 620, 95, ["ID", "growth"], [["P13", "30.8"], ["P14", "21.4"]], [150, 230])
d.text(260, 420, "filter: which observations?", anchor="middle", size=25)
d.text(810, 420, "select: which variables?", anchor="middle", size=25)
save(d, stem, "rows-and-columns.svg")

# Data plots use matplotlib and the actual course measurements.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 16, "axes.spines.top": False, "axes.spines.right": False})
with (ROOT / "data/seedlings.csv").open() as handle:
    seedlings = list(csv.DictReader(handle))
fig, ax = plt.subplots(figsize=(10, 4.5))
for group, colour in [("control", TEAL), ("treated", PURPLE)]:
    records = [row for row in seedlings if row["treatment"] == group]
    ax.scatter([float(row["initial_mm"]) for row in records], [float(row["final_mm"]) for row in records], label=group, color=colour, s=70)
ax.set(xlabel="Initial length (mm)", ylabel="Final length (mm)")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(ROOT / "lectures/08-transform-plot/initial-final.svg")
plt.close(fig)

# Day 9: document dependencies and file products.
stem = "09-rmarkdown"
d = Drawing(title="R Markdown combines text and executable calculations into a report")
d.file(65, 80, "report.Rmd", width=200, height=250)
d.line(95, 145, 230, 145, stroke=GREY, width=7)
d.rect(95, 190, 140, 65, fill=PALE, stroke=TEAL)
d.line(95, 295, 230, 295, stroke=GREY, width=7)
d.arrow(320, 220, 660, 220)
d.text(490, 165, "render / Knit", anchor="middle", size=31)
d.file(740, 80, "report.html", width=245, height=250)
d.line(775, 145, 945, 145, stroke=GREY, width=7)
for x, y in [(790, 265), (835, 235), (875, 250), (920, 200)]:
    d.circle(x, y, 9, fill=TEAL)
d.text(550, 445, "Keep the source, inputs, and readable output.", anchor="middle")
save(d, stem, "render-report.svg")
d = Drawing(title="Report chunks execute in order with explicit dependencies")
for y, label in [(40, "1. load packages + import data"), (190, "2. calculate growth"), (340, "3. plot and interpret")]:
    label_box(d, 260, y, 580, 95, label, size=29)
d.arrow(550, 140, 550, 180)
d.arrow(550, 290, 550, 330)
save(d, stem, "chunk-order.svg")
d = Drawing(title="A console-only object is absent from an independent report render")
label_box(d, 70, 90, 370, 105, "interactive R session", fill="#f4eefb", colour=PURPLE)
label_box(d, 660, 90, 370, 105, "fresh report render", fill=PALE)
d.text(255, 290, "seedlings exists here", anchor="middle", size=27)
d.text(845, 290, "must import its own data", anchor="middle", size=27)
d.line(465, 235, 635, 235, stroke=RED, width=4)
d.line(500, 195, 600, 275, stroke=RED, width=4)
d.line(500, 275, 600, 195, stroke=RED, width=4)
d.text(550, 445, "Put prerequisites in the source; do not rely on remembered state.", anchor="middle", size=24)
save(d, stem, "fresh-session.svg")
d = Drawing(title="A reproducible report needs source and input as well as HTML")
for x, label in [(60, "report.Rmd"), (450, "seedlings.csv"), (840, "report.html")]:
    d.file(x, 110, label, width=180, height=190)
d.text(150, 420, "instructions + prose", anchor="middle", size=23)
d.text(540, 420, "saved measurements", anchor="middle", size=23)
d.text(930, 420, "readable result", anchor="middle", size=23)
save(d, stem, "three-files.svg")

# Day 10: design, observations, and portable reconstruction.
stem = "10-first-report"
d = Drawing(title="The experimental unit is the independently treated plant and pot")
for row, group in enumerate(["control", "treated"]):
    d.text(80, 105 + row * 220, group, size=31, weight="bold")
    for index in range(6):
        x = 340 + index * 120
        y = 130 + row * 220
        d.path(f'M{x-30},{y+25} h60 l-10,50 h-40 Z', fill="#bf8f63", stroke="#795438", width=2)
        d.line(x, y + 25, x, y - 60, stroke=TEAL, width=5)
        d.path(f'M{x},{y-20} q-50,-55 -45,-10 q35,25 45,10', fill="#8fcbaa", stroke=TEAL, width=2)
        d.path(f'M{x},{y-45} q50,-45 45,-5 q-35,25 -45,5', fill="#8fcbaa", stroke=TEAL, width=2)
d.text(550, 475, "Schematic: separate pots; the actual dataset has 12 per group.", anchor="middle", size=23)
save(d, stem, "independent-pots.svg")
d = Drawing(title="A report connects the biological question to observed evidence")
label_box(d, 40, 60, 310, 95, "Question: growth?", size=27)
d.arrow(375, 110, 500, 110)
d.rect(530, 45, 520, 140, fill="#f8fafc", stroke=BLUE)
for x, y in [(610, 145), (665, 125), (730, 150), (810, 95), (865, 120), (950, 75)]:
    d.circle(x, y, 9, fill=TEAL)
d.arrow(785, 210, 785, 300)
label_box(d, 510, 330, 550, 100, "Explain pattern + limitation", fill="#f4eefb", colour=PURPLE, size=28)
d.text(220, 375, "Methods connect", anchor="middle", size=25)
d.text(220, 415, "question and data.", anchor="middle", size=25)
save(d, stem, "evidence-to-interpretation.svg")
d = Drawing(title="A project stays portable when relative input paths stay inside it")
d.folder(60, 60, "project A", width=280)
d.file(90, 245, "report.Rmd", width=160, height=100)
d.folder(360, 250, "data", width=180)
d.arrow(590, 200, 745, 200)
d.folder(790, 60, "new location", width=280)
d.file(795, 245, "report.Rmd", width=140, height=100)
d.folder(960, 255, "data", width=120, height=90)
d.text(550, 450, "data/seedlings.csv works from either complete project root.", anchor="middle", size=24)
save(d, stem, "portable-project.svg")

print("Rebuilt lecture diagrams for days 1–10.")
