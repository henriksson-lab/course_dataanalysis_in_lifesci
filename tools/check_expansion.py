"""Report historical content counts without enforcing minimum writing volume.

Historical comparisons describe the material, not its quality or learner time.
Quiz structure, computations, assets, links, and slide limits have separate checks.
"""

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
for week, old_count in baseline["quiz_questions"].items():
    source = (ROOT / week / "quiz.qmd").read_text()
    current = len(re.findall(r"^(?:## \d+[.)] |\*\*Q\d+\.)", source, re.M))
    topic_questions = sum(len(re.findall(r"^\*\*Q\d+\.", p.read_text(), re.M))
                          for p in (ROOT / week).glob("*-quiz.qmd"))
    print(f"{week}: {current} weekly revision questions; {topic_questions} topic questions")
print("Historical counts only; no minimum prose, step, slide, or question quota.")
