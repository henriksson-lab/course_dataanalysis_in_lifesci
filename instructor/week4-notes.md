# Week 4 teaching notes

All numeric examples use the generated synthetic datasets. Run
`Rscript instructor/week4-solutions.R` from the repository root to verify
calculations and produce plots in a temporary directory. The website's code
blocks are shown without execution; these calculations provide a separate check.
Run the same script with `--figures` to regenerate the six static figures linked
from the lessons in `week4/figures/`.

## Pacing and conceptual priorities

Day 16 is deliberately preparation rather than another inferential procedure.
Ask students to state the question, units, and independent unit before allowing
them to name a test. Protect time for explaining what each dot represents.
Day 17 adds only one core two-group method; Day 18 adds the paired-design
distinction. If pace is too fast, demonstrate the paired function call while
keeping the within-plant subtraction as required practice.

Students should keep each new `.Rmd` at the project root: the lessons' relative
paths assume that location. Previous HTML files remain useful for comparing
interpretation across designs. No examination or graded submission is specified.

## Reference results

- Seedlings: 12 control and 12 treated plants. Mean growth control 15.275 mm,
  treated 21.49167 mm. SDs approximately 3.19 and 4.87 mm respectively.
  Treated-minus-control difference 6.21667 mm; Welch 95% CI
  [2.70098, 9.73235] mm; two-sided p approximately 0.001517.
- Paired photosynthesis: ten plants, mean after-minus-before change
  1.983 µmol m⁻² s⁻¹; 95% CI [1.25494, 2.71107]; p approximately 0.0001664.
  All changes in this prepared example are positive. Discuss how future data
  could contain mixed directions without making pairing meaningless.
- Calibration: intercept 0.03957143, slope 0.06488571 absorbance per mg/L.
  U1 ≈ 4.16777 mg/L; U2 ≈ 7.40423 mg/L. U3 is outside the supported range and
  deliberately has no reported concentration estimate. Rearranging the fitted
  forward model is a first teaching estimate; full inverse-calibration
  uncertainty is deferred.
- Leaf association: intercept 9.476606 mg and slope 4.110117 mg/cm².
  Observed area range [2.96, 14.68] cm². Fitted mean mass at 8 cm² ≈ 42.35754 mg.
  A18 is not a known error. Its omission is a labelled sensitivity demonstration,
  never the main analysis or a reason to remove valid data.

## Misconceptions to listen for

- “A small p-value is the probability the treatment does not work.” Ask the
  student to begin the explanation with “If the equal-means model and its
  assumptions held …”. Avoid claiming a p-value is the probability of the data
  exactly as observed; the definition includes results at least as extreme.
- “The interval contains 95% of the plants.” Return to the individual-dot plot
  and distinguish spread of organisms from uncertainty in the group difference.
- “There are 24 independent data points because 12 plants were measured twice.”
  Ask which unit received treatment and which readings belong to the same plant.
- “Paired means two groups.” Ask whether the identity of a particular pair
  exists in the experimental design. The same plants measured twice are paired;
  unrelated groups are not paired by row position.
- “A significant before–after change proves light caused it.” Measurement order
  and time accompany the change. The test does not separate these explanations.
- “A good calibration line works anywhere.” U3 is a deliberate out-of-range
  example. Students must say how the laboratory could obtain an in-range reading,
  without pretending a dilution has already occurred.
- “The intercept is always a biological measurement at zero.” Zero area is not
  observed in the leaf dataset; the intercept positions an empirical line.
- “Delete points until the model works.” Separate investigation of recording
  errors from deletion of inconvenient biological variation.

## Formative conversations

For each report ask students to point to a number, name its units, and explain
what repeated or independent observation produced it. Ask a peer to read the
Results paragraph without the code and say what question was answered. A good
short answer states the magnitude and limitation, rather than reproducing all
printed R output. Confidence-interval derivation, full regression inference,
formal normality testing, and a menu of alternative tests are deliberately
outside this week.
