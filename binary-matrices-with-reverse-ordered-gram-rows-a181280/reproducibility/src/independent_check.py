#!/usr/bin/env python3
"""Independent, standard-library-only proof checker for A181280.

This file imports no project module.  It uses interval partitions and Boolean
quadratic characters, rather than the primary Gram-parity transfer system.
Run: python -B src/independent_check.py
Optional: --max-brute 7 --output certificates/independent_check.json
"""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import sys


PAIRS = tuple((i, j) for i in range(4) for j in range(i, 4))
COLUMNS = tuple(product((0, 1), repeat=4))
# Products of the distinct roots on the four partition levels.
LEVEL_ROOTS = (
    (0, 2),
    (-2, 0, 2, 4),
    (-4, 0, 4, 8),
    (-8, -4, 0, 4, 8, 16),
)


def interval_partitions():
    """All ordered partitions into nonempty consecutive row-index blocks."""
    result = []
    for number_of_cuts in range(4):
        for cuts in combinations((1, 2, 3), number_of_cuts):
            boundaries = (0,) + cuts + (4,)
            result.append(tuple(tuple(range(a, b))
                                for a, b in zip(boundaries, boundaries[1:])))
    return tuple(result)


PARTITIONS = interval_partitions()
PARTITION_INDEX = {partition: i for i, partition in enumerate(PARTITIONS)}


def polynomial_from_roots(roots):
    """Integer coefficients, increasing powers."""
    coefficients = [1]
    for root in roots:
        new = [0] * (len(coefficients) + 1)
        for i, coefficient in enumerate(coefficients):
            new[i] -= root * coefficient
            new[i + 1] += coefficient
        coefficients = new
    return coefficients


def matrix_product(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(8))
             for j in range(8)] for i in range(8)]


def identity_matrix():
    return [[int(i == j) for j in range(8)] for i in range(8)]


def quadratic_value(character, column):
    return sum(coefficient * column[i] * column[j]
               for coefficient, (i, j) in zip(character, PAIRS)) % 2


def transition_matrix(character):
    matrix = [[0] * 8 for _ in range(8)]
    for state, partition in enumerate(PARTITIONS):
        for column in COLUMNS:
            refined = []
            for block in partition:
                digits = tuple(column[i] for i in block)
                if digits != tuple(sorted(digits)):
                    break
                zeros = tuple(i for i in block if column[i] == 0)
                ones = tuple(i for i in block if column[i] == 1)
                refined.extend(piece for piece in (zeros, ones) if piece)
            else:
                destination = PARTITION_INDEX[tuple(refined)]
                matrix[state][destination] += (-1) ** quadratic_value(character, column)
    return matrix


def descending_gram_coordinates():
    result = []
    for coordinates in product((0, 1), repeat=10):
        gram = [[0] * 4 for _ in range(4)]
        for bit, (i, j) in zip(coordinates, PAIRS):
            gram[i][j] = gram[j][i] = bit
        rows = list(map(tuple, gram))
        if all(rows[i] > rows[i + 1] for i in range(3)):
            result.append(coordinates)
    return result


def multiply_row(row, matrix):
    return [sum(row[i] * matrix[i][j] for i in range(8))
            for j in range(8)]


def fourier_check():
    accepted = descending_gram_coordinates()
    observed_roots = [set() for _ in range(4)]
    totals = [0] * 16
    nonzero_fourier = 0
    for character in product((0, 1), repeat=10):
        coefficient = sum((-1) ** (sum(x * y for x, y in zip(character, gram)) % 2)
                          for gram in accepted)
        nonzero_fourier += coefficient != 0
        matrix = transition_matrix(character)
        for i, partition in enumerate(PARTITIONS):
            level = len(partition) - 1
            diagonal = matrix[i][i]
            observed_roots[level].add(diagonal)
            assert diagonal in LEVEL_ROOTS[level]
            for j, other in enumerate(PARTITIONS):
                if i != j and len(partition) >= len(other):
                    assert matrix[i][j] == 0

        # Evaluate the actual complete annihilating matrix product.  This is
        # stronger than a scalar fit: P(T_character) is the zero 8x8 matrix.
        residual = identity_matrix()
        for roots in LEVEL_ROOTS:
            for root in roots:
                factor = [[matrix[i][j] - root * int(i == j)
                           for j in range(8)] for i in range(8)]
                residual = matrix_product(residual, factor)
        assert not any(any(row) for row in residual)

        vector = [1] + [0] * 7
        for n in range(16):
            totals[n] += coefficient * vector[-1]
            vector = multiply_row(vector, matrix)
    assert all(value % 1024 == 0 for value in totals)
    counts = [value // 1024 for value in totals]
    assert all(observed_roots[i] == set(LEVEL_ROOTS[i]) for i in range(4))
    return counts, len(accepted), nonzero_fourier, [sorted(s) for s in observed_roots]


def formula(n):
    """The published six terms, evaluated as exact rational arithmetic."""
    two = Fraction(2)
    return (two ** (2*n-11) * Fraction(6*n*n-219*n+820, 3)
            - two ** (n-5) * Fraction(3*n+32, 9)
            - (-1)**n * two ** (3*n-14) * Fraction(113, 3)
            + two ** (4*n-9)
            - (-1)**n * two ** (2*n-11) * Fraction(13*n-164, 3)
            + two ** (3*n-14) * Fraction(288*n-3473, 9))


def direct_enumeration(n):
    """Increasing integers encode increasing binary rows, leading zeros kept."""
    size = 1 << n
    parity = [bin(i).count('1') % 2 for i in range(size)]
    inner = [[parity[a & b] for b in range(size)] for a in range(size)]
    count = 0
    example = None
    for rows in combinations(range(size), 4):
        gram_rows = tuple(tuple(inner[a][b] for b in rows) for a in rows)
        if all(gram_rows[i] > gram_rows[i+1] for i in range(3)):
            count += 1
            if example is None:
                example = {'rows_as_integers': rows, 'gram_rows': gram_rows}
    return count, example


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-brute', type=int, default=6)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not 0 <= args.max_brute <= 8:
        parser.error('--max-brute must lie between 0 and 8')
    counts, number_accepted, nonzero_fourier, observed = fourier_check()
    roots = tuple(root for level in LEVEL_ROOTS for root in level)
    multiplicities = Counter(roots)
    # Each exponential-polynomial summand is annihilated by these factors.
    required = {4: 3, 2: 2, -8: 1, 16: 1, -4: 2, 8: 2}
    assert all(multiplicities[root] >= exponent for root, exponent in required.items())
    assert multiplicities[0] == 4
    assert counts[:4] == [0, 0, 0, 0]
    assert all(Fraction(counts[n]) == formula(n) for n in range(4, 16))
    brute = {}
    for n in range(args.max_brute + 1):
        count, example = direct_enumeration(n)
        assert count == counts[n]
        brute[str(n)] = {'count': count, 'first_example': example}
    report = {
        'result': 'PASS',
        'python': sys.version.split()[0],
        'method': 'Independent interval-partition Fourier matrices and direct row enumeration',
        'proof_bridge': 'P(T)=0 for every character; the corrected target obeys the same monic degree-16 recurrence and agrees at n=0,...,15.',
        'characters_checked': 1024,
        'matrix_dimensions': [8, 8],
        'all_matrix_polynomial_residuals_zero': True,
        'gram_acceptance_count': number_accepted,
        'nonzero_fourier_coefficients': nonzero_fourier,
        'observed_level_roots': observed,
        'annihilator_coefficients_in_increasing_order': polynomial_from_roots(roots),
        'counts_n0_through_n15': counts,
        'direct_enumeration': brute,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
