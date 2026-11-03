"""Exact, independent finite checks for the Bernstein elevation proof.

Python 3.9+, standard library only. Run: python src/verify.py
The universal theorem is proved in the paper, not by this finite check.
"""
from fractions import Fraction as Q
from math import comb
import json


def ceiling(x):
    return -(-x.numerator // x.denominator)


def elevate(coefficients):
    """Standard one-step Bernstein degree elevation, not the closed formula."""
    new_degree = len(coefficients)
    result = []
    for i in range(new_degree + 1):
        left = coefficients[i - 1] if i else Q(0)
        right = coefficients[i] if i < new_degree else Q(0)
        result.append((i * left + (new_degree - i) * right) / new_degree)
    return result


def closed(m, r):
    c = [Q(0)] * (2 * m + r + 1)
    for j in range(r + 1):
        c[m + j] = Q(4**m * comb(r, j), comb(2 * m + r, m + j))
    return c


def product(m, r):
    R = 2 * ((r + 1) // 2)
    p = Q(1)
    for ell in range(1, m + 1):
        p *= Q(R + 2 * ell, R + 2 * ell - 1)
    return p


def max_closed(m, r):
    return Q(4**m * comb(r, r // 2), comb(2 * m + r, m + r // 2))


def main():
    cases = 0
    for m in range(1, 31):
        actual = [Q(0)] * (2 * m + 1)
        actual[m] = Q(4**m, comb(2 * m, m))
        for r in range(81):
            explicit = closed(m, r)
            assert actual == explicit
            peak = max(actual)
            indices = [i for i, v in enumerate(actual) if v == peak]
            expected = sorted({m + r // 2, m + (r + 1) // 2})
            assert indices == expected
            if r:
                R = 2 * ((r + 1) // 2)
                assert peak == product(m, r)
                assert peak**2 < Q(R + 2 * m, R) <= Q(r + 2 * m, r)
                if r % 2:
                    assert peak == max_closed(m, r + 1)
            cases += 1
            actual = elevate(actual)

    height_cases = 0
    integer_boundaries = 0
    heights = sorted({Q(a, b) for b in range(2, 31) for a in range(1, b)})
    for m in range(1, 21):
        for h in heights:
            if h * 4**m <= comb(2 * m, m):
                continue
            T = 2 * m * h**2 / (1 - h**2)
            r = 2 * ceiling(T / 2) - 1
            assert 1 <= r <= ceiling(T) <= T.numerator // T.denominator + 1
            assert h * max_closed(m, r) < 1
            assert h * max_closed(m, ceiling(T)) < 1
            height_cases += 1
            integer_boundaries += T.denominator == 1
    assert max_closed(1, 1) * Q(3, 4) == 1
    assert closed(1, 1) == [Q(0), Q(4, 3), Q(4, 3), Q(0)]
    assert Q(32) * Q(3, 5)**2 / (1 - Q(3, 5)**2) == 18
    assert max_closed(16, 17) * Q(3, 5) < 1
    print(json.dumps({
        "status": "PASS",
        "coefficient_recurrence_cases": cases,
        "admissible_height_cases": height_cases,
        "integer_boundary_cases": integer_boundaries,
        "arithmetic": "exact rational and integer",
        "universal_proof": "paper/main.tex, Theorem 1 and Lemmas 2-3",
    }, indent=2))


if __name__ == "__main__":
    main()
