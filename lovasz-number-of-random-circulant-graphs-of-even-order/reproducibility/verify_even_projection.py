#!/usr/bin/env python3
"""Exact auxiliary checks for the even-order tree-field projection.

Only Python's standard library is used. Fourier--Walsh polynomials are
stored as integer coefficient maps (frequency, sign-mask) -> coefficient.
The common factor n**(-number_of_leaves/2) is kept outside each map.
These finite checks concern the algebraic identities, not the asymptotic
estimates proved in the accompanying paper.
"""

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import product
import json
from math import factorial
from pathlib import Path
import sys


if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Run without -O or PYTHONOPTIMIZE: this verifier requires assertion checks.')


LEAF = ()
BINARY = (LEAF, LEAF)


def nodes(tree):
    return 1 + sum(nodes(child) for child in tree)


def leaves(tree):
    return sum(leaves(child) for child in tree) if tree else 1


def automorphisms(tree):
    result = 1
    for child, count in Counter(tree).items():
        result *= factorial(count) * automorphisms(child) ** count
    return result


def label_bit(residue, n):
    """The final bit is the self-inverse label h=n/2."""
    assert residue % n != 0
    return 1 << (min(residue % n, (-residue) % n) - 1)


def clean(poly):
    return {key: value for key, value in poly.items() if value}


@lru_cache(maxsize=None)
def canonical(tree, n):
    """Enumerate all leaf assignments directly, without polynomial products."""
    assert n % 2 == 0 and n >= 4
    output = Counter()
    for assignment in product(range(n), repeat=leaves(tree)):
        leaf_values = iter(assignment)
        flows = []

        def traverse(subtree):
            residue = (sum(traverse(child) for child in subtree) % n
                       if subtree else next(leaf_values))
            flows.append(residue)
            return residue

        root = traverse(tree)
        if any(residue in (0, n // 2) for residue in flows):
            continue
        bits = [label_bit(residue, n) for residue in flows]
        if len(set(bits)) != len(bits):
            continue
        mask = 0
        for bit in bits:
            mask |= bit
        output[root, mask] += 1
    return dict(output)


def multiply(left, right, n):
    result = Counter()
    for (frequency_a, mask_a), value_a in left.items():
        for (frequency_b, mask_b), value_b in right.items():
            result[(frequency_a + frequency_b) % n, mask_a ^ mask_b] += value_a * value_b
    return clean(result)


def power(poly, exponent, n):
    result = {(0, 0): 1}
    for _ in range(exponent):
        result = multiply(result, poly, n)
    return result


def hermite_field(tree, order, n):
    """H_order(Z_tree; aut(tree)), at common scale n**(-order*L/2)."""
    result = Counter()
    variance = automorphisms(tree)
    base = canonical(tree, n)
    for ell in range(order // 2 + 1):
        reduced = order - 2 * ell
        denominator = 2 ** ell * factorial(ell) * factorial(reduced)
        assert factorial(order) % denominator == 0
        coefficient = (factorial(order) // denominator
                       * (-variance) ** ell * n ** (ell * leaves(tree)))
        for key, value in power(base, reduced, n).items():
            result[key] += coefficient * value
    return clean(result)


def apply_operator(poly, n):
    """Apply the full graph operator, including its singleton multiplier."""
    result = Counter()
    for (frequency, mask), value in poly.items():
        if frequency:
            result[frequency, mask ^ label_bit(frequency, n)] += value
    return clean(result)


def project(poly, degree, n):
    singleton = 1 << (n // 2 - 1)
    return {key: value for key, value in poly.items()
            if bin(key[1]).count('1') == degree and not key[1] & singleton}


def energy_numerator(poly):
    """Parseval in spatial frequency and orthogonality in Walsh masks."""
    return sum(value * value for value in poly.values())


def difference(left, right):
    result = Counter(left)
    for key, value in right.items():
        result[key] -= value
    return clean(result)


def check_case(name, child_counts, n):
    tree = tuple(child for child, count in child_counts for _ in range(count))
    field = {(0, 0): 1}
    for child, count in child_counts:
        field = multiply(field, hermite_field(child, count, n), n)
    applied = apply_operator(field, n)
    predicted = canonical(tree, n)
    actual = project(applied, nodes(tree), n)
    assert actual == predicted, (name, n, 'projection identity failed')
    defect = difference(applied, predicted)
    assert energy_numerator(applied) == (energy_numerator(predicted)
                                         + energy_numerator(defect))
    twice = apply_operator(applied, n)
    nonconstant = {key: value for key, value in field.items() if key[0] != 0}
    assert twice == nonconstant, (name, n, 'K squared failed')
    singleton_bit = 1 << (n // 2 - 1)
    singleton_energy = sum(value * value for (_, mask), value in applied.items()
                           if mask & singleton_bit)
    return {
        'case': name, 'n': n, 'tree_nodes': nodes(tree),
        'tree_leaves': leaves(tree), 'tree_automorphisms': automorphisms(tree),
        'canonical_terms': len(predicted),
        'canonical_energy_numerator': energy_numerator(predicted),
        'singleton_defect_energy_numerator': singleton_energy,
        'energy_denominator': n ** leaves(tree),
        'projection_equal': True, 'orthogonal_energy_equal': True,
        'operator_square_equal': True,
    }


def check_leaf_correction(n):
    # At scale 1/n, 2Ke0 has coefficient 2 on every nonzero frequency,
    # while 2Z_leaf/sqrt(n) has coefficient 2 except at the singleton.
    full = {(residue, label_bit(residue, n)): 2 for residue in range(1, n)}
    paired = {key: 2 * value for key, value in canonical(LEAF, n).items()}
    correction = difference(full, paired)
    expected = {(n // 2, label_bit(n // 2, n)): 2}
    assert correction == expected
    # Sum of squares in space is n times the averaged Fourier energy.
    assert energy_numerator(correction) == 4
    return {'n': n, 'squared_euclidean_norm': '4/' + str(n), 'passed': True}


def run():
    orders = (4, 6, 8, 10, 12, 16, 18, 20, 24)
    cases = (
        ('binary root', ((LEAF, 2),)),
        ('four leaf root', ((LEAF, 4),)),
        ('leaf and binary child', ((LEAF, 1), (BINARY, 1))),
        ('two binary children', ((BINARY, 2),)),
    )
    records = [check_case(name, children, n)
               for n in orders for name, children in cases]
    assert sum(record['canonical_terms'] > 0 for record in records) >= 20
    assert any(record['singleton_defect_energy_numerator'] > 0 for record in records)
    return {
        'status': 'PASS',
        'scope': 'Exact finite Fourier-Walsh identities; no numerical asymptotic claim.',
        'orders': list(orders), 'projection_cases': len(records),
        'cases_with_nonzero_canonical_field': sum(record['canonical_terms'] > 0 for record in records),
        'records': records,
        'leaf_corrections': [check_leaf_correction(n) for n in orders],
        'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional JSON report path.')
    args = parser.parse_args()
    report = run()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('records', 'leaf_corrections')}, indent=2))
