# Data Analysis in Life Sciences — proposed content plan

Working proposal for a five-week first course at Umeå. This is not an approved
syllabus. No course code, credit value, or formal timetable is assumed here.
Written examination design is out of scope.

## First teaching draft now implemented

All 25 study units below now have student lessons in `week1/`–`week5/`, with
worked examples, practicals, hints, self-checks, and saved outputs. The site starts
at `index.qmd`; `instructor/README.md` identifies useful review points, worked
solutions, validation, and remaining deployment decisions. Student archives,
simulated data and dictionaries, a working R Markdown template, setup pages,
and reference pages are included. The plan below remains editable as the content
is reviewed. Remote service details, beginner pacing, and student-machine setup
still require a pilot and the forthcoming HPC2N/environment information.

The Quantitative Biology scaffold is now used for separate RevealJS lecture
decks paired with each daily practical, coloured weekly sidebar sections, green
lecture links, blue formative quiz links, and italic practical links. Decks use
speaker notes and explanatory diagrams/plots on roughly half their slides.
The maximum is 45 slides, with fewer preferred and no padding to meet a count.

The user then requested roughly twice the teaching/practice volume. The expanded
version develops worked examples, diagnosis, interpretation, and independent
transfer within the existing topics, with two substantial additional practice
blocks per day. The [student study plan](study-plan.qmd) lists the sequence and
checkpoints. The [expansion record](instructor/workload-expansion.md) preserves
before/after evidence. The later [wording audit](instructor/audit-results.md)
removes pace prescriptions and required peer work and adds topic quizzes.

## Purpose and audience

Students should leave able to handle ordinary data from later biology practicals
without depending on Excel for calculations, plots, or reports. They should also
understand enough about computers to find their work, recognise where a program
is running, and recover from common mistakes.

Assume no understanding of a file system, paths, terminal, programming, or
statistics. Downloading an attachment is not evidence that a student can locate
the file afterwards. Teach saving, locating, reopening, and organising files
explicitly before requiring terminal navigation.

Chemistry can provide laboratory contexts, but students must not need to have
completed Fundamentals of Chemistry (5KE165) to understand what to compute.
Each exercise supplies definitions, quantities, units, constants, the formula,
and calculation instructions. See [the chemistry context note](instructor/chemistry-context.md)
for the initial placement investigation. The day 19 dilution correction and
the expanded solution/dilution practice in days 6–8 are implemented, using the
current lesson inputs. The specific volume-reading illustration remains a
proposal.

Selected organic-laboratory transfer choices are now implemented separately:
supplied sample-label searches, percentage yield from provided masses, variation
between independent runs, and an alternative descriptive report. The
[organic-context review](instructor/organic-context-review.md) maps all 25 exercise
reviews. These choices replace repeated practice, preserve the biology sequence,
and assume neither completion of the shortened 7.5 ECTS Organic Chemistry 1 nor
knowledge of reaction mechanisms, synthesis planning, or spectral assignments.

Biology provides the question from the first day. Use short explanations of the
organism, measurement, and experiment so that students do not need biology from
later courses to understand the task. This is computing for beginning biologists;
database searching and running bioinformatics software belong to a later course.

## Proposed learning outcomes

By the end, a student should be able to:

1. Distinguish a file, folder, application, operating system, and running process;
   explain the practical difference between memory and persistent storage.
2. Save, find, organise, copy, and back up work; interpret absolute and relative
   paths, extensions, and the current working directory.
3. Navigate and inspect small text datasets using a small set of Linux commands,
   and explain a simple pipe or redirection.
4. Connect to a provided Linux environment using SSH, use its remote desktop,
   and identify which computer holds a file or runs a command.
5. Import a CSV into R, check types, units, identifiers, and missing values,
   select observations, calculate new variables, and summarise groups.
6. Make labelled plots showing observations and describe mean, median, variance,
   and standard deviation in the context of biological variation.
