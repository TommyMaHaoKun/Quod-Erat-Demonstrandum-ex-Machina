"""Exhaustive sanity checks of the structural statements for small m.

(1) Base classification: for 3 <= m <= MB, brute force over all subsets of
    [m]x[3] confirms z(m,3) = m+3 and that every C4-free (m+3)-set has exactly
    three degree-2 rows with supports {1,2},{1,3},{2,3} and m-3 degree-1 rows.
(2) Unique-full-row lemma: for 3 <= m <= ML, enumerate EVERY admissible
    limited configuration on EVERY extremal base (not just up to symmetry),
    using only the literal checker zl_core.violations, and confirm that at most
    one row has all three cells occupied; record the maximum |E2|.

These checks are corroboration only; the proofs in the paper are analytic.
Usage: python verify_lemmas.py [MB] [ML]
"""
import sys
from itertools import combinations

from zl_core import cells, has_c4, violations


def check_bases(m):
    allc = cells(m)
    best = 0
    extremal = []
    # z(m,3) <= m+3 is proved analytically; here confirm no C4-free (m+4)-set
    for size in (m + 3, m + 4):
        for S in combinations(allc, size):
            S = set(S)
            # quick C4 test by column-pair counting
            pairs = {}
            ok = True
            for r in range(1, m + 1):
                row = tuple(c for c in (1, 2, 3) if (r, c) in S)
                for pr in combinations(row, 2):
                    if pr in pairs:
                        ok = False
                        break
                    pairs[pr] = r
                if not ok:
                    break
            if not ok:
                continue
            assert not has_c4(S)
            best = max(best, size)
            if size == m + 3:
                extremal.append(S)
    assert best == m + 3, (m, best)
    for S in extremal:
        deg = [sum((r, c) in S for c in (1, 2, 3)) for r in range(1, m + 1)]
        assert sorted(deg) == [1] * (m - 3) + [2] * 3, (m, deg)
        sup = sorted(tuple(c for c in (1, 2, 3) if (r, c) in S) for r in range(1, m + 1) if deg[r - 1] == 2)
        assert sup == [(1, 2), (1, 3), (2, 3)]
    return len(extremal)


def all_configs(m, E1):
    """Yield every admissible E2 (as list of pairs) on base E1."""
    free = [c for c in cells(m) if c not in E1]

    def rec(pos, used, E2):
        while pos < len(free) and free[pos] in used:
            pos += 1
        if pos >= len(free):
            yield list(E2)
            return
        f = free[pos]
        for g in free[pos + 1:]:
            if g in used:
                continue
            E2.append((f, g))
            if not violations(m, E1, E2):  # hereditary: prune on first violation
                yield from rec(pos + 1, used | {f, g}, E2)
            E2.pop()
        yield from rec(pos + 1, used | {f}, E2)

    yield from rec(0, frozenset(), [])


def all_bases(m):
    """Every extremal base (all labelled ones), from the classification."""
    for rows in combinations(range(1, m + 1), 3):
        others = [r for r in range(1, m + 1) if r not in rows]
        from itertools import permutations, product
        for perm in permutations((1, 2, 3)):
            E1 = set()
            for r, miss in zip(rows, perm):
                E1 |= {(r, c) for c in (1, 2, 3) if c != miss}
            for cols in product((1, 2, 3), repeat=len(others)):
                yield E1 | {(r, c) for r, c in zip(others, cols)}


def main():
    MB = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    ML = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    for m in range(3, MB + 1):
        n = check_bases(m)
        print(f"m={m}: z(m,3)=m+3 confirmed; {n} labelled extremal bases, all of the classified form", flush=True)
    for m in range(3, ML + 1):
        nb = ncfg = 0
        smax = 0
        for E1 in all_bases(m):
            nb += 1
            occ1 = set(E1)
            for E2 in all_configs(m, E1):
                ncfg += 1
                occ = occ1 | {x for e in E2 for x in e}
                full = [r for r in range(1, m + 1) if all((r, c) in occ for c in (1, 2, 3))]
                assert len(full) <= 1, (m, sorted(E1), E2, full)
                smax = max(smax, len(E2))
        print(f"m={m}: {nb} labelled bases, {ncfg} admissible configurations, all with <= 1 full row; "
              f"max |E2| = {smax} (formula floor((m-2)/2) = {(m - 2) // 2})", flush=True)
        assert smax == (m - 2) // 2


if __name__ == "__main__":
    main()
