"""Rebuild the new lecture figures for Day 4 (inspect archive), Day 5 (meet R)
and Day 24 (reproduce and share).

Run from anywhere:  python3 instructor/make-lecture-figures-days-4-5-24.py

Needs Rscript with rmarkdown (for the plot and the rendered report) and, for the
report preview only, google-chrome. If the screenshot fails, the previous
report-preview.png is kept and a warning is printed.
"""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lecture_svg import Drawing, INK, TEAL, PURPLE, RED, BLUE, PALE, GREY

DAY4 = ROOT / "lectures" / "04-inspect-archive"
DAY5 = ROOT / "lectures" / "05-meet-r"
DAY24 = ROOT / "lectures" / "24-reproduce"


def mono(d, x, y, text, size=24, fill=INK, anchor="start", weight="normal"):
    """Monospace text for prompts, commands and paths."""
    from html import escape
    d.parts.append(
        f'<text x="{x}" y="{y}" font-family="DejaVu Sans Mono, Consolas, monospace" '
        f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
        f'xml:space="preserve">{escape(text)}</text>')


def cross(d, x, y, r=22):
    d.line(x - r, y - r, x + r, y + r, stroke=RED, width=6)
    d.line(x - r, y + r, x + r, y - r, stroke=RED, width=6)


# ---------------------------------------------------------------- Day 4
d = Drawing(title="cp makes a second file; mv gives the copy a new name")
d.folder(40, 40, "lab-data", width=1020, height=400)
d.file(90, 150, "samples.tsv", width=170, height=150)
d.text(555, 365, "old name gone after mv", anchor="middle", size=20, fill=GREY)
d.text(175, 365, "original: stays", anchor="middle", size=22, fill=TEAL)
d.rect(380, 105, 650, 300, fill="#fffaf0", stroke="#9a7820")
d.text(400, 140, "working/", size=24, weight="bold")
d.arrow(280, 225, 440, 225)
mono(d, 360, 205, "cp", size=26, fill=TEAL, anchor="middle")
d.file(460, 160, "samples-copy.tsv", fill="#f1f5f9", width=190, height=130)
d.line(450, 160, 660, 290, stroke=GREY, width=3, dashed=True)
d.arrow(670, 225, 790, 225, stroke=PURPLE)
mono(d, 730, 205, "mv", size=26, fill=PURPLE, anchor="middle")
d.file(810, 160, "manifest-practice.tsv", width=190, height=130)
d.text(555, 470, "After mv the old name is gone; the original samples.tsv is untouched.",
       anchor="middle", size=24)
d.save(DAY4 / "copy-rename.svg")


# Lengths of the four lab-data seedlings, read from the actual archive.
import csv, io, zipfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams.update({"svg.fonttype": "none", "font.size": 16,
                            "axes.spines.top": False, "axes.spines.right": False})
with zipfile.ZipFile(ROOT / "downloads" / "lab-data.zip") as archive:
    manifest = list(csv.DictReader(io.StringIO(archive.read("samples.tsv").decode()), delimiter="\t"))
    for row in manifest:
        row["length_mm"] = float(list(csv.DictReader(io.StringIO(archive.read(row["file"]).decode())))[0]["length_mm"])
assert [r["length_mm"] for r in manifest] == [32.1, 35.2, 42.4, 39.8]
fig, ax = plt.subplots(figsize=(6.4, 4.6))
for r in manifest:
    x = 0 if r["treatment"] == "control" else 1
    colour = TEAL if x == 0 else PURPLE
    ax.plot(x, r["length_mm"], "o", ms=13, color=colour)
    ax.annotate(f'{r["sample_id"]}  {r["length_mm"]}', (x, r["length_mm"]), xytext=(14, -5),
                textcoords="offset points", fontsize=15)
ax.set_xticks([0, 1], ["control", "treated"])
ax.set_xlim(-0.4, 1.6)
ax.set_ylim(28, 46)
ax.set_ylabel("Length after seven days (mm)")
fig.tight_layout()
fig.savefig(DAY4 / "four-lengths.svg")
plt.close(fig)

