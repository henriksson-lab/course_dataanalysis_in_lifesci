"""Audit the requested content expansion; counts do not validate learner hours."""

from pathlib import Path
import json
import re
from check_lectures import visible_source

ROOT = Path(__file__).resolve().parents[1]
baseline = json.loads((ROOT / "instructor/workload-baseline.json").read_text())
totals = {key: 0 for key in ("practical_words", "numbered_steps", "content_slides", "visual_slides")}
before = {key: sum(row[key] for row in baseline["days"].values()) for key in totals}
rows = []
for stem, old in baseline["days"].items():
    practical = next(ROOT.glob(f"week[1-5]/{stem}.qmd"))
    source = practical.read_text()
    assert re.search(r"^## Extended practical", source, re.M), practical
    assert re.search(r"^## Independent transfer", source, re.M), practical
    deck = ROOT / "lectures" / stem / "lec.qmd"
    slides = re.split(r"^## ", visible_source(deck.read_text()), flags=re.M)[1:]
    row = {
        "practical_words": len(re.findall(r"\b\w+\b", source)),
        "numbered_steps": len(re.findall(r"^\s*\d+\.\s", source, re.M)),
        "content_slides": len(slides),
        "visual_slides": sum(bool(re.search(r"!\[[^\]]*\]\([^)]+\)", slide)) for slide in slides),
    }
    for key in totals:
        totals[key] += row[key]
    rows.append((stem, old["content_slides"], row["content_slides"], row["numbered_steps"]))
print("Day / content slides before→after / numbered practical steps")
for stem, prior, current, steps in rows:
    print(f"{stem}: {prior} → {current}; {steps} steps")
for key in totals:
    print(f"{key}: {before[key]} → {totals[key]} ({totals[key] / before[key]:.2f}×)")
assert totals["content_slides"] >= before["content_slides"] * 1.8, "Lecture depth has not approximately doubled"
assert totals["numbered_steps"] >= before["numbered_steps"] * 1.8, "Active practical work has not approximately doubled"
assert totals["practical_words"] >= before["practical_words"] * 1.5, "New practical instructions need more substance"
assert totals["visual_slides"] / totals["content_slides"] >= 0.40, "Preserve the requested visual balance"
for week, old_count in baseline["quiz_questions"].items():
    source = (ROOT / week / "quiz.qmd").read_text()
    current = len(re.findall(r"^## \d+[.)] ", source, re.M))
    print(f"{week} quiz questions: {old_count} → {current}")
    assert current >= old_count * 1.8, week
assert (ROOT / "docs/study-plan.html").is_file()
print("Expansion and daily study blocks verified. Hour estimates still need a beginner pilot.")
