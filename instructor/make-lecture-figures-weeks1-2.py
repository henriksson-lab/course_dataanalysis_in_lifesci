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


# Day 1: kinds of files — plain text versus Word, Excel and other formats.
stem = "01-files"


def mono(d, x, y, label, size=24, fill=INK, anchor="start", weight="normal"):
    """Monospaced text, for file contents and code."""
    from html import escape
    d.parts.append(f'<text x="{x}" y="{y}" font-family="Consolas, Menlo, monospace" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" xml:space="preserve">{escape(label)}</text>')


def window(d, x, y, w, h, title, colour=BLUE):
    d.rect(x, y, w, h, fill="#f8fafc", stroke=colour)
    d.rect(x, y, w, 40, fill="#dceaf6", stroke=colour)
    d.text(x + 15, y + 28, title, size=20, weight="bold")


tree(stem, "find-the-file.svg")

with open(ROOT / "data/seedlings.csv") as handle:
    seedling_lines = [line.rstrip("\n") for line in handle][:4]
d = Drawing(title="A plain-text file contains only characters")
window(d, 40, 40, 560, 250, "seedlings.csv in a text editor")
for i, line in enumerate(seedling_lines):
    mono(d, 60, 115 + i * 44, line, size=22)
window(d, 40, 320, 560, 120, "dna.txt in a text editor")
mono(d, 60, 400, "ACGTACGTTTAGCCGATATACC...", size=22)
d.text(830, 70, "Plain text, for example:", anchor="middle", weight="bold")
for i, ext in enumerate([".csv  .tsv  tables", ".txt  notes, sequences", ".R  .Rmd  code, reports", ".md  documentation"]):
    mono(d, 680, 130 + i * 52, ext, size=24)
d.text(830, 380, "Every editor shows the same", anchor="middle", size=24)
d.text(830, 415, "characters. R reads them.", anchor="middle", size=24)
save(d, stem, "plain-text.svg")

d = Drawing(title="A Word file is a ZIP package of XML files")
d.file(40, 60, "seedling-notes.docx", width=200, height=150)
window(d, 330, 30, 340, 190, "the .docx in a text editor", colour=RED)
for i, line in enumerate(["PK\u25a1\u25a1\u25a1 \u25a1 \u00cbss]e\u00dd", "\u2039 q\u25a1 &\u25a1 \u25a1 [Con", "tent_Types].xml \u00ec\u00d6\u00e6"]):
    mono(d, 350, 110 + i * 38, line, size=22, fill=RED)
d.arrow(250, 135, 315, 120, stroke=RED)
d.arrow(140, 255, 140, 320)
d.text(160, 295, "copy, rename to .zip, extract", size=22)
d.folder(40, 330, "seedling-notes", width=230, height=100)
d.arrow(285, 380, 320, 380, stroke=GREY)
for i, (name, role) in enumerate([("word/document.xml", "the text"), ("word/styles.xml", "fonts, headings"), ("word/theme/...", "colours"), ("docProps/core.xml", "author, dates"), ("...", "16 files in all")]):
    mono(d, 340, 310 + i * 38, name, size=20)
    d.text(590, 310 + i * 38, role, size=21, fill=GREY)
d.text(760, 90, "Not readable as text:", size=24, fill=RED)
d.text(760, 125, "it is a compressed", size=24, fill=RED)
d.text(760, 160, "ZIP package.", size=24, fill=RED)
d.text(790, 360, "The text is in there,", size=24, fill=TEAL)
d.text(790, 395, "mixed with formatting", size=24, fill=TEAL)
d.text(790, 430, "instructions.", size=24, fill=TEAL)
save(d, stem, "docx-package.svg")

d = Drawing(title="The same table as CSV and as an Excel workbook")
window(d, 30, 30, 470, 300, "seedlings.csv")
for i, line in enumerate(seedling_lines[:3]):
    mono(d, 50, 110 + i * 44, line, size=19)
