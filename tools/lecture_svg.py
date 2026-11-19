"""Small dependency-free SVG primitives for reproducible lecture diagrams."""

from html import escape
from pathlib import Path

INK = "#203247"
TEAL = "#2a7f8f"
PURPLE = "#6b4fa0"
RED = "#a8324a"
BLUE = "#3b5bab"
PALE = "#e6f3f5"
GREY = "#64748b"


class Drawing:
    def __init__(self, width=1100, height=500, title="Teaching diagram"):
        self.width, self.height = width, height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">',
            f'<title>{escape(title)}</title>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>',
            f'<rect width="{width}" height="{height}" fill="white"/>',
        ]

    def text(self, x, y, label, size=26, fill=INK, anchor="start", weight="normal"):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(label))}</text>')
        return self

    def rect(self, x, y, w, h, fill=PALE, stroke=TEAL, radius=10):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        return self

    def line(self, x1, y1, x2, y2, stroke=GREY, width=3, dashed=False):
        dash = ' stroke-dasharray="10 8"' if dashed else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"{dash}/>')
        return self

    def arrow(self, x1, y1, x2, y2, stroke=TEAL, width=4):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" marker-end="url(#arrow)"/>')
        return self

    def circle(self, x, y, r, fill=TEAL, stroke="none"):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        return self

    def path(self, d, fill="none", stroke=TEAL, width=4):
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
        return self

    def file(self, x, y, label, fill="#eef2ff", width=170, height=150):
        self.path(f'M{x},{y} h{width - 30} l30,30 v{height - 30} h-{width} Z', fill=fill, stroke=BLUE, width=3)
        self.line(x + width - 30, y, x + width - 30, y + 30, BLUE)
        self.line(x + width - 30, y + 30, x + width, y + 30, BLUE)
        self.text(x + width / 2, y + height + 35, label, size=23, anchor="middle")
        return self

    def folder(self, x, y, label, width=220, height=100):
        self.path(f'M{x},{y+20} v-20 h{width*0.4} l20,20 h{width*0.6-20} v{height-20} h-{width} Z', fill="#fff2cc", stroke="#9a7820", width=3)
        self.text(x + width / 2, y + height / 2 + 18, label, size=24, anchor="middle")
        return self

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.parts + ["</svg>"]), encoding="utf-8")
        return path
