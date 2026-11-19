"""Check built course links, student archives, and the taught shell workflow."""

from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile
import csv
import io
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

# The daily progression must be present in the student site.
lessons = sorted(p for p in ROOT.glob("week[1-5]/[0-9][0-9]-*.qmd")
                       if not p.stem.endswith("-quiz"))
assert len(lessons) == 25, f"Expected 25 daily lessons, found {len(lessons)}"
for source in lessons:
    assert (ROOT / "docs" / source.relative_to(ROOT).with_suffix(".html")).is_file(), source

class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in {"href", "src"} or not value:
                continue
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = unquote(parsed.path)
            destination = ROOT / "docs" / target.lstrip("/") if target.startswith("/") else self.path.parent / target
            if not destination.exists():
                missing.append((self.path.relative_to(ROOT).as_posix(), value))

missing = []
for path in (ROOT / "docs").rglob("*.html"):
    parser = Links()
    parser.path = path
    parser.feed(path.read_text())
assert not missing, f"Broken local links: {missing}"
assert not (ROOT / "docs/instructor").exists(), "Instructor material was published"
assert not (ROOT / "docs/contentplan.html").exists(), "Internal plan was published"

for download in (ROOT / "downloads").glob("*.zip"):
    assert download.read_bytes() == (ROOT / "docs/downloads" / download.name).read_bytes(), (
        f"Published archive differs from checked download: {download.name}"
    )

with ZipFile(ROOT / "downloads/course-files.zip") as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert all(name.startswith("introcomputing-course/") for name in names)
    assert not any("instructor" in name or "/.git" in name for name in names)
    for source in (ROOT / "data").glob("*"):
        assert archive.read("introcomputing-course/data/" + source.name) == source.read_bytes()
    assert archive.read("introcomputing-course/report.Rmd") == (ROOT / "report.Rmd").read_bytes()

# Run the actual shell commands against the actual download, in a disposable dir.
with tempfile.TemporaryDirectory(prefix="introcomputing-shell-") as directory:
    workspace = Path(directory)
    archive_path = ROOT / "downloads/lab-data.zip"
    subprocess.run(["unzip", "-l", str(archive_path)], check=True, capture_output=True)
    subprocess.run(["unzip", str(archive_path), "-d", str(workspace / "lab-data")],
                   check=True, capture_output=True)
    lab = workspace / "lab-data"
    matches = subprocess.run(["grep", "-F", "treated", "samples.tsv"], cwd=lab,
                             check=True, capture_output=True, text=True).stdout
    assert len(matches.splitlines()) == 2
    assert "S03" in matches and "S04" in matches
    (lab / "treated-samples.txt").write_text(matches)
    with (lab / "treated-samples.txt").open() as handle:
        count = subprocess.run(["wc", "-l"], stdin=handle, check=True,
                               capture_output=True, text=True).stdout
    assert int(count.strip()) == 2
    with (lab / "samples.tsv").open() as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    assert len(manifest) == 4
    assert all((lab / row["file"]).is_file() for row in manifest)
    subprocess.run(["zip", "-r", "lab-copy.zip", "lab-data/"], cwd=workspace,
                   check=True, capture_output=True)
    with ZipFile(workspace / "lab-copy.zip") as archive:
        assert archive.read("lab-data/treated-samples.txt").decode() == matches

with tempfile.TemporaryDirectory(prefix="introcomputing-organic-") as directory:
    workspace = Path(directory)
    subprocess.run(["unzip", str(ROOT / "downloads/organic-lab.zip"), "-d", str(workspace)],
                   check=True, capture_output=True)
    matches = subprocess.run(["grep", "-F", "ester", "inventory.tsv"], cwd=workspace,
                             check=True, capture_output=True, text=True).stdout
    assert len(matches.splitlines()) == 2
    assert "O02" in matches and "O03" in matches
    with (workspace / "inventory.tsv").open() as handle:
        inventory = list(csv.DictReader(handle, delimiter="\t"))
    assert len(inventory) == 4
    assert (workspace / "organic-recovery.csv").read_bytes() == (ROOT / "data/organic-recovery.csv").read_bytes()
    assert "100 * isolated_mass_g / theoretical_mass_g" in (ROOT / "data/README.md").read_text()

print("25 lessons built; local links/resources resolve; student archives and both shell workflows pass.")
