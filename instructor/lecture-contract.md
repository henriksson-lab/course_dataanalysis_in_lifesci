# Lecture scaffold and authoring contract

The course must follow the quantbio scaffold: topic sections link separately to
lecture slides and practical/notes pages. Preserve the 25 existing daily pages
and their URLs. New decks live at `lectures/<daily-stem>/lec.qmd`.

User requirements: decks may be up to **45 slides**, but favour fewer slides and
never pad them. Roughly half should use a meaningful picture: diagrams, real
data plots, file-tree illustrations, or worked visual examples. A code block or
a table alone is not counted as a picture. Existing data plots may be reused.
Prefer compact teaching decks: select the material needed for this topic rather
than trying to reproduce all practical prose. Consolidation days need only a
short briefing. No new methods or expanded course scope.

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
- Worker C: decks 21–25, `instructor/make-lecture-figures-week5.py`, plus
  `week1/quiz.qmd` through `week5/quiz.qmd` (five short formative self-check pages).
- Root: navigation, copied scaffold/theme/style, shared helper, checking,
  cross-links to decks, docs, packaging, commit/push and publication.

No other paths may be changed by workers. Quizzes use ordinary HTML (no reveal
front matter), refer to each week's taught content, and include brief collapsible
worked answers; no new examination/grades. No teacher-only files in student ZIPs.
Keep every lecture <=45 slides. Report slide/image counts and validation.

Daily stems are listed in `instructor/development.md` and match existing pages.
