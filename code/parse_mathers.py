# ruff: noqa: E501, B007, B905
"""Parse the letter squares of Mathers's Book III (witness M: 1900 second edition, as typeset in
the 1999 digital edition on archive.org `sacred-magic-abramelin`, Public Domain Mark).

Input: `pdftotext -bbox` HTML of Abramelin_3.pdf (one word per letter, with coordinates).
Squares sit under numbered headers "(n)"; chapter titles ("THE FIRST CHAPTER.") set the chapter.
Cells are placed on a lattice from the letter pitch, so blank cells (Mathers left many squares
partly empty) stay blank (None).

Usage: python -I parse_mathers.py BBOX_HTML OUT_JSON
"""
import json
import re
import statistics
import sys
from collections import defaultdict

WORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
ORD = ["FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH", "EIGHTH", "NINTH",
       "TENTH", "ELEVENTH", "TWELFTH", "THIRTEENTH", "FOURTEENTH", "FIFTEENTH", "SIXTEENTH",
       "SEVENTEENTH", "EIGHTEENTH", "NINETEENTH", "TWENTIETH"]


def main():
    html, out = open(sys.argv[1], encoding="utf-8").read(), sys.argv[2]
    chapter, squares = 0, {}
    for page_no, page in enumerate(html.split("<page")[1:], start=1):
        words = [(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in WORD.findall(page)]
        # chapter titles: "THE <ORD> CHAPTER."
        events = []
        for i in range(len(words) - 2):
            if words[i][4] == "THE" and words[i + 1][4] in ORD and words[i + 2][4].startswith("CHAPTER"):
                events.append((words[i][1], ORD.index(words[i + 1][4]) + 1))
        heads = [(x0, y0, x1, int(w[1:-1])) for x0, y0, x1, y1, w in words
                 if re.fullmatch(r"\(\d+\)", w)]
        lines = defaultdict(list)
        for x0, y0, _x1, _y1, w in words:
            lines[round(y0 / 3)].append(w)
        prose = {k for k, ws in lines.items() if any(len(w) > 1 and not re.fullmatch(r"\(\d+\)", w)
                                                     for w in ws)}
        letters = [((x0 + x1) / 2, (y0 + y1) / 2, w) for x0, y0, x1, y1, w in words
                   if re.fullmatch(r"[A-Z]", w) and round(y0 / 3) not in prose]
        groups = defaultdict(list)
        for xc, yc, w in letters:
            above = [h for h in heads if h[1] < yc and yc - h[1] < 260]
            if not above:
                continue
            band = max(h[1] for h in above)
            cand = [h for h in above if abs(h[1] - band) < 25]
            h = min(cand, key=lambda h: abs((h[0] + h[2]) / 2 - xc))
            groups[(h[1], h[3])].append((xc, yc, w))
        for (hy, num), cells in sorted(groups.items()):
            ch = chapter
            for ey, c in events:
                if ey < hy:
                    ch = c
            xs = sorted(c[0] for c in cells)
            ys = sorted({round(c[1]) for c in cells})
            dy = [b - a for a, b in zip(ys, ys[1:], strict=False) if b - a > 6]
            pitch_y = statistics.median(dy) if dy else 18.0
            dx = []
            rowmap = defaultdict(list)
            for xc, yc, w in cells:
                rowmap[round((yc - min(c[1] for c in cells)) / pitch_y)].append(xc)
            for xr in rowmap.values():
                xr.sort()
                dx += [b - a for a, b in zip(xr, xr[1:], strict=False) if b - a > 6]
            pitch_x = min(statistics.median(dx), pitch_y * 1.5) if dx else pitch_y
            x0, y0 = xs[0], min(c[1] for c in cells)
            idx = [(round((yc - y0) / pitch_y), round((xc - x0) / pitch_x), w) for xc, yc, w in cells]
            n = max(max(r for r, _, _ in idx), max(c for _, c, _ in idx)) + 1
            grid = [[None] * n for _ in range(n)]
            clash = 0
            for r, c, w in idx:
                clash += grid[r][c] is not None
                grid[r][c] = w
            label = f"{ch}.{num}"
            while label in squares:
                label += "b"
            squares[label] = {"page": page_no, "grid": grid, "clashes": clash,
                              "filled": sum(v is not None for row in grid for v in row)}
        if events:
            chapter = events[-1][1]
    json.dump(squares, open(out, "w"), ensure_ascii=False, indent=0)
    sizes = defaultdict(int)
    for s in squares.values():
        sizes[len(s["grid"])] += 1
    full = sum(s["filled"] == len(s["grid"]) ** 2 for s in squares.values())
    print("squares", len(squares), "full", full, "sizes", dict(sorted(sizes.items())),
          "clashes", sum(s["clashes"] for s in squares.values()))


if __name__ == "__main__":
    main()