d.text(265, 300, "values only", anchor="middle", size=24, fill=TEAL)
window(d, 560, 30, 510, 300, "seedlings.xlsx", colour=PURPLE)
cols = [("plant_id", 100), ("initial_mm", 125), ("final_mm", 110), ("growth_mm", 135)]
x = 580
for name, w in cols:
    d.rect(x, 90, w, 40, fill="#cfe8e3", stroke="#cbd5e1", radius=0)
    d.text(x + 8, 118, name, size=18, weight="bold")
    x += w
x = 580
for value, w in zip(["P01", "25.7", "44.3", "=D2-C2"], [c[1] for c in cols]):
    d.rect(x, 130, w, 40, fill="white", stroke="#cbd5e1", radius=0)
    d.text(x + 8, 158, value, size=18, fill=PURPLE if value.startswith("=") else INK)
    x += w
d.rect(580, 280, 140, 34, fill="#cfe8e3", stroke=PURPLE, radius=0)
d.text(590, 304, "measurements", size=18)
d.rect(720, 280, 80, 34, fill="white", stroke=PURPLE, radius=0)
d.text(730, 304, "notes", size=18)
d.text(580, 215, "+ formatting   + formulas   + several sheets", size=21, fill=PURPLE)
d.text(550, 390, "CSV: any program can read it, and what you see is what is stored.", anchor="middle", size=24)
d.text(550, 430, "xlsx: you need a spreadsheet program, and the screen can hide things.", anchor="middle", size=24)
save(d, stem, "csv-vs-xlsx.svg")

d = Drawing(title="A spreadsheet turns gene symbols into dates")
headers, before, after = ["gene", "log2FC"], [["SEPT2", "-1.31"], ["MARCH1", "-1.53"], ["TP53", "-0.07"]], [["2-Sep", "-1.31"], ["1-Mar", "-1.53"], ["TP53", "-0.07"]]
table(d, 60, 70, headers, before, [170, 140])
d.arrow(400, 200, 640, 200, stroke=RED)
d.text(520, 165, "open in Excel", anchor="middle", size=23)
table(d, 690, 70, headers, after, [170, 140], row_colours={1: "#f8dde3", 2: "#f8dde3"})
d.text(550, 335, "Saved again, the gene names are gone for good.", anchor="middle", size=26, fill=RED)
d.text(550, 385, "About 1 in 5 published papers with Excel gene lists had such errors", anchor="middle", size=23)
d.text(550, 418, "(Ziemann et al. 2016). In 2020, SEPT2 was renamed SEPTIN2", anchor="middle", size=23)
d.text(550, 451, "and MARCH1 MARCHF1, partly because of this.", anchor="middle", size=23)
save(d, stem, "gene-dates.svg")

d = Drawing(title="A Swedish-language Excel saves CSV with semicolons and decimal commas")
window(d, 40, 40, 470, 220, "seedlings.csv  (course format)")
for i, line in enumerate(seedling_lines[:3]):
    mono(d, 60, 115 + i * 44, line, size=19)
window(d, 590, 40, 470, 220, "seedlings-semicolon.csv", colour=RED)
for i, line in enumerate(seedling_lines[:3]):
    mono(d, 610, 115 + i * 44, line.replace(",", ";") if i == 0 else line.replace(",", ";").replace(".", ","), size=19)
d.text(550, 320, "Same numbers. Values are separated by ;  and 25.7 is written 25,7.", anchor="middle", size=24)
d.text(550, 370, "A program expecting commas splits the rows in the wrong places.", anchor="middle", size=24)
d.text(550, 420, "Open a CSV in a text editor to see which kind you have.", anchor="middle", size=24, fill=TEAL)
save(d, stem, "semicolon-csv.svg")

d = Drawing(title="Word turns straight quotes into curly quotes, which R cannot read")
window(d, 40, 40, 480, 140, "text editor (.txt, .R)", colour=TEAL)
mono(d, 60, 135, 'read.csv("data/seedlings.csv")', size=21, fill=TEAL)
window(d, 580, 40, 480, 140, "word processor (.docx)", colour=RED)
mono(d, 600, 135, "read.csv(“data/seedlings.csv”)", size=21, fill=RED)
d.text(280, 225, "works in R", anchor="middle", size=24, fill=TEAL)
d.text(820, 225, "copy into R:", anchor="middle", size=24, fill=RED)
d.rect(580, 250, 480, 70, fill="#fbeff2", stroke=RED)
mono(d, 595, 293, "Error: unexpected input in \"read.csv(\u201c\"", size=18, fill=RED)
d.text(550, 380, "Look closely: curly \u201c \u201d instead of straight \" \".", anchor="middle", size=24)
d.text(550, 415, "Write code and data in a text editor or RStudio, not in Word.", anchor="middle", size=24)
save(d, stem, "smart-quotes.svg")

