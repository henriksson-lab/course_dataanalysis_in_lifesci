"""Build the Day 1 example files in examples/ (plain text versus other formats).

Run from anywhere:  python3 tools/build_examples.py

Needs pandoc (Markdown -> .docx), LibreOffice `soffice` (-> .xlsx and .pdf) and
matplotlib (-> .png). The text and CSV files are fully reproducible. The .docx,
.xlsx, .pdf and .png files embed tool versions and/or timestamps, so they are
generated once and kept in the repository; rerun only when their content
should change.
"""

from pathlib import Path
from xml.sax.saxutils import escape
import csv
import os
import random
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples"
OUT.mkdir(exist_ok=True)

with (ROOT / "data/seedlings.csv").open(newline="") as handle:
    SEEDLINGS = list(csv.reader(handle))
HEADER, ROWS = SEEDLINGS[0], SEEDLINGS[1:]

# --- Plain-text note and the same note as a Word document -------------------
NOTE_TITLE = "Seedling experiment notes"
NOTE_BODY = [
    "These are simulated teaching data, not a real experiment.",
    "24 seedlings were grown in separate pots. 12 received a nutrient "
    "treatment and 12 were controls. Each plant was measured at the start "
    "and after seven days. Lengths are in millimetres.",
    "The measurements are in data/seedlings.csv. One row describes one plant.",
    "Example: plant P01 grew from 25.7 mm to 44.3 mm, so it grew 18.6 mm.",
    "R code to read the table:",
    'seedlings <- read.csv("data/seedlings.csv")',
]
(OUT / "seedling-notes.txt").write_text(
    NOTE_TITLE + "\n\n" + "\n\n".join(NOTE_BODY) + "\n")

