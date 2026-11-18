# Exercise review: week 3, days 11–15

Scope: retain a gentle first data-analysis course and the existing biological
examples. The 2027 Organic Chemistry 1 course is reduced to 7.5 ECTS; its exact
practicals and outcomes are not confirmed in the local dossier. Our additions
use numerical lab records and require no prior chemistry. They do not import
mechanisms, synthesis planning, stereochemistry, or structure interpretation
from the older 15-credit predecessor.

The organic choices reuse one small simulated dataset. They substitute for
selected transfer practice and, if chosen, one descriptive report; they are not
four additional compulsory chemistry exercises. A student can still follow the
complete seedling pathway. Theoretical masses, the yield relationship, and
meaning of each quantity are supplied wherever first needed.

| Day | Exercise issue / decision | Change or reason to retain | Validation |
| --- | --- | --- | --- |
| 11: data quality | Existing repair task provides source-record evidence and a specific missing observation. Another chemistry table would distract from a new and already substantial workflow. | Retained. Explicitly preserve raw data, leave P06 missing, and distinguish 24 plants from 23 available growth values. | Instructor script checks 25 raw rows, 24 repaired unique IDs, one missing growth value, P21 = 43.8 mm, and 11 available control measurements. |
| 12: mean, variance, SD | Seedling summaries test the taught concepts, but an alternate laboratory quantity can demonstrate transfer without extra arithmetic techniques. | Added a substitute for practical step 4: derive percentage yield from supplied dry isolated and theoretical masses, then summarise standard/modified protocols. Defines grams, the ratio, percentage yield, variance units, and SD in percentage points. Keeps worked plant calculations. | Actual file gives Y01 62%; standard mean 68.6667%, variance 18.6667 squared percentage points, SD 4.32049 percentage points; modified mean 77%, SD 3.74166 percentage points. |
| 13: grouped summaries | Students need to retain counts, individual points, units, and the distinction between rows and summaries when changing context. | Added a choice in place of the extra repaired-seedling summary. Reuse import/mutate/group/plot/export operations for yield by protocol. Requires observations, caption, and meaningful filenames; no new package or statistical method. | Instructor script checks 12 independent rows, unique run IDs, positive denominators, no missing mass data, six runs per group; exports summary and plotted individual yields. |
| 14: replication and uncertainty | Existing simulation already introduces several new functions and should not gain a second simulation. | Retained the sampling demo. Added one optional diagram substitution: twelve weighings of one synthesis run versus six separately prepared runs per protocol. This transfers independence reasoning without extra code. | Verified the shared study design: independent run, not balance reading, is the unit randomly allocated a protocol. Numerical sampling demonstration remains unchanged and executes in instructor script. |
| 15: descriptive report | A single report consolidates the workflow; asking for a second chemical report would increase workload. | Added a fully specified alternative `organic-report.Rmd`, with question, input, quantity meanings, equation, checks, summary/plot guidance, expected anchors, interpretation limits, and matching render filename. The default seedling report and its clean/repaired distinction remain. | Instructor script renders complete seedling and organic examples. Organic source includes its own imports/calculations and uses project-relative input paths with an explicit root during teacher rendering. |

## Important interpretation limits

- Different starting scales mean raw collected mass and percentage yield answer
  different questions. Use each run's own supplied theoretical denominator.
- A higher yield does not establish higher purity. Dry pure product is an
  assumption of the numerical exercise, not an analytical finding.
- SD of yield values is expressed in percentage points; it is not a relative
  percentage improvement or the uncertainty in a protocol mean.
- Reweighing one product batch does not create independent synthesis runs.
- The week 3 report remains descriptive. It does not require a t-test, a
  reaction equation, mechanism, chemical structure, or new software.

## Verification performed

`Rscript instructor/week3-solutions.R` computes the existing repairs, numerical
summaries, sampling demo, and new organic transfer results. It writes and renders
complete seedling and organic HTML reports in the ignored instructor output
folder. All five edited/retained lesson files were extracted with `knitr::purl`,
their R syntax parsed, and all extracted chunks executed in fresh environments
against a temporary project copy. The day 15 Console render used the complete
source supplied by the instructor script. This also executed the new organic
calculation and summary blocks against the supplied CSV.