d = Drawing(title="Renaming changes the label, not the contents")
for y, before, after, note, colour in [
        (40, "seedlings.csv", "seedlings.xlsx", ["Still plain text inside.", "Excel refuses to open it."], RED),
        (270, "notes.docx", "notes.zip", ["It was a ZIP all along.", "Now you can look inside."], TEAL)]:
    d.file(40, y, before, width=150, height=120)
    d.arrow(220, y + 60, 400, y + 60, stroke=colour)
    d.text(310, y + 40, "rename", anchor="middle", size=22)
    d.file(430, y, after, width=150, height=120)
    for i, line in enumerate(note):
        d.text(650, y + 50 + i * 36, line, size=25, fill=colour)
save(d, stem, "extension-label.svg")

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

# Day 2: folders and paths. (computer-components.svg is kept for Day 21.)
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
d = Drawing(title="Each part of a path names one folder on the route")
mono(d, 550, 80, "/home/anna/introcomputing-course/data/seedlings.csv", size=30, anchor="middle", weight="bold")
x = 30
for i, (part, w) in enumerate([("/", 80), ("home", 120), ("anna", 120), ("introcomputing-course", 290), ("data", 110)]):
    d.folder(x, 170, part, width=w, height=90)
    d.arrow(x + w + 3, 215, x + w + 27, 215, stroke=GREY, width=3)
    x += w + 30
d.file(x + 5, 160, "seedlings.csv", width=110, height=110)
d.text(550, 390, "Read from left to right: start at the top of the disk, open each folder.", anchor="middle", size=24)
d.text(550, 430, "On Windows the start is a drive, C:\\, and the separator is \\ .", anchor="middle", size=24)
save(d, stem, "path-parts.svg")

d = Drawing(title="Absolute paths differ between computers; the relative path does not")
for x, user, colour in [(40, "anna", TEAL), (580, "ben", PURPLE)]:
    d.rect(x, 40, 480, 300, fill="#f8fafc", stroke=colour)
    d.text(x + 240, 85, f"{user}'s laptop", anchor="middle", weight="bold")
    mono(d, x + 20, 140, f"/Users/{user}/Documents/", size=20)
    mono(d, x + 20, 170, "  introcomputing-course/", size=20)
    mono(d, x + 20, 200, "  data/seedlings.csv", size=20)
    d.line(x + 20, 235, x + 460, 235, stroke="#cbd5e1")
    d.text(x + 20, 275, "from the project folder:", size=21)
    mono(d, x + 20, 315, "data/seedlings.csv", size=22, fill=colour, weight="bold")
d.text(550, 410, "Write paths inside a project relative to the project folder.", anchor="middle", size=25)
d.text(550, 450, "Then the same instructions work on every computer.", anchor="middle", size=25)
save(d, stem, "portable-path.svg")

d = Drawing(title="Moving a folder changes the path, not the file")
for x, title, rows in [(40, "Before the move", ["practice/", "  map-a/", "    note.txt", "  map-b/"]),
                       (600, "After moving map-a into map-b", ["practice/", "  map-b/", "    map-a/", "      note.txt"])]:
    d.text(x + 230, 60, title, anchor="middle", weight="bold")
    d.rect(x, 80, 460, 210, fill="#f8fafc", stroke=BLUE)
    for i, row in enumerate(rows):
        mono(d, x + 30, 125 + i * 42, row, size=24, fill=RED if "note" in row else INK)
