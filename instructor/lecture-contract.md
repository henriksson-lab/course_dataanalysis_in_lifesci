# Lecture scaffold and authoring contract

The course must follow the quantbio scaffold: topic sections link separately to
lecture slides, Exercises pages, and topic quizzes. Preserve the 25 existing daily pages
and their URLs. New decks live at `lectures/<daily-stem>/lec.qmd`.

User requirements: decks may be up to **45 slides**, but favour fewer slides and
never pad them. Roughly half should use a meaningful picture: diagrams, real
data plots, file-tree illustrations, or worked visual examples. A code block or
a table alone is not counted as a picture. Existing data plots may be reused.
Keep each teaching deck focused on its topic rather than reproducing all
practical prose. Consolidation develops case discussion and recovery rather than
introducing another statistical method. The expanded teaching depth is described
below; the introductory topic boundaries remain. The later wording audit
supersedes minimum volume targets and mandatory peer tasks.

The later user-requested [workload expansion](expansion-contract.md) supersedes
the initial short-deck volume: roughly double explanations/demonstrations and
active practice within these topics, while retaining the 45-slide ceiling,
visual balance, and prohibition on filler. Consolidation includes substantial
case review and recovery practice; it introduces no new statistical method.

## Format (copy the sibling course's RevealJS scaffold)

Each deck front matter:

```yaml
---
title: "A short topic title"
subtitle: "Day N — short context"
author: "Data Analysis in Life Sciences"
format:
  revealjs:
    theme: [simple, ../../theme.scss]
    slide-number: c/t
    width: 1280
    height: 720
    transition: none
    history: false
    highlight-style: github
    code-overflow: wrap
    code-line-numbers: false
    incremental: false
    chalkboard: false
    menu: true
    html-math-method: katex
toc: false
---
```

Use `##` headings as slides and `::: notes` for lecturer guidance. Avoid long
bullets and tiny fonts. Images must be real local SVG/PNG assets, not emoji or
empty placeholders. Use informative alt text and suitable explicit height
(typically 350–420px) or columns. Parent copies theme.scss and styles.css from
quantbio and enables the same global navigation controls. Website execution is
disabled: code shown in slides must still be correct against the course data.

Each deck should have a motivating laboratory question, an explanation from
the actual student baseline, at least one concrete worked example or prediction,
an interpretation/recovery check, and a visible link to its existing practical
at `../../weekN/<daily-stem>.qmd`. Use notes for demonstration instructions,
assumptions, and expected answers. Don't add an unrelated question solely to
increase slide count.

## Deck structure (2026-11 makeover; supersedes the one-point-per-slide style)

Every deck follows the quantbio skeleton. Pilots: `lectures/01-files/lec.qmd`
and `lectures/17-welch-test/lec.qmd`.

1. **About this lecture.** One short paragraph with a concrete lab, project or
   thesis situation that motivates the topic, with the key question in bold.
   Then 3–4 bullets with the key ideas, and one line placing the day in the
   course (what kind of day it is, and what builds on it).
2. **The problem / what goes wrong.** Real consequences of not knowing the
   skill (repeated measurements, unverifiable reports, wrong conclusions).
   Motivation belongs on the slide, not only in the speaker notes.
3. **Concept slides.** Each slide is self-contained when watched or read
   without a lecturer: a figure plus 3–5 explanatory bullets, usually as
   `:::: {.columns}` with text left (~40–45%) and figure right. Merge thin
   one-sentence slides; never leave a heading, picture and one line.
4. **Worked example** on the course data, end to end, with checked numbers.
5. **Pitfalls / misreadings,** placed in the story rather than appended after the
   conclusion (material from the workload expansion is folded in here).
6. **Summary.** A concept/key-fact table, then `**Next (Day N, topic):**` and
   `**Now:**` with the exercise link and the files to leave with.

**Match the weight of the structure to the topic.** Hands-on basics (weeks 1–2:
files, folders, terminal, first R) stay plain: "Today you will: …", step-by-step
slides with one figure and one or two lines, and a plain-bullet summary; no
invented failure tables, no abstract framing (see the Day 1 deck). Conceptual
and statistical decks can use the full pattern with problem slides,
misreading tables and a key-fact summary table (see the Day 17 deck).

**Code is never shown without its output.** Students cannot picture what a
command does from the command alone. Show a short session exactly as it appears
on screen, with real output obtained by running it:
terminal as a `text` block with `$ ` prompts (see `lectures/04-inspect-archive`),
R as a `text` block in Console style (`> mean(x)` then `[1] 22.47083`). Code that
makes a plot sits next to the plot it makes. Commands that print nothing (`cp`,
`>`, `write_csv`, `ggsave`) are followed by `ls`/`list.files()`/reading the file
back, so the effect is visible. Trim long output with `...`, never invent it.

Aim for about 10–16 content slides. Use `{.smaller}` only for slides with code
plus a table, or the Summary; otherwise normal text size fills the slide.
Speaker notes add narration and demonstration instructions; they must not be
the only place where an idea is explained. Never state how long anything takes.

## Shared visual helper

`tools/lecture_svg.py` supplies low-level SVG drawing helpers. Use it if helpful
or author vector diagrams directly. Draw meaningful file hierarchies, memory
versus disk, movement/copy arrows, replicate layouts, coordinate/uncertainty
pictures, etc. Avoid disguising bullet lists as pictures. You can reuse existing
plots with `../../week3/variation-examples.png` and similar paths.
For new scientific plots use R/matplotlib and the actual supplied data.

Write a reproducible generator for your new figures in the assigned
`instructor/make-lecture-figures-*.py` file. Use outputs inside owned lecture
folders, and import helper by inserting the repository's tools/ on sys.path.
No AI photos or external image dependencies are needed for these concepts.

## Ownership and shared data

Read `instructor/development.md`, existing daily pages, and relevant instructor
solutions. Same data, units, interpretations, organic alternatives, zero
chemistry prerequisites, and pending remote details apply to slides.

- Worker A: decks 01–10, `instructor/make-lecture-figures-weeks1-2.py`.
- Worker B: decks 11–20, `instructor/make-lecture-figures-weeks3-4.py`.
- Worker C: decks 21–25, `instructor/make-lecture-figures-week5.py`, plus the quizzes within those weeks.
- Root: navigation, copied scaffold/theme/style, shared helper, checking,
  cross-links to decks, docs, packaging, commit/push and publication.

No other paths may be changed by workers. Quizzes use ordinary HTML (no reveal
front matter). Each topic links to `weekN/<daily-stem>-quiz.qmd`, with short
questions and separate collapsible Hint and Answer callouts. Weekly quizzes
provide revision; no new examination/grades. No teacher-only files in student ZIPs.
Keep every lecture <=45 slides. Report slide/image counts and validation.

Daily stems are listed in `instructor/development.md` and match existing pages.
