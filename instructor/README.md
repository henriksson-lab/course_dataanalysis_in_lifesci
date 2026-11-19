# Instructor guide: reviewing the first teaching draft

The course is built for first-year students who may not yet understand files,
folders, or saved application state. Data Analysis in Life Sciences is a
five-week introduction to computing
in a biological setting, with written examination design outside this work.
This is draft teaching content, not an approved syllabus or a fixed timetable.

## Where to start evaluating

The [chemistry context investigation](chemistry-context.md) supplied the initial
placement ideas. The day 19 dilution correction and later solution/dilution
practice in days 6–8 are implemented; the specific volume-reading illustration
remains a proposal. All chemistry exercises supply terms, inputs, units,
relationships, and requested calculations without prior chemistry.

The [organic-exercise review](organic-context-review.md) records the implemented
basic laboratory alternatives and links the parallel reviews of all 25 days.
These use the 2027 Organic Chemistry 1 scope of 7.5 ECTS as a reason to keep
contexts elementary; they do not assume the full older 15-credit course.

Open `docs/index.html` or run `make preview` from the repository root. The sidebar
contains all 25 daily lessons. The source-of-truth teaching sequence remains
`contentplan.md`; student goals and working instructions are in `overview.qmd`.

For a quick cross-section, read these student pages in order:

| Page | What to evaluate |
| --- | --- |
| `week1/01-files.qmd` | Does it truly start below the assumed file-system baseline? |
| `week1/04-inspect-archive.qmd` | Do ordinary terminal tools solve a comprehensible lab task? |
| `week2/08-transform-plot.qmd` | Is the transition from table to derived variable to plot manageable? |
| `week2/09-rmarkdown.qmd` | Can a beginner distinguish prose, code, and rendered output? |
| `week3/12-variation.qmd` | Are mean, variance, and SD light enough but correctly interpreted? |
| `week4/17-welch-test.qmd` | Does the interpretation emphasise size, uncertainty, and independent units? |
| `week4/19-calibration.qmd` | Does it prepare students for ordinary biochemistry practicals? |
| `week5/23-mini-study.qmd` | Could a student transfer the workflow to a new small dataset? |
| `week5/24-reproduce.qmd` | Does the project render from a newly extracted copy? |

Each daily topic now pairs a separate RevealJS lecture deck with its existing
Exercises page. The slide theme and coloured sidebar follow the Quantitative
Biology scaffold. Lecture links are green, quizzes blue, and practical links
italic; week bands use the scaffold's five colours. Each topic has a quiz with separate collapsible hints and answers; weekly
quizzes provide further revision. No grading scheme is introduced.

Decks use lecturer notes and explanatory diagrams/plots on roughly half their
slides. The user permits up to 45 slides but prefers fewer: do not add slides
to reach a quota. Report/consolidation briefings are intentionally shorter.
Use speaker view for notes; the slides and embedded notes are public teaching
material. There are no recorded lecture videos yet, so the menu does not imply
that recordings exist.

The subsequent [workload expansion](workload-expansion.md) roughly doubles
lecture depth and active practice. Each daily practical now has extended core
work and an independent transfer task, with fresh inputs and checkable outputs.
The student [study plan](../study-plan.qmd) gives weekly checkpoints without
prescribing task durations. The [subsequent audit](audit-results.md) removes
required collaboration and redundant prose while retaining the expanded practice.

## What's supplied

- 25 lecture decks and 25 Exercises pages with biological context, examples, practicals, hints,
  completion questions, and explicitly named saved outputs.
- A Quarto website using the sibling course's actual sidebar CSS, slide theme,
  RevealJS format, lecture/practical pairing, navigation controls, and week colours.
  Website code execution is disabled; example figures are generated separately
  from the actual teaching datasets. Twenty-five topic quizzes have separate collapsed hints and answers.
  Five weekly quizzes provide further revision.
- Fifteen CSV datasets, an organic sample-label TSV, and a tiny DNA string, all
  simulated. The data dictionary
  identifies units, experimental units, and missing values. A separate source
  note justifies the planted data-quality corrections.
- A complete student project ZIP with a working root-level `report.Rmd`, plus
  separate seedling and organic ZIPs for terminal practice. None contains
  instructor files.
- Windows Ubuntu/WSL and Mac Terminal instructions; R/RStudio setup; conceptual
  remote-access guidance with the service-dependent steps clearly pending.
- Four reference pages: terminal commands, R, basic statistical interpretation,
  and a glossary.