d.arrow(510, 185, 590, 185)
mono(d, 270, 350, "practice/map-a/note.txt", size=23, anchor="middle")
mono(d, 830, 350, "practice/map-b/map-a/note.txt", size=23, anchor="middle")
d.text(550, 420, "The note's contents are unchanged. Every written route to it must change.", anchor="middle", size=24)
save(d, stem, "move-changes-path.svg")

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
stem = "05-meet-r"
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

# Expanded first-fortnight demonstrations: actual operations and contrasting cases.
def nodes(stem, name, labels, values=None, colours=None):
    d=Drawing(title=' → '.join(labels))
    n=len(labels); gap=1050/n; w=min(240,gap-35)
    for i,label in enumerate(labels):
        x=25+i*gap
        d.rect(x,130,w,150,fill='#eef4f7',stroke=(colours or [TEAL]*n)[i])
        d.text(x+w/2,175,label,size=22,anchor='middle',weight='bold')
        if values: d.text(x+w/2,235,values[i],size=24,anchor='middle')
        if i<n-1: d.arrow(x+w+8,205,x+gap-12,205)
    return d

stem='02-folders-computers'
d=Drawing(title='A route from reports to data must first visit the parent')
d.folder(425,30,'project root',width=260)
d.folder(100,240,'reports');d.folder(770,240,'data')
d.arrow(210,220,450,145);d.arrow(680,145,880,220)
d.text(290,190,'1. parent',size=28);d.text(730,190,'2. data',size=28)
d.file(800,365,'seedlings.csv',width=170,height=75)
d.text(550,455,'The starting folder changes the route.',anchor='middle',size=27)
save(d,stem,'nested-route.svg')
d=Drawing(title='Closing a process can clear working memory while the saved file remains')
for x,title in [(80,'Before closing'),(650,'After closing')]:
 d.rect(x,65,370,190,fill='#f4eefb',stroke=PURPLE);d.text(x+185,110,title,anchor='middle',size=28);d.text(x+185,165,'working memory',anchor='middle',size=25)
d.text(265,220,'edited note',anchor='middle',size=31);d.text(835,220,'session ended',anchor='middle',size=31,fill=GREY)
d.arrow(470,160,620,160);d.file(465,325,'saved note on disk',width=180,height=90)
d.text(550,480,'Check the ordinary saved file, not only an editor window.',anchor='middle',size=24)
save(d,stem,'memory-close.svg')
d=Drawing(title='One installed application can be launched as running processes')
d.file(70,170,'installed application',width=240,height=155)
for y in [80,320]:
 d.arrow(350,245,670,y+50);d.rect(700,y,320,110,fill='#e6f3f5',stroke=TEAL);d.text(860,y+65,'running process',anchor='middle',size=28)
d.text(210,435,'persistent storage',anchor='middle',size=26);d.text(860,485,'CPU + memory now',anchor='middle',size=26)
save(d,stem,'program-process.svg')
d=Drawing(title='Local, cloud and remote storage are distinct locations')
for x,label in [(35,'Laptop'),(415,'Cloud service'),(795,'Remote Linux')]:
 d.rect(x,80,270,260,fill='#f8fafc',stroke=BLUE);d.text(x+135,125,label,anchor='middle',size=28);d.folder(x+30,210,'course',width=210,height=100)
d.arrow(325,260,390,260,stroke=GREY);d.text(550,405,'Only draw copying/sync links you know exist.',anchor='middle',size=28)
d.text(550,460,'A desktop connection is not automatic synchronisation.',anchor='middle',size=26)
save(d,stem,'storage-locations.svg')

stem='03-terminal'
d=Drawing(title='Quotes make a space-containing folder name one argument')
d.text(70,70,'mkdir field notes',size=34);d.arrow(430,65,650,65)
d.folder(650,20,'field',width=160,height=90);d.folder(865,20,'notes',width=160,height=90)
d.text(70,280,'mkdir "field notes"',size=34);d.arrow(500,270,700,270)
d.folder(720,230,'field notes',width=250,height=100)
d.text(550,440,'Unquoted words may become separate arguments.',anchor='middle',size=30)
save(d,stem,'quoted-arguments.svg')
d=nodes(stem,'failed-cd.svg',['Before command','Failed cd','After command'],['day03/','not-present','day03/'],[TEAL,RED,TEAL]);d.text(550,385,'A failed change-directory does not move you.',anchor='middle',size=29);save(d,stem,'failed-cd.svg')
d=Drawing(title='Each terminal session has its own current working directory')
for x,label,path in [(50,'Shell A','.../day03/readings'),(610,'Shell B','.../introcomputing-shell')]:
 d.rect(x,75,440,300,fill='#eef2f6',stroke=BLUE);d.text(x+220,125,label,anchor='middle',size=31);d.text(x+25,205,'$ pwd',size=30);d.text(x+25,270,path,size=25)
