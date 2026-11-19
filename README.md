# Data Analysis in Life Sciences

First complete teaching draft for a new five-week introductory course at Umeå.
No previous programming, terminal, or file-system knowledge is assumed.

- [Content and teaching plan](contentplan.md)
- [Rendered course: start here](docs/index.html)
- [Student course home](index.qmd)
- [Instructor guide and review checklist](instructor/README.md)
- [Ubuntu on Windows / Terminal on macOS](intro/ubuntu-windows.qmd)
- [Remote Linux, SSH, and remote desktop](intro/remote-linux.qmd)

The Quarto website structure follows `../quantbio-3MB00A/`, with a small
navigation tree for this course. Advanced course content and its dependencies
are not copied. Student reports will use **R Markdown (`.Rmd`)**; the teaching
website uses Quarto (`.qmd`).

The draft contains 25 separate RevealJS lecture decks paired with 25 daily
Exercises pages, 25 topic quizzes, five weekly revision quizzes, worked examples, hints,
biological datasets and dictionaries, a working R Markdown template, setup
guides, references, and instructor solutions. Datasets are simulated. The
sidebar and slide theme are copied from the Quantitative Biology scaffold:
coloured week bands, green lecture links, blue quizzes, and italic practicals.

The [course page](overview.qmd) lists outcomes and weekly checkpoints. The instructor
[expansion record](instructor/workload-expansion.md) compares the larger version
with the original draft. The subsequent [wording and quiz audit](instructor/audit-results.md)
removes prescribed timings, required collaboration, and writing quotas while
retaining substantive practice.

Run `make render` to package the downloads and build the student site into
`docs/`, or `make preview` for a local preview. Quarto is required; rendering
lesson code fences also uses R and knitr, though student example execution is
disabled for the website. Install the R packages listed in the setup page to
run instructor checks and reports.

Slide themes live in `theme.scss`; the inherited sidebar styling is in
`styles.css`. New lecture diagrams have reproducible generators; run
`make lecture-figures` to rebuild them. Speaker notes are embedded in the slides
and can be opened using RevealJS's speaker view. Lecture source is under
`lectures/<topic>/lec.qmd`; existing practical URLs remain stable.
The diagram/plot generators use Python, NumPy, and Matplotlib on the instructor
machine; students do not need those packages to view the slides or do practicals.

Run `make check` after rendering to verify the instructor calculations, reports,
archive workflow, and built local links. `make figures` regenerates the embedded
R plots. `python3 tools/build_data.py` regenerates the synthetic data if needed;
ordinary builds reuse the committed CSVs. `make` does not stage or commit files.

Planning and instructor documents are excluded from the student site and ZIPs.
Examination design is outside the scope of these materials. The remote service's
actual account, authentication, desktop, and transfer instructions still need
to be supplied; Windows/Mac setup needs a student-machine pilot.
