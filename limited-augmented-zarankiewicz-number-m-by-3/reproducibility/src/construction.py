"""Explicit extremal construction attaining z_L(m,3) = floor((3m+4)/2), m >= 3.

Rows 1,2,3 are the special rows S_1,S_2,S_3 (S_t misses column t).
N = m-3 singleton rows.  Write N = 2h + e with e in {0,1}.
  * h "colour-3" rows R_1..R_h with 1-edge (R_t,3) and half (R_t,2);
  * h "colour-1" rows P_1..P_h with 1-edge (P_t,1) and half (P_t,3);
    2-edge  (R_t,2 ; P_t,3)  for t = 1..h;
  * if e = 1, one more colour-1 row U with 1-edge (U,1) and the 2-edge
    (S_3,3 ; U,2)  using the free cell Q_3 = (S_3,3) of the special row S_3.
Total 2-edges: h + e = floor((m-2)/2).

Running this file checks the construction with the literal checker
zl_core.violations for every m in a range and prints the m = 14 instance.
"""
import sys

from zl_core import violations


def construction(m):
    assert m >= 3
    E1 = {(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)}
    E2 = []
    N = m - 3
    h, e = divmod(N, 2)
    row = 3
    for _ in range(h):
        R, P = row + 1, row + 2
        row += 2
        E1 |= {(R, 3), (P, 1)}
        E2.append(((R, 2), (P, 3)))
    if e:
        U = row + 1
        row += 1
        E1.add((U, 1))
        E2.append(((3, 3), (U, 2)))
    assert row == m
    return E1, E2


def table(m, E1, E2):
    """ASCII picture: '#' 1-edge, letters = halves of the same 2-edge, '.' empty."""
    g = {}
    for t, (u, v) in enumerate(E2):
        g[u] = g[v] = chr(ord("A") + t)
    lines = []
    for r in range(1, m + 1):
        lines.append(f"{r:>3} " + " ".join("#" if (r, c) in E1 else g.get((r, c), ".") for c in (1, 2, 3)))
    return "\n".join(lines)


def main():
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    for m in range(3, hi + 1):
        E1, E2 = construction(m)
        bad = violations(m, E1, E2)
        assert not bad, (m, bad)
        assert len(E1) + len(E2) == (3 * m + 4) // 2
    print(f"construction admissible with |E1|+|E2| = floor((3m+4)/2) for all 3 <= m <= {hi}")
    E1, E2 = construction(14)
    print("m = 14:  |E1| =", len(E1), " |E2| =", len(E2), " total =", len(E1) + len(E2))
    print("E2 =", E2)
    print(table(14, E1, E2))


if __name__ == "__main__":
    main()