7. Use a guided two-group comparison and straight-line fit, reporting effect
   sizes, uncertainty, assumptions, and a restrained biological interpretation.
8. Render an R Markdown report from saved data and code in a fresh R session,
   with readable figures, methods, and conclusions.

## Five-week progression

The following assumes 25 study days. These are suggested learning units, not
25 full days of new lectures. Protect substantial time for guided practice,
repetition, troubleshooting, and independent work. Adapt contact hours when the
actual timetable is known.

| Week | Guiding biological question | Computing and quantitative focus | Practical result |
| --- | --- | --- | --- |
| 1 | Where are our seedling measurements, and what do the files contain? | Files and folders; how computers work; terminal basics; local and remote computers | An organised data folder, successful navigation, and an inspected CSV |
| 2 | How can we describe growth without manually editing a spreadsheet? | R basics; importing and checking tables; calculations and plots; R Markdown | A short report rendered from a supplied template |
| 3 | How much do individual organisms differ? | Data quality; grouped summaries; mean, variance, SD; sampling and uncertainty | A report showing individual observations and group summaries |
| 4 | Does a treatment change growth, and how do two measurements relate? | Independent versus paired observations; t-tests; effect sizes and intervals; straight-line fitting | A careful comparison and a labelled fitted-line plot |
| 5 | Can someone repeat our analysis from the original measurements? | Integration, practice, error recovery, transfer to another dataset | A reproducible mini-report and a portable project folder |

### Week 1 — Computers, files, and the command line

- **Day 1: A computer as a laboratory tool.** Introduce a small seedling
  experiment and its measurements. File versus application; browser versus file
  manager; Downloads; saving versus opening; folders within folders; file
  extensions. Download, locate, rename, move, close, and reopen a supplied CSV.
  Show extensions in the file manager. Keep an untouched raw-data copy.
- **Day 2: Where is my work?** Draw the folder tree before introducing paths.
  Home directory, parent folder, absolute/relative paths, local disk versus
  cloud storage. Create a project with `data/`, `reports/`, and `output/`.
  Practise finding it after closing applications. Explain CPU, RAM, storage,
  operating system, applications, and processes through opening and saving data.
- **Day 3: The terminal describes the same folders.** Supported Ubuntu/WSL setup
  on Windows; Terminal on Mac. Alternate file-manager and terminal views.
  Introduce prompt, command, argument, Enter, case, spaces, `pwd`, `ls`, `cd`,
  `mkdir`, tab completion, history, and Ctrl+C. Treat deletion cautiously in a
  disposable practice folder; there is no need for recursive deletion commands.
- **Day 4: Inspect files and meet the remote computer.** `cp`, `mv`, `head`,
  `less` (including `q` to quit), `wc`, and a simple `grep`; one pipe and one
  redirection with an explanation that `>` overwrites. Headers versus data
  rows. Introduce `unzip -l` and `unzip` using a supplied archive of lab-group
  files; return to these in day 5's practical. Teacher demonstrates SSH and remote desktop. Students practise connecting
  when accounts are available, and name the computer and folder they are using.
- **Day 5: Consolidate and meet R.** Repeat the download-to-folder-to-terminal
  workflow with less guidance using the archive practical below. Start R/RStudio; distinguish editor, console, and
  terminal; run a calculation and a supplied plot. Demonstrate a complete report
  so students can see the purpose of the next weeks.

#### Command-line practical: receive and share a laboratory dataset

Use familiar utilities rather than introducing a specialist scientific program.
The question is: **which samples received the treatment, and where are their
measurement files?** Supply a small ZIP archive with a README, a tab-separated
sample manifest, and clearly named measurement files from several lab groups.

1. Locate the downloaded archive in the file manager, then locate the same file
   in the terminal. Practise the supported transfer route when using remote Linux.
2. Use `unzip -l lab-data.zip` to inspect the archive before extracting it with
   `unzip lab-data.zip -d lab-data`. Explain that extraction creates ordinary
   files and folders; the archive remains a separate file.
