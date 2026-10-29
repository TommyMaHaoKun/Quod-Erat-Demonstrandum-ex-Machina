"""Exact identity checks for paper/opposite_pair_proof.md; Python standard library.

This script verifies polynomial identities, not inequalities by sampling.
The remaining inequalities in the proof are applications of Cauchy--Schwarz
and nonnegativity of real squares.
"""

from collections import defaultdict


N = 6  # Independent indeterminates m, a, b, p, q, r.
ZERO_EXP = (0,) * N


class Poly:
    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {k: v for k, v in value.items() if v}
        elif isinstance(value, int):
            self.terms = {ZERO_EXP: value} if value else {}
        else:
            raise TypeError(value)

    def __add__(self, other):
        other = Poly(other)
        result = defaultdict(int, self.terms)
        for exp, coefficient in other.terms.items():
            result[exp] += coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({exp: -coefficient for exp, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        other = Poly(other)
        result = defaultdict(int)
        for exp1, coefficient1 in self.terms.items():
            for exp2, coefficient2 in other.terms.items():
                exp = tuple(a + b for a, b in zip(exp1, exp2))
                result[exp] += coefficient1 * coefficient2
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError(power)
        result = Poly(1)
        for _ in range(power):
            result *= self
        return result


def variable(index):
    exp = [0] * N
    exp[index] = 1
    return Poly({tuple(exp): 1})


CHECKS = []


def verify(name, lhs, rhs):
    remainder = Poly(lhs) - rhs
    if remainder.terms:
        raise AssertionError(f"{name}: nonzero remainder {remainder.terms}")
    CHECKS.append(name)
    print(f"PASS: {name}")


def dot(v, w):
    return sum(a * b for a, b in zip(v, w))


def matvec(matrix, v):
    return [dot(row, v) for row in matrix]


def main():
    m, a, b, p, q, r = [variable(i) for i in range(N)]
    c = -a - b
    e = [a, b, c, a, b, c]
    o = [p, q, r, -p, -q, -r]
    u = [s + t for s, t in zip(e, o)]
    x = [m + t for t in u]
    E, O, R = dot(e, e), dot(o, o), dot(u, u)
    A = sum(u[i] * u[(i + 1) % 6] for i in range(6))
    C = sum(u[i] * u[(i + 1) % 6] ** 2 for i in range(6))
    D = R - 2 * A
    v = [p, q, r]
    M = [[c, b, -a], [b, a, c], [-a, c, b]]
    vMv = dot(v, matvec(M, v))
    traceM2 = sum(M[i][j] * M[j][i] for i in range(3) for j in range(3))
    vv = dot(v, v)
    B3 = [[3 * v[i] * v[j] - (vv if i == j else 0)
           for j in range(3)] for i in range(3)]
    traceB3sq = sum(B3[i][j] * B3[j][i]
                   for i in range(3) for j in range(3))
    traceMB3 = sum(M[i][j] * B3[j][i]
                  for i in range(3) for j in range(3))
    SX = sum(x)
    QX = dot(x, x)
    TX = sum(x[i] * x[(i + 1) % 6] ** 2 for i in range(6))
    F = QX ** 2 - SX * TX

    verify("mean zero", sum(u), 0)
    verify("opposite-pair orthogonality", dot(e, o), 0)
    verify("R = E + O", R, E + O)
    verify("D = 2E + 2(p-q+r)^2", D, 2 * E + 2 * (p - q + r) ** 2)
    verify("cubic opposite-pair formula", C,
           2 * (a * b ** 2 + b * c ** 2 + c * a ** 2) + 2 * vMv)
    verify("matrix trace zero", sum(M[i][i] for i in range(3)), 0)
    verify("2 tr(M^2) = 3E", 2 * traceM2, 3 * E)
    verify("O = 2 ||v||^2", O, 2 * vv)
    verify("tr((3vv^T-||v||^2I)^2) = 6 ||v||^4", traceB3sq, 6 * vv ** 2)
    verify("tr(M(3vv^T-||v||^2I)) = 3v^TMv", traceMB3, 3 * vMv)
    verify("sum x = 6m", SX, 6 * m)
    verify("quadratic mean decomposition", QX, 6 * m ** 2 + R)
    verify("cubic mean decomposition", TX, 6 * m ** 3 + m * (R + 2 * A) + C)
    verify("quartic difference identity", F, R ** 2 - 6 * m * C + 6 * m ** 2 * D)
    # This separate two-variable identity is 4 times the final completion of
    # the square, using independent indeterminates a and b for R and z.
    verify("final square completion", 4 * (a ** 2 - 6 * a * b + 12 * b ** 2),
           a ** 2 + 3 * (4 * b - a) ** 2)
    print(f"\nAll {len(CHECKS)} polynomial identities verified exactly over Z.")


if __name__ == "__main__":
    main()
