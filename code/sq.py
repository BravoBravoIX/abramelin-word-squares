# ruff: noqa: E501, B007, B905
"""Shared helpers for the Abramelin squares study: loading witnesses, normalisation (PREREG.md),
symmetries, matching. Grids are lists of rows; a cell is a one-letter string or None.

W1 (Kollatsch's squares, CC BY-NC-ND 4.0) is read from the private work folder that
code/run_all.sh fills from the fetched PDF; it is never written into this repository.
L and M are read from data/."""

import json
from pathlib import Path

SEED = 20261020
DATA = Path(__file__).resolve().parents[1] / "data"
SYMS = ["T", "A", "R2", "R1", "H", "V"]


def norm(c, fold=True):
    if c is None:
        return None
    c = c.strip().lower().replace("ſ", "s")
    if c in ("", "?", "_") or len(c) != 1 or not c.isalpha():
        return None
    if fold:
        c = {"j": "i", "v": "u"}.get(c, c)
    return c


def ngrid(grid, fold=True):
    return [[norm(c, fold) for c in row] for row in grid]


def square(grid):
    n = len(grid)
    return n > 0 and all(len(r) == n for r in grid)


def image(g, r, c, n):
    return {"T": (c, r), "A": (n - 1 - c, n - 1 - r), "R2": (n - 1 - r, n - 1 - c),
            "R1": (c, n - 1 - r), "H": (r, n - 1 - c), "V": (n - 1 - r, c)}[g]


def pairs(g, n):
    """Unordered cell pairs {x, g(x)} with x != g(x) (R1 gives 4-cycles: pairs of neighbours)."""
    seen, out = set(), []
    for r in range(n):
        for c in range(n):
            a, b = (r, c), image(g, r, c, n)
            if a != b and (b, a) not in seen and (a, b) not in seen:
                seen.add((a, b))
                out.append((a, b))
    return out


def load_w1(path, fold=True):
    d = json.load(open(path))
    return {k: ngrid(v["grid"], fold) for k, v in d.items()}


def load_m(fold=True):
    d = json.load(open(DATA / "m_squares.json"))
    return {k: ngrid(v["grid"], fold) for k, v in d.items() if square(v["grid"])}


def load_l(fold=True, path=None):
    """L squares in page order, with squares split over a page break joined: a square at the top
    of a page with no heading continues the previous page's last square when that one is short
    (fewer rows than columns) and the widths agree."""
    d = json.load(open(path or DATA / "L_read.json"))
    corr = DATA / "L_corrections.json"
    fixes = json.load(open(corr)) if corr.exists() else {}
    seq = []
    for page in sorted(d["pages"]):
        p = d["pages"][page]["parsed"]
        if not p:
            continue
        for i, s in enumerate(p["squares"]):
            rows = [list(r) for r in s["rows"]]
            if (i == 0 and seq and not s["heading"].strip() and rows
                    and len(seq[-1]["rows"]) < len(seq[-1]["rows"][0]) == len(rows[0])):
                seq[-1]["rows"] += rows
                seq[-1]["pages"].append(page)
                continue
            seq.append({"heading": s["heading"], "rows": rows, "pages": [page], "idx": i})
    out = {}
    for k, s in enumerate(seq, start=1):
        label = f"L{k:03d}"
        rows = s["rows"]
        for key, val in fixes.get(label, {}).items():  # "r,c": letter (eye-checked)
            r, c = map(int, key.split(","))
            rows[r][c] = val
        out[label] = {"grid": ngrid(rows, fold), "heading": s["heading"], "pages": s["pages"]}
    return out


def agreement(a, b):
    both = [(x, y) for ra, rb in zip(a, b, strict=False) for x, y in zip(ra, rb, strict=False) if x and y]
    return (sum(x == y for x, y in both) / len(both), len(both)) if both else (0.0, 0)


def match(X, Y, minimum=0.5):
    """One-to-one greedy matching of square grids X -> Y by size and same-orientation agreement."""
    cand = []
    for kx, gx in X.items():
        for ky, gy in Y.items():
            if len(gx) == len(gy) and square(gx) and square(gy):
                a, n = agreement(gx, gy)
                if a >= minimum and n >= len(gx):
                    cand.append((a, n, kx, ky))
    cand.sort(reverse=True)
    used_x, used_y, out = set(), set(), {}
    for a, n, kx, ky in cand:
        if kx not in used_x and ky not in used_y:
            out[kx] = (ky, a)
            used_x.add(kx)
            used_y.add(ky)
    return out
