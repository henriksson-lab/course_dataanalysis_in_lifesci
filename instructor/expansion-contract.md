# Five-week workload expansion

The user finds the current lecture/practical volume too small for five weeks
and explicitly requests roughly doubling it, using parallel workers. Expand
depth and independent practice within the existing first-year topic scope.
Keep the 25 units, all URLs, copied scaffold, <=45 slides/deck, and approximately
half visual slides. Do not add advanced methods or pad decks with duplicates.

## What a substantive expansion means

- Aim to approximately double current explanatory slide content: typically
  15–23 total slides rather than 8–13, varying with the topic. Add worked
  demonstrations, contrasting cases, error diagnosis, small predictions, and
  interpretation. Consolidation days remain consolidation, but have substantial
  practice briefings and case discussions. Use meaningful new diagrams/plots,
  not pictures of bullet lists, for roughly half the added slides.
- Every daily practical gains `## Extended practical` and
  `## Independent transfer` sections (a descriptive suffix is fine). These are
  real core study work, not optional stretch tails. Together add around 2–3
  hours of active work with several multi-step tasks (roughly 10–15 operational
  steps), less scaffolding in transfer, hints, a named saved output, and
  interpretation/checks. Add approximately 700–1100 useful words as needed, not
  repeated exposition. Improve earlier instructions when needed rather than
  merely appending a wall of text. Do not solve every independent task in place.
- Teacher solutions/checks must cover all new numerical/file tasks. Use actual
  supplied data and document expected values. No unimplemented input files.
- Roughly double weekly quiz questions, with short worked answers and no grades.
- Root provides a study/workload page with planning estimates: about 35 hours
  structured study plus 5 flexible hours per week (not 40 contact hours), around
 200 learner hours over five weeks; pilot estimates rather than a guarantee.
  Core daily work includes lecture/demonstration, guided work, independent
  transfer, writing/recovery and review. Exam design remains out of scope.

## Additional shared data (root-owned, available shortly)

Existing data remain unchanged; use these for new tasks, not a new method survey:

- `seedlings-transfer.csv`: same columns as seedlings.csv: `plant_id`,
  `treatment` (control/treated), `initial_mm`, `final_mm`. 18 independent potted
  seedlings T01–T18, 9 randomly assigned per group, measured 7 days apart.
  Complete synthetic data. Calculate growth by subtraction. Root dictionary
  supplies design/units. Use it for importing/checking/plots/summaries or a
  second simple comparison as appropriate to the day.
- `solutions.csv`: `solution_id`, `solute`, `mass_g`, `molar_mass_g_mol`,
  `final_volume_ml`. Six supplied salt/sugar solution calculations. Define a
  mole as a chemical amount unit and molar mass as grams per mole. Formula:
  `concentration_mmol_l = 1000 * (mass_g / molar_mass_g_mol) /
  (final_volume_ml / 1000)`. Inputs/constants all given, no chemistry prerequisite.
  Each solute has 50, 100, 150 mmol/L rows. These are calculated preparations,
  not independent treatment evidence.
- `dilutions.csv`: `solution_id`, `stock_mmol_l`, `target_mmol_l`,
  `final_volume_ml`. D01–D03: stock 500, target 50, final 25/50/100 mL. Stock volumes
  are 2.5/5/10 mL via target*final/stock. D04: stock 100, target 200, final 50 mL;
  calculated 100 mL exceeds final 50 mL and must be flagged impossible by dilution.
  Explain final total volume and preserve impossible request as a flagged row.
- `calibration-transfer.csv`: same columns as calibration.csv,6 standards
  at 0..5 mg/L, absorbance .024,.121,.221,.319,.421,.525. Use alongside
  `unknowns-transfer.csv`: X1=.270 (within range), X2=.700 (outside). Do not
  extrapolate X2. If supplying a new diluted measurement, label it explicitly.
- `algae.csv`: `culture_id`, `treatment` (reference/supplement), `biomass_mg`.
  24 independent cultures,12 randomly assigned per group, single7-day harvest.
  A19 supplement reading is missing after a spill. This is a fresh integrated
  transfer dataset, not a known plant file renamed. Count available units,
  describe, and optionally reuse the taught independent comparison. No count
  models, biological inference beyond the simulated conditions, or new packages.

Root adds dictionary, deterministic generator, all files to course ZIP, shared
workload page, tests, and metrics. Workers may create new pictures in their owned
lecture folders via their existing named generator, but must not edit root data.

## Work ownership

A: week1/,week2/,lectures/01..10 assigned existing topic folders;
instructor/week1-solutions.md,week2-solutions.R;
instructor/make-lecture-figures-weeks1-2.py;
instructor/expansion-weeks1-2.md.

B: week3/,week4/,lectures/11..20 assigned topic folders;
instructor/week3-solutions.R,week4-solutions.R;
instructor/make-lecture-figures-weeks3-4.py;
instructor/expansion-weeks3-4.md.

C: week5/,lectures/21..25 assigned topic folders;
instructor/week5-solutions.R;
instructor/make-lecture-figures-week5.py;
instructor/expansion-week5.md.

Each worker owns their week's quiz pages too. No other files. Root owns shared
data, root docs, site config/navigation, tools, and build output. No full-site
render by workers; a test deck may render into /tmp. Don't write/change docs/.

## Constraints retained

Zero file-system/programming baseline. All chemistry terms/inputs/formulas given;
only basic contexts suitable for shortened 7.5 ECTS Organic Chemistry 1. No Python,
specialist software, Git, databases, omics, nonlinear fitting, ANOVA, or matrix
derivations. No need for student-written loops/functions in core. Keep native
RStudio versus WSL files explicit; remote access remains service-dependent, with
local rehearsal and real remote skill correctly distinguished.

Use escaped HTML when showing literal R Markdown chunk fences. Never instruct
a report to render itself. Report sources stay at project root, data/ paths
relative; figures/tables in output/. Captions and summaries preserve independent
units, units, missingness and assumptions. Do not double work by making every
student complete both chemistry and biology alternatives: expand the chosen
route with a genuinely new challenge.

End with a per-day audit of added tasks, approximate time estimates, outputs,
validation, and before/after slide counts. Report any integration dependencies.
