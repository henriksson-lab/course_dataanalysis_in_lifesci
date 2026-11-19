# Audit plan: concise, independent exercises and topic quizzes

## Findings and scope

Review all 25 exercise pages, their lecture decks, quiz pages, setup/reference
pages, and the public study guide. The current daily exercises contain 50
task-duration prompts, repeated partner/peer instructions, and unnecessary
restrictions such as “Do not look up a constant or infer a chemical formula”.
The study guide also prescribes daily time budgets. These need correction.

The quiz scaffold differs from Quantbio. Quantbio's topic pages, such as
`../quantbio-3MB00A/solving-systems/quiz.qmd`, use short questions, multiple-choice
or calculated answers where appropriate, and separate collapsible Hint/Answer
sections. Its sidebar places Quiz within each topic. This course currently has
five weekly self-check pages; they do not provide the same topic-level structure.
The separate Quantbio Canvas/bonus-quiz system is not assumed to apply here.

This is the agreed audit plan. See [audit results](audit-results.md) for the
implemented revisions and verification.

## Rules for the revision

- Remove estimates of how long a student should take, including the public
  daily-hour table. Retain the five-week course sequence and actual time units
  in scientific data. Students can work at different paces.
- Make every exercise completable independently. Replace required exchanges,
  partner checks, and peer reproduction with self-checks using saved files,
  fresh sessions, or a new extraction. Discussion can be optional without
  repeating an “if working alone” alternative in every task.
- State the task directly. Remove unneeded prohibitions, repeated assurances,
  artificial word counts, and commentary about how students should study.
- Supply required quantities, definitions, units, and formulas. This keeps
  chemistry examples self-contained without repeatedly saying what students
  must not look up or need not know.
- Keep a brief relevant caution where it teaches something consequential,
  such as `>` overwriting its destination. Explain scientific limitations where
  they are the learning point. Avoid repeating the same warning across steps.
- Preserve substantive calculations, investigations, data, and interpretation
  questions. Shorter instructions must not undo the expanded practice content.

## Pass 1 — Inventory and a shared editing standard

Create a module checklist recording pace language, mandatory collaboration,
redundant prose, required inputs/outputs, and quiz coverage. Inspect matches in
context rather than globally deleting words: paired observations and biological
replicates are not student group-work requirements.

Use a simple exercise format: **question; given data/formula; tasks; output or
answer check; optional hint**. Move duplicated conceptual teaching to the
lecture or a linked reference, retaining enough information to perform the task.
Replace generic pedagogical headings with task-specific titles where useful.

Examples of the intended editing:

| Current wording | Intended revision |
| --- | --- |
| “Plan 60–90 minutes.” | Remove. |
| “Exchange instructions.” | “Follow your written route and check the destination.” |
| “Do not look up a constant or infer a chemical formula.” | Remove; the supplied constants and formula already define the calculation. |
| “Ask a partner to reproduce the report…” | “Extract the project into a new folder and render the report.” |
| A long preamble about not needing chemistry | Define the unfamiliar term once, then give the inputs and calculation. |

## Pass 2 — Pilot three modules

Revise one file/terminal module, the first R calculation module, and the Welch
comparison module. For each, review the Exercises page alongside its lecture
and a new topic quiz. Check that a student can identify the input, operation,
and expected output without a partner or another subject course.

Use these as the editing examples before applying the standard across the
course. Do not use word counts or minimum step counts as quality targets.

## Pass 3 — Restore topic quizzes

Place a blue **Quiz** link beside **Lecture (slides)** and **Exercises** in each
topic section. Match the public Quantbio question/hint/answer format. Use a mix
of concise multiple-choice, small calculations, code predictions, and figure
interpretation, chosen for the topic's actual outcomes.

Reuse suitable weekly questions, add missing topic coverage, and verify all
answers against the supplied data/code. Weekly pages can serve as revision
collections; students should not need to hunt there for a topic's quiz. Check
desktop and mobile navigation and collapsed-menu discoverability. Do not add
Canvas grading, bonus points, or examination rules.

## Pass 4 — Course-wide review

After the pilot, divide weeks 1–2, weeks 3–4, and week 5 among parallel editors.
Use one independent cross-reviewer for consistency. Include lecture captions
and speaker notes, setup pages, the study guide, and references so removed
requirements do not survive elsewhere. Update authoring instructions to prevent
the same clutter returning in future revisions.

Review the validation tools too: retain numerical, rendering, link, slide-limit,
and asset checks. Remove minimum prose/step/volume gates that would penalise
concise editing or reward padding. Keep historical expansion counts as records,
not as continuing writing requirements.

## Completion checks

- No student task-duration estimates or required collaboration.
- Every exercise has clear inputs, actions, and a checkable result.
- Unnecessary restrictions and repeated boilerplate are removed.
- No chemistry prerequisite is introduced by shortening the text.
- Each topic has a discoverable quiz with verified hints/answers.
- All role labels read **Exercises**; existing URLs remain valid.
- Calculations, reports, downloads, links, and slide layouts still pass checks.

Finish with a change summary identifying removed clutter, retained learning
tasks, quiz coverage, and any unresolved content issues. No pace guarantee or
assessment design is part of this audit.
