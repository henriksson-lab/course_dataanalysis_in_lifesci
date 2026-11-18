# Organic-laboratory contexts and the exercise review

Parallel reviewers checked the exercises in **all 25 daily modules** for given
inputs, understandable operations, units, saved deliverables, checkable results,
and continuity. They implemented a small set of context choices and repaired
ambiguous rendering instructions. Detailed module-by-module decisions are in:

- [Days 1–10](exercise-review-weeks1-2.md).
- [Days 11–15](exercise-review-week3.md).
- [Days 16–25](exercise-review-weeks4-5.md).

## Scope and evidence

The local [Organic Chemistry 1 dossier](../../molbiol_program/courses/5KE231-organic-chemistry-1.md)
records the 2027 course at 7.5 ECTS, with course-specific outcomes and practicals
still unconfirmed. Its [15-credit predecessor](../../molbiol_program/courses/5KE180-organic-chemistry.md)
is a comparator, not a list of prerequisites for these exercises. The
[published predecessor syllabus](https://www.umu.se/en/education/syllabus/5ke180/)
describes experimental records and laboratory reporting, alongside a much wider
organic curriculum. We reuse basic numerical laboratory contexts only; we do not
claim these particular datasets or exercises are confirmed 5KE231 practicals.

No prior chemistry is required. Each exercise supplies definitions, quantities,
units, formula, simplified assumptions, and an answer check. The maximum product
mass is given; students do not calculate it from a reaction or infer structures.
Mechanisms, synthesis planning, stereochemical assignments, IR/NMR interpretation,
and chemical-model fitting are excluded from the new tasks.

## Implemented student material

| Lesson | Basic context | Computing/data-analysis purpose | Workload control |
| --- | --- | --- | --- |
| Day 5 | Search given `ester` labels in a sample inventory | Reuse ZIP extraction, paths, `less`, `grep`, redirection, and counts | Alternative to one partner transfer check |
| Day 6 | Percentage yield from supplied maximum and collected masses | Named inputs, division, percent scale, changing an input | Alternative to the extra plant ratio task |
| Day 8 | Derive yield for 12 independent runs | Import, calculated column, individual-point plot, CSV/PNG export | Alternative to an extra plant plot variation |
| Day 12 | Centre and spread of yields | Mean, variance, SD, units in percentage points | Alternative to one summary task |
| Day 13 | Protocol-level summaries with observations visible | Group counts, individual observations, caption and exports | Alternative to extra transfer practice |
| Day 14 | Repeat weighing versus independent synthesis runs | Identify independent units without another simulation | Alternative diagram context |
| Day 15 | A descriptive organic-laboratory report | Reuse the whole report workflow | One chosen report, not two; `organic-report.Rmd` |
| Day 19 | A newly measured diluted sample within a calibration range | Invert a fitted line and apply a supplied dilution factor | Short general laboratory bridge; no added statistical method |
| Day 23 | Independent report of collected-product yield | Check, calculate, plot, summarise, interpret, render | Alternative to duckweed; `organic-study.Rmd` |
| Days 24–25 | Reproduce and consolidate that chosen report | Package matching source/input files, render fresh, retain limits | One selected study; no extra test required |

The seedling and duckweed pathways remain available, and week 4 still provides
the guided hypothesis-test and line-fitting work. Students selecting a
descriptive final study still complete that earlier statistical practice.
No new days or packages were introduced. Retain day 25 for consolidation.

## Shared assets and numerical anchors

`data/organic-recovery.csv` has 12 unique independent synthesis runs, six per
randomly assigned `standard`/`modified` collection protocol. The supplied
`theoretical_mass_g` differs with starting scale; `isolated_mass_g` is dry
collected product, assumed pure for the simplified calculation. Both are grams.
All measurements are present. The calculation is:

```text
yield_percent = 100 * isolated_mass_g / theoretical_mass_g
```

Y01 is 62%. Standard mean yield is 68.6667%, sample SD 4.32049 percentage points;
modified mean is 77%, SD 3.74166 points. The observed difference is 8.3333
percentage points, not an 8.3333% relative change. More collected grams need not
mean a higher yield when starting scales differ. A higher yield alone establishes
neither purity nor general safety, sustainability, or superiority.

`data/organic-inventory.tsv` contains four supplied sample labels. Two records,
O02 and O03, contain literal `ester`. This is a text search, not an assignment
of chemical class from structure. Both files are in `course-files.zip`.
The separate `organic-lab.zip` has four files: README, inventory, recovery CSV,
and dictionary. The original seedling lab archive and its expected counts remain
unchanged.

The day 19 addition supplies a **new** diluted reading of 0.520 after 1.00 mL
was brought to 10.00 mL total volume. The fitted calibration gives approximately
7.404227 mg/L in the diluted sample and 74.042272 mg/L in the original. The
larger original estimate is supported by the new in-range diluted measurement;
U3 remains unsupported without another reading. Full uncertainty propagation
is not introduced.

## Verification and remaining limits

The updated week 2–5 instructor scripts check the new arithmetic and tables;
week 3 and week 5 also render complete organic report examples. The shell checks
use the actual ZIP and verify extracted content and matches. Root integration
repackages student assets, renders the full site, runs `make check`, and verifies
links/resources before committing and pushing.

These checks do not establish beginner workload, Windows/Mac GUI behaviour, or
the forthcoming remote service's login/desktop route. Those still need the
planned pilots and service details. The exercise reviews are teaching notes,
not examination specifications or a claim about official chemistry assessment.