# ---------------------------------------------------------------- Day 5
d = Drawing(title="Opening introcomputing.Rproj starts RStudio inside the course folder")
d.folder(40, 30, "introcomputing-course", width=420, height=90)
items = [("introcomputing.Rproj", True), ("report.Rmd", False), ("data/", False),
         ("output/", False), ("reports/", False)]
for i, (name, key) in enumerate(items):
    y = 165 + i * 58
    d.line(80, 130, 80, y - 8, stroke=GREY)
    d.line(80, y - 8, 110, y - 8, stroke=GREY)
    mono(d, 120, y, name, size=25, fill=PURPLE if key else INK,
         weight="bold" if key else "normal")
d.arrow(450, 175, 610, 175, stroke=PURPLE)
d.text(530, 150, "double-click", anchor="middle", size=22, fill=PURPLE)
d.rect(630, 60, 430, 300, fill="#f8fafc", stroke=PURPLE)
d.text(845, 105, "RStudio", anchor="middle", size=28, weight="bold")
mono(d, 655, 170, "> getwd()", size=22)
mono(d, 655, 205, "…/introcomputing-course", size=22, fill=GREY)
mono(d, 655, 260, '> file.exists(', size=22)
mono(d, 655, 292, '    "data/seedlings.csv")', size=22)
mono(d, 655, 330, "[1] TRUE", size=22, fill=TEAL)
d.text(550, 470, "R starts in the project folder, so the short path data/seedlings.csv works.",
       anchor="middle", size=24)
d.save(DAY5 / "open-project.svg")

d = Drawing(height=520, title="The four panes of RStudio")
d.rect(20, 15, 1060, 495, fill="#e2e8f0", stroke=GREY, radius=6)
d.text(40, 45, "RStudio", size=22, weight="bold")
d.text(1060, 45, "Project: introcomputing", size=20, anchor="end", fill=PURPLE)
panes = [
    (35, 60, "Editor", "open files: report.Rmd, scripts", ["saved instructions", "(a file on disk)"], BLUE),
    (35, 285, "Console  |  Terminal", "R runs what you type here", ["> 44.3 - 25.7", "[1] 18.6"], TEAL),
    (560, 60, "Environment", "objects R is holding now", ["seedlings", "24 obs. of 4 variables"], PURPLE),
    (560, 285, "Files  |  Plots  |  Help", "the project folder, your plot", ["data/  output/  reports/", "report.Rmd"], "#9a7820"),
]
for x, y, title, role, lines, colour in panes:
    d.rect(x, y, 505, 210, fill="white", stroke=colour)
    d.text(x + 18, y + 38, title, size=25, weight="bold", fill=colour)
    d.text(x + 18, y + 72, role, size=21, fill=GREY)
    for k, line in enumerate(lines):
        mono(d, x + 30, y + 125 + k * 38, line, size=22)
d.save(DAY5 / "rstudio-panes.svg")

d = Drawing(title="The R Console and the terminal read different languages")
for x, title, prompt, colour, rows in [
    (30, "R Console (RStudio)", ">", PURPLE,
     [("44.3 - 25.7", "[1] 18.6", TEAL), ("pwd", "Error: object 'pwd' not found", RED)]),
    (570, "Terminal (shell)", "$", TEAL,
     [("pwd", "/home/you/introcomputing-shell", TEAL), ("44.3 - 25.7", "44.3: command not found", RED)]),
]:
    d.rect(x, 30, 500, 360, fill="#f8fafc", stroke=colour)
    d.text(x + 250, 75, title, anchor="middle", size=27, weight="bold", fill=colour)
    for k, (cmd, out, out_colour) in enumerate(rows):
        y = 150 + k * 120
        mono(d, x + 25, y, f"{prompt} {cmd}", size=23)
        mono(d, x + 25, y + 38, out, size=20, fill=out_colour)
d.text(550, 450, "Look at the prompt first: > waits for R, $ waits for shell commands.",
       anchor="middle", size=25)
d.save(DAY5 / "console-terminal.svg")


