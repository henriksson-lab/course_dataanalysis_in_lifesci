"""Build student archives using an explicit allowlist; exclude instructor files."""

from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import csv
import io

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "downloads"
DOWNLOADS.mkdir(exist_ok=True)


class CourseArchive(ZipFile):
    """Stable timestamps keep checked downloads identical to published copies."""

    def writestr(self, name, data, compress_type=None, compresslevel=None):
        info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED if compress_type is None else compress_type
        info.external_attr = 0o100644 << 16
        return super().writestr(info, data, compresslevel=compresslevel)

    def write(self, filename, arcname=None, compress_type=None, compresslevel=None):
        source = Path(filename)
        return self.writestr(str(arcname or source.name), source.read_bytes(),
                             compress_type=compress_type, compresslevel=compresslevel)


with CourseArchive(DOWNLOADS / "course-files.zip", "w", ZIP_DEFLATED) as archive:
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

with CourseArchive(DOWNLOADS / "lab-data.zip", "w", ZIP_DEFLATED) as archive:
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

with CourseArchive(DOWNLOADS / "organic-lab.zip", "w", ZIP_DEFLATED) as archive:
    archive.write(ROOT / "data/organic-inventory.tsv", "inventory.tsv")
    archive.write(ROOT / "data/organic-recovery.csv", "organic-recovery.csv")
    archive.writestr("README.txt", (
        "SIMULATED ORGANIC-LAB PRACTICE FILES\n"
        "No prior chemistry is needed. This exercise searches supplied labels\n"
        "and inspects numerical records; no laboratory procedure is required.\n"
        "inventory.tsv has one header and four sample records. O01 is labelled\n"
        "alcohol, O02/O03 ester, O04 carboxylic-acid. These labels are given.\n"
        "The recovery CSV describes twelve independent synthesis runs, six\n"
        "per randomly assigned collection protocol. Read DICTIONARY.txt.\n"
    ))
    archive.writestr("DICTIONARY.txt", (
        "SIMULATED DATA DICTIONARY\n"
        "inventory.tsv: sample_id (O01..O04); sample_class (given text label);\n"
        "note (plain text). Two records contain the literal text ester.\n\n"
        "organic-recovery.csv: run_id (Y01..Y12); protocol (standard/modified);\n"
        "theoretical_mass_g (supplied maximum possible product mass, grams);\n"
        "isolated_mass_g (dry collected product, grams, assumed pure here).\n"
        "Percentage yield = 100 * isolated_mass_g / theoretical_mass_g.\n"
        "Example Y01: 100 * 0.62 / 1.00 = 62 percent.\n"
        "Each row is one independent run; there are no missing values.\n"
        "Starting scales vary, so compare percentage yields, not raw grams.\n"
        "Higher yield does not establish purity or overall protocol superiority.\n"
    ))

print("Built course-files.zip, lab-data.zip, and organic-lab.zip in downloads/.")
