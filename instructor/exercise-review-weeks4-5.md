# Exercise review: days 16–25

Reviewed the current tasks against the requirement that a student can identify
the inputs, operations, units, expected output, and saved deliverable without
having taken chemistry. Organic Chemistry 1 is 7.5 ECTS in the 2027 plan; the
dossier does not confirm detailed outcomes or practicals for the new code.
The older 15-credit course's mechanisms and structure elucidation are not
assumed. These additions use basic laboratory arithmetic and reporting only.

| Day | Exercise decision | Change / reason | Validation |
| --- | --- | --- | --- |
| 16: independent groups | Retain | Supplied plant design and directed growth comparison already define all inputs and experimental units; keep the biological thread instead of adding another group analysis. | Week 4 script checks 24 unique plants, 12 per group, and a 6.2167 mm treated-minus-control difference. |
| 17: Welch comparison | Retain | Explicit direction, assumptions, interval, p-value, and root-level report are appropriate. No extra organic t-test is needed for the shortened chemistry context. | Week 4 script checks the actual test and interval from supplied data. |
| 18: paired observations | Retain | IDs, units, supplied paired values, and order limitation are explicit. A second paired chemical example would add workload without a new computing outcome. | Paired and one-sample-on-changes results agree in the instructor script. |
| 19: calibration | Add one short transfer calculation | Provide a new in-range diluted reading, both volumes, the concentration formula, factor, and answers. Distinguish a supported new reading from extrapolating U3. This is a general laboratory context, not a claimed official organic practical. | Script verifies diluted 7.404227 mg/L and original 74.042272 mg/L, and confirms U3 remains unavailable. |
| 20: association | Retain | Existing area/mass association teaches units, residuals, range, and causal limits. Do not replace it with a plot of a formula-generated chemical relationship and call that empirical regression. | Week 4 script checks 18 plants and the fitted slope from actual data. |
| 21: remote workflow | Retain | Generic project workflow also supports chemistry data. Pending service-specific instructions remain explicit; a new remote command sequence would be redundant. | Static check of paths, project root, and supported local rehearsal; no claim of live remote verification. |
| 22: representations | Retain | Text versus numeric representation is already broadly transferable. Spectral assignments would add chemistry prerequisites and exceed this basic context. | Week 5 script verifies DNA length/counts, 8×8 image, and threshold counts. |
| 23: integrated study | Add a descriptive alternative | Students choose one report: duckweed or organic product yield. Supply theoretical maximum, collected mass, percent formula, independent-run design, units, checks, plot, and limits. Starting scales differ, so compare percent yields. Name day 23 source `organic-study.Rmd` to preserve day 15's `organic-report.Rmd`. | Week 5 script checks 12 unique independent runs, six per protocol, no missing values, Y01=62%, protocol means/SD, 8.3333 percentage-point difference, and renders a complete alternative report. |
| 24: reproduce | Clarify study choice | Explicit filename/data substitutions for the organic alternative; reproduce one report and keep its dictionary. Do not demand a confidence interval from a descriptive exercise. | Alternative report renders from its own imports/calculations; manual folder-tree comparison confirms the substitution. |
| 25: consolidation | Clarify alternative output | Accept biological or laboratory question and the correct unit; keep descriptive organic report descriptive, with a purity limitation. No new catch-up topic. | Instructor scripts verify the existing recovery calculations; static check confirms the day 23 filename and data are consistent through days 24–25. |

## Numerical anchors for the organic alternative

- Standard protocol: mean 68.6667%, sample SD 4.32049 percentage points, n=6.
- Modified protocol: mean 77.0000%, sample SD 3.74166 percentage points, n=6.
- Modified minus standard: 8.3333 **percentage points**, not 8.3333% relative change.
- Yield is `100 * isolated_mass_g / theoretical_mass_g`; all theoretical maxima
  are supplied and positive. No reaction balancing or molar-mass lookup is needed.
- Purity is a stated simplifying assumption, not a measured result. No test,
  confidence interval, or causal superiority claim is required by this alternative.

## Checks run

`Rscript instructor/week4-solutions.R` and
`Rscript instructor/week5-solutions.R` exercise the new calculations and render
the two week 5 worked reports. Parent integration owns the complete Quarto build,
download packaging, and published-link checks. Remote accounts and student-machine
setup remain outside these local checks.
