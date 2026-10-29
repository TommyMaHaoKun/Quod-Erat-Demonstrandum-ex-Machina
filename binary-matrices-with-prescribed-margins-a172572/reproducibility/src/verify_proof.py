"""Exact symbolic certificate for the A172572 proof. Python standard library only.

All equalities below are identities in Q(n), not evaluations at sample integers.
Run from any working directory: python path/to/src/verify_proof.py
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb
import argparse
import json
from pathlib import Path


def trim(a):
    a = list(map(F, a))
    while len(a) > 1 and not a[-1]:
        a.pop()
    return tuple(a)


def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def divmod_poly(a, b):
    if b == (0,):
        raise ZeroDivisionError
    q = [F(0)] * max(1, len(a)-len(b)+1)
    while a != (0,) and len(a) >= len(b):
        j = len(a)-len(b)
        v = a[-1]/b[-1]
        q[j] += v
        a = add(a, (F(0),)*j + tuple(-v*x for x in b))
    return trim(q), a


def gcd_poly(a, b):
    while b != (0,):
        a, b = b, divmod_poly(a, b)[1]
    return tuple(x/a[-1] for x in a)


class R:
    """A reduced rational function of the formal variable n."""
    def __init__(self, num=0, den=(1,)):
        if isinstance(num, R):
            self.p, self.q = num.p, num.q
            return
        p = trim(num if isinstance(num, (tuple, list)) else [num])
        q = trim(den)
        if q == (0,):
            raise ZeroDivisionError
        g = gcd_poly(p, q)
        p, r = divmod_poly(p, g)
        q, t = divmod_poly(q, g)
        assert r == t == (0,)
        self.p = tuple(x/q[-1] for x in p)
        self.q = tuple(x/q[-1] for x in q)

    def __add__(self, other):
        other = R(other)
        return R(add(mul(self.p, other.q), mul(other.p, self.q)),
                 mul(self.q, other.q))

    __radd__ = __add__

    def __neg__(self):
        return R(tuple(-x for x in self.p), self.q)

    def __sub__(self, other):
        return self + (-R(other))

    def __rsub__(self, other):
        return R(other) + (-self)

    def __mul__(self, other):
        other = R(other)
        return R(mul(self.p, other.p), mul(self.q, other.q))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = R(other)
        return R(mul(self.p, other.q), mul(self.q, other.p))

    def __rtruediv__(self, other):
        return R(other) / self

    def __pow__(self, power):
        if power < 0:
            return (1/self)**(-power)
        ans = R(1)
        for _ in range(power):
            ans = ans*self
        return ans

    def __eq__(self, other):
        other = R(other)
        return self.p == other.p and self.q == other.q

    def shift(self, amount):
        def evaluate(coeffs):
            ans = R(0)
            for c in reversed(coeffs):
                ans = ans*(n+amount)+c
            return ans
        return evaluate(self.p)/evaluate(self.q)


n = R((0, 1))
zero = (R(0), R(0), R(0))


def vector_sum(*vectors):
    return tuple(sum(v[k] for v in vectors) for k in range(3))


def scale(s, vector):
    return tuple(s*x for x in vector)


@lru_cache(None)
def moment(j, k):
    """M[j,k] as a vector of coefficients of (I2,I4,I6)."""
    if j < 0 or k < 0 or k > 6 or (j+k) % 2:
        return zero
    if j == 0:
        return {0: (5*n, R(0), R(0)),
                2: (R(1), R(0), R(0)),
                4: (R(0), R(1), R(0)),
                6: (R(0), R(0), R(1))}[k]
    if k == 1:
        return scale(1/(j+1+4*n), vector_sum(
            scale(j, moment(j-1, 0)),
            scale(5*n*j, moment(j-1, 2)),
            scale(20*n*n, moment(j, 3))))
    return scale(R(1)/(k-1), vector_sum(
        scale(k, moment(j-1, k-1)),
        scale(-n*(6-k), moment(j-1, k+1)),
        scale(-(j-1), moment(j-2, k))))


def verify():
    f = 102*n**4+204*n**3+145*n**2+43*n+5
    g = 62*n*n+93*n+36
    h = 62*n*n+31*n+5
    expected = [
        (3*n*f/((n+1)*(2*n+1)), -9*n**4*g/(2*(n+1)*(2*n+1)),
         -5*n**6/(2*(n+1))),
        (n*h/(2*n+1), -60*n**4/(2*n+1), R(0)),
        (5*n, R(0), R(0))]
    derived = []
    for k in (2, 4, 6):
        derived.append(vector_sum(*[
            scale(comb(6-k, t)*(-n)**t, moment(6-k-t, t))
            for t in range(7-k)]))
    assert derived == expected, 'Moment transition matrix mismatch'
    # Verify the change of variables W=(5n J2,5n^3 J4,5n^5 J6).
    expected_w = [
        (6*f/(n+1)**4, -9*n*g/(n+1)**4,
         -5*n*(2*n+1)/(n+1)**4),
        (2*h/(n+1), -120*n/(n+1), R(0)),
        (10*(2*n+1)*(n+1), R(0), R(0))]
    scales = [5*n, 5*n**3, 5*n**5]
    ratio = 2*(2*n+1)/(n+1)**4
    for i in range(3):
        for j in range(3):
            assert scales[i].shift(1)*ratio*derived[i][j]/scales[j] == expected_w[i][j]
    p = (5084*n**6+68634*n**5+383756*n**4+1137319*n**3+
         1884032*n**2+1653960*n+601185)
    q = (31372*n**5+313720*n**4+1227805*n**3+2354425*n**2+
         2220988*n+827860)
    assert g*f.shift(1)-20*g.shift(1)*(n+1)**4 == p.shift(-1)
    assert (18*g*g.shift(1)*h + 50*g*(n+1)**2*(4*(n+1)**2-1)
            -720*g.shift(1)*f) == -4*(2*n+1)*q.shift(-1)
    assert g.shift(1) == 62*n*n+217*n+191
    assert g.shift(2) == 62*n*n+341*n+470
    # Original and normalized recurrences are proportional after a=C(3n,n)b.
    c = [6000*(n+1)**2*(2*n+1)*(2*n+3)*g.shift(2),
         -4*(2*n+3)*q, -6*p, (n+3)**4*g.shift(1)]
    u = [20250*(n+1)*(3*n+1)*(3*n+2)*(3*n+4)*(3*n+5)*
         (3*n+7)*(3*n+8)*g.shift(2),
         -9*(3*n+4)*(3*n+5)*(3*n+7)*(3*n+8)*q,
         -9*(n+2)*(3*n+7)*(3*n+8)*p,
         (n+2)*(n+3)**5*(2*n+5)*g.shift(1)]
    ratios = [R(1)]
    for j in range(3):
        m = n+j
        ratios.append(ratios[-1]*3*(3*m+1)*(3*m+2)/(2*(m+1)*(2*m+1)))
    common = u[0]/c[0]
    assert all(u[j]*ratios[j] == common*c[j] for j in range(4))
    return {
        'status': 'EXACT_SYMBOLIC_IDENTITIES_PASSED',
        'arithmetic': 'rational functions in a formal variable over Q',
        'external_dependencies': [],
        'verified': ['integration-by-parts moment reduction to explicit matrix',
                     'normalization and change of moment basis',
                     'two polynomial identities eliminating the auxiliary moment',
                     'all target coefficient polynomials',
                     'conversion to the published unnormalized recurrence'],
        'scope': 'The analytic and combinatorial bridges are proved in the paper; '
                 'these symbolic identities are its finite algebraic certificate.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print('PASS: all exact symbolic identities in Q(n).')
    for item in result['verified']:
        print('  '+item)
