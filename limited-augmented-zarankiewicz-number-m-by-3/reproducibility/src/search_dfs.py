"""Exact branch-and-bound search for the maximum number of 2-edges on a fixed base.

Method A (primary).  All conditions of Definition 1 are monotone in the set of
occupied cells, so a configuration is admissible iff no "witness" set of a
chosen 2-edge is fully occupied.  For each candidate 2-edge P we precompute its
witnesses:
  * Condition 2: {opposite cell 1, opposite cell 2}       (nondegenerate P)
  * Condition 3: {(k,l),(k,j),(k,q),(i,l),(p,l)}          (all valid (k,l))
The DFS decides free cells in a fixed order: the first undecided free cell is
either left empty (a buffer) or paired with a later undecided free cell.
Because the occupied set only grows along a branch, any witness already fully
occupied kills the branch (monotonicity).

Usage:  python search_dfs.py M            (all base types of M x 3)
"""
import sys
import time
from itertools import combinations

from zl_core import base_graph, base_types, cells


def build(m, E1):
    allc = cells(m)
    idx = {c: t for t, c in enumerate(allc)}
    E1mask = 0
    for c in E1:
        E1mask |= 1 << idx[c]
    free = [c for c in allc if c not in E1]
    cand = {}  # (f,g) index pair in free order -> (cellmask, [witness masks])
    for x, y in combinations(range(len(free)), 2):
        (i, j), (p, q) = free[x], free[y]
        wit = []
        if i != p and j != q:
            wit.append((1 << idx[(i, q)]) | (1 << idx[(p, j)]))
        for (k, l) in allc:
            if k in (i, p) or l in (j, q):
                continue
            w = 0
            for z in {(k, l), (k, j), (k, q), (i, l), (p, l)}:
                w |= 1 << idx[z]
            wit.append(w)
        pm = (1 << idx[free[x]]) | (1 << idx[free[y]])
        O = E1mask | pm
        if any((w & O) == w for w in wit):
            continue  # violates even with the pair alone
        cand[(x, y)] = (pm, wit)
    return free, E1mask, cand


def max_pairs(m, E1, target=None, want_example=True):
    """Return (best s, example list of pairs).  If target is given, stop as soon
    as a configuration with s >= target is found (existence query)."""
    free, E1mask, cand = build(m, E1)
    nf = len(free)
    partners = {x: [y for y in range(x + 1, nf) if (x, y) in cand] for x in range(nf)}
    best = [-1, None]
    nodes = [0]

    def ok(O, chosen):
        for (_, wit) in chosen:
            for w in wit:
                if (w & O) == w:
                    return False
        return True

    def dfs(pos, decided, O, chosen):
        nodes[0] += 1
        # advance to first undecided free cell
        while pos < nf and (decided >> pos) & 1:
            pos += 1
        s = len(chosen)
        undecided = nf - bin(decided).count("1")
        if s + undecided // 2 <= best[0]:
            return
        if target is not None and best[0] >= target:
            return
        if pos >= nf:
            if s > best[0]:
                best[0] = s
                best[1] = [(free[x], free[y]) for (x, y) in chosen_ids]
            return
        # option 1: pair pos with a later undecided cell
        for y in partners[pos]:
            if (decided >> y) & 1:
                continue
            pm, wit = cand[(pos, y)]
            O2 = O | pm
            new = chosen + [(pm, wit)]
            if ok(O2, new):
                chosen_ids.append((pos, y))
                dfs(pos + 1, decided | (1 << pos) | (1 << y), O2, new)
                chosen_ids.pop()
        # option 2: leave pos empty
        dfs(pos + 1, decided | (1 << pos), O, chosen)

    chosen_ids = []
    sys.setrecursionlimit(10000)
    dfs(0, 0, E1mask, [])
    return best[0], best[1], nodes[0]


def main():
    m = int(sys.argv[1])
    overall = -1
    for (a, b, c) in base_types(m):
        mm, E1 = base_graph(a, b, c)
        t0 = time.time()
        s, ex, nodes = max_pairs(mm, E1)
        overall = max(overall, s)
        print(f"m={m} base=({a},{b},{c}) max s={s} nodes={nodes} time={time.time()-t0:.1f}s example={ex}", flush=True)
    print(f"m={m}: max s = {overall}, z_L(m,3) = {m + 3 + overall}")


if __name__ == "__main__":
    main()
