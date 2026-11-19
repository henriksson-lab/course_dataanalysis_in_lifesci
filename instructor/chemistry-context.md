# Chemistry contexts: findings and proposed insertions

These are the initial investigated proposals. The day 19 dilution correction is
implemented. The later [workload expansion](workload-expansion.md) also implements
self-contained solution-concentration calculations and a dilution table in
days 6–8, with some different numerical examples. The specific volume-reading
task below remains a proposal; use the current student pages for active tasks.
Use chemistry to reinforce the existing computing outcomes without adding a
prerequisite, another week, new packages, or a separate chemistry track.

The subsequent [organic-context review](organic-context-review.md) implements
selected basic organic-laboratory alternatives. Its yield exercises are distinct
from the proposed general-chemistry mass/dilution tasks here. Consult that review
for implemented placements; the volume-reading task here remains a proposal.

## Evidence

Read the local [5KE165 dossier](../../molbiol_program/courses/5KE165-fundamentals-of-chemistry.md),
[programme overview](../../molbiol_program/README.md), and
[5KE232 dossier](../../molbiol_program/courses/5KE232-data-analysis-in-life-sciences.md).
The programme overview lists chemistry earlier, but flags semester sequencing as
an inference rather than a confirmed timetable. Our exercises must work without
prior completion regardless of the eventual order.

