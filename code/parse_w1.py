# ruff: noqa: E501, B007, B905
"""Parse Kollatsch's figures of the 257 letter squares (witness W1, Cod. Guelf. 47.13 Aug. 4°,
as edited, with his few conjectures; KCWorks doi:10.17613/3hfq-9a74, CC BY-NC-ND 4.0) into grids.

Input: the `pdftotext -bbox` HTML of the PDF (one word per letter, with coordinates).
Output: JSON {label: [[cell, ...], ...]} written to the private data folder only. The licence
forbids sharing adapted material, so the parsed squares never go into git; only counts,
hashes and coordinates do.

Usage: python -I parse_w1.py BBOX_HTML OUT_JSON
"""
import json
import re
import sys
from collections import defaultdict

WORD = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')


def cluster(vals, gap):
    """Sorted 1-D clusters: a new cluster starts where consecutive values differ by > gap."""
    vals = sorted(vals)
    out = [[vals[0]]]
    for v in vals[1:]:
        (out[-1].append(v) if v - out[-1][-1] <= gap else out.append([v]))
    return [sum(c) / len(c) for c in out]


def nearest(centres, v):
    return min(range(len(centres)), key=lambda i: abs(centres[i] - v))


def main():
    html, out = open(sys.argv[1], encoding="utf-8").read(), sys.argv[2]
    squares, problems = {}, []
    for page_no, page in enumerate(html.split("<page")[1:], start=1):
        words = [(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in WORD.findall(page)]
        heads = []
        for i, (x0, y0, x1, y1, w) in enumerate(words):
            if w == "Qu." and i + 1 < len(words) and re.fullmatch(r"\d+\.\d+", words[i + 1][4]):
                heads.append((x0, y0, words[i + 1][2], words[i + 1][4]))
        if not heads:
            continue
        letters = [(x0, y0, x1, y1, w) for x0, y0, x1, y1, w in words
                   if re.fullmatch(r"[A-Za-zÄÖÜäöüßſ]", w) and y0 > 280 or
                   (re.fullmatch(r"[A-Za-zÄÖÜäöüßſ]", w) and any(y0 > h[1] for h in heads))]
        groups = defaultdict(list)
        for x0, y0, x1, y1, w in letters:
            above = [h for h in heads if h[1] < y0]
            if not above:
                continue
            band = max(h[1] for h in above)
            cand = [h for h in above if abs(h[1] - band) < 20]
            xc = (x0 + x1) / 2
            h = min(cand, key=lambda h: abs((h[0] + h[2]) / 2 - xc))
            groups[h[3]].append((xc, (y0 + y1) / 2, w))
        for label, cells in groups.items():
            rows = cluster([c[1] for c in cells], 5)
            cols = cluster([c[0] for c in cells], 4)
            grid = [[None] * len(cols) for _ in rows]
            for xc, yc, w in cells:
                r, c = nearest(rows, yc), nearest(cols, xc)
                if grid[r][c] is not None:
                    problems.append((label, "collision", r, c))
                grid[r][c] = w
            n = len(rows)
            if len(cols) != n or any(v is None for row in grid for v in row):
                problems.append((label, f"shape {len(rows)}x{len(cols)}",
                                 sum(v is None for row in grid for v in row)))
            squares[label] = {"page": page_no, "grid": grid}
    json.dump(squares, open(out, "w"), ensure_ascii=False, indent=0)
    sizes = defaultdict(int)
    for s in squares.values():
        sizes[len(s["grid"])] += 1
    print("squares", len(squares), "sizes", dict(sorted(sizes.items())))
    print("problems", len(problems))
    for p in problems:
        print(" ", p)


if __name__ == "__main__":
    main()