d = Drawing(title="Quitting R clears objects in memory; saved files stay on disk")
d.rect(40, 40, 430, 330, fill="#f5f0ff", stroke=PURPLE)
d.text(255, 85, "R's memory (Environment)", anchor="middle", size=25, weight="bold", fill=PURPLE)
mono(d, 90, 175, "seedlings", size=26)
mono(d, 90, 215, "24 obs. of 4 variables", size=20, fill=GREY)
cross(d, 380, 190, 30)
d.text(255, 320, "gone when R quits", anchor="middle", size=23, fill=RED)
d.rect(630, 40, 430, 330, fill="#fffaf0", stroke="#9a7820")
d.text(845, 85, "Disk (Files pane)", anchor="middle", size=25, weight="bold", fill="#9a7820")
for k, name in enumerate(["data/seedlings.csv", "report.Rmd", "report.html", "reports/day05-notes.txt"]):
    mono(d, 670, 150 + k * 45, name, size=22)
d.text(845, 345, "still there next time", anchor="middle", size=23, fill=TEAL)
d.arrow(620, 240, 480, 240, stroke=TEAL)
d.text(550, 225, "read again", anchor="middle", size=18, fill=TEAL)
d.text(550, 450, "Keep the instructions in a saved file, and every object can be made again.",
       anchor="middle", size=24)
d.save(DAY5 / "memory-and-files.svg")

# Base-R scatter plot exactly as the supplied Console code draws it.
plot_code = f"""
seedlings <- read.csv("{(ROOT / 'data' / 'seedlings.csv').as_posix()}")
png("{(DAY5 / 'first-plot.png').as_posix()}", width = 1500, height = 1050, res = 200)
par(mar = c(4.5, 4.5, 1, 1))
plot(seedlings$initial_mm, seedlings$final_mm,
     xlab = "Initial length (mm)", ylab = "Final length (mm)")
invisible(dev.off())
stopifnot(nrow(seedlings) == 24)
"""
subprocess.run(["Rscript", "-e", plot_code], check=True)

