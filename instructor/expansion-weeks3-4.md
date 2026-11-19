# Expanded teaching and practice: days 11–20

This expansion responds to the request for roughly twice the teaching and
practice volume while retaining the first-year methods and five-week sequence.
The added work develops independent analysis, error diagnosis, interpretation,
and report revision. It does not add advanced models, another software tool,
or a requirement to complete both biology and chemistry routes.

## Content and activity changes

Every daily page now has core **Extended practical** and **Independent
transfer** sections, with concrete steps, hints, output names, and checks. No
duration is stated; how long they take beginners is unknown until piloted.

| Day | Added worked and independent work | Additional saved outputs |
| --- | --- | --- |
| 11 | Audit every source-supported repair; compare text/numeric representations; deliberately demonstrate the wrong missing-to-zero result in a separate object; inspect a fresh transfer file and a classroom-created duplicate | Correction audit, transfer audit, derived transfer CSV, handover paragraph |
| 12 | Hand-work deviations and transformations; investigate one changed observation; plot observations/means; independently describe the new class in mm and cm | Transformation note, transfer summary/figure, 120–180 word interpretation |
| 13 | Compare mean-only and individual displays; repair misleading captions; vary bins and document stable patterns; export a complete new-class figure/table package | Caption log, figures, transfer summary, handover request and rerun note |
| 14 | Diagram four designs; distinguish technical readings from units; vary seed/sample size/repetitions in supplied simulations; explain why precision cannot establish design validity | Design diagrams, sampling CSV/figure, source-versus-estimate spread table, interpretation |
| 15 | Review one chosen descriptive report as reader and analyst; trace numerical claims; add inline calculations; reproduce and revise; create a new-class descriptive report | Revision log, revised report, transfer-description.Rmd/HTML, minimum-file handover |
| 16 | Plan the contrast before a test; separate starting size/final size/growth; check direction and individual overlap; prepare another class's comparison without yet adding inference | Analysis plan, paired figure set, descriptive paragraph, transfer-comparison.Rmd/HTML |
| 17 | Annotate full output; reverse vectors; compare interval coverage levels; repair misinterpretations; extend the new-class report with the taught Welch comparison | Output-reading table, interval-level check, corrected statements, transfer comparison report |
| 18 | Preserve pair identity; demonstrate independent sorting as a deliberately invalid object; compare equivalent paired/on-changes calculations; interpret a fully supplied tiny paired case | Identity audit, valid/wrong comparison, change figures, paired-transfer.Rmd/HTML |
| 19 | Audit calibration direction/units/residuals; investigate rounded coefficients; preserve range reasons; trace dilution evidence; independently process a second calibration | Workflow/precision audit, range-checked tables, transfer-calibration.Rmd/HTML with figures |
| 20 | Interpret slope/residuals and range; conduct transparent sensitivity and unit checks; distinguish an arithmetic formula from empirical evidence; analyse a new observed association | Revised leaf report, unit/sensitivity checks, transfer-association.Rmd/HTML, three-question comparison sheet |

The organic alternatives remain basic and self-contained. Maximum possible
product mass, collected mass, formula, units, and simplified purity assumption
are supplied. The extended work develops whichever context is selected, rather
than making every student complete two parallel required studies.

## Lecture and practical volume

Baseline figures come from `instructor/workload-baseline.json`. Counts describe
material volume, not a guarantee of learning time. Word counts include code and
instructions; numbered-step counts are only a rough indicator because steps
can contain several connected actions.

