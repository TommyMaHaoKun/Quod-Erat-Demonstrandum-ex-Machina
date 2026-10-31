"""Exact verification of the two-dimensional telescoping relation (Lemma 9).

With H0 = H(n+2,k,l) and the certificate u = Utilde/(delta(n) Q(n,k,l)) of
certificates/telescoping_certificate.json, the relation

  T(n+1,k,l) - T(n,k,l) = Delta_k[G(n,k,l)] + Delta_l[G(n,l,k)],
  G(n,k,l) = H(n+2,k,l) (n+1+k) u(n,k,l) / lambda(n),
  lambda(n) = 5 n^2 (5n+1)(5n+2)(5n+3)(5n+4) g(n+2)/g(n+1),

is equivalent (after division by H0, see the paper) to the rational identity

  -(n+1)^2 L0 + 5 n^2 (5n+1)(5n+2)(5n+3)(5n+4) L1
     = -(n+1-k) u(k+1,l) - (n+1+k) u(k,l) - (n+1-l) u(l+1,k) - (n+1+l) u(l,k),

  L0 = Pi0 P(n,k,l)   / (D_n(k) D_n(l) (2n+k+l)),
  L1 = Pi1 P(n+1,k,l) / (D_{n+1}(k) D_{n+1}(l) (2n+2+k+l)),
  Pi1 = (n+1-k)(n+1+k)(n+1-l)(n+1+l),  Pi0 = (n-k)(n+k)(n-l)(n+l) Pi1.

All denominators are cleared to a common product of linear forms and the
resulting polynomial identity in Q[n,k,l] is checked exactly.  A second,
independent check sums the relation over k,l >= 0 in exact rational
arithmetic for n = 1..25.
"""
import json
import os
import sys
import time
from collections import Counter
from fractions import Fraction
from math import factorial

from sympy.polys.rings import ring
from sympy.polys.domains import QQ

from common import CERT, P_TERMS, T, g, chi, P, Dn

R, n, k, l = ring("n,k,l", QQ)


def load():
    with open(os.path.join(CERT, "telescoping_certificate.json")) as fh:
        return json.load(fh)


def U_poly(cert):
    U = R(0)
    for i, a, b, num, den in cert["Utilde_terms"]:
        U += QQ(int(num), int(den)) * n**i * k**a * l**b
    return U


def lin_factors_Q(cert, kv, lv):
    """Linear forms (cn, ck, cl, c0) of Q evaluated at (k,l) -> (kv,lv)."""
    add = lambda x, y: tuple(p + q for p, q in zip(x, y))
    fs = []
    for m, offs in cert["Q_chains"].items():
        for i in offs:
            fs.append(add(kv, (int(m), 0, 0, i)))
            fs.append(add(lv, (int(m), 0, 0, i)))
    for i in cert["Q_coupling"]:
        fs.append(add(add(kv, lv), (2, 0, 0, i)))
    return fs


def D_factors(j):
    fs = []
    for m in range(1, 5):
        fs.append((m, 1, 0, m * j))
        fs.append((m, 0, 1, m * j))
    fs.append((2, 1, 1, 2 * j))
    return fs


def lin(f):
    return f[0] * n + f[1] * k + f[2] * l + f[3]


def delta_poly(cert):
    out = R(1)
    for expr, e in cert["delta_factors"]:
        a, b = expr.split("n")
        a = a.replace("*", "")
        a = int(a) if a else 1
        b = int(b) if b else 0
        out *= (a * n + b) ** e
    return out


