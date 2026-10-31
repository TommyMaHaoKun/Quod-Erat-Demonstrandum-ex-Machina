"""Checks for Sections 3-4 of the paper (volume -> Pfaffian -> double sum).

(a) The fifteen pairing terms of the 6 x 6 Pfaffian are summed symbolically
    and the symmetrisation in (k,l) is compared with the closed form
    P(n,k,l) / (120 n^3 D_n(k) D_n(l) (2n+k+l)).
(b) The kernel Psi_N(a,b) of de Bruijn's formula is computed from its
    integral definition for N = 1..8 and compared with the coefficient
    formula of Lemma 6.
(c) Independent of de Bruijn's theorem: the left-part volume J_N(t) is
    computed by iterated integration of polynomials,
        J_0 = 1,  J_N(t) = int_{u interlacing t} J_{N-1}(u) du,
    and compared with the Pfaffian expression for N = 1..7.
"""
import itertools
import sympy as sp
from common import P_TERMS

K = 5
n, N, k, l = sp.symbols("n N k l")


def matchings(s):
    if not s:
        yield []
        return
    a = s[0]
    for i in range(1, len(s)):
        rest = s[1:i] + s[i + 1:]
        for m in matchings(rest):
            yield [(a, s[i])] + m


def perm_sign(seq):
    sgn = 1
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                sgn = -sgn
    return sgn


def pairings():
    out = []
    for m in matchings(list(range(1, K + 2))):
        sg = perm_sign([x for pr in m for x in pr])
        r = [a for (a, b) in m if b == K + 1][0]
        prs = [(a, b) for (a, b) in m if b != K + 1]
        out.append((sg, r, prs))
    return out


def simplex_weight(e):
    """1 / prod_s E_s  with E_s = e_1 + ... + e_s + s."""
    v, s = sp.Integer(1), 0
    for x in e:
        s += x + 1
        v /= sp.expand(s)
    return v


def check_kernel_sum():
    terms = []
    for sg, r, ((p1, q1), (p2, q2)) in pairings():
        e = [0] * (K + 1)
        e[r] = N
        e[p1] += N + k
        e[q1] += N - k
        e[p2] += N + l
        e[q2] += N - l
        terms.append(sp.factor(sg * simplex_weight(e[1:])))
    R = sp.together(sum(terms))
    Rsym = sp.together((R + R.subs({k: l, l: k}, simultaneous=True)) / 2).subs(N, n - 1)
    Pn = sum(c * n**i * k**j * l**m for (i, j, m), c in P_TERMS.items())
    closed = Pn / (120 * n**3 * sp.prod([(k + i * n) * (l + i * n) for i in range(1, 5)]) * (2 * n + k + l))
    assert sp.cancel(Rsym - closed) == 0
    return [str(t) for t in terms]


def Psi_integral(Nv, a, b):
    x, y = sp.symbols("x y", positive=True)
    phi_a = lambda z: (a - z) ** (Nv - 1) / sp.factorial(Nv - 1)
    phi_b = lambda z: (b - z) ** (Nv - 1) / sp.factorial(Nv - 1)
    # a < b ; support of phi_a is (0,a), of phi_b is (0,b)
    I1 = sp.integrate(sp.integrate(phi_b(y), (y, x, b)) * phi_a(x), (x, 0, a))   # x < y
    I2 = sp.integrate(sp.integrate(phi_a(y), (y, x, a)) * phi_b(x), (x, 0, a))   # x < y, roles swapped
    return sp.expand(I1 - I2)


def Psi_formula(Nv, a, b):
    return sp.expand(sum((1 if kk == 0 else 2) * (-1) ** kk * a ** (Nv + kk) * b ** (Nv - kk)
                         / (sp.factorial(Nv - kk) * sp.factorial(Nv + kk)) for kk in range(Nv + 1)))


def check_kernel(maxN=8):
    a, b = sp.symbols("a b", positive=True)
    for Nv in range(1, maxN + 1):
        assert sp.expand(Psi_integral(Nv, a, b) - Psi_formula(Nv, a, b)) == 0, Nv


def J_iterated(maxN):
    t = sp.symbols("t1:%d" % (K + 1))
    us = sp.symbols("u1:%d" % (K + 1))
    J = sp.Integer(1)
    out = [J]
    for _ in range(maxN):
        f = J.subs(dict(zip(t, us)), simultaneous=True)
        lower = [0] + list(t[:-1])
        for i in range(K):
            f = sp.integrate(f, (us[i], lower[i], t[i]))
        J = sp.expand(f)
        out.append(J)
    return t, out


def J_pfaffian(t, Nv):
    total = 0
    for sg, r, prs in pairings():
        term = t[r - 1] ** Nv / sp.factorial(Nv)
        for (p, q) in prs:
            term *= Psi_formula(Nv, t[p - 1], t[q - 1])
        total += sg * term
    return sp.expand(total)


def check_J(maxN=6):
    t, Js = J_iterated(maxN)
    for Nv in range(1, maxN + 1):
        assert sp.expand(Js[Nv] - J_pfaffian(t, Nv)) == 0, Nv


def main():
    terms = check_kernel_sum()
    check_kernel(8)
    check_J(6)
    return {"pairing_terms": terms, "kernel_formula_checked_N": [1, 8],
            "pfaffian_left_volume_checked_N": [1, 6], "closed_form_kernel": "ok"}


if __name__ == "__main__":
    r = main()
    for s in r["pairing_terms"]:
        print(s)
    print({k_: v for k_, v in r.items() if k_ != "pairing_terms"})