d.text(550,455,'Navigating A does not automatically navigate B.',anchor='middle',size=29)
save(d,stem,'shell-cwd.svg')
d=Drawing(title='Two starting locations need different relative paths')
d.folder(425,25,'workspace',width=250);d.folder(60,230,'inputs');d.folder(770,230,'results');d.folder(770,365,'notes',height=90)
d.line(550,128,170,220);d.line(550,128,880,220);d.line(880,332,880,355)
d.arrow(790,390,570,160,stroke=PURPLE);d.arrow(520,155,220,240,stroke=PURPLE)
d.text(370,340,'From notes: up twice,',size=28);d.text(370,380,'then enter inputs.',size=28)
save(d,stem,'route-two-starts.svg')

stem='04-inspect-archive'
d=Drawing(title='Literal treated search also matches untreated')
for i,(label,col) in enumerate([('S01 untreated',RED),('S02 control',GREY),('S03 treated',TEAL),('S04 treated',TEAL)]):
 y=60+i*85;d.rect(75,y,450,65,fill='#f8fafc',stroke=col);d.text(100,y+43,label,size=29)
 if i!=1: d.arrow(550,y+30,800,y+30,stroke=col);d.circle(860,y+30,14,fill=col)
d.text(550,455,'Three text matches; not evidence for three treated samples.',anchor='middle',size=26)
save(d,stem,'grep-substring.svg')
d=Drawing(title='Five text lines contain one header and four sample records')
for i in range(5):
 y=50+i*70;d.rect(100,y,450,52,fill='#dceaf6' if i==0 else '#e6f3f5',stroke=BLUE if i==0 else TEAL);d.text(130,y+35,'header' if i==0 else f'sample record {i}',size=27)
d.path('M590,50 h30 v332 h-30',stroke=BLUE);d.text(680,145,'wc: 5 lines',size=33,fill=BLUE)
d.path('M590,120 h30 v262 h-30',stroke=TEAL);d.text(680,280,'4 plants',size=33,fill=TEAL)
save(d,stem,'header-lines.svg')
d=Drawing(title='An output filename can remain unchanged while redirection replaces contents')
for x,label,ids in [(70,'Before >','S03, S04'),(690,'After >','S01, S02')]:
 d.file(x,70,'treated-audit.txt',width=250,height=170);d.text(x+125,330,ids,anchor='middle',size=34);d.text(x+125,390,label,anchor='middle',size=29)
d.arrow(390,160,630,160,stroke=RED);d.text(550,460,'Check contents: the name does not protect their meaning.',anchor='middle',size=27)
save(d,stem,'overwrite-state.svg')
d=Drawing(title='A manifest path and a renamed file can disagree')
d.file(60,100,'manifest',width=200,height=155);d.text(40,380,'measurements/S04.csv',size=27)
d.arrow(310,175,570,175,stroke=RED);d.text(430,135,'path not found',anchor='middle',size=25,fill=RED)
d.file(660,100,'S04-renamed.csv',width=230,height=155);d.text(780,380,'contents: S04,39.8',anchor='middle',size=27)
d.text(550,465,'Inspect identity before restoring a name; do not delete the record.',anchor='middle',size=24)
save(d,stem,'manifest-path.svg')