3. Navigate into the extracted folder and read its README with `less`.
4. Search the manifest with `grep -F treated samples.tsv`. Design the example
   with unambiguous labels such as `control` and `treated`, and one record per
   line, so this literal search has a clear meaning. Compare the matching lines
   with the complete manifest rather than treating text search as a table query.
5. Save matching records with `grep -F treated samples.tsv > treated-samples.txt`
   and count them with `grep -F treated samples.tsv | wc -l`. Explain why counting
   lines is appropriate for this supplied file and why a header changes a total
   line count. The saved search result is a text extract, not a replacement for
   the original table.
6. Later, package a small report folder with `zip -r report-bundle.zip report/`.
   List its contents, extract it into a fresh folder, and locate the report.

This gives paths, options, pipes, and redirection a concrete purpose. Keep the
command vocabulary small and repeat it during remote work. Explain that a ZIP
is a convenient package for sharing, not a backup if it is stored only beside
the originals. Check that `zip` and `unzip` are available in the teaching
environments; provide setup support rather than making installation a new topic.

Installation and login support belong in scheduled teaching time. A student who
cannot install locally needs access to the supported remote environment, rather
than a requirement to solve system administration alone. If remote accounts are
not yet ready, use local folders for navigation practice and revisit the remote
exercises later without delaying R.

### Week 2 — R and the first report

- **Day 6:** Objects, assignment, numbers, text, logical values, vectors,
  functions, and help. Predict a small result, run it, and explain it. Use units
  and simple biological calculations such as change in seedling length.
- **Day 7:** RStudio projects and relative paths; read a small CSV; inspect rows,
  columns, types, and dimensions. Explain one observation per row, one variable
  per column, identifiers, units, and missing values. Do not edit raw measurements
  to make an import succeed.
- **Day 8:** Select rows and columns, calculate a new column, and make a scatter
  plot. Distinguish numeric measurements from group labels. Use one consistent
  syntax in exercises; avoid teaching parallel base-R and tidyverse solutions.
- **Day 9:** Render a supplied `.Rmd` to HTML. Text, code chunks, headings,
  inline results, figure captions, and reading an error. Explain that rendering
  must reproduce the calculation without relying on console objects.
- **Day 10:** Repeat on a similar small dataset. Add biological context, methods,
  a figure, and a few sentences of interpretation to the report. Reopen and
  render it after restarting R.

Default teaching choice: base R for simple calculations and introductory object
handling, then a small, consistent `readr`/`dplyr`/`ggplot2` vocabulary for tables
and plots. Provide function reference sheets. Use `stats::t.test` and
`stats::lm` later. No general programming survey, loops, or student-written
functions are required for the core workflow.

### Week 3 — Measurements, variation, and reliable tables

- **Day 11:** Check a deliberately imperfect laboratory table: missing values,
  implausible units, numbers read as text, duplicate sample identifiers, and
  group spelling. Record corrections in code. Explain that zero is a value and
  is not a substitute for an unknown measurement.
- **Day 12:** Mean and median; deviations from the mean; variance and standard
  deviation. Compare small groups with similar means but different spreads.
  Explain that variance has squared units and SD has the measurement's units.
- **Day 13:** Group summaries and plots of individual observations; histogram,
  scatter plot, and a simple group comparison plot. Include sample sizes,
  axis units, and a clear account of any error bars. Avoid bars of means alone.
- **Day 14:** Biological versus technical replicates, sampling variation, and
  why more measurements of one plant do not create more independent plants.
  A teacher-provided repeated-sampling demonstration introduces the difference
  between spread among observations and uncertainty in an estimated mean.
- **Day 15:** Produce a descriptive report with a data-quality note, group
  summaries, a figure, and an interpretation. Practise the same workflow in the
  remote environment if available; explicitly locate source files and outputs.

### Week 4 — Comparing groups and fitting lines

