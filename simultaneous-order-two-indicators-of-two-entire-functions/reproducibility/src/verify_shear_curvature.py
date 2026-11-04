"""Check the shear-curvature identity by exact formal polynomial arithmetic.

This checks a symbolic identity, not a numerical sample.  All first and mixed
derivatives are independent formal variables.  A and B stand for exp(-2u)
and exp(-2v); Laurent powers permit their inverses.  No third-party modules
or assertion-dependent checks are used.
"""

from fractions import Fraction
import json


NAMES = (
    "A", "B", "uz", "ub", "uzb", "vz", "vb", "vzb",
    "cz", "cb", "czb", "dz", "db", "dzb",
)
ZERO_EXPONENT = (0,) * len(NAMES)


class Poly:
    """A sparse Laurent polynomial over the rational numbers."""

    def __init__(self, terms=None):
        self.terms = {e: Fraction(c) for e, c in (terms or {}).items() if c}

    @staticmethod
    def constant(value):
        return Poly({ZERO_EXPONENT: Fraction(value)})

    @staticmethod
    def variable(name, power=1):
        exponent = list(ZERO_EXPONENT)
        exponent[NAMES.index(name)] = power
        return Poly({tuple(exponent): Fraction(1)})

    def __add__(self, other):
        if not isinstance(other, Poly):
            other = Poly.constant(other)
        result = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            result[exponent] = result.get(exponent, 0) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        if not isinstance(other, Poly):
            other = Poly.constant(other)
        result = {}
        for e1, c1 in self.terms.items():
            for e2, c2 in other.terms.items():
                exponent = tuple(a + b for a, b in zip(e1, e2))
                result[exponent] = result.get(exponent, 0) + c1 * c2
        return Poly(result)

    __rmul__ = __mul__


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(2)), Poly())
             for j in range(2)] for i in range(2)]


def main():
    A, B, uz, ub, uzb, vz, vb, vzb, cz, cb, czb, dz, db, dzb = (
        Poly.variable(name) for name in NAMES
    )
    invA, invB = Poly.variable("A", -1), Poly.variable("B", -1)
    zero = Poly()
    qinv = [[invA, zero], [zero, invB]]

    # In q=A|x|^2+B|y+cx|^2, d denotes the conjugate of c.
    # A constant holomorphic frame change makes c=d=0 at the base point.
    # Differentiation is performed BEFORE substituting c=d=0.
    qz = [[-2*A*uz, B*dz], [B*cz, -2*B*vz]]
    qb = [[-2*A*ub, B*db], [B*cb, -2*B*vb]]
    qzb = [
        [A*(4*uz*ub-2*uzb)+B*(cz*db+cb*dz),
         B*(dzb-2*vz*db-2*vb*dz)],
        [B*(czb-2*vz*cb-2*vb*cz), B*(4*vz*vb-2*vzb)],
    ]
    product = mm(mm(mm(qinv, qb), qinv), qz)
    second = mm(qinv, qzb)
    curvature = [[product[i][j]-second[i][j]
                  for j in range(2)] for i in range(2)]
    w = B*invA
    expected = [
        [2*uzb-w*cb*dz, -w*(dzb-2*(vb-ub)*dz)],
        [-czb+2*(vz-uz)*cb, 2*vzb+w*cb*dz],
    ]
    identities = []
    for i in range(2):
        for j in range(2):
            difference = curvature[i][j]-expected[i][j]
            if difference.terms:
                raise RuntimeError(f"Curvature entry ({i+1},{j+1}) differs")
            identities.append(f"K{i+1}{j+1}")

    # Trace cancels the shear term and equals -dbar d log det Q.
    trace_error = curvature[0][0]+curvature[1][1]-2*(uzb+vzb)
    if trace_error.terms:
        raise RuntimeError("Trace curvature identity differs")

    print(json.dumps({
        "status": "PASS_EXACT_SYMBOLIC_IDENTITIES",
        "identities": identities + ["trace"],
        "arithmetic": "sparse Laurent polynomials over Q",
        "independent_formal_variables": list(NAMES),
        "normalization": "conjugate K by diag(sqrt(A),sqrt(B))",
        "scope": "shear-curvature algebra; analytic construction reviewed separately",
    }, indent=2))


if __name__ == "__main__":
    main()
