"""Build student archives using an explicit allowlist; exclude instructor files."""

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import csv
import io

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "downloads"
DOWNLOADS.mkdir(exist_ok=True)

with ZipFile(DOWNLOADS / "course-files.zip", "w", ZIP_DEFLATED) as archive:
    files = [ROOT / "introcomputing.Rproj", ROOT / "report.Rmd"]
    files += sorted((ROOT / "data").glob("*"))
    files += [ROOT / "reports/README.txt", ROOT / "output/README.txt"]
    for source in files:
        archive.write(source, "introcomputing-course/" + source.relative_to(ROOT).as_posix())
    archive.writestr("introcomputing-course/START-HERE.txt", (
        "All datasets are simulated teaching data.\n"
        "Extract this entire folder before opening introcomputing.Rproj in RStudio.\n"
        "Use data/README.md for study designs, units, and missing-value meanings.\n"
        "report.Rmd is an intentionally guided first report; render with Knit.\n"
        "Save new .Rmd reports beside report.Rmd in this project root.\n"
        "Never include passwords or login codes in reports.\n"
    ))

with ZipFile(DOWNLOADS / "lab-data.zip", "w", ZIP_DEFLATED) as archive:
    archive.writestr("README.txt", (
        "SIMULATED LAB-GROUP DATA\n"
        "Four independent seedling pots, two control and two nutrient-treated.\n"
        "Each measurement file has one observation of length after seven days.\n"
        "Lengths are millimetres. samples.tsv lists sample IDs and file locations.\n"
        "The field-notes folder contains short observations; it is plain text.\n"
    ))
    manifest = io.StringIO()
    writer = csv.writer(manifest, delimiter="\t", lineterminator="\n")
    writer.writerow(["sample_id", "treatment", "file"])
    for index, (group, length) in enumerate([
        ("control", 32.1), ("control", 35.2), ("treated", 42.4), ("treated", 39.8)
    ], 1):
        sample = f"S{index:02d}"
        path = f"measurements/{sample}.csv"
        writer.writerow([sample, group, path])
        archive.writestr(path, f"sample_id,length_mm\n{sample},{length}\n")
    archive.writestr("samples.tsv", manifest.getvalue())
    archive.writestr("field-notes/day1.txt", "All four pots were watered at 09:00.\n")
    archive.writestr("field-notes/day7.txt", "Lengths were measured after seven days.\n")

print("Built downloads/course-files.zip and downloads/lab-data.zip")