The [published 5KE165 syllabus](https://www.umu.se/en/education/syllabus/5ke165/)
includes stoichiometry, equilibrium calculations, kinetic models, and evaluating
and reporting laboratory results. This is the syllabus effective from 30 May
2022, not confirmation of future practicals or problem sheets. Those actual
materials are not supplied in the local dossier or syllabus. Absorbance
calibration and dispenser checks below are proposed laboratory contexts, not
documented named 5KE165 practicals. Do not substitute 5KE206's module details as
evidence for 5KE165.

## Required design rule

Every exercise must explain what to compute to a student who has never taken
chemistry. Supply the purpose, definitions, every input and constant, units and
conversions, the actual formula with symbols explained, assumptions, a worked
example, and a requested output with a checkable answer. Prior chemistry can
make a question familiar; it must not supply missing instructions. Normal prior
R lessons can still be assumed as the computing course progresses.

Avoid instructions such as “calculate the molarity” or “apply Beer–Lambert”
without explaining the requested operation. A chemical name is context, not an
instruction. All new example data should be labelled simulated.

## Best insertion points

| Priority | Existing lesson | Proposed task | Existing computing skill | Scope |
| --- | --- | --- | --- | --- |
| Core, short | Day 6: first R calculations | Calculate a solute mass from supplied concentration, final volume, and molar mass | Objects, arithmetic, comments, units, changing an input | Replace one repeated arithmetic task |
| Core, short | Day 8: derived columns | Calculate stock volumes for three dilutions using a supplied relationship | Import a tiny table, `mutate`, export calculated columns | Replace an extra plot variation |
| Small transfer check | Day 12: variation | Summarise repeated volume readings | Mean, variance, SD, spread versus a common offset | No new workflow |
| Strongest existing fit | Day 19: calibration | Explain the chemistry context and correct one newly measured diluted sample | Existing line fit, inversion, units, range checks | Retain the lesson; adds a small amount of arithmetic |

Retain seedlings as the recurring dataset and duckweed as the integrated study.
Do not fill the final catch-up day with new chemistry. Timing needs a beginner
pilot. Below are standalone wording and numerical anchors for implementation.

## Day 6: mass from supplied concentration and final volume

Suggested instructions:

> A solution contains a substance mixed into a solvent. We describe its chemical
> amount per litre using mol/L. A mole (mol) is a unit of chemical amount; you
> do not need to count particles here. Molar mass tells us the number of grams
> per mole. Use 58.44 g/mol for sodium chloride (NaCl).
>
> Calculate the mass corresponding to 0.150 mol/L in a **final solution volume**
> of 100 mL. Divide mL by 1000 to get litres. Amount in mol = concentration in
> mol/L × final volume in L. Mass in g = amount in mol × molar mass in g/mol.
> Save inputs as named objects and print the mass in grams. This is a calculation,
> not a laboratory protocol.

```r
concentration_mol_l <- 0.150
final_volume_ml <- 100
molar_mass_g_mol <- 58.44
final_volume_l <- final_volume_ml / 1000
amount_mol <- concentration_mol_l * final_volume_l
mass_g <- amount_mol * molar_mass_g_mol
mass_g
```

Answer: **0.8766 g**. Units cancel as `(mol/L) × L × (g/mol) = g`.
Change final volume to 200 mL and predict the doubled mass before rerunning.
Do not require looking up atomic masses, interpreting a reaction, or remembering
a formula. Keep the existing seedling vectors and matched-observation example.

## Day 8: a dilution table

Suggested instructions:

> A stock is a prepared solution of known concentration. A dilution uses some
> stock and solvent to reach a stated **final total volume**. Assume no solute
> reacts or is lost. Use stock volume = target concentration × final total
> volume / stock concentration. Both concentrations must have the same units;
> the resulting stock volume has the same units as final volume.
>
> With stock concentration 0.500 mol/L and target concentration 0.050 mol/L,
> final volumes of 25, 50, and 100 mL need 2.5, 5, and 10 mL of stock. For the
> 50 mL case, solvent brings the total to 50 mL; this does not mean adding
> 50 mL of solvent to the stock.

Proposed CSV for later implementation (not currently a shipped file):

```text
solution_id,stock_mol_l,target_mol_l,final_volume_ml
D01,0.500,0.050,25
D02,0.500,0.050,50
D03,0.500,0.050,100
```

After importing as `dilutions`, reuse this familiar pattern:

```r
dilutions <- dilutions |>
  mutate(stock_volume_ml = target_mol_l * final_volume_ml / stock_mol_l)
```

Provide its dictionary and biological-laboratory purpose in the same lesson.
An optional plot of calculated stock volume against final volume shows the
supplied relationship, not empirical evidence needing regression or a t-test.
A target concentration above the stock cannot be obtained by dilution alone;
flag that request rather than treating an excessive stock volume as a recipe.

## Day 12: measurement spread

Suggested instructions:

> A dispenser was set to deliver 10.0 mL. Three repeat checks gave 9.8, 10.0,
> and 10.2 mL. Calculate the mean, sample variance, and SD using today's
> definitions. Give their units. Add 0.5 mL to every reading and compare the
> new mean and SD with the originals.

```r
volume_ml <- c(9.8, 10.0, 10.2)
mean(volume_ml)
var(volume_ml)
sd(volume_ml)
mean(volume_ml + 0.5)
sd(volume_ml + 0.5)
```

Answers: mean **10.0 mL**, variance **0.04 mL²**, SD **0.2 mL**; the shifted
mean is **10.5 mL** and SD remains **0.2 mL**. Spread and common offset are
different. The example alone does not validate instrument accuracy: the check
method and reference have uncertainty too.

These are repeated checks of a measurement process, not independent organisms.
Link to day 14's replication distinction; do not turn repeat readings of one
chemical sample into independent treatment evidence.

## Day 19: keep calibration, add one dilution correction

The existing lesson already defines standards, provides known concentrations
and readings, fits absorbance as a function of concentration, and rearranges the
line. Keep that self-contained structure. Explain briefly that absorbance
describes light attenuation and that known standards connect the reading to
concentration over a tested range. Do not require recall of an optical law.

Possible follow-on instructions:

> A separate unknown was too concentrated for the instrument. For a **new**
> measurement, 1.00 mL of original sample was diluted to a total of 10.00 mL.
> The diluted reading is 0.520, the same as U2 in our teaching table. Use the
> fitted line to estimate the diluted concentration. Multiply it by total volume
> / original-sample volume = 10 to estimate the original concentration. State
> which measurement was within the calibration range.

Using current unrounded coefficients gives about **7.4042 mg/L** diluted and
**74.0423 mg/L** original. The larger original concentration is supported by a
new in-range diluted reading, not extrapolation. U3 remains unsupported unless
a new diluted measurement is explicitly supplied. Report sensible precision and
retain the explanation that full calibration/dilution uncertainty is omitted.

## Lower priorities and exclusions

**pH:** potentially useful for powers and logarithms, but it needs definitions,
a stated dilute-solution approximation, positive concentrations, and an
explanation of `log10()` and its inverse. Keep as a possible later alternative,
not a new core requirement. Do not silently average pH as if it were a linear
concentration scale, or require buffer/equilibrium knowledge.

**Kinetics:** a supplied first-order decay equation could illustrate time vectors,
`exp()`, and plotting model predictions. Selecting a rate law must not be assumed.
Defer fitting rate constants, nonlinear models, and model comparison.

**Reaction ratios:** possible arithmetic when a balanced reaction and ratio are
given; concentration/dilution transfers more directly with fewer new concepts.

Exclude equilibrium solvers, titration-curve models, speciation, Gibbs-energy
models, electrochemical calculations, quantum chemistry, and molecular software
from the core. They create chemical-model prerequisites or displace the computing
skills this course is meant to establish.

## Implementation sequence

1. Insert the short day 6 calculation and day 12 transfer check, preserving the
   existing computing explanations and biological examples.
2. Add the tiny dilution CSV and dictionary to the student ZIP; substitute a
   day 8 transfer task rather than adding a study unit.
3. Add the new diluted reading and correction to day 19, keeping the unsupported
   U3 example and the point-estimate/uncertainty distinction.
4. Extend instructor solutions, regenerate downloads and site, and pilot the
   text with someone without chemistry. Ask them to identify the given inputs,
   formula, units, and requested output before using R.

Original 5KE165 sheets could help choose recognisable situations, but are not
required to construct these exercises and must not become required reading.
