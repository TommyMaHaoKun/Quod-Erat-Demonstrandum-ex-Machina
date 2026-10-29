"""Exact identity checks for the analytic proof; Python standard library only.

The finite examples are regression checks, not a substitute for the proof.
All polynomial identities are checked coefficient by coefficient over Q.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
N = 6
ZERO = (0,) * N


class Poly:
    def __init__(self, terms=None):
        self.terms = {k: F(v) for k, v in (terms or {}).items() if v}

    @staticmethod
    def cast(value):
        return value if isinstance(value, Poly) else Poly({ZERO: value})

    def __add__(self, other):
        result = dict(self.terms)
        for mon, value in self.cast(other).terms.items():
            result[mon] = result.get(mon, F(0)) + value
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({mon: -v for mon, v in self.terms.items()})

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        result = {}
        for a, av in self.terms.items():
            for b, bv in self.cast(other).terms.items():
                mon = tuple(i + j for i, j in zip(a, b))
                result[mon] = result.get(mon, F(0)) + av * bv
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, k):
        if not isinstance(k, int) or k < 0:
            raise ValueError('Exponent must be a nonnegative integer')
        result = Poly.cast(1)
        for _ in range(k):
            result *= self
        return result


def variable(i):
    mon = [0]*N
    mon[i] = 1
    return Poly({tuple(mon): 1})


def squares(values):
    return sum(v*v for v in values)


def adjacent(values):
    return sum(values[i]*values[(i+1)%6] for i in range(6))


def cubic(values):
    return sum(values[i]*values[(i+1)%6]**2 for i in range(6))


checks = []


def identity(name, lhs, rhs):
    residual = Poly.cast(lhs)-rhs
    if residual.terms:
        raise ArithmeticError(f'{name}: nonzero coefficients {residual.terms}')
    checks.append(name)


def main():
    t,a,b,p,v,w = [variable(i) for i in range(6)]
    h=-a-b
    e=[a,b,h,a,b,h]
    o=[p,v,w,-p,-v,-w]
    u=[ei+oi for ei,oi in zip(e,o)]
    x=[t+ui for ui in u]
    q=squares(u)
    r=adjacent(u)
    c=cubic(u)
    s2=squares(e)
    matrix=[[h,b,-a],[b,a,h],[-a,h,b]]
    z=[p,v,w]
    Fpoly=squares(x)**2-sum(x)*cubic(x)
    identity('zero centered sum',sum(u),0)
    identity('orthogonal opposite-pair split',sum(ei*oi for ei,oi in zip(e,o)),0)
    identity('centered norm',q,s2+squares(o))
    identity('variance',squares(x)-F(1,6)*sum(x)**2,q)
    identity('centering the cubic',cubic(x),6*t**3+t*(q+2*r)+c)
    identity('centering the quartic',Fpoly,q*q-6*t*c+6*t*t*(q-2*r))
    identity('quadratic remainder',q-2*r,2*s2+2*(p-v+w)**2)
    identity('cubic matrix decomposition',c,cubic(e)+2*sum(z[i]*matrix[i][j]*z[j] for i in range(3) for j in range(3)))
    identity('matrix trace zero',sum(matrix[i][i] for i in range(3)),0)
    identity('matrix square trace',sum(matrix[i][j]*matrix[j][i] for i in range(3) for j in range(3)),F(3,2)*s2)
    # Here t,a,b stand for independent scalar symbols |mean|, s, q.
    identity('final completion of square',b*b-6*t*a*b+12*t*t*a*a,12*(t*a-F(1,4)*b)**2+F(1,4)*b*b)
    examples=0
    for xval in product([-1,0,1], repeat=6):
        S=sum(xval); Q=sum(y*y for y in xval)
        C=sum(xval[i]*xval[(i+1)%6]**2 for i in range(6))
        centered=F(Q)-F(S*S,6)
        value=Q*Q-S*C
        if F(value)<centered**2/4:
            raise ArithmeticError(f'Remainder failed at {xval}')
        if (value==0)!=(len(set(xval))==1):
            raise ArithmeticError(f'Equality classification failed at {xval}')
        examples+=1
    report={'status':'PASS','arithmetic':'fractions.Fraction; exact rational coefficients','identities':checks,'regression_vectors':examples,'note':'The finite examples are not the proof. Matrix norm and Cauchy-Schwarz bounds are proved analytically in paper/main.tex.'}
    (ROOT/'certificates'/'identity_verification_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
