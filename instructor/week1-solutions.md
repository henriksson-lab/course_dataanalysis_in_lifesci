# Week 1 — instructor notes and solutions

Student pages deliberately assume no file-system vocabulary. A successful day
can be finding and reopening a saved file, not reaching more commands. There
are no assessment requirements here. Protect time for installation help and
repeat navigation whenever students cannot explain their current location.

## Common setup for demonstrations

Keep the native R project and terminal workspace distinct. Native course
project: extracted `introcomputing-course/` in an accessible laptop folder.
Terminal workspace: `~/introcomputing-shell`. On Windows, use `explorer.exe .`
to reveal that Ubuntu workspace, then copy the downloaded `lab-data.zip` there
visibly. Do not assume a Linux `~/Downloads` directory maps to the browser's
Windows Downloads folder. On Mac, `open .` reveals the workspace in Finder.

Remote account setup is pending. Demonstrate local/remote location explicitly
when available, but do not stall week 2 because accounts are missing. SSH and
remote desktop are access routes, not automatic file synchronisation. Exact
hostname, authentication, service policy, and transfer route must come from the
confirmed course service.

## Day 1

Topic: kinds of files, especially plain text versus Word/Excel. Example files
are in `examples/` (built by `tools/build_examples.py`; see `examples/README.txt`).

Expected files: unchanged `data/seedlings.csv`, practice copy
`output/seedlings-practice.csv`, plain-text `reports/day01-notes.txt`, and
`reports/file-types.txt`. Day 2 relies on the first two.

Accept notes equivalent to: one row describes one seedling; lengths in mm; an
`.xlsx` can store formatting, formulas or several sheets; saving raw data from
a spreadsheet can change it (gene names to dates, semicolon/decimal-comma CSV).
P01 grows 44.3 − 25.7 = 18.6 mm.

`file-types.txt` solution. Plain text: all of `data/`, `report.Rmd`,
`introcomputing.Rproj` (RStudio settings as text; often a surprise),
`START-HERE.txt`, `examples/README.txt`, `seedling-notes.txt`, `genes.csv`,
`seedlings-semicolon.csv`. Not text: `seedling-notes.docx` (16-file ZIP; the
text is in `word/document.xml`), `seedlings.xlsx` (bold coloured header,
formula `growth_mm` = `=D2-C2` showing 18.6 in E2, second sheet `notes`),
`seedling-notes.pdf` (starts `%PDF`), `seedlings-plot.png` (starts `PNG`).

Teaching points and pitfalls:

- Test the Mac route before class. TextEdit renders `.docx` as a formatted
  document; **File → Open → Options → Ignore rich text commands** should show
  the raw content, and renaming a copy to `.txt` is the fallback. Notepad on
  Windows shows `PK...` directly.
- `genes.csv`: Excel (English locale) shows `SEPT2` as `2-Sep` and `MARCH1` as
  `1-Mar`. LibreOffice 7.3 kept the symbols as text in our test, and Swedish
  Excel may behave differently; the lecture figure is the fallback. Source:
  Ziemann, Eren & El-Osta (2016), *Genome Biology* 17:177 (704 of 3,597 papers,
  about 20%). HGNC renamed SEPT/MARCH genes (SEPTIN2, MARCHF1) in 2020.
- `seedlings-semicolon.csv`: R's `read.csv()` stops with "more columns than
  column names"; `read.csv2()` reads it. Mention only; R comes later.
- The `.docx` has curly quotes in its R line (pandoc's smart quotes, as Word's
  autocorrect would do). Pasting it into R gives `Error: unexpected input`.
- Renaming a `.csv` to `.xlsx` makes Excel refuse to open it; renaming the
  `.docx` copy to `.zip` works because it is a ZIP.
- Watch students reopen the note from the file manager, and check the name ends
  in `.txt` (not `.rtf` or `.txt.txt`).

## Day 2

Topic: folders and paths. Hardware (CPU, RAM, storage, processes) moved to a
later day; keep only "unsaved work is in memory and disappears; saved work is
on disk".

Expected tree extension:

