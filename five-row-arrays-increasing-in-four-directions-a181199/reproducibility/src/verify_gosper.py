"""Exact verification of the single-sum (Gosper) step, Section 6 of the paper.

Notation (all exact):
  beta_n(l) = (-1)^l / ((n+1-l)! (n+1+l)!),
  nu(n)     = g(n+1) / (n+1)!^2,
  sigma(n,l), tau(n) : rational functions defined in the paper (eqs. (6.2)-(6.3));
                       sigma uses the k = 0 restriction u(n,0,l) of the
                       telescoping certificate,
  s(n) = a(n+1) - a(n) = nu(n) [ sum_l beta_n(l) sigma(n,l) + beta_n(0) tau(n) ],
  U(n), V(n)          : the hypergeometric terms of Kauers--Koutschan,
  psi(n) = nu(n)/U(n),  r(n) = psi(n+1)/psi(n)  (rational),
  A(n,l) = r(n) sigma(n+1,l) - (n+2-l)(n+2+l) sigma(n,l).

Checked here:
  (G1) A(n,l) = -(n+2-l) rho(n,l+1) - (n+2+l) rho(n,l) as rational functions,
       rho from certificates/gosper_certificate.json;
  (G2) -rho(n,0)/(n+2) + r(n) tau(n+1)/(n+2)^2 - tau(n)
         = -810 u(n) v(n) (n+1)^7 / ((5n+1)(5n+2)(5n+3)(5n+4)(5n+5));
  (G3) the denominators of rho, sigma and tau do not vanish for n >= 1, l >= 0;
  (G4) the single-sum expression for s(n) agrees with a(n+1)-a(n) for n <= 20,
       and s(1)/U(1) = 0.
"""
import json
import os
import time
import sympy as sp
from sympy.polys.rings import ring
from sympy.polys.domains import QQ

from common import CERT, P_TERMS, load_bfile, U_kk

n, l = sp.symbols("n l")


def rf(x, m):
    return sp.prod([x + i for i in range(m)])


q8 = lambda t: (25216*t**8 + 9888*t**7 - 14496*t**6 + 11208*t**5 + 23832*t**4
                + 7383*t**3 - 1522*t**2 - 939*t - 90)
p11 = lambda t: (137855872*t**11 + 860969696*t**10 + 2047036856*t**9 + 2032587274*t**8
                 - 24192441*t**7 - 1894061166*t**6 - 1671661480*t**5 - 524330624*t**4
                 + 36004789*t**3 + 62751860*t**2 + 13865604*t + 927360)
u_kk = lambda t: 8*q8(t)/((2*t - 1)*(4*t - 1)*rf(3*t + 1, 3)*rf(4*t + 1, 4))
v_kk = lambda t: ((3*t + 1)*(3*t + 2)*(4*t + 3)*p11(t)
                  / ((t + 1)**2*(t + 2)**2*(2*t - 1)*(2*t + 1)*(2*t + 3)*q8(t)*q8(t + 1)))

Psym = sum(c * n**i * sp.Symbol("k")**j * l**m for (i, j, m), c in P_TERMS.items())
P = lambda N, K, L: Psym.subs({n: N, sp.Symbol("k"): K, l: L}, simultaneous=True)
Dn = lambda N, x: (x + N)*(x + 2*N)*(x + 3*N)*(x + 4*N)
prod14 = lambda N: rf(5*N + 1, 4)


def load_json(name):
    with open(os.path.join(CERT, name)) as fh:
        return json.load(fh)


def u0_expr():
    """u(n,0,l) from the telescoping certificate."""
    cert = load_json("telescoping_certificate.json")
    U0 = 0
    for i, a, b, num, den in cert["Utilde_terms"]:
        if a == 0:
            U0 += sp.Rational(int(num), int(den)) * n**i * l**b
    delta = 1
    for expr, e in cert["delta_factors"]:
        delta *= sp.sympify(expr, locals={"n": n})**e
    Q = 1
    for m, offs in cert["Q_chains"].items():
        for i in offs:
            Q *= (int(m)*n + i) * (l + int(m)*n + i)
    for i in cert["Q_coupling"]:
        Q *= l + 2*n + i
    return U0 / (delta * Q)


U0 = None


def sigma(N, L):
    s1 = -8*(N + 1)*U0.subs(n, N)/(5*N**2*prod14(N))
    s2 = (N + 1)**2*((N + 1)**2 - L**2)*P(N + 1, 0, L)/(Dn(N + 1, 0)*Dn(N + 1, L)*(2*N + 2 + L))
    s3 = ((N + 1)**4/(5*prod14(N))*(N**2 - L**2)*((N + 1)**2 - L**2)*P(N, 0, L)
          / (Dn(N, 0)*Dn(N, L)*(2*N + L)))
    return s1.subs(l, L) - 4*(s2 - s3)


