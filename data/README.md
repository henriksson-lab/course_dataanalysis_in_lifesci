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
