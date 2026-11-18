# Exercise review: weeks 1–2

Reviewed all ten modules against the actual files and progression. The 2027
Organic Chemistry 1 dossier identifies a shortened 7.5 ECTS course, while its
detailed syllabus and practical list remain unconfirmed. The 15 ECTS predecessor
is not a prerequisite list for our computing exercises. Added only basic sample
records and numerical product-yield contexts; no reactions, structures,
mechanisms, spectra, or specialist software.

Every new chemistry instruction defines terms, gives masses/units or supplied
labels, states the operation, and provides a checkable answer. The additions are
choose-one replacements for transfer practice, not a second mandatory workload.

| Day | Exercise review / decision | Change or reason to retain | Validation |
| --- | --- | --- | --- |
| 1: files | Download, extract, preserve, and reopen remain the priority | Retained the seedling file throughout; another subject context would obscure the first file-system encounter | Checked expected project files and P01 values against the supplied CSV; links and syntax reviewed |
| 2: paths/computer | Folder tree and save/discard exercise are concrete and independent of chemistry | Retained: this is the prerequisite for reliable laboratory files of any kind | Followed the folder routes in the illustrated tree; relative-path answers and saved note locations agree |
| 3: terminal | Navigation, empty folders, case differences, and recovery are paced before file searching | Retained: no additional organic terminology or commands | Checked command sequence in a disposable shell workspace; acknowledged default Mac case behaviour |
| 4: archives | Four-record seedling archive makes headers, matching, pipes, and preserved input explicit | Retained its original fixture and answers; organic transfer belongs after repetition | Tested supplied archive: 4 records, 5 lines, S03/S04 matched, input preserved |
| 5: repeat/share | Partner explanation can transfer the same file skills to a new context | Added choose-one organic-inventory task using a separate ZIP, supplied class labels, and same commands; original report packaging retained | Actual organic ZIP extraction, inventory, two ester matches, saved extract and original preservation checked |
| 6: R arithmetic | Existing plant subtraction/vectors establish the main R progression | Added percentage-yield alternative to the ratio task: 1.00 g supplied maximum, 0.62 g collected, formula and assumptions explicit | R reference script checks 62%, then 70% after input change; plant vector checks retained |
| 7: table import | Columns, types, units, paths, NA, and a second table already provide transfer | Retained: adding another import exercise would duplicate day 8's organic table | R reference script checks 24 × 4 complete seedling table, types, leaf table and identifiers |
| 8: derived columns/plots | Extra plant-plot variation is a natural substitution point | Added choose-one organic table transfer: derive yield percentages, plot observations, export table/figure; scaling and interpretation limits explicit | Script checks all 12 yields against actual data, produces PNG/CSV, and preserves input; Y01 = 62% |
| 9: R Markdown | Instructions could be misread as asking a report to render itself | Explicitly put `rmarkdown::render()` in the Console and prohibit putting it inside the report; kept the complete literal example and biological report | All R chunks parse; complete generated week2 report renders in a fresh environment; literal example inspected |
| 10: complete report | Same self-render ambiguity; otherwise question/data/method/results/interpretation are well specified | Explicit Console-only render command; retained main seedling report and existing leaf-table transfer to avoid another required report | Instructor source renders; checks its input data, derived column and plot; output location remains documented |

Validation uses `Rscript instructor/week2-solutions.R` from the repository root
and disposable shell workspaces. `knitr::purl()` plus `parse()` checks executable
R chunks in the ten lesson pages. Graphical file-manager actions and Mac keyboard
behaviour still require the planned student-machine pilot; no such cross-platform
execution is claimed here. Root performs final website/link/packaging checks.
