# Shared scope for the organic-chemistry exercise review

Review every daily module's exercise for clear inputs, operations, units, saved
outputs, prerequisites, and checkable answers. Add a small number of organic
laboratory transfer tasks where they reuse existing skills. Do not append extra
required work to every day. Keep the biology core, 25-day structure, and catch-up.

## Evidence and level

Read `/data/henriksson/github/course/molbiol_program/courses/5KE231-organic-chemistry-1.md`
and its linked 5KE180 predecessor dossier. 5KE231 is planned at 7.5 ECTS in 2027.
Detailed course-specific outcomes and practicals remain unconfirmed. The older
5KE180 is 15 ECTS: its mechanisms, synthesis planning, and IR/NMR requirements
are not assumed for our students. Use basic lab records and numerical summaries.

Students need no prior chemistry course. Define yield, theoretical maximum,
isolated mass, and all units/formulas wherever an exercise first uses them.
Supply theoretical mass; do not require deriving it from a balanced reaction.
No reaction prediction, mechanisms, stereochemical assignments, spectroscopy
interpretation, equilibrium solvers, specialist software, or chemistry grading.
All new data are simulated. Calculations are not wet-lab instructions.

## Shared assets owned by root

- `data/organic-recovery.csv`: `run_id`, `protocol` (`standard`/`modified`),
  `theoretical_mass_g`, `isolated_mass_g`. Twelve independent synthesis runs,
  six per randomly assigned protocol. The theoretical mass is the supplied
  maximum mass of product from that run's starting materials. Isolated mass is
  dry collected product, assumed pure for this simplified calculation.
  `yield_percent = 100 * isolated_mass_g / theoretical_mass_g`.
  Theoretical masses differ with starting scale; compare percentages, not raw
  grams across runs. Greater yield does not establish greater purity, safety,
  sustainability, or general superiority. Dataset has no missing values.
- Y01: 1.00 g theoretical, 0.62 g isolated, 62%. Standard yields:
  62,70,68,74,66,72; modified yields: 72,78,76,82,74,80.
- `data/organic-inventory.tsv`: `sample_id`, `sample_class`, `note`. O01 alcohol,
  O02 ester, O03 ester, O04 carboxylic-acid. These are supplied text labels, not
  molecular structures students must identify. Two literal matches for `ester`.
- `downloads/organic-lab.zip`: separate optional shell transfer fixture. README.txt,
  inventory.tsv, organic-recovery.csv, and DICTIONARY.txt. No change to existing
  lab-data.zip or its five-line/two-treated-record exercise. Extraction example
  `unzip organic-lab.zip -d organic-lab`; commands run inside organic-lab/.
- All new data also shipped in existing course-files.zip. Root updates dictionaries,
  generator, archives, references, teacher overview, validation, and site.
- Existing student report convention: root-level `.Rmd`, inputs relative to
  `data/`. No new packages. Do not rename existing files/objects unless needed.

## Division of work

- Worker 1: week1/, week2/, instructor/week1-solutions.md,
  instructor/week2-solutions.R, instructor/exercise-review-weeks1-2.md.
  Review all ten days. Natural targets: day5 optional rotation using organic ZIP;
  day6 a short fully defined percentage-yield arithmetic variant; day8 transfer
  to yield column. Keep plant worked examples. At most a few small tasks, clearly
  substitute/choose rather than mandatory extras. Fix actual exercise ambiguity.
- Worker 2: week3/, instructor/week3-solutions.R,
  instructor/exercise-review-week3.md. Review all five days. Natural target day12
  or13: calculate mean/SD of yield across independent runs; contrast repeat
  weighings of one run. Consider a report alternative day15 without adding a
  second required report. Keep complete/messy seedling distinction explicit.
- Worker 3: week4/, week5/, instructor/week4-solutions.R,
  instructor/week5-solutions.R, instructor/exercise-review-weeks4-5.md.
  Review all ten days. Natural targets day19: basic in-range diluted measurement
  explanation if useful, no assertion that optical assay is a confirmed orgchem
  practical. Day23: a fully specified organic-yield alternative to duckweed,
  preferably descriptive to avoid scope growth; day24/25 accept its filename
  consistently. Keep required simple tests and biological examples intact.

Each review file needs one row per assigned day: exercise issue/decision,
change or retain with reason, and validation performed. Instructor scripts should
validate the added exercise calculations against the actual shared data and
save optional outputs in existing ignored output/ directories or tempdir().
Do not edit other workers' files, root assets, navigation, or this contract.