stem='05-meet-r'
d=Drawing(title='A sharing archive is a snapshot, not a live copy')
d.file(50,85,'ordinary source',width=210,height=150);d.file(440,85,'report-v1.zip',width=210,height=150);d.file(830,85,'report-v2.zip',width=210,height=150)
d.arrow(285,145,410,145);d.arrow(285,300,800,300,stroke=PURPLE)
d.text(155,370,'edited to version 2',anchor='middle',size=26);d.text(545,370,'still version 1',anchor='middle',size=26,fill=RED);d.text(935,370,'new snapshot',anchor='middle',size=26)
d.text(550,460,'Repackage, extract, and check the actual revised sentence.',anchor='middle',size=27)
save(d,stem,'version-snapshot.svg')
d=Drawing(title='Extraction can preserve the archived report folder as another level')
d.folder(60,45,'receiver-v1',width=250);d.folder(400,210,'report');d.file(790,350,'findings.txt',width=170,height=75)
d.arrow(300,130,400,225);d.arrow(620,290,790,375)
d.text(550,80,'receiver-v1/report/findings.txt',anchor='middle',size=31)
save(d,stem,'zip-nesting.svg')
d=Drawing(title='The receiver checks an extracted result in a new location')
d.folder(45,80,'sender',width=250);d.file(445,120,'sharing.zip',width=185,height=140);d.folder(790,80,'receiver',width=250)
d.arrow(320,180,415,180);d.arrow(665,180,760,180)
d.file(835,285,'README + input',width=160,height=95);d.text(550,450,'Can another person identify and verify the selected records?',anchor='middle',size=27)
save(d,stem,'receiver-proof.svg')
d=Drawing(title='The shell and R interpret different instruction languages')
for x,label,cmd in [(60,'Shell','grep -F treated ...'),(610,'R Console','mean(c(12, 14, 16))')]:
 d.rect(x,70,430,300,fill='#f8fafc',stroke=TEAL if x==60 else PURPLE);d.text(x+215,125,label,anchor='middle',size=32);d.text(x+215,235,cmd,anchor='middle',size=28)
d.text(550,450,'An interpreter mismatch calls for the right window, not system repair.',anchor='middle',size=25)
save(d,stem,'interpreter-choice.svg')

stem='06-r-basics'
d=nodes(stem,'stale-value.svg',['Initial inputs','Change final','Rerun calculation'],['20 → 37: 17 mm','final = 39; old 17','39 − 20 = 19'],[TEAL,RED,PURPLE]);d.text(550,390,'An assigned result is not a live spreadsheet formula.',anchor='middle',size=28);save(d,stem,'stale-value.svg')
d=Drawing(title='Position-by-position subtraction needs corresponding plants')
for i,(plant,initial,final) in enumerate([('P1',20,37),('P2',22,40),('P3',19,34)]):
 y=100+i*110;d.text(65,y,plant,size=30);d.text(260,y,initial,size=30);d.text(820,y,final,size=30);d.arrow(350,y-12,735,y-12)
d.path('M840,95 Q1060,170 840,315',stroke=RED);d.text(550,445,'Reordering one vector changes the biological pairing.',anchor='middle',size=28)
save(d,stem,'vector-shuffle.svg')
d=nodes(stem,'solution-units.svg',['Mass ÷ molar mass','Amount ÷ volume','Convert scale'],['0.2922 / 58.44','0.005 / 0.100','0.050 × 1000'])
d.text(165,350,'mol',size=30,anchor='middle');d.text(515,350,'mol/L',size=30,anchor='middle');d.text(865,350,'50 mmol/L',size=30,anchor='middle');d.text(550,450,'Every factor and conversion is supplied.',anchor='middle',size=28)
save(d,stem,'solution-units.svg')
fig,ax=plt.subplots(figsize=(10,4));ax.bar(['Original','Double mass','Double volume'],[50,100,25],color=[TEAL,PURPLE,BLUE]);ax.set_ylabel('Calculated concentration (mmol/L)');ax.set_ylim(0,115);fig.tight_layout();fig.savefig(ROOT/'lectures'/stem/'scale-change.svg');plt.close(fig)

