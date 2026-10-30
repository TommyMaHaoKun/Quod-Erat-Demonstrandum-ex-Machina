"""Symbolic verification of the Markov-WZ pair used in the paper (SymPy).

F(n,k) = (-1)^n (2/3)_n (4/3)_n (1+2a)_n (1-2a)_n / C(2n,n)
         * (n+2k+1) * prod_x (x)_k / (x)_{n+k+1},   x in {1/3+a, 1/3-a, 2/3+a, 2/3-a},
G(n,k) = F(n,k) * N(n,k) / (2(2n+1)(n+2k+1)),
N(n,k) = 5n^2 + 6nk + 2k^2 + 7n + 4k + 22/9 - 2a^2.

Claim (Lemma 3.1): F(n+1,k) - F(n,k) = G(n,k+1) - G(n,k).
After division by F(n,k) and clearing denominators this is the polynomial identity (9)
of the paper, checked here by exact expansion.  The script also confirms that the mate
G is forced: the general quadratic ansatz for N has this unique solution.
"""
import json
import sys

import sympy as sp

n, k, a = sp.symbols("n k a")
third = sp.Rational(1, 3)
XS = [third + a, third - a, 2 * third + a, 2 * third - a]


def Pi(m):
    r = sp.Integer(1)
    for x in XS:
        r *= x + m
    return sp.expand(r)


def N(nn, kk):
    return 5 * nn**2 + 6 * nn * kk + 2 * kk**2 + 7 * nn + 4 * kk + sp.Rational(22, 9) - 2 * a**2


def main():
    results = {}
    # Ratios read off from the definition of F.
    Rn = (-(n + sp.Rational(2, 3)) * (n + sp.Rational(4, 3)) * (n + 1 + 2 * a) * (n + 1 - 2 * a)
          * (n + 1) / (2 * (2 * n + 1)) * (n + 2 * k + 2) / ((n + 2 * k + 1) * Pi(n + k + 1)))
    Rk = Pi(k) * (n + 2 * k + 3) / (Pi(n + k + 1) * (n + 2 * k + 1))
    Q = lambda nn, kk: N(nn, kk) / (2 * (2 * nn + 1) * (nn + 2 * kk + 1))
    rational_residual = sp.simplify(sp.together(Rn - 1 - (Rk * Q(n, k + 1) - Q(n, k))))
    results["rational_identity_residual"] = str(rational_residual)

    # Polynomial form (9):
    # -(n+2/3)(n+4/3)(n+1+2a)(n+1-2a)(n+1)(n+2k+2) - 2(2n+1)(n+2k+1)Pi(n+k+1)
    #     = Pi(k) N(n,k+1) - Pi(n+k+1) N(n,k)
    lhs = (-(n + sp.Rational(2, 3)) * (n + sp.Rational(4, 3)) * (n + 1 + 2 * a) * (n + 1 - 2 * a)
           * (n + 1) * (n + 2 * k + 2) - 2 * (2 * n + 1) * (n + 2 * k + 1) * Pi(n + k + 1))
    rhs = Pi(k) * N(n, k + 1) - Pi(n + k + 1) * N(n, k)
    poly_residual = sp.expand(lhs - rhs)
    results["polynomial_identity_residual"] = str(poly_residual)
    results["degrees_in_n_k_a_lhs"] = [int(sp.degree(sp.expand(lhs), v)) for v in (n, k, a)]
    results["degrees_in_n_k_a_rhs"] = [int(sp.degree(sp.expand(rhs), v)) for v in (n, k, a)]

    # Uniqueness of the mate among N quadratic in (n, k) with coefficients c_i + c_6 a^2.
    cs = sp.symbols("c0:7")
    Ngen = lambda nn, kk: cs[0] + cs[6] * a**2 + cs[1] * nn + cs[2] * kk + cs[3] * nn**2 + cs[4] * nn * kk + cs[5] * kk**2
    eq = sp.expand(lhs - (Pi(k) * Ngen(n, k + 1) - Pi(n + k + 1) * Ngen(n, k)))
    sol = sp.solve(sp.Poly(eq, n, k, a).coeffs(), cs, dict=True)
    results["quadratic_ansatz_solutions"] = [{str(s): str(v) for s, v in d.items()} for d in sol]

    ok = rational_residual == 0 and poly_residual == 0 and len(sol) == 1
    results["status"] = "PASS" if ok else "FAIL"
    print(json.dumps(results, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
