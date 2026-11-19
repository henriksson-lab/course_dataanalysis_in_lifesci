# Week 5 instructor notes

## Day 21 — how a computer works, and data size

Goal: a rough working model (CPU, RAM, disk, GPU; program versus process) and
the habit of estimating RAM before loading data: rows × numeric columns × 8
bytes, then 2–3× working space. Units are decimal (1 MB = 1e6 bytes); use
`format(object.size(x), units = "MB", standard = "SI")`.

Checked numbers (see `week5-solutions.R`, which writes
`output/instructor-week5/data-size.txt`):

- `rnorm(1e6)`: 8,000,048 bytes. `data/seedlings.csv`: 592 bytes on disk, a few
  thousand bytes as a tibble (bookkeeping dominates tiny tables).
- `set.seed(21)`, 100,000 × 10 rounded values: CSV 4.79 MB, object 8.0 MB.
  Adding unique IDs `S000001`…: CSV 5.59 MB, object 14.4 MB (IDs 6.4 MB).
  One million unrounded numbers: CSV 18.6 MB, object 8.0 MB.
- `data/dna.txt`: 40 letters, 41 bytes; A11, C9, G9, T11. Genome ≈ 3.1 GB as
  text, ≈ 25 GB as separate letters in R. `data/pixels.csv`: 8 × 8, 24 pixels
  above 100. 2048 × 2048 image: 4.2 MB file, 33.6 MB in R; 100 images 3.4 GB.
- Single-cell: 30,000 × 100,000 × 8 = 24 GB > 16 GB laptop.

Do not let students try to exhaust RAM on their own laptops. Logical cores from
`parallel::detectCores()` may be twice the physical count; that is fine.

## Day 22 — remote workflow

Only mark the practical complete after students have used the real service.
The local rehearsal cannot validate authentication, host verification, desktop
access, transfer, or where computations are permitted. Supply a one-page service
guide once those details are confirmed. Demonstrate a deliberate transfer with
source and destination visible; ask which computer contains each copy.

Common misconception: the terminal window stores the files. Reconnect and find
the saved file to distinguish session state from persistent storage. Do not
promise that a process continues after disconnection; that depends on how the
service runs it. No scheduler or HPC administration curriculum is assumed.
Open by linking back to Day 21: data larger than laptop RAM is the reason to use
a bigger computer.

## Day 23 — integrated duckweed study

See `week5-solutions.R` for a complete source report and actual estimates. There
are 20 unique flasks, 10 control observations, and 9 available nutrient observations.
F17's missing measurement stays missing in the raw table. Inferential direction
is nutrient minus control. Look for explanation of the experiment, units, counts,
observations, difference, interval, and limitation rather than a p-value alone.

Use the source-report generator as an instructor reference. It is excluded from
the student ZIP and website. This is formative work, not an assessment rubric.

## Day 24 — reproduce and share

The day now also teaches ZIP packaging (moved from the old Day 5). Sequence:
restart R and Knit; build `report-share/` outside the project; from its parent
run `zip -r report-share-v1.zip report-share/` and `unzip -l`; extract with
`unzip report-share-v1.zip -d receiver-v1`, which yields
`receiver-v1/report-share/...` (one extra level); open that copy's `.Rproj`,
restart and Knit. Expected duckweed values: control n = 10, mean 32.28 mg;
nutrient n = 9, mean 39.63 mg (F17 missing). Then edit the source README, show
that v1 and `receiver-v1` still hold the old text, make and test
`report-share-v2.zip`. A ZIP beside the original is not a backup; students record
where their separate copy is.

Controlled cases in disposable copies: renamed CSV stops rendering with an error
naming the file; "All 20 flasks had a measured biomass." renders but is false.
Algae brief: reference n = 12, mean 28.20 mg; supplement n = 11, mean 33.92 mg
(33.91818 unrounded; A19 missing).

Have a peer try the package before offering to fix it. Common problems: `.Rmd`
moved into a subfolder; data omitted; absolute input paths; objects created only
in console; package loading omitted; a shortcut mistaken for a copied file; the
ZIP made inside the folder it packs; Knitting the original instead of the
extracted copy (check the project name). On Windows, copying to WSL creates a
separate working copy: revise, recopy, repackage, and return the ZIP to native
Windows storage for testing.

## Day 25 — completion checks

Station 1: five manifest lines including header, two treated records; extraction
creates ordinary files. Redirection changes the destination text file only.
Station 2: load packages, use data/ path, use consistent object/column names,
and subtract initial from final. P01 grew 18.6 mm. Station 3 answers are on the
student page. Student self-checks concern understanding and recovery, not grading.

Protect catch-up time. If students cannot find their project or render a report,
more modelling content is not the remedy.
