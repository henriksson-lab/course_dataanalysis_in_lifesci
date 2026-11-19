# Data dictionary and study descriptions

All files here are **simulated teaching data**, not observations from a real
experiment. Values were generated for this course with fixed random seeds by
`tools/build_data.py`. Do not use them as biological evidence. Identifiers are
fictional. Read the study description before deciding what counts as a replicate.

Blank numeric cells represent missing measurements. They are not zero. CSV
files have one header row and use a decimal point, with no units in numeric cells.
Units belong in the column definitions and plot labels.

## seedlings.csv — a small plant experiment

Twenty-four seedlings were grown in separate pots under the same conditions.
Twelve were randomly allocated to a nutrient treatment and twelve to a control.
Length was measured at the start and after seven days. One pot contains one plant;
the plant/pot is the independent experimental unit. Treat these simulated
measurements as independent for the introductory exercises.

| Column | Meaning |
| --- | --- |
| `plant_id` | Unique identifier P01–P24; a label, not a measurement |
| `treatment` | `control` or `treated` nutrient allocation |
| `initial_mm` | Initial seedling length, millimetres |
| `final_mm` | Length after seven days, millimetres |

Calculate `growth_mm = final_mm - initial_mm`. There are 24 plants, not 48
independent plants. The grouping of rows in the file is for readability; it does
not describe the order of measurement or the allocation method.

## seedlings-messy.csv — a transcription exercise

An intentionally imperfect export of the same study, with 25 rows and problems
in labels, units, an imported duplicate, and a missing measurement. This is a
separate teaching exercise: preserve its raw contents and repair a copy in code.

Use the accompanying `field-notes.txt` as evidence for corrections. For the
missing value, the original reading is unavailable in this exercise; retain it as
missing. Do not copy a value from seedlings.csv to fill the gap. The later
statistics lessons deliberately use the complete, separate seedlings.csv file.

## calibration.csv and unknowns.csv — a colorimetric assay

A fictional colour assay produces greater absorbance at higher concentration.
Six known standards were prepared, one reading per standard. Use a straight line
as a teaching approximation within 0–10 mg/L. The standard at 0 mg/L includes
background signal; do not force the line through zero. No blank subtraction has
been performed.

| File / column | Meaning |
| --- | --- |
| calibration.csv: `standard_id` | S1–S6, identifiers for prepared standards |
| calibration.csv: `concentration_mg_l` | Known concentration in milligrams per litre |
| calibration.csv: `absorbance` | Measured absorbance, dimensionless |
| unknowns.csv: `sample_id` | U1–U3, identifiers for separate unknown samples |
| unknowns.csv: `absorbance` | Measured absorbance, dimensionless |

These standards are calibration points, not independent treatment groups. U3 is
outside the measured calibration range. Flag it for dilution and remeasurement;
do not present an extrapolated concentration as a supported assay result.
Inverting a fitted line gives a point estimate, without propagating uncertainty
in standards, preparation, or measurement.

## paired.csv — the same plants measured twice

Ten independent plants each had a non-destructive photosynthesis measurement
before and after increasing illumination. Pair the two readings by plant ID.
All plants were measured in the same before/after order, with no parallel
unchanged-light group. The difference is descriptive evidence of a change under
these conditions, but does not isolate light from time/order effects.

| Column | Meaning |
| --- | --- |
| `plant_id` | Unique plant identifier L01–L10 |
| `before_umol_m2_s` | Before reading, micromoles CO2 per square metre per second |
| `after_umol_m2_s` | After reading, same units |

There are ten independent pairs, not twenty independent plants. Positive
`after - before` means the measured rate increased.

## leaf-mass.csv — an observational association

One leaf was collected from each of eighteen independent plants. Its area was
measured and it was dried and weighed. No treatment was assigned.

| Column | Meaning |
| --- | --- |
| `plant_id` | Unique identifier A01–A18 |
| `leaf_area_cm2` | Leaf area, square centimetres |
| `dry_mass_mg` | Dry mass, milligrams |

A fitted slope describes association in this sample, not an intervention that
increases area. Do not extrapolate well beyond the measured area range.

## duckweed.csv — the integrated practice study