```text
introcomputing-course/
├── practice/
│   ├── field-notes/
│   │   └── seedling-observations.txt
│   ├── figures/
│   └── map-b/
│       └── map-a/
│           └── note.txt
└── reports/
    └── day02-map.txt
```

From the project folder, the original table is `data/seedlings.csv`; from
`reports` it is `../data/seedlings.csv` (introduce `..` verbally; the terminal
day uses it). Map task: before the move `practice/map-a/note.txt` and, from
inside `map-b`, `../map-a/note.txt`; after the move
`practice/map-b/map-a/note.txt` and `map-a/note.txt`. The note's contents are
unchanged.

Do not imply that cloud files always have full local copies, or that closing an
editor always discards unsaved text: many editors autosave or restore drafts.
Compare saved contents explicitly. No specific backup service has yet been
approved; supply the university-supported route before teaching it.

## Day 3

Minimal navigation sequence:

```bash
cd
mkdir -p introcomputing-shell/practice
cd introcomputing-shell/practice
mkdir seedlings
mkdir observations
cd seedlings
pwd
cd ..
pwd
```

First path ends `/introcomputing-shell/practice/seedlings`; second ends
`/introcomputing-shell/practice`. Folder creation without `-p` will produce an
"already exists" error if repeated. This is an opportunity to inspect, not
delete. Some Mac disks are case-insensitive; Ubuntu is case-sensitive. Teach
matching actual spelling on both rather than promising a particular error.

Distinguish terminal location from file-manager location. A mouse click in Finder
does not execute `cd` in the shell. `ls` in an empty directory prints no visible
entries; this is a successful result. `~` means the current user's home, not a
literal directory named tilde. Never ask learners to type a printed `$` prompt.

## Day 4

Archive contract: README.txt, samples.tsv, field-notes/, measurements/S01.csv
through S04.csv. Manifest has a header plus four rows; control S01/S02 and
treated S03/S04. Expected counts are 5 full-manifest lines and 2 matching
treated lines. Generated data use trailing newlines so `wc -l` matches records.

```bash
cd ~/introcomputing-shell
unzip -l lab-data.zip
unzip lab-data.zip -d lab-data
cd lab-data
head -n 3 samples.tsv
wc -l samples.tsv
grep -F treated samples.tsv
grep -F treated samples.tsv > treated-samples.txt
grep -F treated samples.tsv | wc -l
mkdir working
cp samples.tsv working/samples-copy.tsv
mv working/samples-copy.tsv working/manifest-practice.tsv
```

Search is literal substring matching, not a TSV-column query. The data labels
were chosen to avoid an `untreated` trap, but explain that limitation. `>` may
truncate an existing destination; do not demonstrate an input/output collision
on actual course files. No recursive delete is needed for this practical.

Expected `working/observations.txt`: four records; S03/S04 treated; S04
measurements at `measurements/S04.csv`; five lines includes one header. A result
with five plants indicates a header was interpreted biologically.

### Day 4 optional organic-laboratory inventory

Optional transfer task at the end of the Day 4 practical.
Use the separate `organic-lab.zip` download so the original `lab-data.zip`
fixture and its treated-sample answers stay unchanged. Students must first use
the file manager to copy the downloaded ZIP into `~/introcomputing-shell`,
including the Windows/Ubuntu bridge. From that workspace:

```bash
unzip -l organic-lab.zip
unzip organic-lab.zip -d organic-lab
cd organic-lab
less README.txt
less DICTIONARY.txt
head inventory.tsv
grep -F ester inventory.tsv > ester-samples.txt
grep -F ester inventory.tsv | wc -l
```

Expected: four sample records and five newline-terminated lines including the
header. O02 and O03 have the supplied class label `ester`, giving two matching
lines. No structure recognition or reaction knowledge is required. Search is
literal substring matching; it does not identify chemical classes itself.
Students locate their saved extract and the untouched inventory. The other
archive file, organic-recovery.csv, is for later numerical work, not a hidden
week1 calculation requirement.

## Day 5 — meet R and RStudio

