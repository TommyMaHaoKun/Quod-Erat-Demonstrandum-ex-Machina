"""Regenerate the computational certificates in ../certificates/.

  python make_certificates.py dfs M_LO M_HI   exhaustive DFS (Method A) per base type
  python make_certificates.py z3 M S          z3 feasibility of >= S 2-edges (Method B)
  python make_certificates.py construction    explicit family, m = 3..200

Every reported optimum is re-checked with the literal checker zl_core.violations.
Paths are relative to this file, so the package can be moved anywhere.
"""
import json
import os
import platform
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, "..", "certificates")
sys.path.insert(0, HERE)

from zl_core import base_graph, base_types, violations  # noqa: E402

PUBLISHED = {3: 6, 4: 8, 5: 9, 6: 11, 7: 12, 8: 14, 9: 15, 10: 17, 11: 18, 12: 20, 13: 21}


def dump(name, obj):
    os.makedirs(CERT, exist_ok=True)
    with open(os.path.join(CERT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)


def run_dfs(lo, hi):
    from search_dfs import max_pairs
    out = {"method": "A: exhaustive branch-and-bound over all 2-edge sets (search_dfs.py)",
           "python": platform.python_version(), "results": {}}
    for m in range(lo, hi + 1):
        rows = []
        best = -1
        for t in base_types(m):
            mm, E1 = base_graph(*t)
            t0 = time.time()
            s, ex, nodes = max_pairs(mm, E1)
            assert not violations(mm, E1, ex), (m, t)
            rows.append({"base": t, "max_s": s, "nodes": nodes, "seconds": round(time.time() - t0, 1),
                         "optimal_E2": ex})
            best = max(best, s)
            print(m, t, s, nodes, flush=True)
        zl = m + 3 + best
        out["results"][m] = {"bases": rows, "max_s": best, "z_L": zl,
                             "formula_floor_(3m+4)/2": (3 * m + 4) // 2,
                             "published_value": PUBLISHED.get(m)}
        assert zl == (3 * m + 4) // 2
        if m in PUBLISHED:
            assert zl == PUBLISHED[m]
        dump(f"dfs_m{lo}_{hi}.json", out)


def _z3_job(args):
    m, s, abc, E1 = args
    from verify_z3 import feasible
    t0 = time.time()
    ex = []
    r = feasible(m, E1, s, ex)
    if ex:
        assert not violations(m, E1, ex)
    return {"base": abc, "result": str(r), "seconds": round(time.time() - t0, 1), "model_E2": ex}


def run_z3(m, s, workers=8):
    import multiprocessing as mp
    import z3
    from verify_z3 import extremal_bases
    out = {"method": "B: independent z3 encoding (verify_z3.py)", "z3": z3.get_version_string(),
           "m": m, "s_at_least": s, "bases": []}
    jobs = [(m, s, abc, E1) for abc, E1 in extremal_bases(m)]
    with mp.Pool(workers) as pool:
        for row in pool.imap_unordered(_z3_job, jobs):
            out["bases"].append(row)
            print(m, row["base"], row["result"], row["seconds"], flush=True)
            dump(f"z3_m{m}_s{s}.json", out)
    out["complete"] = len(out["bases"]) == len(jobs)
    out["any_sat"] = any(r["result"] == "sat" for r in out["bases"])
    dump(f"z3_m{m}_s{s}.json", out)


def run_construction():
    from construction import construction
    res = {}
    for m in range(3, 201):
        E1, E2 = construction(m)
        assert not violations(m, E1, E2)
        res[m] = len(E1) + len(E2)
        assert res[m] == (3 * m + 4) // 2
    E1, E2 = construction(14)
    dump("construction.json", {"checked_m": [3, 200], "total_edges": res,
                               "m14": {"E1": sorted(E1), "E2": E2, "total": len(E1) + len(E2)}})
    print("construction verified for m = 3..200")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "dfs":
        run_dfs(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "z3":
        run_z3(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "construction":
        run_construction()
