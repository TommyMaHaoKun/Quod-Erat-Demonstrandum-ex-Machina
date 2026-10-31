"""Shared exact definitions for the A181199 proof.

Everything here is exact (Python integers, fractions.Fraction or SymPy
rationals).  The notation follows the paper:

  w_k        = 1 if k = 0 and 2 if k >= 1,
  chi_n(k)   = (-1)^k / ((n-1-k)! (n-1+k)!),
  g(n)       = (5n)! / (120 n^3 (n-1)!),
  H(n,k,l)   = g(n) chi_n(k) chi_n(l),
  T(n,k,l)   = H(n,k,l) P(n,k,l) / (D_n(k) D_n(l) (2n+k+l)),
  D_n(x)     = (x+n)(x+2n)(x+3n)(x+4n),

and a(n) = sum_{k,l=0}^{n-1} w_k w_l T(n,k,l)   (Theorem 3 of the paper).
"""
from fractions import Fraction
from math import factorial
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CERT = os.path.join(ROOT, "certificates")
DATA = os.path.join(ROOT, "data")

# The degree-7 numerator P(n,k,l) of the symmetric kernel, as {(i,j,m): c}
# meaning c * n^i k^j l^m.
P_TERMS = {
    (0, 4, 3): 15, (1, 4, 2): 115, (2, 4, 1): 250, (3, 4, 0): 120,
    (0, 3, 4): 15, (1, 3, 3): 200, (2, 3, 2): 999, (3, 3, 1): 1870, (4, 3, 0): 840,
    (1, 2, 4): 115, (2, 2, 3): 999, (3, 2, 2): 3598, (4, 2, 1): 5600, (5, 2, 0): 2400,
    (2, 1, 4): 250, (3, 1, 3): 1870, (4, 1, 2): 5600, (5, 1, 1): 7400, (6, 1, 0): 2976,
    (3, 0, 4): 120, (4, 0, 3): 840, (5, 0, 2): 2400, (6, 0, 1): 2976, (7, 0, 0): 1152,
}


def P(n, k, l):
    return sum(c * n**i * k**j * l**m for (i, j, m), c in P_TERMS.items())


def Dn(n, x):
    return (x + n) * (x + 2 * n) * (x + 3 * n) * (x + 4 * n)


def w(k):
    return 1 if k == 0 else 2


def chi(n, k):
    if k < 0 or k > n - 1:
        return Fraction(0)
    return Fraction((-1) ** k, factorial(n - 1 - k) * factorial(n - 1 + k))


def g(n):
    return Fraction(factorial(5 * n), 120 * n**3 * factorial(n - 1))


def T(n, k, l):
    c = chi(n, k) * chi(n, l)
    if c == 0:
        return Fraction(0)
    return g(n) * c * Fraction(P(n, k, l), Dn(n, k) * Dn(n, l) * (2 * n + k + l))


def a_double_sum(n):
    """The double-sum representation of a(n), n >= 1."""
    return sum(w(k) * w(l) * T(n, k, l) for k in range(n) for l in range(n))


def load_bfile():
    """OEIS b-file (n, a(n)) for n = 1..100, used only for comparison."""
    out = {}
    with open(os.path.join(DATA, "OEIS_b181199.txt")) as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                a, b = line.split()
                out[int(a)] = int(b)
    return out


# ---------------------------------------------------------------------------
# The Kauers--Koutschan nested sum (their Section 6.4, conjecture for A181199)
# ---------------------------------------------------------------------------

def q8(t):
    return (25216 * t**8 + 9888 * t**7 - 14496 * t**6 + 11208 * t**5
            + 23832 * t**4 + 7383 * t**3 - 1522 * t**2 - 939 * t - 90)


def p11(t):
    return (137855872 * t**11 + 860969696 * t**10 + 2047036856 * t**9
            + 2032587274 * t**8 - 24192441 * t**7 - 1894061166 * t**6
            - 1671661480 * t**5 - 524330624 * t**4 + 36004789 * t**3
            + 62751860 * t**2 + 13865604 * t + 927360)


def rising(x, m):
    out = 1
    for i in range(m):
        out *= x + i
    return out


def u_kk(k):
    return Fraction(8 * q8(k), (2 * k - 1) * (4 * k - 1) * rising(3 * k + 1, 3) * rising(4 * k + 1, 4))


def v_kk(i):
    num = (3 * i + 1) * (3 * i + 2) * (4 * i + 3) * p11(i)
    den = ((i + 1)**2 * (i + 2)**2 * (2 * i - 1) * (2 * i + 1) * (2 * i + 3)
           * q8(i) * q8(i + 1))
    return Fraction(num, den)


def U_kk(n):
    return (Fraction(-27, 4) * (-1) ** n * u_kk(n)
            * Fraction(factorial(5 * n), factorial(3 * n) * factorial(n) ** 2))


def V_kk(i):
    return (-1) ** i * v_kk(i) * Fraction(factorial(3 * i), factorial(i) ** 3)


def a_nested(n):
    total, S = Fraction(1), Fraction(0)
    for k in range(1, n):
        total += U_kk(k) * S
        S += V_kk(k)
    return total
