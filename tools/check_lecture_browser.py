"""Optional local Chrome/CDP check of slide overflow and sidebar colours.

Start a headless Chrome at localhost:9223 and serve docs/ at localhost:8765.
Requires websocket-client; not part of the ordinary make check dependencies.
Writes inspection screenshots and a JSON report into ignored output/.
"""

import base64
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen
import websocket

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "lecture-preview"
OUT.mkdir(parents=True, exist_ok=True)
with urlopen(Request("http://127.0.0.1:9223/json/new?about:blank", method="PUT")) as response:
    target = json.load(response)
socket = websocket.create_connection(target["webSocketDebuggerUrl"], timeout=30,
                                     suppress_origin=True)
serial = 0


def command(method, params=None):
    global serial
    serial += 1
    socket.send(json.dumps({"id": serial, "method": method, "params": params or {}}))
    while True:
        response = json.loads(socket.recv())
        if response.get("id") == serial:
            if "error" in response:
                raise RuntimeError(response["error"])
            return response.get("result", {})


def evaluate(expression):
    result = command("Runtime.evaluate", {"expression": expression,
                     "awaitPromise": True, "returnByValue": True})
    if "exceptionDetails" in result:
        raise RuntimeError(result["exceptionDetails"])
    return result.get("result", {}).get("value")


def navigate(path, slides=False):
    command("Page.navigate", {"url": "http://127.0.0.1:8765/" + path})
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        try:
            condition = "document.readyState === 'complete'"
            if slides:
                condition += " && window.Reveal && Reveal.isReady()"
            if evaluate(f"Boolean({condition})"):
                evaluate("document.fonts.ready.then(() => true)")
                return
        except RuntimeError:
            pass
        time.sleep(0.1)
    raise RuntimeError(f"Page did not become ready: {path}")


command("Page.enable")
command("Emulation.setDeviceMetricsOverride", {"width": 1440, "height": 900,
        "deviceScaleFactor": 1, "mobile": False})
navigate("index.html")
sidebar = evaluate("""(() => {
  const root = document.querySelector('#quarto-sidebar');
  const lecture = root.querySelector('a[href*="lectures/"]');
  const quiz = root.querySelector('a[href*="quiz.html"]');
  const practical = root.querySelector('a[href*="week1/01-files"]');
  const bands = [...root.querySelectorAll('.sidebar-menu-container > ul > li')]
    .slice(2,7).map(el => getComputedStyle(el).borderLeftColor);
  return {lecture: getComputedStyle(lecture).color,
          quiz: getComputedStyle(quiz).color,
          practical: getComputedStyle(practical).fontStyle, bands};
})()""")
assert sidebar["lecture"] == "rgb(26, 122, 59)", sidebar
assert sidebar["quiz"] == "rgb(42, 85, 194)", sidebar
assert sidebar["practical"] == "italic", sidebar
assert sidebar["bands"] == ["rgb(42, 127, 143)", "rgb(107, 79, 160)",
    "rgb(168, 50, 74)", "rgb(138, 106, 18)", "rgb(59, 91, 171)"], sidebar
shot = command("Page.captureScreenshot", {"format": "png"})
(OUT / "sidebar.png").write_bytes(base64.b64decode(shot["data"]))

