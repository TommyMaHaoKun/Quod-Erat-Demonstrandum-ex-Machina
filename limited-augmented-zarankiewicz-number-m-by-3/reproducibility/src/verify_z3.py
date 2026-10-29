"""Method B (independent): SAT / pseudo-Boolean encoding solved with z3.

This file deliberately shares no code with search_dfs.py or zl_core.py.  It
re-derives the extremal bases, encodes Definition 1 of Qi-Cui-Xu directly as
Boolean constraints, and asks z3 whether at least `s` 2-edges can be placed.

Variables: x[P] for every unordered pair P of free cells (no pre-filtering).
  occ(c) = True              if c is a 1-edge
         = OR_{P containing c} x[P]   otherwise
  (S):  at most one chosen pair contains any given free cell.
  Cond 2: x[P] -> not(occ(opp1) and occ(opp2))   for nondegenerate P.
  Cond 3: x[P] -> not(all occ(five cells))        for every admissible (k,l).
  sum x[P] >= s.

Usage: python verify_z3.py M S     -> checks every base type of M x 3 for >= S 2-edges
"""
import sys
import time
from itertools import combinations

import z3


def extremal_bases(m):
    """All extremal C4-free bases of [m]x[3] up to row/column permutation:
    special rows 1..3 with supports {2,3},{1,3},{1,2}; then singleton rows
    with column multiplicities (a,b,c), a>=b>=c, a+b+c=m-3."""
    out = []
    N = m - 3
    for a in range(N + 1):
        for b in range(a + 1):
            c = N - a - b
            if 0 <= c <= b:
                E1 = {(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)}
                row = 3
                for col, k in ((1, a), (2, b), (3, c)):
                    for _ in range(k):
                        row += 1
                        E1.add((row, col))
                out.append(((a, b, c), E1))
    return out


def feasible(m, E1, s, model_out=None):
    grid = [(r, c) for r in range(1, m + 1) for c in (1, 2, 3)]
    free = [g for g in grid if g not in E1]
    pairs = list(combinations(free, 2))
    x = {P: z3.Bool(f"x_{P[0][0]}_{P[0][1]}_{P[1][0]}_{P[1][1]}") for P in pairs}
    inc = {f: [] for f in free}
    for P in pairs:
        inc[P[0]].append(x[P])
        inc[P[1]].append(x[P])
    solver = z3.Solver()
    occ = {}
    for g in grid:
        if g in E1:
            occ[g] = z3.BoolVal(True)
        else:
            occ[g] = z3.Or(inc[g])
            solver.add(z3.AtMost(*inc[g], 1))
    for P in pairs:
        (i, j), (p, q) = P
        if i != p and j != q:
            solver.add(z3.Implies(x[P], z3.Not(z3.And(occ[(i, q)], occ[(p, j)]))))
        for (k, l) in grid:
            if k == i or k == p or l == j or l == q:
                continue
            five = {(k, l), (k, j), (k, q), (i, l), (p, l)}
            solver.add(z3.Implies(x[P], z3.Not(z3.And([occ[c] for c in five]))))
    solver.add(z3.AtLeast(*[x[P] for P in pairs], s))
    res = solver.check()
    if res == z3.sat and model_out is not None:
        mdl = solver.model()
        model_out.extend(P for P in pairs if z3.is_true(mdl.eval(x[P])))
    return res


def main():
    m, s = int(sys.argv[1]), int(sys.argv[2])
    any_sat = False
    for (abc, E1) in extremal_bases(m):
        t0 = time.time()
        ex = []
        r = feasible(m, E1, s, ex)
        any_sat |= (r == z3.sat)
        print(f"m={m} base={abc} s>={s}: {r} ({time.time()-t0:.1f}s) {ex if ex else ''}", flush=True)
    print(f"m={m}: some base admits >= {s} 2-edges: {any_sat}")


if __name__ == "__main__":
    main()
