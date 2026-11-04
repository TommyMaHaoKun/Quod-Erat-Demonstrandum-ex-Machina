"""Independent exact model and point checks using only Python's standard library.

This verifies the algebraic bridge and the named points. The global point
classification is checked separately by verify_quintic.m in Magma.
"""
from fractions import Fraction as F
import json
from pathlib import Path

H = (1, 3, -3, -4, 1)  # r^5 = -sum(H[i]*r^i).


class K:
    def __init__(self, values=0):
        if isinstance(values, K):
            self.c = values.c
        elif isinstance(values, (int, F)):
            self.c = (F(values),) + (F(0),)*4
        else:
            values = list(map(F, values))
            self.c = tuple(values + [F(0)]*(5-len(values)))

    def __add__(self, other):
        other = K(other)
        return K(a+b for a, b in zip(self.c, other.c))
    __radd__ = __add__

    def __neg__(self):
        return K(-a for a in self.c)

    def __sub__(self, other):
        return self + -K(other)

    def __rsub__(self, other):
        return K(other) + -self

    def __mul__(self, other):
        other = K(other)
        values = [F(0)]*9
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                values[i+j] += a*b
        for j in range(8, 4, -1):
            for i, a in enumerate(H):
                values[j-5+i] -= a*values[j]
        return K(values[:5])
    __rmul__ = __mul__

    def __pow__(self, exponent):
        if exponent < 0:
            return self.inverse()**(-exponent)
        answer, base = K(1), self
        while exponent:
            if exponent & 1:
                answer *= base
            base *= base
            exponent //= 2
        return answer

    def inverse(self):
        if self == 0:
            raise ZeroDivisionError()
        columns = [(self*K([0]*i+[1])).c for i in range(5)]
        matrix = [[columns[j][i] for j in range(5)] + [F(i == 0)] for i in range(5)]
        for j in range(5):
            pivot = next(i for i in range(j, 5) if matrix[i][j])
            matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
            scale = matrix[j][j]
            matrix[j] = [a/scale for a in matrix[j]]
            for i in range(5):
                if i != j:
                    scale = matrix[i][j]
                    matrix[i] = [a-scale*b for a, b in zip(matrix[i], matrix[j])]
        result = K(matrix[i][-1] for i in range(5))
        assert self*result == 1
        return result

    def __truediv__(self, other):
        return self*K(other).inverse()

    def __eq__(self, other):
        return self.c == K(other).c


def padd(a, b):
    out = [K(0)]*max(len(a), len(b))
    for i, value in enumerate(a): out[i] += value
    for i, value in enumerate(b): out[i] += value
    return out


def pmul(a, b):
    out = [K(0)]*(len(a)+len(b)-1)
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            out[i+j] += left*right
    return out


def ppow(a, n):
    result = [K(1)]
    for _ in range(n): result = pmul(result, a)
    return result


def mod2_remainder(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length()-b.bit_length())
    return a


def main():
    if not __debug__:
        raise RuntimeError("Run without -O or PYTHONOPTIMIZE: verification requires assertions.")
    # A reducible degree-five polynomial has a factor of degree at most two.
    # These are all monic irreducibles of degree one or two over F_2.
    for polynomial in (0b101001, 0b110111):
        assert all(mod2_remainder(polynomial, divisor) for divisor in (0b10, 0b11, 0b111))

    r = K([0, 1])
    alpha = r-r**2-r**3
    assert r**5+r**4-4*r**3-3*r**2+3*r+1 == 0
    assert alpha**5+6*alpha**4-alpha**3-10*alpha**2-6*alpha-1 == 0
    k = r-1
    b = -2*r**4-4*r**3+6*r**2+11*r-4
    A = 2*r**4-r**3-8*r**2+2*r+4
    B = 5*r**4+4*r**3-r**2-6*r-41
    C = -11*r**4+77*r**2-132
    assert b*b == 11*(4-r*r)
    assert b != 0 and k != 0
    q = [alpha**4+6*alpha**3-alpha**2-10*alpha-6,
         alpha**3+6*alpha**2-alpha-10,
         alpha**2+6*alpha-1, alpha+6, K(1)]
    target_f = [-1, -6, -10, -1, 6, 1]
    assert pmul(q, [-alpha, K(1)]) == [K(v) for v in target_f]
    d = [b, k]
    lhs = [K(0)]
    for i in range(5):
        lhs = padd(lhs, [K(0)]*i + [q[i]*v for v in ppow(d, 4-i)])
    rhs = [b*b*v for v in (C, B, A, K(1), K(0))]
    assert lhs == rhs

    def on_curve(point):
        x, y = point
        return y*y == x**3+A*x*x+B*x+C

    def add(point, other):
        if point is None: return other
        if other is None: return point
        x, y = point
        u, v = other
        if x == u and y == -v: return None
        if x == u:
            slope = (3*x*x+2*A*x+B)/(2*y)
        else:
            slope = (v-y)/(u-x)
        xx = slope*slope-A-x-u
        answer = (xx, -y+slope*(x-xx))
        assert on_curve(answer)
        return answer

    T1 = (-r**4+5*r**2+r-6, K(0))
    T2 = (-2*r**4+2*r**3+9*r**2-7*r-6, K(0))
    P = (7*r**4+r**3-22*r**2-5*r+11,
         8*r**4-19*r**3-r**2+31*r-23)
    assert all(on_curve(point) for point in (T1, T2, P))
    assert T1 != T2 and add(T1, T1) is None and add(T2, T2) is None
    for point in (add(T2, P), add(T2, (P[0], -P[1]))):
        x, y = point
        assert k*x+b == 0
        assert x == -b/k and (y == b/k**2 or y == -b/k**2)

    result = {
        "status": "PASS_EXACT_MODEL_AND_POINT_IDENTITIES",
        "implementation": "Python standard library; rational coefficient field arithmetic",
        "polynomial": "x^5+6*x^4-x^3-10*x^2-6*x-1",
        "checks": ["irreducibility modulo 2", "root-field representation",
                   "quartic factorization", "birational model identity",
                   "two-torsion points and free-subgroup generator on curve",
                   "T2+P and T2-P are exactly the two points above infinity"],
        "global_point_classification": "verified separately by verify_quintic.m",
    }
    dest = Path(__file__).resolve().parents[1]/"certificates"/"model_identities.json"
    dest.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
