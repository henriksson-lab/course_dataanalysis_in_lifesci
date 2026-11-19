# Wording and quiz audit — results

Audit of the draft at `6943181`, following [the agreed plan](audit-plan.md).
The three pilot modules were terminal navigation, initial R calculations, and
Welch comparisons. Parallel editors then revised weeks 1–2, weeks 3–4, and week 5;
root reviewed the changes, and a separate editor cross-reviewed the other weeks.

## Changes

- Removed all 50 explicit exercise-duration estimates and the public daily-hour
  budget. The study guide now gives the sequence, outputs, and checkpoints.
- Replaced required exchanges and peer checks with fresh-terminal, fresh-session,
  saved-instruction, or new-extraction checks. All exercises can be completed
  independently. Scientific pairs and biological replication remain distinct.
- Removed redundant prohibitions, repeated scope disclaimers, writing quotas,
  and generic preambles. Task headings describe the actual operation. Kept
  beginner definitions, supplied formulas and units, and consequential cautions
  such as output redirection overwriting a file.
- Retained the expanded calculations, plots, investigations, transfer datasets,
  report tasks, and lecture examples. Biological/chemistry alternatives remain
  choices within a task; no chemistry course is a prerequisite.
- Added 25 topic quizzes with 126 questions and separate collapsed hints and
  answers. Each topic sidebar has Lecture, Exercises, and Quiz links. The five
  weekly quizzes remain revision collections with 62 further questions.
- Removed minimum word, step, and slide-growth gates from the historical expansion
  counter. Counts are descriptive; checks still cover calculations, reports,
  downloads, links, quiz structure, slide limits, and assets.

## Corrections found during review

- Day 2: moving `map-a` changes both documented routes, not just one.
- Day 9: the copied project explicitly includes its `.Rproj` and the folders
  needed by output-writing code.
- Day 18: supplied the connected before/after plot pattern and qualified the
  change vector in the equivalent one-sample calculation. Clarified that this
  is an equivalent calculation, not formal equivalence testing.
- Corrected two LaTeX multiplication escapes and a revision-question typo.

## Module checklist

For each module, the wording check covered pace prescriptions, mandatory
collaboration, repeated restrictions, and writing quotas. The workflow check
covered supplied inputs/definitions, independent actions, saved outputs, and
answer checks. Lecture notes and associated weekly revision questions were
included. Quiz counts report coverage; they are not writing targets.

| Module | Wording | Workflow and supplied inputs | Topic questions |
| --- | --- | --- | --- |
| [01-files](../week1/01-files.qmd) | Checked | Checked | 5 |
| [02-folders-computers](../week1/02-folders-computers.qmd) | Checked | Checked | 5 |
| [03-terminal](../week1/03-terminal.qmd) | Checked | Checked | 5 |
| [04-inspect-archive](../week1/04-inspect-archive.qmd) | Checked | Checked | 5 |
| [05-meet-r](../week1/05-meet-r.qmd) | Checked | Checked | 5 |
| [06-r-basics](../week2/06-r-basics.qmd) | Checked | Checked | 6 |
| [07-import](../week2/07-import.qmd) | Checked | Checked | 5 |
| [08-transform-plot](../week2/08-transform-plot.qmd) | Checked | Checked | 5 |
| [09-rmarkdown](../week2/09-rmarkdown.qmd) | Checked | Checked | 5 |
| [10-first-report](../week2/10-first-report.qmd) | Checked | Checked | 5 |
| [11-data-quality](../week3/11-data-quality.qmd) | Checked | Checked | 5 |
| [12-variation](../week3/12-variation.qmd) | Checked | Checked | 5 |
| [13-group-summaries](../week3/13-group-summaries.qmd) | Checked | Checked | 5 |
| [14-replicates-uncertainty](../week3/14-replicates-uncertainty.qmd) | Checked | Checked | 5 |
| [15-descriptive-report](../week3/15-descriptive-report.qmd) | Checked | Checked | 5 |
| [16-comparisons](../week4/16-comparisons.qmd) | Checked | Checked | 5 |
| [17-welch-test](../week4/17-welch-test.qmd) | Checked | Checked | 6 |
| [18-paired](../week4/18-paired.qmd) | Checked | Checked | 5 |
| [19-calibration](../week4/19-calibration.qmd) | Checked | Checked | 5 |
| [20-association](../week4/20-association.qmd) | Checked | Checked | 6 |
| [21-computer](../week5/21-computer.qmd) | New (2026-11) | New (2026-11) | 7 |
| [22-remote-workflow](../week5/22-remote-workflow.qmd) | Checked | Checked | 5 |
| [23-mini-study](../week5/23-mini-study.qmd) | Checked | Checked | 5 |
| [24-reproduce](../week5/24-reproduce.qmd) | Checked | Checked | 4 |
| [25-consolidate](../week5/25-consolidate.qmd) | Checked | Checked | 4 |

## Verification

Numerical and code-prediction quiz answers were checked in R or shell fixtures
against the actual supplied datasets and toy inputs. This included vector
assignment, growth, missingness, concentrations and dilution, yield, variance and
rescaling, sampling, Welch and paired results, calibration/range checks, line
units, sequence/pixel counts, and algae sensitivity. New paired-plot code builds
successfully and its paired/one-sample intervals agree.

The instructor calculation/report scripts for weeks 2–5 and transfer-data checks
pass. The starter report renders from an extracted student project. Source
comparison confirms that day 18 is the only exercise with changed code blocks;
other edits retain their original executable examples.

The full 91-page render, archive/link checks, and quiz-structure checks pass.
The browser check passes all 25 decks / 459 slides with no presentation-frame
overflow and verifies the sidebar colours. It also opens a collapsed topic Quiz
entry and reveals an answer at desktop (1440 px) and mobile (390 px) widths.
All decks stay below 45 slides; 224 of 434 content slides contain visuals.

## Remaining deployment dependencies

HPC2N/service account, host-verification, desktop, transfer, and execution details
are still pending. Local rehearsal is labelled separately and does not count as
real remote access. Windows/Mac installation and beginner usability still need a
student-machine pilot. These were not invented or treated as resolved by the
audit. Examination design remains outside the work.
