"""Independent exact verification using only the Python standard library (fractions).

Nothing here is derived from verify_wz.py; every quantity is recomputed from the
definitions in the paper.

1. Lemma 3.1 (polynomial form).  Both sides of identity (9) have degree <= 6 in each of
   n, k, a (by inspection of the factors).  A polynomial in three variables of degree <= 6
   in each variable that vanishes on a 7 x 7 x 7 product grid is the zero polynomial, so
   checking (9) on {0..6} x {0..6} x {0, 1/7, ..., 6/7} is a proof of (9).
2. The WZ relation itself, F(n+1,k) - F(n,k) = G(n,k+1) - G(n,k), with F and G computed
   directly from their Pochhammer definitions, for 0 <= n, k <= 12 and several rational a.
3. Lemma 4.1: G(m-1, 0) = T_m(a) at the same rational points.
4. Proposition 5.2: the Taylor coefficients [a^0] T_m and [a^2] T_m equal 27 times the
   terms of Sun's L_{-3}(2) and L_{-3}(4) series, exactly, for 1 <= m <= 80.
5. The partial-fraction step (2k+1)/(Pi(k)) = 3/((k+1/3)^2-a^2) - 3/((k+2/3)^2-a^2).
"""
import json
import sys
from fractions import Fraction as Fr
from math import comb

THIRD = Fr(1, 3)


def poch(x, m):
    r = Fr(1)
    for j in range(m):
        r *= x + j
    return r


def xs(a):
    return [THIRD + a, THIRD - a, 2 * THIRD + a, 2 * THIRD - a]


def Pi(m, a):
    r = Fr(1)
    for x in xs(a):
        r *= x + m
    return r


def N(n, k, a):
    return 5 * n * n + 6 * n * k + 2 * k * k + 7 * n + 4 * k + Fr(22, 9) - 2 * a * a


def F(n, k, a):
    r = Fr((-1) ** n) * poch(Fr(2, 3), n) * poch(Fr(4, 3), n) * poch(1 + 2 * a, n) * poch(1 - 2 * a, n)
    r /= comb(2 * n, n)
    r *= n + 2 * k + 1
    for x in xs(a):
        r *= poch(x, k) / poch(x, n + k + 1)
    return r


def G(n, k, a):
    return F(n, k, a) * N(n, k, a) / (2 * (2 * n + 1) * (n + 2 * k + 1))


def T(m, a):
    r = Fr((-1) ** (m - 1)) * poch(Fr(2, 3), m - 1) * poch(Fr(4, 3), m - 1)
    r *= poch(1 + 2 * a, m - 1) * poch(1 - 2 * a, m - 1)
    r *= 5 * m * m - 3 * m + Fr(4, 9) - 2 * a * a
    r /= m * comb(2 * m, m)
    for x in xs(a):
        r /= poch(x, m)
    return r


# --- truncated power series in a, modulo a^3: (c0, c1, c2) ---
def smul(p, q):
    return (p[0] * q[0], p[0] * q[1] + p[1] * q[0], p[0] * q[2] + p[1] * q[1] + p[2] * q[0])


def sinv(p):
    c0 = 1 / p[0]
    c1 = -p[1] * c0 * c0
    c2 = (p[1] * p[1] - p[0] * p[2]) * c0 * c0 * c0
    return (c0, c1, c2)


def T_series(m):
    one = (Fr(1), Fr(0), Fr(0))
    r = (Fr((-1) ** (m - 1)) * poch(Fr(2, 3), m - 1) * poch(Fr(4, 3), m - 1) / (m * comb(2 * m, m)), Fr(0), Fr(0))
    for j in range(m - 1):
        r = smul(r, (Fr(1 + j), Fr(2), Fr(0)))     # (1+2a+j)
        r = smul(r, (Fr(1 + j), Fr(-2), Fr(0)))    # (1-2a+j)
    r = smul(r, (Fr(5 * m * m - 3 * m) + Fr(4, 9), Fr(0), Fr(-2)))
    den = one
    for j in range(m):
        for c, s in ((THIRD, 1), (THIRD, -1), (2 * THIRD, 1), (2 * THIRD, -1)):
            den = smul(den, (c + j, Fr(s), Fr(0)))
    return smul(r, sinv(den))


def sun_terms(m):
    """(term of the L_{-3}(2) series, term of the L_{-3}(4) series (3.13))."""
    H3 = sum(Fr(1, j * j) for j in range(1, 3 * m))
    H1 = sum(Fr(1, j * j) for j in range(1, m))
    den = Fr(m ** 3 * comb(2 * m, m) ** 2 * comb(3 * m, m))
    base = Fr((-27) ** (m - 1)) / den
    return base * (15 * m - 4), base * ((15 * m - 4) * (9 * H3 - 5 * H1) - Fr(18, 3 * m - 1))


def main():
    out = {}
    # 1. grid proof of (9)
    grid_fail = 0
    pts = 0
    for n in range(7):
        for k in range(7):
            for i in range(7):
                a = Fr(i, 7)
                lhs = (-(n + Fr(2, 3)) * (n + Fr(4, 3)) * (n + 1 + 2 * a) * (n + 1 - 2 * a) * (n + 1) * (n + 2 * k + 2)
                       - 2 * (2 * n + 1) * (n + 2 * k + 1) * Pi(n + k + 1, a))
                rhs = Pi(k, a) * N(n, k + 1, a) - Pi(n + k + 1, a) * N(n, k, a)
                pts += 1
                grid_fail += lhs != rhs
    out["identity_3_3_grid_points"] = pts
    out["identity_3_3_grid_failures"] = grid_fail

    # 2. + 3. WZ relation from definitions, and G(m-1,0) = T_m
    avals = [Fr(0), Fr(1, 10), Fr(-1, 7), Fr(1, 6), Fr(2, 13), Fr(5, 4), Fr(-3, 11)]
    wz_fail = 0
    wz_pts = 0
    t_fail = 0
    for a in avals:
        for n in range(13):
            for k in range(13):
                wz_pts += 1
                wz_fail += (F(n + 1, k, a) - F(n, k, a)) != (G(n, k + 1, a) - G(n, k, a))
        for m in range(1, 25):
            t_fail += G(m - 1, 0, a) != T(m, a)
    out["wz_relation_points"] = wz_pts
    out["wz_relation_failures"] = wz_fail
    out["G_equals_T_failures"] = t_fail

    # 4. Taylor coefficients versus Sun's terms
    coef_fail = 0
    odd_fail = 0
    M = 80
    for m in range(1, M + 1):
        c0, c1, c2 = T_series(m)
        s2, s4 = sun_terms(m)
        coef_fail += (c0 != 27 * s2) + (c2 != 27 * s4)
        odd_fail += c1 != 0
    out["taylor_coefficient_terms_checked"] = M
    out["taylor_coefficient_failures"] = coef_fail
    out["odd_coefficient_failures"] = odd_fail

    # 5. partial fractions
    pf_fail = 0
    for kk in range(30):
        for a in avals:
            lhs = Fr(2 * kk + 1) / Pi(kk, a)
            rhs = 3 / ((kk + THIRD) ** 2 - a * a) - 3 / ((kk + 2 * THIRD) ** 2 - a * a)
            pf_fail += lhs != rhs
    out["partial_fraction_failures"] = pf_fail

    ok = grid_fail == 0 and wz_fail == 0 and t_fail == 0 and coef_fail == 0 and odd_fail == 0 and pf_fail == 0
    out["status"] = "PASS" if ok else "FAIL"
    print(json.dumps(out, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
