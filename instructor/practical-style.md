# Writing style for practical pages (weekN/*.qmd)

Owner feedback (2026-11): the practical pages read as "random sentences slapped
together", headers "sound like company slogans", and tasks are lists of things
to do with no reason why a student would want to do them. Example of the
problem: `week2/07-import.qmd`, section "Inspect an unfamiliar table
systematically". These rules apply to every practical page.

## Headers

- A header names the topic in plain words, or asks the question the student
  actually has. Good: "Does R see all 24 plants?", "Reading the CSV into R",
  "Missing values", "A second class's data".
- Not slogans or imperatives: "Build a record you can audit", "Inspect an
  unfamiliar table systematically", "Leave a repair trail", "Explain the number
  you calculate".

## Motivation is built into the task, not explained

- Motivation does not need to be spelled out in a "why this matters" paragraph.
  Phrase each task as **"Use `xxx()` to find out yyy"**, where yyy is a
  biological question: "Use `table()` to find out how many plants received each
  treatment." "Use `sum(is.na())` to find out how many plants have no final
  length." The purpose is then obvious.
- Then say what you should see and what it means for the plants.
- If a task has no biological question it answers, cut it.

## Tasks

- Fewer tasks, each with a purpose. Do not list commands to "run and record".
- Give the expected result so students can check themselves.
- A transfer task on a second dataset is a new situation with its own question,
  not the same checklist repeated.
- Keep the file and object names later days rely on.

## Sentences

- Write connected paragraphs (because, so, then). Read it aloud: it should sound
  like a teacher explaining, not a list of disclaimers.
- Cut hedges and "X does not establish Y" clauses. Keep at most one warning per
  section, and only for a mistake students really make.
- Describe the study design once (link to `data/README.md`), not in every section.
- Plain words over jargon; define a term the first time it is needed.
- Never state how long anything takes.
