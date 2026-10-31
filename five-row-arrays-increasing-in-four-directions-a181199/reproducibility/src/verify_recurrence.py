"""The nested sum of Kauers--Koutschan satisfies the order-3 OEIS recurrence.

Let p_0,...,p_3 be the coefficients of a(n),...,a(n+3) in the recurrence
recorded in OEIS A181199 (data/oeis_recurrence.json).  If a(n+1)-a(n) =
U(n) S(n) with S(n+1) = S(n) + V(n), then for every n >= 1

  sum_j p_j a(n+j) = (sum_j p_j) a(n) + S(n) * X(n) + Y(n),

  X = Q1 U(n) + Q2 U(n+1) + Q3 U(n+2),
  Y = Q2 U(n+1) V(n) + Q3 U(n+2) (V(n) + V(n+1)),   Q_i = p_i + ... + p_3.

We check exactly that sum_j p_j = 0, X/U(n) = 0 and Y/(U(n) V(n)) = 0 as
rational functions of n, and that p_3(n) has no zero at an integer n >= 1,
so the recurrence (with a(1), a(2), a(3)) determines the sequence.
"""
import json
import os
import sympy as sp
from common import DATA, load_bfile, a_nested

n = sp.symbols("n")


def rf(x, m):
    return sp.prod([x + i for i in range(m)])


q8 = lambda t: (25216*t**8 + 9888*t**7 - 14496*t**6 + 11208*t**5 + 23832*t**4
                + 7383*t**3 - 1522*t**2 - 939*t - 90)
p11 = lambda t: (137855872*t**11 + 860969696*t**10 + 2047036856*t**9 + 2032587274*t**8
                 - 24192441*t**7 - 1894061166*t**6 - 1671661480*t**5 - 524330624*t**4
                 + 36004789*t**3 + 62751860*t**2 + 13865604*t + 927360)
u = lambda t: 8*q8(t)/((2*t - 1)*(4*t - 1)*rf(3*t + 1, 3)*rf(4*t + 1, 4))
v = lambda t: ((3*t + 1)*(3*t + 2)*(4*t + 3)*p11(t)
               / ((t + 1)**2*(t + 2)**2*(2*t - 1)*(2*t + 1)*(2*t + 3)*q8(t)*q8(t + 1)))
# ratios U(n+j)/U(n) and V(n+1)/V(n), with U(n) = -27/4 (-1)^n u(n) (5n)!/((3n)! n!^2),
# V(n) = (-1)^n v(n) (3n)!/n!^3
def U_ratio(j):
    r = sp.Integer(1)
    for i in range(j):
        m = n + i
        r *= -u(m + 1)/u(m) * rf(5*m + 1, 5)/(rf(3*m + 1, 3)*(m + 1)**2)
    return r
V_ratio = -v(n + 1)/v(n) * rf(3*n + 1, 3)/(n + 1)**3


def main():
    with open(os.path.join(DATA, "oeis_recurrence.json")) as fh:
        rec = json.load(fh)
    p = [sp.sympify(rec["A%d" % j]) for j in range(4)]
    assert sp.expand(sum(p)) == 0
    Q = [None] + [sum(p[i:]) for i in range(1, 4)]
    X = Q[1] + Q[2]*U_ratio(1) + Q[3]*U_ratio(2)
    Y = Q[2]*U_ratio(1) + Q[3]*U_ratio(2)*(1 + V_ratio)
    assert sp.cancel(X) == 0
    assert sp.cancel(Y) == 0
    # integer roots of the leading coefficient and of q8, p11 (none for n >= 1)
    roots = {}
    for name, poly in [("p3", p[3]), ("q8", q8(n)), ("p11", p11(n))]:
        rts = [r for r in sp.Poly(poly, n).ground_roots() if r.is_integer]
        roots[name] = [int(r) for r in rts]
        assert all(r < 1 for r in rts)
    # numerical cross-check with the b-file
    b = load_bfile()
    for m in range(1, 98):
        assert sum(p[j].subs(n, m)*b[m + j] for j in range(4)) == 0
    assert all(a_nested(m) == b[m] for m in range(1, 101))
    return {"sum_p_zero": True, "X_zero": True, "Y_zero": True,
            "integer_roots_(all<1)": roots, "bfile_recurrence_checked_n": [1, 97],
            "nested_sum_equals_bfile_n": [1, 100]}


if __name__ == "__main__":
    print(main())
