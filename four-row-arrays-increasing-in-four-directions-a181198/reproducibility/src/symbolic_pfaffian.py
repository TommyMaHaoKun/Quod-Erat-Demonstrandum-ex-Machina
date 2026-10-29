"""Independent exact Pfaffian-integral enumeration of the four-row arrays.

Only the Python standard library is used. This computes the combinatorial
integral, not the proposed recurrence. See SYMBOLIC_NOTES.md for its derivation.
"""
from fractions import Fraction
from math import factorial, comb
import argparse
import json


def count(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    m = n - 1
    coefficients = [Fraction(2 * (-1) ** (m-i), factorial(i)*factorial(2*m-i))
                    for i in range(m)] + [Fraction(1, factorial(m)**2)]
    total = Fraction(0)
    for i, ci in enumerate(coefficients):
        for j, cj in enumerate(coefficients):
            # Integrals of the three terms in the 4 by 4 Pfaffian.
            term = (Fraction(1, (2*m-i+1)*(2*m+2)*(4*m-j+3))
                    - Fraction(1, (2*m-i+1)*(4*m-i-j+2)*(4*m-j+3))
                    + Fraction(1, (2*m-i+1)*(4*m-i-j+2)*(4*m-i+3)))
            total += ci*cj*term
    result = factorial(4*m+3)*total
    assert result.denominator == 1
    return result.numerator


def recurrence_residual(n: int, values: list[int]) -> int:
    p2 = 3*(n+1)*(2*n+3)*(3*n+4)*(3*n+5)*(7*n*n-1)*(n+2)**3
    p1 = 8*(n+1)*(2*n+1)*(4*n+3)*(4*n+5)*(364*n**5+84*n**4-1025*n**3-534*n*n+157*n+54)
    p0 = 64*(2*n-1)**2*(2*n+1)*(4*n-1)*(4*n+1)*(4*n+3)*(4*n+5)*(7*n*n+14*n+6)
    return p2*values[n+1]-p1*values[n]-p0*values[n-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=20)
    args = parser.parse_args()
    values = [count(n) for n in range(1, args.max_n+1)]
    residuals = [recurrence_residual(n, values) for n in range(1, args.max_n-1)]
    print(json.dumps({"method": "Pfaffian integral, exact rational arithmetic",
                      "values": {str(i+1): str(v) for i,v in enumerate(values)},
                      "recurrence_verified_through": args.max_n-2,
                      "all_residuals_zero": all(v == 0 for v in residuals)}, indent=2))