Orientation only; Day 6 teaches objects, assignment and vectors. Students open
`introcomputing.Rproj` from the extracted course folder (not a ZIP preview, not
RStudio's recent list). Expected Console output:

```r
getwd()                              # ends in introcomputing-course
file.exists("data/seedlings.csv")    # [1] TRUE
44.3 - 25.7                          # [1] 18.6  (P01 growth, mm)
32.3 - 24.3                          # [1] 8     (P02)
pwd                                  # Error: object 'pwd' not found
```

In the shell, `44.3 - 25.7` gives `44.3: command not found`. The supplied plot
(`read.csv` + base `plot`) shows 24 points, final against initial length; the
correlation is weak (r = 0.23), so the plot does not show a strong relationship
and does not show growth. The Environment lists `seedlings` as 24 obs. of 4
variables. Knitting `report.Rmd` gives 12 control plants (mean growth 15.28 mm,
SD 3.19) and 12 treated (21.49 mm, SD 4.87). After quitting and reopening via the
`.Rproj`, the Environment is empty (`SaveWorkspace: No`) while
`reports/day05-notes.txt` and `report.html` remain.

Common problems: `file.exists()` FALSE because the project is not open or an
extra nested folder; `+` prompt after an unfinished line (Esc); Knit fails for a
missing package (installation line on the setup page). RStudio's Terminal tab on
Windows may not be the Ubuntu shell; students keep using their usual terminal.

ZIP packaging (formerly on Day 5) is now taught on Day 24, where a report is
shared; see `week5-notes.md`.

## Quick formative observations

Ask a student to show the actual folder, identify an unchanged source file,
explain the selected record count, and reopen their extracted findings. Listen
for "it's in Excel" or "it's in the terminal" as location answers: these name
applications, not saved file locations. Use another short navigation attempt to
resolve the misconception before adding syntax.

## Expanded practicals and independent transfer, days 1–5

These are core practice blocks, not additional chemistry alternatives or grades.
Check prediction, explanation, and recovery from saved work; each task can be
completed independently.

| Day | Expected evidence and checks |
| --- | --- |
| 1 | file-types.txt classifies every file in data/, examples/ and the project root (see Day 1 solution); the .xlsx extras (formatting, formula, second sheet) and the semicolon/decimal-comma CSV are named; day01-notes.txt is plain text and reopened from the file manager; raw files preserved. |
| 2 | Routes to note.txt before and after moving map-a into map-b are correct (practice/map-b/map-a/note.txt; map-a/note.txt from inside map-b); note contents unchanged; saved/discarded sentence test acknowledges autosave if present; day02-map.txt has a project tree and data/seedlings.csv. |
| 3 | Quoted field notes is one folder; unquoted words may become separate arguments. Failed cd leaves pwd unchanged. Two shells retain different current folders. From results/notes to neighbouring inputs use the common ancestor: up twice, then inputs. Log states computer and predicted versus observed location. |
| 4 | Source manifest: 5 lines / 4 records / 2 treated (S03 42.4 mm, S04 39.8 mm; controls S01 32.1, S02 35.2). Trap copy: untreated makes a third substring match. Deliberate rename of S04 breaks its manifest path; contents S04, 39.8 plus the known action support restoring the filename. Optional organic inventory: 2 ester records (O02, O03). |
| 5 | Project opens from the `.Rproj`; `file.exists("data/seedlings.csv")` TRUE; `pwd`/arithmetic placed in the right program; P01 18.6 mm; plot has 24 points and y is final length, not growth; report.Rmd knits; note survives restart while objects do not. |

A representative safe shell check in a temporary directory follows the same
operations as the student work: create nested directories and a quoted name;
inspect and extract the actual archive; make a manifest copy with S01 labelled
untreated; verify three substring matches; preserve the original; rename and
restore S04 in a copied extraction. Do not demonstrate
input-equals-output redirection on originals. GUI actions and OS-specific
extension/autosave behaviour still need a supported student-machine pilot.

Reproducible command paths are relative to the disposable workspace. When
marking a check as complete, ask the student to locate the ordinary file and
explain the action; a memorised output alone is insufficient.
