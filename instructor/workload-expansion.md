# Expanding the course to a full five-week study plan

Historical expansion record. The later [audit](audit-results.md) supersedes the
time estimates and minimum writing/step targets below. These counts describe a
past version; they are not continuing authoring requirements.


The user judged the initial volume insufficient and requested approximately
twice as much lecture and exercise material. Three parallel workers developed
weeks 1–2, weeks 3–4, and week 5. Root integration supplies the shared datasets,
workload plan, packaging, tests, and publication.

## What changes in the learning experience

Every daily module retains its explanation and guided practical, then adds two
substantial core blocks:

- **Extended practical:** trace a larger case, inspect intermediate results,
  diagnose a believable mistake, and explain a decision.
- **Independent transfer:** use a changed input or question with fewer prompts,
  save a result, interpret it, and regenerate it after restarting.

The blocks contain multi-step work and named outputs, not additional slides of
definitions or optional challenges for students already ahead. Chemistry remains
self-contained and elementary. Context choices remain choices; the expansion
does not require duplicate chemistry and biology reports for every practical.

Lectures gain additional explanations, contrasting cases, visual worked examples,
prediction pauses, and recovery demonstrations. The existing topic progression,
45-slide ceiling, approximately half-visual balance, copied sidebar/scaffold,
and separation of lectures from practicals are retained. Report/consolidation
units develop case review and recovery instead of adding new methods.

## Planning learner time

The [student study plan](../study-plan.qmd) allocates about 35 structured plus 5
flexible learner hours per week, approximately 200 over five weeks. These are
provisional learner-workload estimates, not 40 contact hours and not a new
examination specification. A typical day budgets explanation/demonstration,
guided work, extended/independent practice, interpretation/reporting, and
protected catch-up. Longer independent blocks use the catch-up allocation;
the largest allowances should not all be added together.

The estimate must be tested with beginners. Record which outputs students
complete, where they need help, and actual task durations. If a unit persistently
overruns, revise its scaffolding or allocation. If it is too easy, the less-guided
transfer is the appropriate check, not extra statistical methods or arbitrary
typing. File-system fluency, a fresh-session render, and explained independent
units remain more valuable than nominal slide counts.

## Additional input files

All are simulated and fully documented in `data/README.md`:

| File | Role and limits |
| --- | --- |
| seedlings-transfer.csv | A separate complete 18-plant study,9 independent pots per randomised allocation; same units/schema, new values and IDs |
| solutions.csv | Supplied masses, molar masses and final volumes; named objects/unit conversions, no chemistry lookup |
| dilutions.csv | Three feasible requests and one impossible by dilution alone; calculate and flag rather than treating every number as a usable recipe |
| calibration-transfer.csv | Six new standards; refit the line rather than reuse another instrument run's coefficients |
| unknowns-transfer.csv | One supported and one out-of-range reading; retain range/uncertainty limits |
| algae.csv | Fresh 24-culture study,12 allocations/group; one supplement measurement unavailable after a spill; distinguish 24 enrolled from 23 observed |

No new student software is needed. There are no new omics/database workflows,
nonlinear models, multiple regression, ANOVA, or statistical selection trees.

## Per-module evidence and solutions

- [Weeks 1–2 audit](expansion-weeks1-2.md): file/terminal/R foundations, new tasks,
  saved outputs, and checks.
- [Weeks 3–4 audit](expansion-weeks3-4.md): data quality, variation, interpretation,
  comparisons, pairs, calibration and association.
- [Week 5 audit](expansion-week5.md): local/remote work, representations, independent
  study, reproducibility, recovery, and consolidation.

The existing week-specific instructor solutions now cover the new numerical,
file, and report tasks. `instructor/transfer-data-checks.R` separately verifies
the shared new datasets and their supplied calculation/range/design anchors.

## Baseline and volume audit

`instructor/workload-baseline.json` records the prior version at commit
`b27d47c`: 220 content slides, 116 visual slides, 25,819 practical words including
code, 145 numbered practical steps, and 31 weekly-quiz questions. These are
mechanical descriptors of the original material, not measured student effort.


| Descriptor | Earlier draft | Expanded draft | Ratio |
| --- | ---: | ---: | ---: |
| Explanatory content slides | 220 | 434 | 1.97× |
| Content slides using pictures | 116 | 224 | 1.93× |
| Numbered practical steps | 145 | 459 | 3.17× |
| Practical words, including code | 25,819 | 46,933 | 1.82× |
| Weekly self-check questions | 31 | 62 | 2.00× |

The expanded decks contain 459 slides including titles; 51.6% of content slides use pictures. Each daily practical has both new core blocks. These counts describe material, not validated learner time.

`python3 tools/check_expansion.py` reports current per-day and total counts,
checks that both new core blocks exist in all 25 modules, checks approximate
lecture/practice expansion, and checks the weekly quizzes. It is deliberately
not presented as a validation of 200 student hours. The substantive evidence is
the task text, independent outputs, tested solutions, and eventual beginner pilot.

`make check` additionally checks computations, rendered report examples, fresh
student-project extraction, real shell archives, internal site links, and
lecture assets/limits. The optional browser check inspects every rendered slide
for frame overflow and verifies the scaffold's computed sidebar colours.
