"""Check lecture/practical pairing, slide limits, and real local visual assets."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def visible_source(source):
    """Ignore front matter, speaker notes, and code when finding slide markers."""
    body = source.split("\n---", 1)[1]
    lines = []
    fence = None
    notes = False
    for line in body.splitlines():
        if line.strip().startswith("::: notes"):
            notes = True
            continue
        if notes:
            if line.strip() == ":::":
                notes = False
            continue
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            if fence is None:
                fence = match[1]
            elif match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def check():
    practicals = sorted(p for p in ROOT.glob("week[1-5]/[0-9][0-9]-*.qmd")
                       if not p.stem.endswith("-quiz"))
    decks = sorted(ROOT.glob("lectures/*/lec.qmd"))
    assert len(practicals) == len(decks) == 25
    config = (ROOT / "_quarto.yml").read_text()
    print("Day  Slides  Visual slides (excluding title)")
    total_slides = total_visual = 0
    for practical in practicals:
        deck = ROOT / "lectures" / practical.stem / "lec.qmd"
        assert deck in decks, practical
        source = deck.read_text()
        assert "revealjs:" in source and "../../theme.scss" in source, deck
        assert "Data Analysis in Life Sciences" in source, deck
        assert f"../../{practical.relative_to(ROOT).as_posix()}" in source, deck
        assert f"lectures/{practical.stem}/lec.qmd" in practical.read_text(), practical
        assert f"lectures/{practical.stem}/lec.qmd" in config, practical
        slides = re.split(r"^## ", visible_source(source), flags=re.MULTILINE)[1:]
        assert 3 <= len(slides) <= 44, (deck, len(slides) + 1)
        visual = 0
        for slide in slides:
            images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", slide)
            if images:
                visual += 1
            for alt, target in images:
                assert alt.strip(), f"Missing image description in {deck}: {target}"
                path = (deck.parent / target.split('"')[0].strip()).resolve()
                assert path.is_file(), (deck, target)
                if path.suffix == ".svg":
                    ET.parse(path)
        ratio = visual / len(slides)
        assert ratio >= 0.30, f"Too few visual slides in {deck}: {visual}/{len(slides)}"
        built = ROOT / "docs" / deck.relative_to(ROOT).with_suffix(".html")
        html = built.read_text()
        assert 'class="reveal"' in html, f"Deck did not render as RevealJS: {deck}"
        print(f"{practical.stem[:2]}   {len(slides)+1:>3}      {visual}/{len(slides)} ({ratio:.0%})")
        total_slides += len(slides) + 1
        total_visual += visual
    for week in range(1, 6):
        quiz = ROOT / f"week{week}" / "quiz.qmd"
        assert quiz.is_file() and quiz.relative_to(ROOT).as_posix() in config
        assert (ROOT / "docs" / quiz.relative_to(ROOT).with_suffix(".html")).is_file()
    print(f"25 lecture/exercise pairs, five weekly revision quizzes, {total_slides} slides incl. titles, {total_visual} visual slides. All decks <=45 slides.")


if __name__ == "__main__":
    check()