navigation = []
for width, height, mobile in [(1440, 900, False), (390, 844, True)]:
    command("Emulation.setDeviceMetricsOverride", {"width": width, "height": height,
            "deviceScaleFactor": 1, "mobile": mobile})
    navigate("index.html")
    if mobile:
        evaluate("document.querySelector('button[aria-label=\"Toggle sidebar navigation\"]').click()")
        evaluate("new Promise(resolve => setTimeout(resolve, 450))")
    state = evaluate("""(() => {
      const sidebar = document.querySelector('#quarto-sidebar');
      const quiz = sidebar.querySelector('a[href$="01-files-quiz.html"]');
      const section = quiz.closest('ul');
      const toggle = sidebar.querySelector('[data-bs-target="#' + section.id + '"]');
      const initiallyCollapsed = !section.classList.contains('show');
      if (initiallyCollapsed) toggle.click();
      return new Promise(resolve => setTimeout(() => {
        const box = quiz.getBoundingClientRect();
        resolve({width: innerWidth, initiallyCollapsed,
          expanded: section.classList.contains('show'),
          visible: box.width > 0 && box.height > 0,
          colour: getComputedStyle(quiz).color,
          label: quiz.textContent.trim()});
      }, 450));
    })()""")
    assert state["initiallyCollapsed"] and state["expanded"] and state["visible"], state
    assert state["label"] == "Quiz" and state["colour"] == "rgb(42, 85, 194)", state
    navigation.append(state)
    navigate("week1/01-files-quiz.html")
    answer = evaluate("""(() => {
      const callout = [...document.querySelectorAll('.callout')]
        .find(el => el.querySelector('.callout-title-container')?.textContent.trim() === 'Answer');
      const content = callout.querySelector('.callout-collapse');
      const collapsed = !content.classList.contains('show');
      callout.querySelector('[data-bs-toggle="collapse"]').click();
      return new Promise(resolve => setTimeout(() => resolve({collapsed,
        opens: content.classList.contains('show'),
        horizontalOverflow: document.documentElement.scrollWidth > innerWidth + 2}), 450));
    })()""")
    assert answer["collapsed"] and answer["opens"] and not answer["horizontalOverflow"], answer
command("Emulation.setDeviceMetricsOverride", {"width": 1440, "height": 900,
        "deviceScaleFactor": 1, "mobile": False})

overflows = []
counts = {}
for deck in sorted(ROOT.glob("lectures/*/lec.qmd")):
    route = deck.relative_to(ROOT).with_suffix(".html").as_posix()
    navigate(route, slides=True)
    slides = evaluate("Reveal.getSlides().map(s => Reveal.getIndices(s))")
    counts[deck.parent.name] = len(slides)
    assert len(slides) <= 45, route
    for number, index in enumerate(slides):
        evaluate(f"Reveal.slide({index['h']}, {index.get('v', 0) or 0})")
        evaluate("new Promise(resolve => setTimeout(resolve, 45))")
        result = evaluate("""(() => {
          const area = document.querySelector('.reveal .slides').getBoundingClientRect();
          const slide = Reveal.getCurrentSlide();
          const outside = [...slide.children].filter(el => !el.matches('aside.notes'))
            .map(el => ({el, box:el.getBoundingClientRect()}))
            .filter(({box}) => box.width > 0 && box.height > 0 &&
              (box.bottom > area.bottom + 4 || box.right > area.right + 4 ||
               box.top < area.top - 4 || box.left < area.left - 4))
            .map(({el,box}) => ({tag:el.tagName, text:el.innerText?.slice(0,90),
              bottom:Math.round(box.bottom-area.bottom), right:Math.round(box.right-area.right)}));
          return {title:slide.querySelector('h1,h2')?.textContent, outside};
        })()""")
        if result["outside"]:
            overflows.append({"deck": deck.parent.name, "slide": number+1, **result})
        if number == 2 and deck.parent.name in {"01-files", "12-variation", "19-calibration", "23-mini-study"}:
            shot = command("Page.captureScreenshot", {"format": "png"})
            (OUT / f"{deck.parent.name}.png").write_bytes(base64.b64decode(shot["data"]))
report = {"sidebar": sidebar, "quiz_navigation": navigation,
          "slides": counts, "overflows": overflows}
(OUT / "browser-check.json").write_text(json.dumps(report, indent=2))
socket.close()
print(f"Browser checked {len(counts)} decks / {sum(counts.values())} slides; sidebar colours and desktop/mobile quiz navigation verified.")
if overflows:
    print(json.dumps(overflows, indent=2))
    raise SystemExit(1)
print("No slide content exceeds the presentation frame. Screenshots:", OUT)