| Day | Slides before → after, including title | Picture-bearing content slides | Practical words before → after | Numbered steps before → after |
| --- | --- | --- | --- | --- |
| 11 | 10 → 18 | 9 / 17 | 792 → 1680 | 5 → 18 |
| 12 | 10 → 18 | 9 / 17 | 1044 → 1928 | 5 → 18 |
| 13 | 10 → 18 | 9 / 17 | 961 → 1801 | 5 → 18 |
| 14 | 10 → 18 | 9 / 17 | 883 → 1704 | 5 → 18 |
| 15 | 8 → 15 | 8 / 14 | 1311 → 2176 | 11 → 24 |
| 16 | 10 → 18 | 9 / 17 | 883 → 1680 | 5 → 18 |
| 17 | 10 → 19 | 9 / 18 | 908 → 1690 | 3 → 17 |
| 18 | 10 → 18 | 9 / 17 | 889 → 1698 | 5 → 18 |
| 19 | 12 → 22 | 11 / 21 | 1109 → 1887 | 4 → 17 |
| 20 | 11 → 20 | 11 / 19 | 889 → 1691 | 3 → 16 |

Totals: **91 → 174 content slides**, plus ten titles; **93 / 174** content
slides use pictures (53%). Practical source grows from **9669 to 17935 words**
and **51 to 182 numbered steps**. Both weekly quizzes grow from six to twelve
questions with worked answers. Forty-one new reproducible SVG diagrams/plots
bring the owned lecture assets to 82 SVGs, alongside reused course PNGs.

Added visuals include actual transfer-data plots, changed-value/shift/unit
comparisons, histogram and axis choices, simulation-level comparisons,
precision-versus-offset illustration, report dependencies, directed contrasts,
coverage-level intervals, correct/wrong pairings, a new calibration/range check,
and unit-consistent observational fits. They are explanatory assets, not slides
created solely to meet a number.

## Numerical anchors

- Defensible repaired mean across 23 available growths: 18.4869565 mm.
  An invented zero final reading for P06 creates −24.7 mm growth and changes
  the overall mean to 16.6875 mm.
- New seedling study: 18 independent plants, nine per group, no missing values;
  T01 growth 15.0 mm. Control mean 13.6555556 mm, treated mean 17.8666667 mm.
  The treated-minus-control difference is 4.2111111 mm, with Welch 95% interval
  approximately 1.94844–6.47378 mm and p about 0.00124.
- Main-study reversed vector order reflects and negates the confidence interval
  and preserves the two-sided p-value. The same-data 99% interval is wider
  than the 95%, which is wider than the 90%; the observed means do not change.
- Independently sorting paired columns preserves the mean change but changes
  its SD from about 1.01777 to 0.50454 rate units. This is deliberately invalid
  matching, not improved evidence. The three supplied illustrative pairs have
  changes 2, 1, 3, mean 2, SD 1, and approximate 95% mean interval −0.484–4.484.
- New calibration: intercept 0.02161905 and slope 0.10008571 per mg/L.
  X1 is supported at about 2.48168 mg/L; X2 is retained as outside range with
  no supported concentration. Forward substitution is an algebra check only.
- Converting leaf area from cm² to mm² divides the slope by 100 but leaves
  fitted masses unchanged. A separate fit without A18 is sensitivity work;
  the full observations remain the main analysis.

## Validation performed

`Rscript instructor/week3-solutions.R` and
`Rscript instructor/week4-solutions.R` pass. They compute the added tasks,
export derived tables/figures, and render complete instructor examples. The
new reports are transfer-description, transfer-comparison, paired-transfer,
transfer-calibration, and transfer-association, each with its own saved inputs
and calculations; they are written beneath ignored `output/instructor-week*/`.

All ten lecture code sequences were extracted and **executed in separate fresh
R processes** against a disposable course-data fixture, not merely parsed with
preloaded objects. This caught and repaired a missing saved-file step on day 11
and missing package loading on day 12. Day 13's plot creation and day 14/17
prerequisite imports were also made explicit. Local practical/image links resolve,
SVGs parse, every new explanatory slide has speaker notes, and all decks stay
below 45 slides. Root owns full-site rendering and browser overflow checks.

No root data/configuration/output paths or other workers' teaching sources were
edited. Native Windows/Mac interface details, remote service access, and actual
beginner timing still require the central pilots; these local checks do not
claim to have tested those environments.