- Instructor worked solutions and scripts, including generated report examples.

## Instructor solutions and generated examples

| Block | Source | Outputs/checks |
| --- | --- | --- |
| Week 1 | `instructor/week1-solutions.md` | File and shell workflow, expected counts and recovery hints |
| Week 2 | `instructor/week2-solutions.R` | Growth calculations, exported figures, complete first report |
| Week 3 | `instructor/week3-solutions.R` | Documented cleaning, numerical summaries, sampling demonstration, descriptive report |
| Week 4 | `instructor/week4-solutions.R` | Welch/paired results, calibration inversion with range check, association and residual plots |
| Week 5 | `instructor/week5-solutions.R` | Representation checks and complete duckweed report |

Run the R scripts from the repository root, or use `make check`. Week 2, 3, and
5 report artifacts are saved in `output/instructor-week*/`, ignored by Git and
excluded from the site and ZIPs. Week 4 defaults to temporary outputs; use
`--figures` to regenerate its published lesson plots. Week 2/3 also support
`--figures` for their linked lesson figures. Scripts print output locations.

These scripts check the computations, not just code syntax. A separate check
extracts the actual student ZIP into a temporary folder and renders its report
without using the repository's data paths. `tools/check_course.py` checks the
shell commands against the actual lab archive and verifies built local links.

## Pacing and support

Use each day number as a study unit. A reasonable initial teaching pattern is
a short explanation followed by demonstration and guided work, then another
explanation and practice. Actual contact hours are not specified.
Many students will need substantially more time for installations, paths, typing,
and reopening work than the conceptual explanation takes.

On day 1, find who can save and reopen a file without a recent-files menu. On
day 5, find who can name the current folder and explain an extracted archive.
On day 10, find who can render after restarting R. Use these as support signals,
not grades. Collaboration can be optional, and every task must be completable independently.
Each student practises controlling their session and locating their saved files.

Keep day 25 as consolidation and catch-up. If overloaded, shorten the representations demonstration
and paired-test calculation practice while retaining the paired-design concept.
Do not remove file literacy or fresh-session rendering to fit more methods.

The expanded version uses more independent practice within the same topic
list, rather than a broader method catalogue. New inputs include a second
seedling study, supplied solution/dilution calculations, a second calibration
run, and an algae study. Preserve the distinction between independent units and
repeated measurements when transferring calculations to each new context.

## Known limitations and next decisions

1. **Remote access:** actual service, accounts, authentication, host verification,
   desktop client/browser route, transfer method, home-directory sharing, R
   availability, and execution policy are pending. Conceptual material and a local
   rehearsal are present. The course is not fully deployable remotely until this
   guide is completed and tested.
2. **Student-machine pilot:** Windows WSL, file-manager actions, Mac Terminal,
   software installation, fonts, and keyboard shortcuts need testing on the
   supported student operating systems. Current checks ran on this Linux host.
   Add screenshots from those tested environments rather than fabricated UI.
3. **Workload:** the scope has been constrained, but the daily lesson length and
   number of new terms need a real beginner pilot. Extra practice is preferable
   to adding software or statistical methods.
4. **Biological transfer:** agree CSV conventions, independent units, acceptable
   HTML reports, and the reusable R Markdown template with later practical teachers.
   Replacing Excel requires their adoption, not just this course's instruction.
5. **Statistical scope:** two-group/paired comparisons and simple lines only.
   Students recognise unsuitable assumptions and ask for help; they do not learn
   a catalogue of tests or a decision tree based on normality tests.
6. **Formal administration:** code, credits, teaching hours, calendar, accessibility
   arrangements, and approved outcomes remain institutional decisions. There is
   no inferred examination, rubric, or assignment grading scheme here.

## Rebuilding

```bash
make render
make check
make preview
```

If the execution environment prevents Quarto writing its normal cache, point
`XDG_CACHE_HOME` at a writable temporary cache directory for the render command.
This is an environment workaround, not a student installation step.

Lecture diagrams can be regenerated with `make lecture-figures`. The ordinary
checks include `tools/check_lectures.py`: paired links, real image assets,
RevealJS output, slide limits, and visual-slide counts. An optional local-browser
check (`tools/check_lecture_browser.py`) inspects all presentation frames for
overflow and verifies the actual computed sidebar colours. It needs a local
Chrome debugging endpoint, a localhost server for `docs/`, and websocket-client;
those are developer tools, not student dependencies. Inspection screenshots and
reports go to ignored `output/lecture-preview/`.
