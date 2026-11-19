"""Check topic quiz navigation and the student-visible hint/answer structure."""

from pathlib import Path
from html.parser import HTMLParser
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


class Callouts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.collapsed = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and "callout-collapse" in attrs.get("class", "").split():
            assert "show" not in attrs.get("class", "").split(), "Answer starts expanded"
            self.collapsed += 1


config = yaml.safe_load((ROOT / "_quarto.yml").read_text())
topics = {}


def walk(items):
    for item in items:
        if isinstance(item, dict) and "contents" in item:
            leaves = item["contents"]
            exercises = [leaf for leaf in leaves if isinstance(leaf, dict)
                         and leaf.get("text") == "Exercises"]
            for exercise in exercises:
                topics[exercise["href"]] = leaves
            walk(leaves)


walk(config["website"]["sidebar"]["contents"])
assert len(topics) == 25, f"Expected 25 navigable topics, got {len(topics)}"
total = 0
for exercise, leaves in topics.items():
    lesson = ROOT / exercise
    quiz = lesson.with_name(lesson.stem + "-quiz.qmd")
    route = quiz.relative_to(ROOT).as_posix()
    assert {"text": "Quiz", "href": route} in leaves, f"Missing topic Quiz link: {exercise}"
    assert quiz.is_file(), quiz
    source = quiz.read_text()
    assert lesson.name in source, f"Quiz must link back to Exercises: {quiz}"
    assert quiz.name in lesson.read_text(), f"Exercises must link to their quiz: {lesson}"
    questions = re.split(r"^\*\*Q\d+\.\*\*", source, flags=re.M)[1:]
    assert questions, f"No questions: {quiz}"
    for question in questions:
        for title in ("Hint", "Answer"):
            assert re.search(r'\{[^}]*collapse="true"[^}]*title="' + title + r'"[^}]*\}', question), (
                f"Missing collapsed {title} in {quiz}"
            )
    built = ROOT / "docs" / quiz.relative_to(ROOT).with_suffix(".html")
    parser = Callouts()
    parser.feed(built.read_text())
    assert parser.collapsed == 2 * len(questions), (quiz, parser.collapsed, len(questions))
    total += len(questions)
    print(f"{quiz.stem}: {len(questions)} questions")

assert len(list(ROOT.glob("week[1-5]/*-quiz.qmd"))) == len(topics), "Unlinked topic quiz"
print(f"25 topic quizzes, {total} questions; navigation, return links, collapsed hints/answers verified.")
