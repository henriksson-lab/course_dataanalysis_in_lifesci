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

Expected files: unchanged `data/seedlings.csv`, practice copy at
`output/seedlings-practice.csv`, and a plain-text `reports/day01-notes.txt`.

Accept notes equivalent to: one row describes one seedling; lengths are in mm;
original file is inside project `data/`. Initial/final are two observations of
the same plant, not two independent plants. P01 grows 18.6 mm, not 44.3 mm.

Watch students perform closing and reopening rather than accepting an already
open window. Show file extensions on a projected machine, and explain that
changing an extension does not convert the format. If a spreadsheet autoformats
on open, closing without saving protects the supplied raw file. TextEdit needs
plain-text mode. Avoid silently repairing students' locations for them: narrate
each folder choice.

## Day 2

Expected tree extension:

```text
introcomputing-course/
├── practice/
│   ├── field-notes/
│   │   └── seedling-observations.txt
│   └── figures/
└── reports/
    └── day02-map.txt
```

From project root, original table is `data/seedlings.csv`. Relative paths depend
on the starting folder; a path that works in the project root need not work
inside `reports`. Introduce this verbally before syntax involving `..`.

RAM is working memory for running programs; persistent storage retains saved
files. CPU executes instructions. OS manages resources. A process is a running
instance. Do not imply cloud files always have full local copies or that the
application closing always discards unsaved text: many editors recover sessions
or autosave. Compare saved contents explicitly. No specific backup service has
yet been approved; supply the university-supported route before teaching it.

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

## Day 5

Full repeat and package sequence, starting where `lab-data.zip` is located:

```bash
cd ~/introcomputing-shell
mkdir day5
cp lab-data.zip day5/
cd day5
unzip -l lab-data.zip
unzip lab-data.zip -d lab-data
cd lab-data
less README.txt
grep -F treated samples.tsv > treated-samples.txt
grep -F treated samples.tsv | wc -l
mkdir report
cp treated-samples.txt report/
cp README.txt report/context.txt
```

Students create `report/findings.txt` in a plain-text editor, then:

```bash
zip -r report-bundle.zip report/
unzip -l report-bundle.zip
unzip report-bundle.zip -d review
ls review/report
```

Check extracted `context.txt`, `findings.txt`, `treated-samples.txt`. Exact archive
dates and size summaries need not match. A ZIP next to source files is not an
independent backup. Re-running `zip` can update an archive; using a new name
after revisions is simpler for novices than teaching archive-update semantics.

R calculation: 18.6 mm. Supplied scatter plot contains three points, initial
length on horizontal axis and final length on vertical axis. These three P01–P03
records are controls; do not present their plot as a treatment comparison. The
purpose is distinguishing R console, editor, and shell and seeing a future result.

### Day 5 alternative partner task: organic inventory

This replaces the partner explanation exercise; it is not extra required work.
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

## Quick formative observations

Ask a student to show the actual folder, identify an unchanged source file,
explain the selected record count, and reopen their extracted findings. Listen
for "it's in Excel" or "it's in the terminal" as location answers: these name
applications, not saved file locations. Use another short navigation attempt to
resolve the misconception before adding syntax.
