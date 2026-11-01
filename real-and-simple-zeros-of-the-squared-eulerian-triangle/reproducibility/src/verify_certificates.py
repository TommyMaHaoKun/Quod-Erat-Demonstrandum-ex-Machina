"""Independent exact check of the sign-alternation certificates.

The Eulerian numbers are recomputed here from the closed formula
    A(n,k) = sum_{i=0}^{k} (-1)^i C(n+1,i) (k-i)^n      (n >= 1, 1 <= k <= n)
and compared with the recurrence used in eulerian_core.py.  Only Python integers
and fractions are used; no floating point enters the verification.

Usage: python verify_certificates.py path/to/sign_certificates.json
Exit code 0 means every certificate is valid.
"""
import json
import sys
from fractions import Fraction
from math import comb, factorial

from eulerian_core import eulerian_triangle


def eulerian_closed(n, k):
    if n == 0:
        return 1 if k == 0 else 0
    if k < 1 or k > n:
        return 0
    return sum((-1) ** i * comb(n + 1, i) * (k - i) ** n for i in range(k + 1))


def horner_fraction(coeffs, q):
    """Original rational Horner routine, retained as an independent cross-check."""
    v = Fraction(0)
    for c in reversed(coeffs):
        v = v * q + c
    return v


def horner(coeffs, q):
    """Return d**m R(a/d) exactly as an integer, for q=a/d and m=deg R.

    The positive denominator factor preserves the sign. Clearing it during
    Horner evaluation avoids the repeated large gcds of Fraction arithmetic.
    """
    a, d = q.numerator, q.denominator
    h = coeffs[-1]
    d_power = d
    for c in reversed(coeffs[:-1]):
        h = a*h+c*d_power
        d_power *= d
    return h


def main():
    data = json.load(open(sys.argv[1]))
    N = data["N"]
    Arec = eulerian_triangle(N)
    A = [[eulerian_closed(n, k) for k in range(N + 1)] for n in range(N + 1)]
    assert A == [row[:N + 1] for row in Arec], "closed formula and recurrence disagree"
    certs = {c["n"]: c for c in data["certificates"]}
    assert sorted(certs) == list(range(1, N + 1)), "missing certificates"
    for n in range(1, N + 1):
        B = [sum(A[n][j] * A[j][k] for j in range(k, n + 1)) for k in range(n + 1)]
        assert B[0] == 0 and B[n] == 1 and B[1] == factorial(n)
        assert all(b > 0 for b in B[1:]), "nonpositive coefficient"
        R = B[1:]                       # P_n = x * R_n,  deg R_n = n-1
        pts = [Fraction(s) for s in certs[n]["points"]]
        assert len(pts) == n - 1
        assert all(q < 0 for q in pts)
        assert all(a > b for a, b in zip(pts, pts[1:]))
        assert R[0] > 0                  # sign at x = 0
        for i, q in enumerate(pts, start=1):
            v = horner(R, q)
            if n <= 20:
                baseline = horner_fraction(R, q)*q.denominator**(n-1)
                assert v == baseline, f"Horner cross-check failed n={n} i={i}"
            assert (v > 0) - (v < 0) == (-1) ** i, f"bad sign n={n} i={i}"
    print("OK: integer Horner equals the original Fraction evaluation at every certificate point for n <= 20.")
    print(f"OK: for every 1 <= n <= {N}, R_n = P_n/x has n-1 sign changes on (-inf,0);")
    print("hence P_n has n simple real zeros, all <= 0 (P_0 = 1 has none).")


if __name__ == "__main__":
    main()
