# Instructor guide: reviewing the first teaching draft

The course is built for first-year students who may not yet understand files,
folders, or saved application state. Data Analysis in Life Sciences is a
five-week introduction to computing
in a biological setting, with written examination design outside this work.
This is draft teaching content, not an approved syllabus or a fixed timetable.

## Where to start evaluating

The [chemistry context investigation](chemistry-context.md) proposes short
insertions in days 6, 8, 12, and 19. These must be understandable without prior
chemistry: all terms, inputs, units, relationships, and requested calculations
are supplied. The proposals have not yet changed the daily student lessons.

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
| `week5/24-reproduce.qmd` | Does the project work when another student receives it? |

The course currently uses lesson pages combining explanation and practical work.
There are no recorded lectures or separate slide decks yet. Evaluate the level
and workflow before adapting the prose into recordings or slides.

## What's supplied

- 25 student lessons with biological context, examples, practicals, hints,
  completion questions, and explicitly named saved outputs.
- A small Quarto website following the sibling course's Cosmo/docked-sidebar
  structure. Website code execution is disabled; example figures are generated
  separately from the actual teaching datasets.
- Eight CSV datasets and a tiny DNA string, all simulated. The data dictionary
  identifies units, experimental units, and missing values. A separate source
  note justifies the planted data-quality corrections.
- A complete student project ZIP with a working root-level `report.Rmd`, plus
  a separate ZIP for the terminal practical. Neither contains instructor files.
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
10–15 minutes of explanation followed by demonstration and guided work, then a
second short explanation and practice. Actual contact hours are not specified.
Many students will need substantially more time for installations, paths, typing,
and reopening work than the conceptual explanation takes.

On day 1, find who can save and reopen a file without a recent-files menu. On
day 5, find who can name the current folder and explain an extracted archive.
On day 10, find who can render after restarting R. Use these as support signals,
not grades. Pair work can help troubleshooting, but each student needs hands-on
practice controlling their own session and locating their own saved files.

Keep day 25 as catch-up. If overloaded, shorten the representations demonstration
and paired-test calculation practice while retaining the paired-design concept.
Do not remove file literacy or fresh-session rendering to fit more methods.

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
