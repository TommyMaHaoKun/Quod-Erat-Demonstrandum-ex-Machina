"""Exact, dependency-free structural audit of the array polytope.

Run with Python 3.9+: python src/vertices.py
The proof does not rely on floating point or a polyhedral library.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json

POSITIONS = [(i, j, 4-i-j) for i in range(5) for j in range(5-i)
             if max(i, j, 4-i-j) < 4]
# Columns are (a,c,e,f,p,q); rows are POSITIONS.
B = [
    [1,0,0,0,2,1], [0,1,0,0,-3,-1], [0,0,1,0,1,0],
    [0,0,1,0,-1,-1], [0,0,0,1,3,1], [0,0,0,1,3,2],
    [1,0,0,0,0,0], [0,1,0,0,0,1], [0,0,0,1,0,0],
    [0,1,0,0,0,0], [1,0,0,0,1,0], [0,0,1,0,0,0],
]
ROOTS = [(1,0), (0,1), (1,1), (2,1), (3,1), (3,2)]
GROUPS = [((0,0),(1,0),(2,1)), ((0,0),(0,1),(-3,-1)),
          ((0,0),(1,0),(-1,-1)), ((0,0),(3,1),(3,2))]


def determinant(matrix):
    """Bareiss elimination with exact divisions and row pivoting."""
    a = [list(row) for row in matrix]
    n = len(a)
    previous, sign = 1, 1
    for k in range(n-1):
        pivot_row = next((r for r in range(k,n) if a[r][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = pivot*a[i][j] - a[i][k]*a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    r = 0
    for c in range(len(a[0]) if a else 0):
        pivot_row = next((i for i in range(r,len(a)) if a[i][c]), None)
        if pivot_row is None:
            continue
        a[r], a[pivot_row] = a[pivot_row], a[r]
        pivot = a[r][c]
        a[r] = [x/pivot for x in a[r]]
        for i in range(r+1,len(a)):
            scale = a[i][c]
            a[i] = [x-scale*y for x,y in zip(a[i],a[r])]
        r += 1
    return r


def audit():
    constraints = [[int(x[0] == level)-int(x[axis] == level)
                    for x in POSITIONS]
                   for level in range(5) for axis in (1,2)]
    assert rank(constraints) == 6
    assert all(sum(row[i]*B[i][j] for i in range(12)) == 0
               for row in constraints for j in range(6))
    # Integral left inverse recovers (a,c,e,f,p,q).
    selected = [6,9,11,8]
    inverse = [[int(i == index) for i in range(12)] for index in selected]
    inverse += [[int(i == 10)-int(i == 6) for i in range(12)],
                [int(i == 7)-int(i == 9) for i in range(12)]]
    assert [[sum(row[i]*B[i][j] for i in range(12)) for j in range(6)]
            for row in inverse] == [[int(i==j) for j in range(6)] for i in range(6)]
    assert all(sum(row[j]*Fraction(j < 4,2) for j in range(6)) == Fraction(1,2)
               for row in B)
    # Every within-group difference is a signed root.
    signed_roots = set(ROOTS) | {(-r,-s) for r,s in ROOTS}
    for group in GROUPS:
        assert all((a[0]-b[0],a[1]-b[1]) in signed_roots
                   for a,b in combinations(group,2))
    root_determinants = [abs(a*d-b*c) for (a,b),(c,d) in combinations(ROOTS,2)]
    assert set(root_determinants) == {1,2,3}
    # Exhaustive cross-check of the analytic two-dimensional argument.
    minors = Counter(abs(determinant([B[i] for i in rows]))
                     for rows in combinations(range(12),6))
    assert dict(minors) == {0:384,1:324,2:108,3:108}
    return {
        "constraint_rank": 6, "integral_left_inverse": True,
        "dimension": 6, "root_pair_absolute_determinants": root_determinants,
        "maximal_minor_histogram": dict(sorted(minors.items())),
        "proven_polytope_denominator_divides": 6,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
