"""Supplementary high-precision checks (mpmath).  The proof does not depend on them.

1. Sun's series (3.13), summed to M terms, plus the explicit tail bound of Remark 6.3,
   compared with 9 L_{-3}(4) computed from Hurwitz zeta values.
2. The same for the companion L_{-3}(2) series.
3. The one-parameter identity (Theorem 2.1) at a few complex points |a| <= 1/6.
"""
import json
import sys

from mpmath import mp, mpf, mpc, binomial, digamma, zeta, rf, nstr

mp.dps = 130
DIGITS = 110


def L(s):
    return (zeta(s, mpf(1) / 3) - zeta(s, mpf(2) / 3)) / mpf(3) ** s


def sun_partial(M):
    s4 = mpf(0)
    s2 = mpf(0)
    H3 = mpf(0)  # H^{(2)}_{3m-1}
    H1 = mpf(0)  # H^{(2)}_{m-1}
    for m in range(1, M + 1):
        if m > 1:
            H1 += mpf(1) / (m - 1) ** 2
            for j in (3 * m - 3, 3 * m - 2, 3 * m - 1):
                H3 += mpf(1) / j ** 2
        else:
            H3 = mpf(1) + mpf(1) / 4
        base = mpf(-27) ** (m - 1) / (mpf(m) ** 3 * binomial(2 * m, m) ** 2 * binomial(3 * m, m))
        s2 += base * (15 * m - 4)
        s4 += base * ((15 * m - 4) * (9 * H3 - 5 * H1) - mpf(18) / (3 * m - 1))
    return s2, s4


def tail_bound(M):
    # Remark 6.3: |[a^2] T_m| <= 36 * (5/2) * 6^4 * m^5 * 4^(1-m); Sun term = [a^2]T_m / 27.
    return sum(mpf(36) * mpf(5) / 2 * 6 ** 4 * mpf(m) ** 5 * mpf(4) ** (1 - m) / 27 for m in range(M + 1, M + 2000))


def T(m, a):
    r = mpf(-1) ** (m - 1) * rf(mpf(2) / 3, m - 1) * rf(mpf(4) / 3, m - 1)
    r *= rf(1 + 2 * a, m - 1) * rf(1 - 2 * a, m - 1)
    r *= 5 * m * m - 3 * m + mpf(4) / 9 - 2 * a * a
    r /= m * binomial(2 * m, m)
    for x in (mpf(1) / 3 + a, mpf(1) / 3 - a, mpf(2) / 3 + a, mpf(2) / 3 - a):
        r /= rf(x, m)
    return r


def lhs_family(a):
    # 3 * sum_k [1/((k+1/3)^2-a^2) - 1/((k+2/3)^2-a^2)], a != 0, using
    # sum_k 1/((k+c)^2-a^2) = (psi(c+a) - psi(c-a)) / (2a).
    def U(c):
        return (digamma(c + a) - digamma(c - a)) / (2 * a)
    return 3 * (U(mpf(1) / 3) - U(mpf(2) / 3))


def main():
    out = {}
    M = 400
    s2, s4 = sun_partial(M)
    tb = tail_bound(M)
    t4 = 9 * L(4)
    t2 = L(2)
    out["terms"] = M
    out["tail_bound"] = nstr(tb, 5)
    out["sun_L4_series_partial_sum"] = nstr(s4, DIGITS)
    out["nine_L_minus3_of_4"] = nstr(t4, DIGITS)
    out["L4_difference"] = nstr(abs(s4 - t4), 5)
    out["L2_series_partial_sum"] = nstr(s2, DIGITS)
    out["L_minus3_of_2"] = nstr(t2, DIGITS)
    out["L2_difference"] = nstr(abs(s2 - t2), 5)
    fam = {}
    for a in (mpf(1) / 10, mpc(0, mpf(3) / 20), mpc(mpf(1) / 10, mpf(1) / 9), mpf(1) / 6):
        rhs = sum(T(m, a) for m in range(1, 450))
        lhs = lhs_family(a)
        fam[nstr(a, 6)] = nstr(abs(lhs - rhs), 5)
    out["family_identity_abs_differences"] = fam
    eps = mpf(10) ** (-DIGITS)
    ok = abs(s4 - t4) <= tb + eps and abs(s2 - t2) < eps and all(mpf(v) < eps for v in fam.values())
    out["status"] = "PASS" if ok else "FAIL"
    print(json.dumps(out, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