stem='07-import'
d=Drawing(title='Import interprets stored fields as columns with types and meanings')
d.file(60,130,'solutions.csv',width=200,height=150);d.arrow(300,205,515,205)
for i,(name,col) in enumerate([('solution_id: label',PURPLE),('mass_g: measurement',TEAL),('final_volume_ml: measurement',BLUE)]):
 y=55+i*130;d.rect(550,y,480,95,fill='#f8fafc',stroke=col);d.text(790,y+60,name,anchor='middle',size=29)
save(d,stem,'import-roles.svg')
d=Drawing(title='The transfer study has eighteen independent plants, nine per group')
for row,(label,col) in enumerate([('control',TEAL),('treated',PURPLE)]):
 d.text(65,130+row*220,label,size=32)
 for i in range(9):
  x=355+i*75;y=120+row*220;d.circle(x,y,18,fill=col);d.line(x,y+20,x,y+62,stroke=col,width=5);d.path(f'M{x-20},{y+62} h40 l-7,32 h-26 Z',fill='#c8a47a',stroke='#795438',width=2)
d.text(550,470,'18 rows × 4 columns; the header is not a plant.',anchor='middle',size=28)
save(d,stem,'transfer-inventory.svg')
fig,ax=plt.subplots(figsize=(9,4));ax.bar(['10, NA, 20\n(available values)','10, 0, 20\n(three observed values)'],[15,10],color=[TEAL,RED]);ax.set_ylabel('Mean measurement');ax.set_ylim(0,18);fig.tight_layout();fig.savefig(ROOT/'lectures'/stem/'missing-zero-means.svg');plt.close(fig)
d=Drawing(title='Opening the right kind of folder does not identify which dataset was read')
for x,title,n in [(65,'Study A',24),(680,'Study B',18)]:
 d.folder(x,65,title,width=290);d.file(x+45,235,'measurement table',width=190,height=100);d.text(x+145,435,f'{n} plant records',anchor='middle',size=30)
d.text(550,40,'Check filename, project, dimensions, and dictionary.',anchor='middle',size=27)
save(d,stem,'project-identity.svg')

stem='08-transform-plot'
d=Drawing(title='Selecting rows and selecting columns act in different directions')
for x,label,orientation in [(60,'filter: keep observations','rows'),(610,'select: keep variables','columns')]:
 d.text(x+205,65,label,anchor='middle',size=29)
 for row in range(5):
  for col in range(4):
   on=(row in [2,3]) if orientation=='rows' else (col in [0,3])
   d.rect(x+col*100,110+row*57,95,52,fill=PALE if on else '#f8fafc',stroke=TEAL if on else '#cbd5e1',radius=0)
 d.arrow(x+205,415,x+205,465)
