# Instructor notes — weeks 2–3

These lessons turn repeated small actions into an independent workflow. They are
first-draft teaching content, not a fixed contact-hour allocation or examination
specification. Allow substantial supported practice. Students should not need to
finish every transfer exercise before receiving the next explanation.

## Run the worked solutions

From the repository root:

```bash
Rscript instructor/week2-solutions.R
Rscript instructor/week3-solutions.R
```

Add `--figures` to either command to also regenerate the corresponding static
teaching figures in `week2/` or `week3/`. The website does not execute student
code chunks on render; these checked figures show worked results alongside them.

Both scripts import the shared files, calculate the worked answers, save figures
and tables in `output/instructor-week2/` and `output/instructor-week3/`, and render self-contained instructor R Markdown
reports. Each prints its output location. These are instructor reference scripts;
they are excluded from student downloads. Rendered example sources use the
repository/project root as their input root during this instructor check. If
copying a generated `.Rmd` into a student project, place it at the project root.

## Teaching rhythm

Start each session by naming the biological question and the expected unit of
observation. Demonstrate one small calculation, ask for a prediction, run it,
and inspect the result. Let students repeat it, then alter one detail. Do not
introduce all dplyr verbs or ggplot options at once. Reference pages are allowed;
correct reasoning and recovery from mistakes are more valuable than speed.

## Day-by-day focus and likely difficulties

| Day | Main check | Common difficulty / response |
| --- | --- | --- |
| 6 | Student can reopen and run a saved four-plant script | They confuse saving with running, or objects with files. Restart R and recreate the values from the saved source. |
| 7 | Student identifies the file, row unit, units, and 24 × 4 structure | A ZIP remains unextracted, a project is opened at the wrong folder level, or the working directory is `data/`. Inspect graphically before changing code. |
| 8 | Growth means final minus initial and each point is one plant | Learner interprets final length as growth, forgets assignment, or filters columns instead of rows. Revisit one plant by hand. |
| 9 | Report renders with its own imports and calculations | An object existed only in the Console; labels are duplicated; chunk fence is missing. Use the first reported error and its chunk label. |
| 10 | Reader understands a short report without the editor | Students list code rather than explain measurements, or assert an effect without considering uncertainty. Ask what a dot and an axis mean. |
| 11 | Repairs have documented evidence and P06 remains missing | Students delete unusual observations, replace missing values by zero, or deduplicate by ID without inspecting records. Compare the protocol and source notes. |
| 12 | Mean and SD have measurement units; variance has squared units | Student treats SD as error in the mean or expects all observations inside ±1 SD. Use two toy sets with equal means but different spread. |
| 13 | Table has two group rows; raw data still have 24 plant rows | Student interprets summary rows as observations or draws an unlabelled error bar. Keep the individual dots visible. |
| 14 | Independent unit follows assignment/sampling, not row count | Student counts repeated ruler readings as independent plants. Draw pots, plants, and treatment assignments. |
| 15 | Fresh-session report contains question, checks, results, and limitations | Student mixes clean-file values with repaired-file counts. Require an explicit input filename and rebuild all results from it. |

## Numerical anchors

For `seedlings.csv`, control mean growth is approximately 15.28 mm, median
15.65 mm, SD 3.19 mm, and variance 10.18 mm². Treated mean growth is approximately
21.49 mm, median 20.85 mm, SD 4.87 mm, and variance 23.67 mm². Both groups have
12 observations. Use the scripts for unrounded values rather than treating
rounded teaching prose as a source dataset.

The deliberately messy table has 25 rows. Supported corrections yield 24 unique
plants, with P06 final length and growth still missing. There are 12 plants in
each group but only 11 observed control growth values. Its control summary is
therefore different from that of the complete clean teaching file. Keep this
contrast explicit: the clean file is a separate supplied complete dataset, not a
licence to recover an unavailable measurement from another exercise.

For the toy values 12, 14, 16 mm, mean and median are 14 mm, sample variance
4 mm², and SD 2 mm. Adding a constant shifts the mean but not variance or SD;
rescaling lengths rescales SD linearly and variance quadratically.

The sampling demonstration uses observed growth values from both groups as a
fixed toy population. It illustrates the spread of repeated sample means, not a
treatment test or a defensible estimate for all seedlings. Explain the sampling
mechanism before students press Run. Students are not expected to author loops,
functions, or simulation code.

## Content boundaries

No inferential test is needed until week 4. The week 3 report is intentionally
descriptive. The paired-design distinction can be introduced when discussing
repeated measurements, without teaching its test yet. HTML avoids a PDF toolchain.
R Markdown (`.Rmd`) is the student format; Quarto belongs to the teaching site.

All student `.Rmd` sources live at the project root; `reports/` stores generated
HTML. The Knit button may put HTML next to the source. The explicit
`rmarkdown::render(..., output_dir = "reports")` command standardises the output
location without moving input paths. Remote rendering remains optional practice
until the course service, application access, and file-transfer route are confirmed.
