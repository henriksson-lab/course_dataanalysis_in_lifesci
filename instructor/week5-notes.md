# Week 5 instructor notes

## Day 21 — remote workflow

Only mark the practical complete after students have used the real service.
The local rehearsal cannot validate authentication, host verification, desktop
access, transfer, or where computations are permitted. Supply a one-page service
guide once those details are confirmed. Demonstrate a deliberate transfer with
source and destination visible; ask which computer contains each copy.

Common misconception: the terminal window stores the files. Reconnect and find
the saved file to distinguish session state from persistent storage. Do not
promise that a process continues after disconnection; that depends on how the
service runs it. No scheduler or HPC administration curriculum is assumed.

## Day 22 — representations

The DNA string has 40 characters: A11, C9, G9, T11. There is one stored input
string. The image is 8 by 8: 24 cells have intensity 210 and 40 have intensity 25.
Thresholds 50 and 100 select 24 cells, whereas 220 selects none. A pixel count
does not specify physical size without a calibration. Neither count supplies
independent biological replication.

Run the supplied unfamiliar syntax as a demonstration and focus on its meaning;
do not make `[[1]]` or graphics internals a new programming unit.

## Day 23 — integrated duckweed study

See `week5-solutions.R` for a complete source report and actual estimates. There
are 20 unique flasks, 10 control observations, and 9 available nutrient observations.
F17's missing measurement stays missing in the raw table. Inferential direction
is nutrient minus control. Look for explanation of the experiment, units, counts,
observations, difference, interval, and limitation rather than a p-value alone.

Use the source-report generator as an instructor reference. It is excluded from
the student ZIP and website. This is formative work, not an assessment rubric.

## Day 24 — reproducibility

Test extraction in a folder with a different name. A successful original-session
run is insufficient. Have a peer try the package before offering to fix it.
Common problems: `.Rmd` moved into a subfolder; data omitted; absolute input paths;
objects created only in console; package loading omitted; a shortcut mistaken
for a copied file. On Windows, copying to WSL creates a separate working copy:
revise, recopy, repackage, and return the ZIP to native Windows storage for testing.

## Day 25 — completion checks

Station 1: five manifest lines including header, two treated records; extraction
creates ordinary files. Redirection changes the destination text file only.
Station 2: load packages, use data/ path, use consistent object/column names,
and subtract initial from final. P01 grew 18.6 mm. Station 3 answers are on the
student page. Student self-checks concern understanding and recovery, not grading.

Protect catch-up time. If students cannot find their project or render a report,
more modelling content is not the remedy.
