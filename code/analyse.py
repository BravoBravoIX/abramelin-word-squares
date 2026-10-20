# ruff: noqa: E501, B007, B905
"""Tests A (symmetry census), B (held-out slip location) and C (shared slips) of PREREG.md v1.0.

Writes results/census.json, results/slips.json, results/shared.json and prints a summary.
W1 letters are never written out (CC BY-NC-ND); results carry labels, coordinates, counts and
L/M letters only.

Usage: nice -n 19 python analyse.py W1_SQUARES_JSON [--nofold] [--fold-it]
  W1_SQUARES_JSON: Kollatsch's squares as parsed by parse_w1.py into the git-ignored work/ folder.
The results files hold no machine- or time-dependent fields; the original run's code commit is
recorded in results/run_records.json.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import binom, fisher_exact

sys.path.insert(0, str(Path(__file__).parent))
from sq import SEED, SYMS, image, load_l, load_m, load_w1, match, pairs  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
FOLD = "--nofold" not in sys.argv
FOLD_IT = "--fold-it" in sys.argv  # POST HOC, not pre-registered: L's scribe writes I and T alike
TAG = ("" if FOLD else "_nofold") + ("_foldit" if FOLD_IT else "")
P_BAR, A_BAR = 0.05 / (6 * 260), 0.85


def letters(g):
    return [x for row in g for x in row if x]


def collision(g):
    cnt = Counter(letters(g))
    tot = sum(cnt.values())
    return sum((v / tot) ** 2 for v in cnt.values()) if tot else 1.0


def sym_scores(g):
    n, q = len(g), collision(g)
    out = {}
    for s in SYMS:
        both = [(g[a[0]][a[1]], g[b[0]][b[1]]) for a, b in pairs(s, n)]
        both = [(x, y) for x, y in both if x and y]
        k = sum(x == y for x, y in both)
        N = len(both)
        p = float(binom.sf(k - 1, N, q)) if N else 1.0
        out[s] = {"agree": k / N if N else 0.0, "pairs": N, "p": p,
                  "has": bool(N and k / N >= A_BAR and p < P_BAR), "exact": bool(N and k == N)}
    return out


def census(W, name, rng, n_perm=1000):
    per, combos, _ctrl_any = {}, Counter(), 0
    for i, (k, g) in enumerate(sorted(W.items())):
        sc = sym_scores(g)
        has = tuple(s for s in SYMS if sc[s]["has"])
        per[k] = {"n": len(g), "syms": list(has), "exact": [s for s in SYMS if sc[s]["exact"]],
                  "agree": {s: round(sc[s]["agree"], 3) for s in SYMS}}
        combos["+".join(has) or "none"] += 1
    # permutation controls (same rule)
    ctrl_hits = 0
    ctrl_total = 0
    for i, (k, g) in enumerate(sorted(W.items())):
        r = np.random.default_rng(SEED + i)
        cells = [(a, b) for a in range(len(g)) for b in range(len(g))]
        vals = [g[a][b] for a, b in cells]
        for _ in range(n_perm):
            perm = r.permutation(len(vals))
            h = [[None] * len(g) for _ in g]
            for (a, b), j in zip(cells, perm, strict=False):
                h[a][b] = vals[j]
            ctrl_total += 1
            ctrl_hits += any(v["has"] for v in sym_scores(h).values())
    by_sym = {s: sum(s in v["syms"] for v in per.values()) for s in SYMS}
    return {"witness": name, "squares": len(W), "with_any_symmetry": sum(bool(v["syms"]) for v in per.values()),
            "by_symmetry": by_sym, "combinations": dict(combos.most_common()),
            "exact_any": sum(bool(v["exact"]) for v in per.values()),
            "control_permutations": ctrl_total, "control_with_any_symmetry": ctrl_hits,
            "per_square": per}


def orbits(n, syms):
    parent = {(r, c): (r, c) for r in range(n) for c in range(n)}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for s in syms:
        for r in range(n):
            for c in range(n):
                a, b = find((r, c)), find(image(s, r, c, n))
                if a != b:
                    parent[a] = b
    groups = defaultdict(list)
    for x in parent:
        groups[find(x)].append(x)
    return [sorted(v) for v in groups.values() if len(v) > 1]


def poibin_sf(k, ps):
    """P(sum of Bernoulli(ps) >= k), exact by convolution."""
    dist = np.array([1.0])
    for p in ps:
        dist = np.convolve(dist, [1 - p, p])
    return float(dist[k:].sum())


def test_b(X, Y, cen, mp, xname, yname):
    slip_diff = slip_n = ctrl_diff = ctrl_n = 0
    rep_hit, rep_ps, items = 0, [], []
    un_sym = un_n = ctl2_sym = ctl2_n = 0
    rnd_p = []
    diff_in_sym = diff_in_broken = 0
    for kx, (ky, _) in mp.items():
        syms = cen["per_square"][kx]["syms"]
        if not syms:
            continue
        gx, gy = X[kx], Y[ky]
        n = len(gx)
        ycnt = Counter(letters(gy))
        ytot = sum(ycnt.values())
        broken_cells = set()
        for orb in orbits(n, syms):
            vals = [gx[r][c] for r, c in orb]
            present = [v for v in vals if v]
            if len(present) < 2:
                continue
            if len(set(present)) == 1:
                for r, c in orb:
                    if gx[r][c] and gy[r][c]:
                        ctrl_n += 1
                        ctrl_diff += gx[r][c] != gy[r][c]
                if len(orb) == 2 and all(gy[r][c] for r, c in orb):
                    ctl2_n += 1
                    ctl2_sym += gy[orb[0][0]][orb[0][1]] == gy[orb[1][0]][orb[1][1]]
                continue
            broken_cells.update(orb)
            cnt = Counter(present).most_common()
            if len(orb) == 2:
                if all(gy[r][c] for r, c in orb):
                    un_n += 1
                    un_sym += gy[orb[0][0]][orb[0][1]] == gy[orb[1][0]][orb[1][1]]
                    rnd_p.append(collision(gy))
                continue
            if len(cnt) > 1 and cnt[0][1] == cnt[1][1]:
                continue  # no strict majority: located, unresolved
            m = cnt[0][0]
            for r, c in orb:
                if gx[r][c] and gx[r][c] != m and gy[r][c]:
                    slip_n += 1
                    d = gy[r][c] != gx[r][c]
                    slip_diff += d
                    hit = gy[r][c] == m
                    if d:
                        rep_hit += hit
                        rep_ps.append(ycnt[m] / ytot if ytot else 0)
                    items.append({"x": kx, "y": ky, "cell": [r, c], "y_letter": gy[r][c] if yname != "W1" else None,
                                  "x_letter": gx[r][c] if xname != "W1" else None,
                                  "y_differs": d, "y_is_symmetric_reading": hit})
        for r in range(n):
            for c in range(n):
                if gx[r][c] and gy[r][c] and gx[r][c] != gy[r][c]:
                    diff_in_sym += 1
                    diff_in_broken += (r, c) in broken_cells
    fe = fisher_exact([[slip_diff, slip_n - slip_diff], [ctrl_diff, ctrl_n - ctrl_diff]],
                      alternative="greater") if slip_n and ctrl_n else None
    return {"source": xname, "held_out": yname, "matched_squares": len(mp),
            "B1": {"predicted_slips": slip_n, "held_out_differs": slip_diff,
                   "rate": slip_diff / slip_n if slip_n else None,
                   "control_cells": ctrl_n, "control_differs": ctrl_diff,
                   "control_rate": ctrl_diff / ctrl_n if ctrl_n else None,
                   "odds_ratio": float(fe[0]) if fe else None, "p": float(fe[1]) if fe else None},
            "B2": {"differs": slip_diff, "held_out_has_symmetric_reading": rep_hit,
                   "expected_by_chance": float(sum(rep_ps)),
                   "p": poibin_sf(rep_hit, rep_ps) if rep_ps else None},
            "B3": {"two_cell_breaks": un_n, "held_out_symmetric": un_sym,
                   "control_two_cell_orbits": ctl2_n, "control_symmetric": ctl2_sym,
                   "chance_expected": float(sum(rnd_p))},
            "precision": rep_hit / slip_n if slip_n else None,
            "recall": diff_in_broken / diff_in_sym if diff_in_sym else None,
            "differences_in_symmetric_squares": diff_in_sym, "items": items}


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i] if ps[i] is not None else 2)
    adj, run = [None] * len(ps), 0.0
    for rank, i in enumerate(order):
        if ps[i] is None:
            continue
        run = max(run, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = run
    return adj


def test_c(W1, L, M, cens, m_wl, m_wm, n_perm=10000):
    trip = [(k, m_wl[k][0], m_wm[k][0]) for k in m_wl if k in m_wm]
    rng = np.random.default_rng(SEED)
    names = ["W1", "L", "M"]
    obs = Counter()
    perm = np.zeros((n_perm, 3))
    slips_total = Counter()
    used = 0
    for kw, kl, km in trip:
        sets = [cens["W1"]["per_square"][kw]["syms"], cens["L"]["per_square"][kl]["syms"],
                cens["M"]["per_square"].get(km, {}).get("syms", [])]
        syms = [s for s in SYMS if sum(s in st for st in sets) >= 2]
        if not syms:
            continue
        gs = [W1[kw], L[kl], M[km]]
        n = len(gs[0])
        eligible, slips = [], [dict(), dict(), dict()]
        for orb in orbits(n, syms):
            allv = [g[r][c] for g in gs for r, c in orb if g[r][c]]
            cnt = Counter(allv).most_common()
            if not cnt or (len(cnt) > 1 and cnt[0][1] == cnt[1][1]):
                continue
            ref = cnt[0][0]
            for r, c in orb:
                eligible.append((r, c))
                for w, g in enumerate(gs):
                    if g[r][c] and g[r][c] != ref:
                        slips[w][(r, c)] = g[r][c]
        if not eligible:
            continue
        used += 1
        for w in range(3):
            slips_total[names[w]] += len(slips[w])
        pairs_ = [(0, 1), (0, 2), (1, 2)]
        for j, (a, b) in enumerate(pairs_):
            obs[j] += sum(1 for cell, x in slips[a].items() if slips[b].get(cell) == x)
        # permutation: move each witness's slips to random eligible cells (keep letters)
        E = len(eligible)
        sl = [list(s.values()) for s in slips]
        for t in range(n_perm):
            maps = [dict(zip(rng.choice(E, size=len(s), replace=False).tolist(), s, strict=False)) for s in sl]
            for j, (a, b) in enumerate(pairs_):
                perm[t, j] += sum(1 for cell, x in maps[a].items() if maps[b].get(cell) == x)
    res = {"triples_matched": len(trip), "triples_used": used, "slips": dict(slips_total), "pairs": {}}
    ps = []
    for j, (a, b) in enumerate([(0, 1), (0, 2), (1, 2)]):
        p = float((1 + (perm[:, j] >= obs[j]).sum()) / (n_perm + 1))
        ps.append(p)
        res["pairs"][f"{names[a]}-{names[b]}"] = {"shared": obs[j], "expected": float(perm[:, j].mean()),
                                                  "p": p}
    for (_k, v), a in zip(res["pairs"].items(), holm(ps), strict=False):
        v["p_holm"] = a
    return res


def main():
    W1, L, M = load_w1(sys.argv[1], FOLD), {k: v["grid"] for k, v in load_l(FOLD).items()}, load_m(FOLD)
    L = {k: g for k, g in L.items() if g and all(len(r) == len(g) for r in g)}
    if FOLD_IT:
        W1, L, M = ({k: [[("i" if x == "t" else x) for x in row] for row in g] for k, g in W.items()}
                    for W in (W1, L, M))
    rng = np.random.default_rng(SEED)
    cens = {name: census(W, name, rng) for name, W in (("W1", W1), ("L", L), ("M", M))}
    m_wl, m_wm = match(W1, L), match(W1, M)
    m_lw = {v[0]: (k, v[1]) for k, v in m_wl.items()}
    m_mw = {v[0]: (k, v[1]) for k, v in m_wm.items()}
    m_lm = match(L, M)
    m_ml = {v[0]: (k, v[1]) for k, v in m_lm.items()}
    tests = {
        "W1->L": test_b(W1, L, cens["W1"], m_wl, "W1", "L"),
        "L->W1": test_b(L, W1, cens["L"], m_lw, "L", "W1"),
        "L->M": test_b(L, M, cens["L"], m_lm, "L", "M"),
        "M->L": test_b(M, L, cens["M"], m_ml, "M", "L"),
        "W1->M": test_b(W1, M, cens["W1"], m_wm, "W1", "M"),
        "M->W1": test_b(M, W1, cens["M"], m_mw, "M", "W1"),
    }
    main4 = ["W1->L", "L->W1", "L->M", "M->L"]
    for k, a in zip(main4, holm([tests[k]["B1"]["p"] for k in main4]), strict=False):
        tests[k]["B1"]["p_holm"] = a
    shared = test_c(W1, L, M, cens, m_wl, m_wm)
    meta = {"prereg": "PREREG.md v1.0", "seed": SEED, "fold_i_j_u_v": FOLD,
            "fold_i_t_post_hoc": FOLD_IT,
            "matches": {"W1-L": len(m_wl), "W1-M": len(m_wm), "L-M": len(m_lm)},
            "unmatched_W1_vs_L": sorted(set(W1) - set(m_wl)),
            "unmatched_L_vs_W1": sorted(set(L) - set(m_lw))}
    res = HERE / "results"
    res.mkdir(exist_ok=True)
    json.dump({**meta, "census": {k: {kk: vv for kk, vv in v.items() if kk != "per_square"}
                                  for k, v in cens.items()},
               "per_square": {k: v["per_square"] for k, v in cens.items() if k != "W1"},
               "per_square_W1_symmetries": {k: v["syms"] for k, v in cens["W1"]["per_square"].items()}},
              open(res / f"census{TAG}.json", "w"), indent=1, ensure_ascii=False)
    json.dump({**meta, "tests": tests}, open(res / f"slips{TAG}.json", "w"), indent=1, ensure_ascii=False)
    json.dump({**meta, "shared": shared}, open(res / f"shared{TAG}.json", "w"), indent=1)
    print(json.dumps(meta["matches"]))
    for k, v in cens.items():
        print(k, {kk: vv for kk, vv in v.items() if kk not in ("per_square", "combinations")})
        print("   combos", v["combinations"])
    for k, t in tests.items():
        print(k, "B1", {kk: t["B1"][kk] for kk in t["B1"]}, "\n    B2", t["B2"], "\n    B3", t["B3"],
              "\n    precision", t["precision"], "recall", t["recall"])
    print("C", json.dumps(shared, indent=1))


if __name__ == "__main__":
    main()
