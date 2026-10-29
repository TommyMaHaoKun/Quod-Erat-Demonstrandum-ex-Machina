"""Core definitions for the original (strong) limited augmented Zarankiewicz problem.

Cells are pairs (row, col) with rows 1..m and columns 1..n (here n = 3).
A 2-edge is an unordered pair of distinct cells.

The function `violations` is a literal transcription of Definition 1 of
Qi, Cui and Xu (Mathematics 14 (2026) 1552); it does not use any structure
theory and is used as the independent admissibility checker.
"""
from itertools import combinations


def cells(m, n=3):
    return [(r, c) for r in range(1, m + 1) for c in range(1, n + 1)]


def has_c4(E1):
    """Classical C4 among 1-edges: rows r<s, columns a<b with all four cells in E1."""
    E1 = set(E1)
    rows = sorted({r for r, _ in E1})
    cols = sorted({c for _, c in E1})
    for r, s in combinations(rows, 2):
        for a, b in combinations(cols, 2):
            if {(r, a), (r, b), (s, a), (s, b)} <= E1:
                return True
    return False


def zarankiewicz_m3(m):
    """z(m,3) = m+3 for m >= 3 (Culik); verified by brute force for small m in tests."""
    return m + 3


def violations(m, E1, E2, n=3, limited=True):
    """Return a list of human-readable reasons why (E1,E2) is NOT admissible.

    Empty list  <=>  the augmented graph is a limited augmented bipartite graph
    containing no generalized C4-cycle in the sense of Definition 1.
    """
    out = []
    E1 = set(E1)
    allc = set(cells(m, n))
    if not E1 <= allc:
        out.append("1-edge outside grid")
    halves = []
    for e in E2:
        u, v = tuple(e)
        if u == v:
            out.append(f"2-edge {e} has equal halves")
        if u not in allc or v not in allc:
            out.append(f"2-edge {e} outside grid")
        halves += [u, v]
    # (S) simplicity
    if len(set(halves)) != len(halves):
        out.append("(S) two 2-edges share a cell")
    if set(halves) & E1:
        out.append("(S) a 2-edge half is a 1-edge")
    if limited and len(E1) != zarankiewicz_m3(m):
        out.append(f"not limited: |E1|={len(E1)} != z(m,3)={zarankiewicz_m3(m)}")
    occ = E1 | set(halves)
    # Condition 1
    if has_c4(E1):
        out.append("Condition 1: classical C4 in E1")
    for e in E2:
        (i, j), (p, q) = tuple(e)
        # Condition 2 (nondegenerate only)
        if i != p and j != q:
            if (i, q) in occ and (p, j) in occ:
                out.append(f"Condition 2: 2-edge {(i, j)}-{(p, q)} has both opposite cells occupied")
        # Condition 3 (all types)
        for (k, l) in allc:
            if k in (i, p) or l in (j, q):
                continue
            five = [(k, l), (k, j), (k, q), (i, l), (p, l)]
            if i != p and j != q and len(set(five)) != 5:
                continue  # distinctness clause (automatic, kept for literalness)
            if all(x in occ for x in five):
                out.append(f"Condition 3: 2-edge {(i, j)}-{(p, q)} with cell {(k, l)}")
    return out


def is_admissible(m, E1, E2, n=3, limited=True):
    return not violations(m, E1, E2, n, limited)


# ---------------------------------------------------------------------------
# Extremal base graphs for n = 3
# ---------------------------------------------------------------------------

def base_graph(a, b, c):
    """Canonical extremal base with singleton multiplicities (a,b,c).

    Rows 1,2,3 are the special rows S_1,S_2,S_3 where S_t misses column t
    (S_1 = {2,3}, S_2 = {1,3}, S_3 = {1,2}); then a rows of colour 1,
    b rows of colour 2, c rows of colour 3.
    Returns (m, E1).
    """
    E1 = set()
    for t in (1, 2, 3):
        for col in (1, 2, 3):
            if col != t:
                E1.add((t, col))
    r = 3
    for colour, mult in ((1, a), (2, b), (3, c)):
        for _ in range(mult):
            r += 1
            E1.add((r, colour))
    return r, E1


def base_types(m):
    """Multisets {a,b,c} with a+b+c = m-3, listed as a >= b >= c >= 0."""
    N = m - 3
    res = []
    for a in range(N, -1, -1):
        for b in range(min(a, N - a), -1, -1):
            c = N - a - b
            if 0 <= c <= b:
                res.append((a, b, c))
    return res