save(d,stem,'table-operations.svg')
with (ROOT/'data/seedlings-transfer.csv').open() as f: rows=list(csv.DictReader(f))
initial=[float(r['initial_mm']) for r in rows];final=[float(r['final_mm']) for r in rows];growth=[b-a for a,b in zip(initial,final)]
fig,axes=plt.subplots(1,2,figsize=(11,4.3));axes[0].scatter(initial,final,color=TEAL);axes[0].set(xlabel='Initial length (mm)',ylabel='Final length (mm)');axes[1].scatter(initial,growth,color=PURPLE);axes[1].set(xlabel='Initial length (mm)',ylabel='Growth (mm)');fig.tight_layout();fig.savefig(ROOT/'lectures'/stem/'two-outcomes.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(10,4));ax.bar([0,1,2,3],[25,50,100,50],width=.6,color='#e2e8f0',label='final total volume');ax.bar([0,1,2,3],[2.5,5,10,100],width=.25,color=[TEAL,TEAL,TEAL,RED],label='calculated stock volume');ax.set_xticks([0,1,2,3],['D01','D02','D03','D04: impossible']);ax.set_ylabel('Volume (mL)');ax.legend(fontsize=12);fig.tight_layout();fig.savefig(ROOT/'lectures'/stem/'dilution-feasibility.svg');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(11,4));x=[0 if r['treatment']=='control' else 1 for r in rows]
for j,ax in enumerate(axes):
 xx=[v+(0 if j==0 else ((i%5)-2)*.025) for i,v in enumerate(x)];ax.scatter(xx,growth,color=TEAL);ax.set(xticks=[0,1],xticklabels=['control','treated'],ylabel='Growth (mm)',title='No jitter' if j==0 else 'Horizontal jitter only',ylim=(7,23))
fig.tight_layout();fig.savefig(ROOT/'lectures'/stem/'jitter-invariance.svg');plt.close(fig)

stem='09-rmarkdown'
d=nodes(stem,'chunk-collision.svg',['Chunk: import','Chunk: import','Render stops'],['first label','duplicate label','rename labels'],[TEAL,RED,RED]);d.text(550,390,'Chunk labels identify code locations and must be unique.',anchor='middle',size=28);save(d,stem,'chunk-collision.svg')
d=nodes(stem,'inline-dependency.svg',['CSV input','Imported table','Inline result'],['18 plant rows','transfer object','nrow → 18']);d.text(550,395,'The number in the prose comes from this saved input.',anchor='middle',size=28);save(d,stem,'inline-dependency.svg')
d=Drawing(title='A source report without its input is not a complete reproducible package')
d.file(60,90,'report.Rmd',width=205,height=145);d.file(60,320,'input.csv',width=205,height=90);d.arrow(310,165,725,165);d.arrow(310,365,725,195)
d.file(780,100,'report.html',width=205,height=145);d.text(545,345,'omit input → missing dependency',anchor='middle',size=28,fill=RED)
save(d,stem,'missing-input.svg')
d=Drawing(title='Edit the source document and render to update its readable output')
d.file(90,100,'report.Rmd',width=210,height=155);d.arrow(360,180,720,180);d.text(540,135,'render',anchor='middle',size=31);d.file(790,100,'report.html',width=210,height=155)
d.path('M890,340 Q550,490 195,345',stroke=RED);d.text(550,455,'HTML edits do not rewrite the source recipe.',anchor='middle',size=28)
save(d,stem,'source-html.svg')

stem='10-first-report'
fig,ax=plt.subplots(figsize=(10,4));
for group,col,pos in [('control',TEAL,0),('treated',PURPLE,1)]:
 vals=[float(r['final_mm'])-float(r['initial_mm']) for r in rows if r['treatment']==group];ax.scatter([pos]*len(vals),vals,color=col,s=55)
ax.set(xticks=[0,1],xticklabels=['control','treated'],ylabel='Growth (mm)',title='Different centres can still have overlapping observations');fig.tight_layout();fig.savefig(ROOT/'lectures'/stem/'claim-evidence.svg');plt.close(fig)
d=Drawing(title='A laboratory report connects question, measurement, method and explanation')
d.folder(55,75,'data');d.arrow(300,150,470,150);d.rect(500,60,220,200,fill='#f8fafc',stroke=TEAL)
for x,y in [(535,220),(565,185),(610,205),(655,130),(685,155)]:d.circle(x,y,7)
d.arrow(755,150,890,150);d.file(905,75,'report',width=130,height=150);d.text(550,370,'Which recorded evidence supports this sentence?',anchor='middle',size=31)
save(d,stem,'report-story.svg')
d=Drawing(title='A complete project can be copied while its relative input relationships remain valid')
for x,label in [(60,'working project'),(690,'received copy')]:
 d.folder(x,50,label,width=320);d.file(x+20,245,'brief.Rmd',width=145,height=105);d.folder(x+185,260,'data',width=150,height=90);d.arrow(x+165,290,x+180,290)
d.arrow(420,160,655,160);d.text(550,455,'Move the structure together, then test a fresh render.',anchor='middle',size=29)
save(d,stem,'portable-root.svg')
fig,axes=plt.subplots(1,2,figsize=(10,4));axes[0].bar(['P01'],[18.6],color=RED);axes[0].set(ylabel='Growth (cm): WRONG',title='Only relabelled');axes[1].bar(['P01'],[1.86],color=TEAL);axes[1].set(ylabel='Growth (cm)',title='Converted mm ÷ 10');fig.tight_layout();fig.savefig(ROOT/'lectures'/stem/'unit-label-check.svg');plt.close(fig)
print('Rebuilt 40 additional first-fortnight lecture visuals.')