def symbolic_check():
    t0 = time.time()
    cert = load()
    U = U_poly(cert)
    delta = delta_poly(cert)
    K, L, K1, L1 = (0, 1, 0, 0), (0, 0, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1)
    dens = {"L0": D_factors(0), "L1": D_factors(1),
            "r1": lin_factors_Q(cert, K1, L), "r0": lin_factors_Q(cert, K, L),
            "r2": lin_factors_Q(cert, L1, K), "r3": lin_factors_Q(cert, L, K)}
    Om = Counter()
    for fs in dens.values():
        for f, m in Counter(fs).items():
            Om[f] = max(Om[f], m)

    def cof(fs):
        c = Om.copy()
        c.subtract(Counter(fs))
        out = R(1)
        for f, m in c.items():
            assert m >= 0
            out *= lin(f) ** m
        return out

    P0 = R(0)
    for (i, j, m), c in P_TERMS.items():
        P0 += c * n**i * k**j * l**m
    P1 = P0.compose(n, n + 1)
    Pi1 = (n + 1 - k) * (n + 1 + k) * (n + 1 - l) * (n + 1 + l)
    Pi0 = (n - k) * (n + k) * (n - l) * (n + l) * Pi1
    c0 = -(n + 1) ** 2
    c1 = 5 * n**2 * (5 * n + 1) * (5 * n + 2) * (5 * n + 3) * (5 * n + 4)
    lhs = delta * (c0 * Pi0 * P0 * cof(dens["L0"]) + c1 * Pi1 * P1 * cof(dens["L1"]))

    def swap(Pl):
        out = R(0)
        for (e0, e1, e2), c in Pl.terms():
            out += c * n**e0 * k**e2 * l**e1
        return out

    Ulk = swap(U)
    rhs = (-(n + 1 - k) * U.compose(k, k + 1) * cof(dens["r1"])
           - (n + 1 + k) * U * cof(dens["r0"])
           - (n + 1 - l) * Ulk.compose(l, l + 1) * cof(dens["r2"])
           - (n + 1 + l) * Ulk * cof(dens["r3"]))
    ok = (lhs - rhs) == 0
    return {"identity_holds": bool(ok), "certificate_terms": len(cert["Utilde_terms"]),
            "common_denominator_linear_factors": sum(Om.values()),
            "cleared_identity_terms": len(lhs), "seconds": round(time.time() - t0, 1)}


# ---------------------------------------------------------------------------
# summed check in exact arithmetic
# ---------------------------------------------------------------------------

def u_value(cert, nv, kv, lv):
    U = Fraction(0)
    for i, a, b, num, den in cert["Utilde_terms"]:
        U += Fraction(int(num), int(den)) * nv**i * kv**a * lv**b
    d = Fraction(1)
    for expr, e in cert["delta_factors"]:
        a, b = expr.split("n")
        a = a.replace("*", "")
        a = int(a) if a else 1
        b = int(b) if b else 0
        d *= (a * nv + b) ** e
    q = 1
    for m, offs in cert["Q_chains"].items():
        for i in offs:
            q *= (kv + int(m) * nv + i) * (lv + int(m) * nv + i)
    for i in cert["Q_coupling"]:
        q *= kv + lv + 2 * nv + i
    return U / (d * q)


def G(cert, nv, kv, lv):
    c = chi(nv + 2, kv) * chi(nv + 2, lv)
    if c == 0:
        return Fraction(0)
    lam = 5 * nv**2 * (5 * nv + 1) * (5 * nv + 2) * (5 * nv + 3) * (5 * nv + 4) * g(nv + 2) / g(nv + 1)
    return g(nv + 2) * c * (nv + 1 + kv) * u_value(cert, nv, kv, lv) / lam


def summed_check(nmax=25):
    cert = load()
    for nv in range(1, nmax + 1):
        D = lambda m: sum(T(m, a, b) for a in range(m) for b in range(m))
        bound = sum(G(cert, nv, 0, b) for b in range(nv + 2))
        assert D(nv + 1) - D(nv) == -2 * bound, nv
        # pointwise check on the full support, including the boundary rows
        for a in range(nv + 3):
            for b in range(nv + 3):
                lhs = T(nv + 1, a, b) - T(nv, a, b)
                rhs = G(cert, nv, a + 1, b) - G(cert, nv, a, b) + G(cert, nv, b + 1, a) - G(cert, nv, b, a)
                assert lhs == rhs, (nv, a, b)
    return {"summed_and_pointwise_checked_n": [1, nmax]}


if __name__ == "__main__":
    print(symbolic_check())
    print(summed_check(int(sys.argv[1]) if len(sys.argv) > 1 else 25))
