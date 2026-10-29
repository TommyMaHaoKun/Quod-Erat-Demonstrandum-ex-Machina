"""Fast end-to-end check of the package (a few minutes; no long searches).

1. Construction admissible with floor((3m+4)/2) edges, m = 3..120 (literal checker).
2. Exhaustive Lemma checks (base classification m<=6, unique full row m<=6).
3. Method A reproduces the published z_L(m,3), m = 3..12.
4. Method B (z3) agrees at m = 10 and m = 11.
5. Re-validates the stored certificates: every stored optimum / model is re-checked
   with the literal checker, the m = 14 DFS maximum is 6 on all 16 base types
   combined, and the z3 files are consistent with the DFS file.
Run from anywhere:  python src/check_package.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from zl_core import base_graph, base_types, violations  # noqa: E402

PUBLISHED = {3: 6, 4: 8, 5: 9, 6: 11, 7: 12, 8: 14, 9: 15, 10: 17, 11: 18, 12: 20, 13: 21}


def step(msg):
    print("==", msg, flush=True)


def main():
    from construction import construction
    step("1. construction")
    for m in range(3, 121):
        E1, E2 = construction(m)
        assert not violations(m, E1, E2) and len(E1) + len(E2) == (3 * m + 4) // 2
    print("ok: m = 3..120")

    step("2. exhaustive lemma checks (m <= 6)")
    subprocess.run([sys.executable, os.path.join(HERE, "verify_lemmas.py"), "6", "6"], check=True)

    step("3. Method A vs published values (m = 3..12)")
    from search_dfs import max_pairs
    for m in range(3, 13):
        best = max(max_pairs(*base_graph(*t))[0] for t in base_types(m))
        assert m + 3 + best == PUBLISHED[m] == (3 * m + 4) // 2, m
    print("ok")

    step("4. Method B (z3) at m = 10, 11")
    try:
        import z3  # noqa: F401
        from verify_z3 import extremal_bases, feasible
        for m in (10, 11):
            s = (m - 2) // 2
            assert any(str(feasible(m, E1, s)) == "sat" for _, E1 in extremal_bases(m))
            assert all(str(feasible(m, E1, s + 1)) == "unsat" for _, E1 in extremal_bases(m))
        print("ok")
    except ImportError:
        print("SKIPPED: z3-solver not installed")

    step("5. stored certificates")
    cdir = os.path.join(ROOT, "certificates")
    dfs = json.load(open(os.path.join(cdir, "dfs_m3_14.json"), encoding="utf-8"))
    for m, rec in dfs["results"].items():
        m = int(m)
        assert len(rec["bases"]) == len(base_types(m))
        for row in rec["bases"]:
            mm, E1 = base_graph(*row["base"])
            E2 = [tuple(map(tuple, e)) for e in row["optimal_E2"]]
            assert len(E2) == row["max_s"] and not violations(mm, E1, E2)
        assert rec["z_L"] == (3 * m + 4) // 2
        if m in PUBLISHED:
            assert rec["z_L"] == PUBLISHED[m]
    per_base14 = {tuple(r["base"]): r["max_s"] for r in dfs["results"]["14"]["bases"]}
    assert max(per_base14.values()) == 6 and len(per_base14) == 16
    print("dfs_m3_14.json ok (m = 3..14; m = 14 maximum 6)")
    for name, s in (("z3_m14_s6.json", 6), ("z3_m14_s7.json", 7)):
        p = os.path.join(cdir, name)
        if not os.path.exists(p):
            print(f"{name}: not present")
            continue
        z = json.load(open(p, encoding="utf-8"))
        for row in z["bases"]:
            t = tuple(sorted(row["base"], reverse=True))
            expect = "sat" if per_base14[t] >= s else "unsat"
            assert row["result"] == expect, (name, t, row["result"])
            if row["model_E2"]:
                _, E1 = base_graph(*t)
                E2 = [tuple(map(tuple, e)) for e in row["model_E2"]]
                assert len(E2) >= s and not violations(14, E1, E2)
        print(f"{name}: {len(z['bases'])}/16 base types, consistent with Method A"
              + ("" if z.get("complete") else "  (INCOMPLETE run)"))
    c = json.load(open(os.path.join(cdir, "construction.json"), encoding="utf-8"))
    E1 = set(map(tuple, c["m14"]["E1"]))
    E2 = [tuple(map(tuple, e)) for e in c["m14"]["E2"]]
    assert not violations(14, E1, E2) and len(E1) + len(E2) == 23
    print("construction.json ok (m = 14 total 23)")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