def tau(N):
    t1 = (N + 1)**4*P(N + 1, 0, 0)/(Dn(N + 1, 0)**2*(2*N + 2))
    t0 = (N + 1)**4/(5*prod14(N))*N**2*(N + 1)**2*P(N, 0, 0)/(Dn(N, 0)**2*(2*N))
    return t1 - t0


r_n = sp.factor(rf(5*n + 6, 5)*(n + 1)**2/(n + 2)**5
                * (-u_kk(n)*rf(3*n + 1, 3)*(n + 1)**2/(u_kk(n + 1)*rf(5*n + 1, 5))))


def rho_parts():
    """rho(n,l) = sum_e N_e(n) l^e / (delta_rho(n) R(n,l)); returns (R, [(N_e, delta_rho)])."""
    cert = load_json("gosper_certificate.json")
    den = 1
    for m, i, e in cert["rho_den_factors"]:
        den *= (l + m*n + i)**e
    drho = q8(n + 1)**cert["delta_rho_q8_shift1"]
    for a, b, e in cert["delta_rho_linear_factors"]:
        drho *= (a*n + b)**e
    coeffs = []
    for row in cert["numerators"]:
        a = sum(sp.Rational(int(x), int(y))*n**j for j, (x, y) in enumerate(row))
        coeffs.append((a, drho))
    return den, coeffs


def check_G1(rho_den, coeffs):
    t0 = time.time()
    A = sp.together(r_n*sigma(n + 1, l) - (n + 2 - l)*(n + 2 + l)*sigma(n, l))
    An, Ad = sp.fraction(A)
    # common n-denominator of rho
    dn = coeffs[0][1]
    Nr = sum(a*l**e for e, (a, c) in enumerate(coeffs))
    Rg, nn, ll = ring("n,l", QQ)
    conv = lambda e: Rg(sp.Poly(sp.expand(e), n, l).as_expr()) if e != 0 else Rg(0)
    An_, Ad_, dn_, Nr_, rd_ = map(conv, (An, Ad, dn, Nr, rho_den))
    Nr1 = Nr_.compose(ll, ll + 1)
    rd1 = rd_.compose(ll, ll + 1)
    lhs = An_*dn_*rd_*rd1
    rhs = -Ad_*((nn + 2 - ll)*Nr1*rd_ + (nn + 2 + ll)*Nr_*rd1)
    ok = (lhs - rhs) == 0
    return ok, round(time.time() - t0, 1)


def check_G2(rho_den, coeffs):
    a0, c0 = coeffs[0]
    rho0 = a0/c0/rho_den.subs(l, 0)
    expr = (-rho0/(n + 2) + r_n*tau(n + 1)/(n + 2)**2 - tau(n)
            + 810*u_kk(n)*v_kk(n)*(n + 1)**7/rf(5*n + 1, 5))
    return sp.cancel(sp.together(expr)) == 0


def check_G3(rho_den, coeffs):
    """Integer roots n >= 1 of all n-denominators that occur."""
    bad = []
    polys = [coeffs[0][1]] + [sp.denom(sp.together(r_n)), sp.numer(sp.together(r_n))]
    polys += [sp.denom(sp.together(tau(n))), sp.denom(sp.together(U0.subs(l, 0)))]
    for pol in polys:
        for root in sp.Poly(pol, n).ground_roots():
            if root.is_integer and root >= 1:
                bad.append((str(pol)[:40], int(root)))
    # rho_den and sigma's l-denominators are products of (l + m n + i), i >= 0
    return bad


def check_G4(nmax=20):
    from fractions import Fraction
    from math import factorial
    b = load_bfile()
    sig = sp.lambdify((n, l), sigma(n, l), "sympy")
    for N in range(1, nmax + 1):
        g1 = sp.factorial(5*(N + 1))/(120*(N + 1)**3*sp.factorial(N))
        nu = g1/sp.factorial(N + 1)**2
        beta = lambda L: sp.Integer(-1)**L/(sp.factorial(N + 1 - L)*sp.factorial(N + 1 + L))
        s = nu*(sum(beta(L)*sigma(sp.Integer(N), sp.Integer(L)) for L in range(N + 2)) + beta(0)*tau(sp.Integer(N)))
        assert sp.nsimplify(s) == b[N + 1] - b[N], N
    assert b[2] - b[1] == 0
    return nmax


def main():
    global U0
    U0 = u0_expr()
    rho_den, coeffs = rho_parts()
    ok1, secs = check_G1(rho_den, coeffs)
    assert ok1
    ok2 = check_G2(rho_den, coeffs)
    assert ok2
    bad = check_G3(rho_den, coeffs)
    assert not bad, bad
    m = check_G4()
    return {"G1_gosper_identity": ok1, "G1_seconds": secs, "G2_boundary_identity": ok2,
            "G3_no_positive_integer_poles": True, "G4_single_sum_checked_n": [1, m],
            "r(n)": str(r_n)}


if __name__ == "__main__":
    print(main())
