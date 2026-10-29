"""Exact independent counts for A172572; uses only the Python standard library.

Two independent coefficient evaluations are compared: a recursion choosing the
two occupied columns of the first row, and the identity 2*e_2=e_1**2-p_2.
The checks of the proposed recurrence are finite diagnostics, not its proof.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import json
from math import comb, factorial
from pathlib import Path


@lru_cache(maxsize=None)
def row_count(margins: tuple[int, ...]) -> int:
    """Number of ordered remaining rows for a sorted six-column margin tuple."""
    total = sum(margins)
    if total == 0:
        return 1
    if total % 2 or margins[-1] > total // 2:
        return 0
    classes = Counter(margins)
    positive = sorted(v for v in classes if v)
    count = 0
    for ai, a in enumerate(positive):
        for b in positive[ai:]:
            multiplicity = (comb(classes[a], 2) if a == b
                            else classes[a] * classes[b])
            if not multiplicity:
                continue
            rest = list(margins)
            rest.remove(a)
            rest.remove(b)
            rest.extend((a - 1, b - 1))
            count += multiplicity * row_count(tuple(sorted(rest)))
    return count


def convolution(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def coefficient_count(n: int) -> int:
    """Evaluate [x_1^n ... x_6^n] e_2(x)^(3*n) via an alternating sum."""
    nf = factorial(n)
    h = [nf // (factorial(r) * factorial(n - 2*r))
         for r in range(n // 2 + 1)]
    h6 = [1]
    for _ in range(6):
        h6 = convolution(h6, h)
    numerator = factorial(3*n) * sum(
        (-1)**k * factorial(6*n - 2*k) // factorial(3*n - k) * coefficient
        for k, coefficient in enumerate(h6)
    )
    denominator = 2**(3*n) * nf**6
    result, remainder = divmod(numerator, denominator)
    assert remainder == 0, (n, remainder)
    return result


def recurrence_residual(n: int, b: list[int]) -> int:
    p = (5084*n**6 + 68634*n**5 + 383756*n**4 + 1137319*n**3
         + 1884032*n**2 + 1653960*n + 601185)
    q = (31372*n**5 + 313720*n**4 + 1227805*n**3 + 2354425*n**2
         + 2220988*n + 827860)
    return ((n+3)**4 * (62*n*n+217*n+191) * b[n+3]
            - 6*p*b[n+2] - 4*(2*n+3)*q*b[n+1]
            + 6000*(n+1)**2*(2*n+1)*(2*n+3)
            * (62*n*n+341*n+470)*b[n])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=100)
    parser.add_argument('--dp-max-n', type=int, default=15)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    assert 3 <= args.max_n and 0 <= args.dp_max_n <= args.max_n
    counts = [coefficient_count(n) for n in range(args.max_n + 1)]
    assert counts[:4] == [1, 90, 67950, 90291600]
    for n in range(args.dp_max_n + 1):
        assert row_count((n,)*6) == counts[n], n
    normalized = []
    for n, count in enumerate(counts):
        value, remainder = divmod(count, comb(3*n, n))
        assert not remainder, n
        normalized.append(value)
    residuals = [recurrence_residual(n, normalized)
                 for n in range(args.max_n - 2)]
    assert all(value == 0 for value in residuals)
    report = {
        'status': 'FINITE_CHECKS_PASSED',
        'note': 'These finite checks do not prove the infinite recurrence.',
        'coefficient_max_n': args.max_n,
        'independent_row_dp_max_n': args.dp_max_n,
        'recurrence_checked_n': [0, args.max_n - 3],
        'a': [str(value) for value in counts],
        'b': [str(value) for value in normalized],
        'recurrence_residuals': residuals,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f'PASS: coefficient counts n=0..{args.max_n}; independent row DP '
          f'n=0..{args.dp_max_n}; recurrence n=0..{args.max_n - 3}.')
    print('a(0..3) =', counts[:4])
    print('b(0..5) =', normalized[:6])


if __name__ == '__main__':
    main()