- **Day 16:** Start with the experimental design, individual measurements, and
  the difference in means. Independent plants in two treatments versus before
  and after measurements of the same organism. Introduce the null hypothesis
  and a p-value as a probability of results at least as extreme under that model,
  not the probability that the null hypothesis is true.
- **Day 17:** Guided Welch two-sample t-test using independent replicate plants.
  Read the estimated difference, confidence interval, and p-value. Discuss
  independence, small samples, severe skew, and influential observations;
  do not teach a normality-test decision tree. Explain confidence intervals
  through repeated sampling, without a derivation. Emphasise biological size
  and uncertainty over a threshold alone.
- **Day 18:** A short paired example: measure the same subjects before and after
  a treatment and analyse their differences. Match by subject identifier, never
  by accidental row order. Contrast this design with the independent example.
  Consolidate: an inconclusive result does not establish no effect, and a small
  p-value does not establish a large or causal effect.
- **Day 19:** Fit a straight line to a prepared concentration/absorbance
  calibration dataset using `lm`. Interpret slope and intercept with units;
  show residuals and the measured range. Use the calibration to interpret an
  unknown sample within range. No derivation or matrix algebra.
- **Day 20:** Repeat a line fit for a biological association, such as leaf area
  and mass. Explain association versus causation, influence of an unusual point,
  and risks of extrapolation. Consolidate with a short report using either a
  comparison or a line, chosen for the question.

No ANOVA, multiple regression, multiple-testing procedures, or catalogue of
alternative tests. Where the simple methods are unsuitable, the outcome is to
recognise a limitation and seek advice, not to select from a menu of tests.

### Week 5 — An analysis that survives reopening

- **Day 21:** Rehearse remote access: connect with SSH, identify the remote home
  directory, locate a file, disconnect, reconnect, and use remote desktop.
  Practise a supported file-transfer route and check which copy was transferred.
  Render a small report in the supported R environment. If these skills were
  completed earlier, use the time for troubleshooting and extra data practice.
- **Day 22:** A brief breadth session: DNA as text and an image as pixel values.
  Use supplied tiny examples, such as counting letters and viewing intensity
  values. Reuse familiar objects and plots; explain the biological question.
  Keep this to a short demonstration/exercise, not two additional workflows.
- **Day 23:** Start a small integrated practice study using a new, documented
  dataset with a familiar structure. Students organise files, check the data,
  plot measurements, and perform one appropriate guided analysis.
- **Day 24:** Finish the R Markdown report; extract the project into a new folder
  and attempt to render from a fresh session. Resolve missing files, absolute
  paths, console-only objects, and missing explanations. This is formative
  practice, not a proposed examination component.
- **Day 25:** Protected catch-up, practice on another dataset, and consolidation.
  Repeat file recovery and report rendering as needed. Do not fill this buffer
  with advanced topics.

## Biological examples and transfer to later practicals

Use one recurring seedling dataset for early practice and a few small transfer
datasets. Label simulated teaching data clearly; supply a data dictionary and
enough experimental context to identify an independent replicate.

| Later practical | Plausible input | Skill established here |
| --- | --- | --- |
| Plant physiology | Plant ID, treatment, length or mass, units | Group summaries, individual observations, independent comparisons |
| Biochemistry | Standard concentrations, absorbance, unknown sample IDs | Calibration line, units, range checks, a reported derived concentration |
| Physiology | Subject ID and matched before/after measurements | Matching pairs, change per subject, paired comparison |
| Ecology | Quadrat ID, habitat, species counts | Tidy tables, missing versus zero, descriptive summaries and plots; defer count models |
| Microbiology | Culture ID, time, optical density | Repeated-measurement plots; recognise that time points from one culture are dependent |
| Microscopy | Image ID, organism ID, supplied cell measurements | Summarise measurements without treating every cell as an independent organism |

Do not introduce a hypothesis test for every example. Many first analyses should
end with a useful plot and an honest description.