# Render the supplied report.Rmd in a temporary copy and screenshot the HTML.
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    project = tmp / "introcomputing-course"
    project.mkdir()
    shutil.copy(ROOT / "report.Rmd", project / "report.Rmd")
    shutil.copytree(ROOT / "data", project / "data")
    subprocess.run(["Rscript", "-e", 'rmarkdown::render("report.Rmd", quiet = TRUE)'],
                   cwd=project, check=True)
    shot = tmp / "shot.png"
    for attempt in range(3):
        try:
            subprocess.run(["google-chrome", "--headless", "--no-sandbox", "--disable-gpu",
                            "--disable-dev-shm-usage", "--hide-scrollbars",
                            f"--user-data-dir={tmp / 'chrome'}", "--window-size=1000,1560",
                            f"--screenshot={shot}", (project / "report.html").as_uri()],
                           timeout=90, capture_output=True)
        except subprocess.TimeoutExpired:
            pass
        if shot.is_file():
            break
    if shot.is_file():
        from PIL import Image
        page = Image.open(shot).convert("RGB")
        top = page.crop((30, 0, 970, 450))          # title, question, data and methods
        bottom = page.crop((30, 920, 970, 1560))    # summary table and growth plot
        gap = 40
        canvas = Image.new("RGB", (top.width * 2 + gap, max(top.height, bottom.height)), "white")
        canvas.paste(top, (0, 0))
        canvas.paste(bottom, (top.width + gap, 0))
        for x in range(top.width + gap // 2 - 1, top.width + gap // 2 + 2):
            for y in range(canvas.height):
                canvas.putpixel((x, y), (180, 190, 200))
        canvas.save(DAY5 / "report-preview.png")
    else:
        print("WARNING: report screenshot failed; kept the previous report-preview.png")

# ---------------------------------------------------------------- Day 24
d = Drawing(title="The ZIP is made beside the share folder, not inside it")
d.folder(30, 25, "", width=1040, height=420)
d.text(60, 75, "Documents/", size=25, weight="bold")
d.rect(70, 110, 520, 300, fill="#fffaf0", stroke="#9a7820")
d.text(90, 145, "report-share/", size=25, weight="bold")
for k, name in enumerate(["introcomputing.Rproj", "duckweed-report.Rmd", "duckweed-report.html",
                          "README.txt", "data/duckweed.csv", "data/README.md", "output/"]):
    mono(d, 110, 185 + k * 32, name, size=21)
d.arrow(610, 260, 790, 260)
mono(d, 700, 240, "zip -r", size=24, fill=TEAL, anchor="middle")
d.file(820, 170, "report-share-v1.zip", width=220, height=160)
d.text(550, 480, "Run zip from Documents. A ZIP saved inside report-share/ would pack itself.",
       anchor="middle", size=23)
d.save(DAY24 / "share-zip.svg")

d = Drawing(title="Extracting into a new folder adds one folder level")
d.folder(40, 40, "receiver-v1", width=260)
d.folder(330, 170, "report-share", width=260)
d.file(650, 300, "duckweed-report.Rmd", width=200, height=90)
d.folder(880, 300, "data", width=170, height=90)
d.line(170, 140, 170, 220, stroke=GREY)
d.line(170, 220, 330, 220, stroke=GREY)
d.line(460, 270, 460, 345, stroke=GREY)
d.line(460, 345, 650, 345, stroke=GREY)
d.line(850, 345, 880, 345, stroke=GREY)
mono(d, 40, 470, "receiver-v1/report-share/duckweed-report.Rmd", size=26, fill=PURPLE)
d.text(1060, 90, "unzip report-share-v1.zip -d receiver-v1", size=22, anchor="end", fill=TEAL)
d.save(DAY24 / "receiver-nesting.svg")

d = Drawing(title="A ZIP is a snapshot: an older archive keeps the older text")
d.folder(40, 50, "report-share/", width=250, height=95)
d.text(165, 205, "README edited", anchor="middle", size=23)
d.text(165, 240, "after v1 was made", anchor="middle", size=23)
d.file(440, 60, "report-share-v1.zip", width=220, height=130)
d.text(550, 270, "still the old README", anchor="middle", size=23, fill=RED)
d.file(830, 60, "report-share-v2.zip", width=220, height=130)
d.text(940, 270, "contains the edit", anchor="middle", size=23, fill=TEAL)
d.arrow(300, 100, 420, 100, stroke=GREY)
mono(d, 360, 80, "zip -r", size=19, fill=GREY, anchor="middle")
d.path("M 165,265 Q 165,360 600,360 Q 940,360 940,300", stroke=PURPLE)
d.arrow(940, 310, 940, 300, stroke=PURPLE)
d.text(560, 345, "zip again, new name", anchor="middle", size=22, fill=PURPLE)
d.text(550, 455, "Editing the folder never changes an existing ZIP. Make a new one and test it.",
       anchor="middle", size=24)
d.save(DAY24 / "zip-snapshot.svg")

d = Drawing(title="A ZIP beside the original is not a backup")
d.rect(40, 50, 500, 330, fill="#f8fafc", stroke=GREY)
d.text(290, 95, "Your laptop", anchor="middle", size=27, weight="bold")
d.folder(80, 150, "report-share", width=200, height=90)
d.file(330, 130, "report-share.zip", width=170, height=120)
cross(d, 290, 320, 28)
d.text(290, 420, "lost together if the laptop is lost", anchor="middle", size=22, fill=RED)
d.arrow(560, 210, 690, 210, stroke=TEAL)
d.rect(710, 50, 350, 330, fill=PALE, stroke=TEAL)
d.text(885, 95, "Separate supported", anchor="middle", size=25, weight="bold")
d.text(885, 128, "storage", anchor="middle", size=25, weight="bold")
d.file(800, 160, "copy of the project", width=170, height=120)
d.text(885, 420, "survives a lost laptop", anchor="middle", size=22, fill=TEAL)
d.text(550, 480, "Share with a ZIP; protect with a copy somewhere else.", anchor="middle", size=24)
d.save(DAY24 / "share-vs-backup.svg")

print("Wrote Day 4, Day 5 and Day 24 lecture figures.")