Twenty separate flasks were started with equal amounts of duckweed, a small
floating aquatic plant. Ten flasks were randomly allocated additional nutrients;
ten were controls. Final dry biomass was measured once after seven days. Assume
independent flasks and that the remaining growing conditions were comparable.

| Column | Meaning |
| --- | --- |
| `flask_id` | Unique culture-flask identifier F01–F20 |
| `treatment` | `control` or `nutrient` allocation |
| `biomass_mg` | Final dry biomass, milligrams |

F17 was spilled at harvest, before weighing. Its biomass is missing. Explain the
loss, show the number available in each group, and make conclusions conditional
on the observed data. Twenty flasks were started; nineteen have usable biomass
measurements. A flask's many fronds are not separate independent replicates.

## dna.txt and pixels.csv — how information is represented

`dna.txt` contains a short invented DNA sequence on one line, followed by a
newline. It is plain text, not a database record or a real gene. The letters
illustrate character data; there is no sequence-analysis workflow.

`pixels.csv` contains eight rows and eight columns (`x1`–`x8`) of grayscale
intensities, from 0 (black) to 255 (white). Each cell is one pixel, not a plant or
biological replicate. Values 25 and 210 form a simple bright object against a
dark background. The table is a teaching image, not a microscope measurement.

## organic-recovery.csv — a basic organic-laboratory transfer example

This is an alternative practice dataset, not a requirement to have studied
organic chemistry. Twelve independent synthesis runs were randomly allocated
one of two fictional collection protocols, `standard` or `modified`, six each.
A synthesis makes a product from starting materials; collecting that product
may leave less material than a theoretical maximum. We supply that maximum for
every run: no reaction equation or chemical calculation is needed to obtain it.
Runs used different starting scales, so their maximum masses differ.

| Column | Meaning |
| --- | --- |
| `run_id` | Unique independent-run identifier Y01–Y12 |
| `protocol` | Randomly assigned collection protocol, `standard` or `modified` |
| `theoretical_mass_g` | Supplied maximum possible product mass for that run, grams |
| `isolated_mass_g` | Mass of dry collected product, grams; assumed pure for this simplified example |

Calculate **percentage yield** as
`yield_percent = 100 * isolated_mass_g / theoretical_mass_g`.
For Y01, 0.62 g collected from a maximum of 1.00 g gives 62%. Compare percentages
when comparing differently scaled runs; larger raw mass alone need not mean
greater yield. There are no missing values in this dataset. Preserve the raw
mass columns and save calculated values separately.

Each row is one independent run, not a repeat weighing of the same material.
The six values per protocol can describe run-to-run variation. Three readings
from one run would not be three independent runs. We assume the supplied mass
and simplified purity conditions; the dataset does not establish actual purity,
the reason for losses, or a protocol's general safety or sustainability. A
higher yield alone establishes none of those things. No wet-lab procedure is
specified or required.

## organic-inventory.tsv — supplied sample labels, not structure identification

This text table has one header and four records. Its columns are `sample_id`,
`sample_class`, and `note`. IDs O01–O04 identify fictional samples; the classes
are supplied labels: O01 `alcohol`, O02/O03 `ester`, O04 `carboxylic-acid`.
The words name classes of organic compounds, but the exercise only searches
already assigned text labels. No structures, reactions, or chemical
classification knowledge are needed. There are two records containing the
literal text `ester`; the header and other notes do not contain that term.

The separate `organic-lab.zip` packages this inventory as `inventory.tsv`, the
recovery CSV, and short explanatory notes for a command-line transfer exercise.
It is an alternative to repeated seedling-file practice, not a new software unit.

## seedlings-transfer.csv — a second seedling study

Eighteen new simulated seedlings were grown in separate pots. Nine were randomly
assigned a control allocation and nine a nutrient treatment; each was measured
at the start and seven days later. These are independent plants in a separate
study, not additional readings from the original 24 plants.

The columns have the same definitions as seedlings.csv: `plant_id` (T01–T18),
`treatment` (`control`/`treated`), `initial_mm`, and `final_mm`. Both lengths are
millimetres. Calculate `growth_mm = final_mm - initial_mm`. All readings are
available. Use it to check that an analysis works when the data and sample sizes
change. Do not combine studies without discussing their different conditions;
our exercises analyse them separately.

