# Shared teaching contract

## Current editing requirements

- Student tasks have no expected completion times.
- Exercises are completable independently; collaboration is optional.
- Give concise tasks, supplied quantities/formulas, and checks. Remove redundant
  prohibitions and reassurance; do not add prose to satisfy a length quota.
- The student-facing role label is **Exercises**.
- Each topic has a quiz matching Quantbio's public question/hint/answer format:
  short questions and separate collapsible hints and answers. Use questions that
  check the topic's outcomes, without a question quota. See `audit-plan.md` and
  `audit-results.md` for the revision scope and findings.

## Course background

This is a first teaching draft, not an approved syllabus or an examination plan.
Students have no assumed file-system or programming knowledge. The current
five-week sequence is in `contentplan.md`.

The user subsequently requested approximately doubling lecture and exercise
content to support five weeks of study. Substantive practice and fresh inputs
remain, without broadening the method list or adding chemistry prerequisites.
The later audit supersedes the historical expansion contract's timing, prose,
and step targets. `study-plan.qmd` lists the sequence and checkpoints without
prescribing how long a student should take.

Chemistry contexts must be self-contained. Completion of Fundamentals of
Chemistry (5KE165), or recall of a chemical formula or method, is not required
to understand an instruction. Supply definitions, inputs, constants, units,
the relationship to compute, assumptions, and a worked/checkable result.
Prior chemistry can make an example familiar; it cannot supply missing steps.
See `instructor/chemistry-context.md` for investigated insertion points.

Organic Chemistry 1 (5KE231) is planned at 7.5 ECTS in 2027. Detailed content
remains unconfirmed; do not assume the full 15-credit predecessor's mechanisms,
synthesis planning, or spectral assignments. Organic examples use supplied
sample labels and basic product masses/yield, with no prior chemistry needed.
Use context choices to replace repeated practice, not add required workload.
See `instructor/organic-exercise-contract.md` for the shared data and review scope.

## Authoring conventions

- Daily student pages live in `week1/01-files.qmd` through the named day 25 page.
  Every page needs explanation, a worked example, a biological practical,
  actionable hints, a completion check, and an explicit deliverable. Do not
  substitute lists of topics for teaching content. Use ordinary HTML pages.
- Website pages are Quarto; student reports are R Markdown. Teach these as
  different things. Students never need to author Quarto for this course.
- Topic sections pair `lectures/<daily-stem>/lec.qmd` RevealJS lectures with the
  existing daily practical URLs. Reuse the Quantitative Biology sidebar colours
  and root `theme.scss`. Keep decks as short as useful, at most 45 slides,
  roughly half using explanatory diagrams/plots. Topic quizzes live at
  `weekN/<daily-stem>-quiz.qmd`; weekly `quiz.qmd` pages provide revision.
  See `instructor/lecture-contract.md` for authoring rules.
- Students download `downloads/course-files.zip`, extract the enclosed
  `introcomputing-course/` folder, and use it as their project root. It contains
  `introcomputing.Rproj`, `data/`, `output/`, `report.Rmd`, and `reports/`.
  R code paths are always relative to that root: `data/seedlings.csv`.
- Teach base R object handling first, then `readr::read_csv`, `dplyr` functions,
  and `ggplot2`. Use the base pipe `|>` sparingly and explain it at first use.
  Prefer `data =` explicitly in statistical functions. Avoid switching between
  equivalent syntaxes. Statistics use `stats::t.test` and `stats::lm`.
- All data are simulated teaching data generated with fixed seeds. Each CSV has
  a dictionary and experimental-design description in `data/README.md`.
- `seedlings.csv`: `plant_id`, `treatment` (`control`/`treated`),
  `initial_mm`, `final_mm`. Twenty-four independently potted seedlings, twelve
  per group; treatment randomly assigned. Derived `growth_mm = final_mm - initial_mm`.
- `seedlings-messy.csv`: same schema; known planted errors documented privately
  in `instructor/data-notes.md` and explained to students as a repair exercise.
- `calibration.csv`: `standard_id`, `concentration_mg_l`, `absorbance`.
  `unknowns.csv`: `sample_id`, `absorbance`. Standards are prepared solutions;
  these are calibration points, not independent treatment replicates.
- `paired.csv`: `plant_id`, `before_umol_m2_s`, `after_umol_m2_s`.
  Ten independent plants, the same plant measured twice after changing light.
  Order is not counterbalanced: causal claims need this limitation.
- `leaf-mass.csv`: `plant_id`, `leaf_area_cm2`, `dry_mass_mg`.
  One leaf from each of eighteen independent plants. Observational association.
- `duckweed.csv`: `flask_id`, `treatment` (`control`/`nutrient`), `biomass_mg`.
  Twenty independent culture flasks, ten per randomised group, one harvest.
  One nutrient measurement is missing after a spill; never replace it by zero.
- `samples.tsv` in the shell archive: `sample_id`, `treatment`, `file`.
  Two control and two treated records; header contains no `treated` token.
  `downloads/lab-data.zip` extracts into a user-chosen `lab-data/` folder, with
  README.txt, samples.tsv, measurements/ and field-notes/.
- `dna.txt`: a tiny single-line DNA string, no FASTA parsing needed.
  `pixels.csv`: 8 x 8 numeric values with a header; use `as.matrix(read.csv(...))`.
- Never require software beyond R/RStudio, the small R package set,
  terminal utilities (`zip`, `unzip`, `grep`, etc.), and supported remote access.
  No ImageMagick, csvkit, SLiM, bioinformatics databases, or specialist tools.
- No actual remote hostname, account procedure, scheduler command, or desktop
  product is known. Explain SSH and file location; retain clearly marked setup
  dependencies. No executable example may pretend an invented host is real.
- Instructor solutions go in `instructor/`; exclude them from the website and
  student downloads. Hints and short self-check answers may be student-visible.
  Do not introduce assessment requirements or grades.
- Root agent owns navigation, shared data/assets, setup pages, validation,
  and packaging. Parallel editors own their assigned weeks and lecture folders.

## Daily filenames

Week 1: `01-files`, `02-folders-computers`, `03-terminal`, `04-inspect-archive`,
`05-lab-files`.

Week 2: `06-r-basics`, `07-import`, `08-transform-plot`, `09-rmarkdown`,
`10-first-report`.

Week 3: `11-data-quality`, `12-variation`, `13-group-summaries`,
`14-replicates-uncertainty`, `15-descriptive-report`.

Week 4: `16-comparisons`, `17-welch-test`, `18-paired`, `19-calibration`,
`20-association`.

Week 5: `21-remote-workflow`, `22-data-representations`, `23-mini-study`,
`24-reproduce`, `25-consolidate`.