## Environments and the local/remote distinction

- Windows: Ubuntu through WSL for the Linux command line; see the setup page.
- Mac: the existing Terminal and shell for the portable commands used here.
  Avoid Linux-specific flags in shared exercises; label Ubuntu-only commands.
- Remote: HPC2N or another supported Linux environment. Teach SSH and a separate
  remote-desktop route; exact service, authentication, and desktop instructions
  will be supplied later. Do not invent hostnames or account procedures.
- R and RStudio: prefer native desktop applications on laptops and a supported
  R environment remotely. Windows users do not need a second R installation
  inside WSL for the introductory course.
- Keep shell exercises in the Linux home directory. Keep native R projects in
  the laptop's normal file system. Demonstrate the bridge between these locations
  using one small file; avoid making every R session depend on crossing WSL paths.
- Use a visible local/remote indicator in teaching instructions. A path on the
  remote computer is not automatically accessible from local RStudio. Remote
  desktop is another view into a remote system, not automatic file synchronisation.

When HPC2N details arrive, confirm which host permits teaching work, how R runs,
and whether the desktop and SSH sessions share a home directory. If scheduling
is required, provide the smallest supported route for the exercise; HPC job
management is not a new course topic. Use an alternative teaching environment
if necessary to keep the core workflow approachable.

## Teaching approach and scope control

Use short explanations followed immediately by action: teacher demonstration,
guided repetition, a small independent variation, then explanation of the result.
Provide screenshots when developing the file-system materials, a keyboard and
terminal reference, a glossary, and worked examples with progressively fewer
prompts. Practise reading errors and asking for help without sharing passwords.

Every core practical should revisit file location, the biological question,
units, a figure, and a written interpretation. Students should explain what a
command changed and where output was saved, rather than only copy a command.
Use quick formative checks to find difficulties; these do not specify examination.

Introduce backups and an untouched raw-data folder early. Export CSV, plots,
and HTML reports for later courses. HTML is the initial report format to avoid
introducing a PDF/LaTeX toolchain. Replacing Excel also requires later-course
teachers to accept these formats and reuse the project/report template.

Explicitly defer sequence alignment, databases, BLAST, RNA-seq, Bioconductor,
PCA, machine learning, advanced image processing, shell scripting, Git, system
administration, and statistical derivations. DNA and image examples only
illustrate representations and reuse the skills already taught.

If students need more time, shorten the DNA/image session and paired-test
calculation practice first; retain the paired-design distinction. Protect file
literacy, data import, plotting, variation, one independent comparison, a straight
line, and repeated report rendering.

## Material development plan

1. **Foundation:** retain the sibling course's Quarto website/navigation pattern,
   small topic units, and lecture/exercise pairing. Replace its advanced audience,
   outcomes, dependencies, and syllabus references. Do not copy its omics units
   or examination assumptions. The initial scaffold and two setup pages are here.
2. **Environment pilot:** test the Windows instructions on a fresh student-style
   account, the Mac commands on macOS, and the remote route once supplied. Add
   illustrated file-manager instructions and a separate R/RStudio installation
   page. Reserve a supported installation session.
3. **Data and report template:** create a small seedling dataset, dictionary,
   clear replicate structure, and an HTML R Markdown template. Establish the
   vocabulary and package set before writing all exercises.
4. **Build the core progression:** write week 1 and a complete week 2 workflow
   first. Pilot with genuine beginners before filling weeks 3–5. Keep instructor
   solutions and troubleshooting notes alongside the materials.
5. **Transfer and coordination:** prepare calibration and paired datasets, then
   a fresh integrated practice dataset. Agree expected report formats and data
   conventions with teachers of subsequent biology practicals.

Decisions still needed: actual contact hours and class size; supported R access
and software provisioning; remote accounts, host, authentication, transfer route,
and desktop service; and the biological examples later practical teachers will
reuse. None of these should be assumed to be familiar to incoming students.
