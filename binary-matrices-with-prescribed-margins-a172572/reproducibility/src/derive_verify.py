"""Independent exact-arithmetic checks for the Hermite proof (standard library only).

Run from any working directory: python src/derive_verify.py
The finite moment checks are diagnostics; the symbolic polynomial identities
and the integration-by-parts proof in notes/derivation.md establish all indices.
"""
from fractions import Fraction
from math import factorial, comb
import json
from pathlib import Path


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, v in enumerate(a):
        c[i] += v
    for i, v in enumerate(b):
        c[i] += v
    return c


def neg(a):
    return [-v for v in a]


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i + j] += u * v
    return c


def scale(a, k):
    return [v * k for v in a]


def power(a, k):
    r = [1]
    for _ in range(k):
        r = mul(r, a)
    return r


def shift(a, k):
    r = [0]
    for i, v in enumerate(a):
        r = add(r, scale(power([k, 1], i), v))
    return r


def evaluate(a, n):
    r = 0
    for v in reversed(a):
        r = r * n + v
    return r


def gaussian_expectation(a):
    moment = 1
    result = 0
    for j in range(0, len(a), 2):
        if j:
            moment *= j - 1
        result += a[j] * moment
    return result


F = [5, 43, 145, 204, 102]
G = [36, 93, 62]
H = [5, 31, 62]
P = [601185, 1653960, 1884032, 1137319, 383756, 68634, 5084]
Q = [827860, 2220988, 2354425, 1227805, 313720, 31372]


def symbolic_checks():
    r1 = add(add(mul(G, shift(F, 1)),
                 neg(scale(mul(shift(G, 1), power([1, 1], 4)), 20))),
             neg(shift(P, -1)))
    r2 = add(add(add(scale(mul(mul(G, shift(G, 1)), H), 18),
                         scale(mul(mul(G, power([1, 1], 2)),
                                   add(scale(power([1, 1], 2), 4), [-1])), 50)),
                     neg(scale(mul(shift(G, 1), F), 720))),
                 scale(mul([1, 2], shift(Q, -1)), 4))
    assert not any(r1), r1
    assert not any(r2), r2
    return [r1, r2]


def hermites(max_n):
    polys = [[1], [0, 1]]
    for n in range(1, max_n):
        polys.append(add(mul([0, 1], polys[-1]), scale(polys[-2], -n)))
    return polys


def scaled_state(n, polynomials):
    hn = Fraction(factorial(2 * n), factorial(n) ** 5)
    y, u = polynomials[n], polynomials[n - 1]
    moments = [gaussian_expectation(mul(power(y, 6 - k), power(u, k)))
               for k in [2, 4, 6]]
    return [5 * n ** k * hn * value
            for k, value in zip([1, 3, 5], moments)]


def transition(n, state):
    x, y, z = state
    f, g, h = [evaluate(p, n) for p in [F, G, H]]
    return [(6 * f * x - 9 * n * g * y - 5 * n * (2 * n + 1) * z) / (n + 1) ** 4,
            (2 * h * x - 120 * n * y) / (n + 1),
            10 * (2 * n + 1) * (n + 1) * x]


def main():
    residues = symbolic_checks()
    polynomials = hermites(10)
    bs = [Fraction(factorial(2 * n), factorial(n) ** 5)
          * gaussian_expectation(power(polynomials[n], 6)) for n in range(11)]
    assert all(v.denominator == 1 for v in bs)
    counts = [int(v) * comb(3 * n, n) for n, v in enumerate(bs)]
    assert counts[:4] == [1, 90, 67950, 90291600]
    assert scaled_state(1, polynomials) == [30, 10, 10]
    assert scaled_state(2, polynomials) == [4530, 2340, 1800]
    for n in range(1, 10):
        state = scaled_state(n, polynomials)
        assert transition(n, state) == scaled_state(n + 1, polynomials), n
        assert state[0] == bs[n], n
        assert state[2] == 10 * n * (2 * n - 1) * bs[n - 1], n
    for n in range(8):
        r = ((n + 3) ** 4 * (62 * n * n + 217 * n + 191) * bs[n + 3]
             - 6 * evaluate(P, n) * bs[n + 2]
             - 4 * (2 * n + 3) * evaluate(Q, n) * bs[n + 1]
             + 6000 * (n + 1) ** 2 * (2 * n + 1) * (2 * n + 3)
             * (62 * n * n + 341 * n + 470) * bs[n])
        assert r == 0, (n, r)
    result = {
        'method': 'Independent standard-library exact integer/Fraction arithmetic',
        'symbolic_elimination_residual_coefficients': residues,
        'hermite_transition_indices_verified': [1, 9],
        'recurrence_diagnostic_indices_verified': [0, 7],
        'normalized_initial_state_n1': [30, 10, 10],
        'normalized_initial_state_n2': [4530, 2340, 1800],
        'a_n_0_through_10': counts,
        'b_n_0_through_10': [int(v) for v in bs],
        'proof_boundary': 'Finite diagnostics do not themselves prove the recurrence; the exact identities verify the algebra in the all-index Hermite argument.'
    }
    out = Path(__file__).resolve().parent.parent / 'certificates' / 'independent_derivation_checks.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('PASS: symbolic identities, exact Hermite transitions, initial values, and recurrence diagnostics.')
    print(out)


if __name__ == '__main__':
    main()