## solutions.csv — quantities and unit conversions

A solution contains a substance mixed into a solvent. A mole (mol) is a unit
of chemical amount; molar mass gives grams per mole. A millimole (mmol) is
one-thousandth of a mole. Chemical constants are supplied, not something students
must remember or look up. Sodium chloride and glucose are simply two named
solutes for this calculation exercise; no reaction knowledge is needed.

| Column | Meaning |
| --- | --- |
| `solution_id` | Q01–Q06, identifiers of six proposed preparations |
| `solute` | Supplied substance label: `sodium-chloride` or `glucose` |
| `mass_g` | Mass of substance in grams |
| `molar_mass_g_mol` | Supplied molar mass in grams per mole, 58.44 or 180.16 |
| `final_volume_ml` | Final total solution volume in millilitres, not solvent volume added |

For these simplified complete-dissolution calculations, amount in mol is
`mass_g / molar_mass_g_mol`, final volume in litres is `final_volume_ml / 1000`,
and concentration in mmol/L is `1000 * amount_mol / final_volume_l`.
Each solute has proposed concentrations of 50, 100, and 150 mmol/L. For Q01,
0.2922 g / 58.44 g/mol = 0.005 mol, in 0.100 L: 0.050 mol/L = 50 mmol/L.
These are arithmetic preparations, not replicate observations for a treatment
test. Values and assumptions are given for numerical practice, not a lab protocol.

## dilutions.csv — flag an impossible request

A stock is a prepared solution of stated concentration. Dilution adds solvent
to a portion of stock to reach a specified final total volume. Assume no solute
is lost or reacts. All concentrations here use mmol/L and all volumes use mL.

| Column | Meaning |
| --- | --- |
| `solution_id` | D01–D04, identifiers of requested dilutions |
| `stock_mmol_l` | Supplied starting-stock concentration |
| `target_mmol_l` | Requested final concentration |
| `final_volume_ml` | Requested final total volume |

Use `stock_volume_ml = target_mmol_l * final_volume_ml / stock_mmol_l`.
D01–D03 need 2.5, 5, and 10 mL of stock respectively. D04 requests 200 mmol/L
from a 100 mmol/L stock; the formula returns 100 mL stock for a final 50 mL.
That is impossible by dilution alone. Keep D04 visible and flag it; do not treat
the numeric result as a feasible recipe. Bringing a solution to a final total
volume is different from adding that volume of solvent.

## calibration-transfer.csv and unknowns-transfer.csv — another instrument run

These are separate simulated readings for the same introductory calibration
workflow. Do not reuse the original instrument run's fitted coefficients.
`calibration-transfer.csv` has six prepared standards R1–R6 with the same columns
as calibration.csv: `standard_id`, `concentration_mg_l` (0–5 mg/L), and
`absorbance` (dimensionless). The standards are not treatment replicates.

`unknowns-transfer.csv` has `sample_id` and `absorbance`: X1 reads 0.270, inside
the measured standard range; X2 reads 0.700, outside it. Fit absorbance as a
function of known concentration, inspect the fit, then invert only within the
supported range. Flag X2 rather than extrapolate. Any exercise using a new
diluted reading must supply that new reading and both volumes explicitly.
Inverse estimates still omit full calibration/measurement uncertainty.

## algae.csv — independent transfer study

Twenty-four separate algae cultures started with equal material. Twelve were
randomly assigned a reference medium and twelve a nutrient supplement. Final
dry biomass was measured once after seven days. Treat cultures as independent
for this simulated study; cells or repeated balance readings are not additional
independent cultures. The culture, not a cell, received the allocation.

| Column | Meaning |
| --- | --- |
| `culture_id` | Unique culture identifiers A01–A24, local to this study |
| `treatment` | `reference` or `supplement` random allocation |
| `biomass_mg` | Dry biomass after seven days, milligrams |

A19 was spilled before weighing and has unavailable biomass. There are 24
records, with 12 available reference and 11 available supplement measurements.
Preserve the missing value; never replace it with zero. Report the loss and
make interpretation conditional on the available observations. The input remains
untouched while code creates summaries, figures, and the chosen report. IDs
may resemble IDs in other files but do not identify the same organisms across
studies. Do not join unrelated studies merely because identifiers look similar.