# --- Swedish-Excel style "CSV": semicolons and decimal commas ---------------
with (OUT / "seedlings-semicolon.csv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter=";", lineterminator="\r\n")
    writer.writerow(HEADER)
    for row in ROWS:
        writer.writerow([cell.replace(".", ",") for cell in row])

# --- Gene list with pre-2020 symbols that spreadsheets turn into dates ------
rng = random.Random(2016)
genes = ["ACTB", "SEPT2", "GAPDH", "MARCH1", "TP53", "SEPT7", "MYC", "MARCH5"]
with (OUT / "genes.csv").open("w", newline="") as handle:
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(["gene", "log2_fold_change"])
    for gene in genes:
        writer.writerow([gene, f"{rng.gauss(0, 1.2):.2f}"])

(OUT / "README.txt").write_text("""\
EXAMPLE FILES FOR DAY 1: KINDS OF FILES

These files show the difference between plain text and other file formats.
All values are simulated teaching data. Open each file in a plain-text editor
(Notepad, TextEdit in plain-text mode, or RStudio) and see what you get.

seedling-notes.txt       A short note as plain text.
seedling-notes.docx      The same note as a Word document.
seedling-notes.pdf       The same note as a PDF.
seedlings.xlsx           data/seedlings.csv as an Excel workbook, with a
                         formatted header, a growth formula and a second sheet.
seedlings-semicolon.csv  The same table as a Swedish-language Excel saves "CSV":
                         semicolons between values and decimal commas.
genes.csv                A small gene list using old gene symbols (SEPT2,
                         MARCH1, ...) that spreadsheets may turn into dates.
                         The numbers are invented.
seedlings-plot.png       A picture (plot) of the seedling growth.

Do not edit these files in place. Copy one to output/ before experimenting.
""")

# --- Binary formats ----------------------------------------------------------
env = dict(os.environ, SOURCE_DATE_EPOCH="1767225600")  # 2026-01-01
with tempfile.TemporaryDirectory(prefix="build-examples-") as tmp:
    tmp = Path(tmp)
    profile = f"-env:UserInstallation=file://{tmp}/lo-profile"

    markdown = tmp / "seedling-notes.md"
    # In Markdown the title becomes a heading; ordinary quotes become curly
    # "smart" quotes, exactly as a word processor does when you type them.
    markdown.write_text("# " + NOTE_TITLE + "\n\n" + "\n\n".join(NOTE_BODY) + "\n")
    subprocess.run(["pandoc", str(markdown), "-o", str(OUT / "seedling-notes.docx")],
                   check=True, env=env)
    subprocess.run(["soffice", profile, "--headless", "--convert-to", "pdf",
                    "--outdir", str(OUT), str(OUT / "seedling-notes.docx")],
                   check=True, capture_output=True)

    # A flat OpenDocument spreadsheet lets us describe styles, a formula
    # column and a second sheet in plain XML; LibreOffice converts it to .xlsx.
    def cell(value, style=None):
        attr = f' table:style-name="{style}"' if style else ""
        try:
            number = float(value)
        except ValueError:
            return (f'<table:table-cell{attr} office:value-type="string">'
                    f"<text:p>{escape(value)}</text:p></table:table-cell>")
        return (f'<table:table-cell{attr} office:value-type="float" '
                f'office:value="{number}"><text:p>{value}</text:p></table:table-cell>')

    rows = ["<table:table-row>" + "".join(cell(h, "header") for h in HEADER + ["growth_mm"])
            + "</table:table-row>"]
    for i, row in enumerate(ROWS, start=2):
        formula = f'<table:table-cell table:style-name="onedec" table:formula="of:=[.D{i}]-[.C{i}]" office:value-type="float"/>'
        rows.append("<table:table-row>" + "".join(cell(v) for v in row) + formula
                    + "</table:table-row>")
    notes = ["Simulated teaching data, not a real experiment.",
             "Lengths in millimetres. growth_mm is a formula: final_mm - initial_mm.",
             "The same values are in data/seedlings.csv."]
    note_rows = "".join(f"<table:table-row>{cell(n)}</table:table-row>" for n in notes)
    fods = f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
 xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
 xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
 xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
 office:version="1.2" office:mimetype="application/vnd.oasis.opendocument.spreadsheet">
<office:automatic-styles>
 <number:number-style style:name="N1"><number:number number:decimal-places="1" number:min-integer-digits="1"/></number:number-style>
 <style:style style:name="header" style:family="table-cell">
  <style:table-cell-properties fo:background-color="#cfe8e3"/>
  <style:text-properties fo:font-weight="bold"/>
 </style:style>
 <style:style style:name="onedec" style:family="table-cell" style:data-style-name="N1">
  <style:text-properties fo:color="#6b3fa0"/>
 </style:style>
</office:automatic-styles>
<office:body><office:spreadsheet>
<table:table table:name="measurements">{''.join(rows)}</table:table>
<table:table table:name="notes">{note_rows}</table:table>
</office:spreadsheet></office:body></office:document>
"""
    (tmp / "seedlings.fods").write_text(fods)
    subprocess.run(["soffice", profile, "--headless", "--convert-to", "xlsx",
                    "--outdir", str(OUT), str(tmp / "seedlings.fods")],
                   check=True, capture_output=True)

# --- A picture of the data ----------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

growth = {"control": [], "treated": []}
for plant, group, initial, final in ROWS:
    growth[group].append(float(final) - float(initial))
fig, ax = plt.subplots(figsize=(5, 3.5), dpi=100)
for x, group in enumerate(["control", "treated"]):
    values = growth[group]
    ax.scatter([x + (i % 5 - 2) * 0.04 for i in range(len(values))], values,
               color=["#0f766e", "#6b3fa0"][x])
ax.set_xticks([0, 1], ["control", "treated"])
ax.set_xlim(-0.6, 1.6)
ax.set_ylabel("Growth over seven days (mm)")
ax.set_title("Simulated seedling growth")
fig.tight_layout()
fig.savefig(OUT / "seedlings-plot.png", metadata={"Software": None})
plt.close(fig)

for leftover in OUT.glob("*.fods"):
    leftover.unlink()
print("Built", ", ".join(sorted(p.name for p in OUT.iterdir())))
