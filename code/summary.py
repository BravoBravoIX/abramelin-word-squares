# ruff: noqa: E501
"""Print a compact summary of results/{census,slips,shared}<TAG>.json (numbers for the README).

Usage: python -I summary.py RESULTS_DIR [TAG]   (TAG: "", "_nofold", "_foldit")
"""
import json
import sys
from pathlib import Path

res, tag = Path(sys.argv[1]), (sys.argv[2] if len(sys.argv) > 2 else "")
c = json.load(open(res / f"census{tag}.json"))
print("matches", c["matches"], "fold_i_t_post_hoc", c.get("fold_i_t_post_hoc"))
for w, v in c["census"].items():
    print(w, "squares", v["squares"], "any symmetry", v["with_any_symmetry"], "by", v["by_symmetry"],
          "controls with any", v["control_with_any_symmetry"], "of", v["control_permutations"])
    print("   combos", v["combinations"])
d = json.load(open(res / f"slips{tag}.json"))
for k, t in d["tests"].items():
    b1, b2, b3 = t["B1"], t["B2"], t["B3"]
    p2 = None if b2["p"] is None else f"{b2['p']:.2e}"
    print(f"{k:6} B1 slips {b1['predicted_slips']} differ {b1['held_out_differs']} ({b1['rate'] or 0:.2f}) "
          f"vs control {b1['control_differs']}/{b1['control_cells']} ({b1['control_rate'] or 0:.3f}) "
          f"p={b1['p']:.2e} holm={b1.get('p_holm')} | B2 symmetric reading {b2['held_out_has_symmetric_reading']} "
          f"expected {b2['expected_by_chance']:.2f} p={p2} | B3 {b3['held_out_symmetric']}/{b3['two_cell_breaks']} "
          f"chance {b3['chance_expected']:.1f}, control {b3['control_symmetric']}/{b3['control_two_cell_orbits']} | "
          f"precision {t['precision']} recall {t['recall']} of {t['differences_in_symmetric_squares']}")
s = json.load(open(res / f"shared{tag}.json"))["shared"]
print("C triples", s["triples_matched"], "used", s["triples_used"], "slips", s["slips"])
for k, v in s["pairs"].items():
    print("  ", k, "shared", v["shared"], "expected", round(v["expected"], 2), "p", v["p"], "holm", v["p_holm"])
