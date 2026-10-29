"""Exact counting and finite certificate for A181280; Python 3.9+, stdlib only.

Run from any directory: python path/to/src/verify.py
The proof that these finitely many values suffice is in paper/main.tex.
No fitted recurrence is used by this program.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [(i, j) for i in range(4) for j in range(i, 4)]


def gram_rows(g):
    rows = [0] * 4
    for k, (i, j) in enumerate(PAIRS):
        if (g >> k) & 1:
            rows[i] |= 1 << (3 - j)
            rows[j] |= 1 << (3 - i)
    return rows


def transitions():
    result = [[] for _ in range(8)]
    for s in range(8):
        for c in range(16):
            bits = [(c >> (3 - i)) & 1 for i in range(4)]
            t = s
            for i in range(3):
                if (s >> i) & 1:
                    continue
                if bits[i] > bits[i + 1]:
                    break
                if bits[i] < bits[i + 1]:
                    t |= 1 << i
            else:
                h = sum((bits[i] * bits[j]) << k
                        for k, (i, j) in enumerate(PAIRS))
                result[s].append((t, h))
    return result


def count_terms(last):
    tr = transitions()
    accepting = [g for g in range(1024)
                 if all(x > y for x, y in zip(gram_rows(g), gram_rows(g)[1:]))]
    v = [[0] * 1024 for _ in range(8)]
    v[0][0] = 1
    counts = []
    for n in range(last + 1):
        counts.append(sum(v[7][g] for g in accepting))
        if n == last:
            break
        w = [[0] * 1024 for _ in range(8)]
        for s in range(8):
            for t, h in tr[s]:
                for g, value in enumerate(v[s]):
                    w[t][g ^ h] += value
        v = w
    return counts, len(accepting)


def conjecture(n):
    # Algebraically identical to the six-term expression in the conjecture.
    return (Fraction(4**n * (6*n*n - 219*n + 820), 6144)
            - Fraction(2**n * (3*n + 32), 288)
            - Fraction(113 * (-8)**n, 49152)
            + Fraction(16**n, 512)
            - Fraction((-4)**n * (13*n - 164), 6144)
            + Fraction(8**n * (288*n - 3473), 147456))


def multiply(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i+j] += ai*bj
    return c


def product_roots(roots):
    p = [1]
    for r in roots:
        p = multiply(p, [-r, 1])
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--last', type=int, default=30)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    if args.last < 16:
        ap.error('--last must be at least 16')
    counts, terminal_count = count_terms(args.last)
    for n, a in enumerate(counts):
        expected = Fraction(0) if n < 4 else conjecture(n)
        assert expected.denominator == 1 and a == expected, (n, a, expected)
    level_roots = [[0, 2], [-2, 0, 2, 4], [-4, 0, 4, 8],
                   [-8, -4, 0, 4, 8, 16]]
    universal = product_roots([r for level in level_roots for r in level])
    assert len(universal) == 17
    for n in range(len(counts) - 16):
        assert sum(c * counts[n+k] for k, c in enumerate(universal)) == 0
    formula_roots = [2, 2, 4, 4, 4, -4, -4, 8, 8, -8, 16]
    minimal = product_roots(formula_roots)
    denominator = list(reversed(minimal))
    numerator = multiply(counts[:15], denominator)[:15]
    for n in range(15, len(counts)):
        assert sum(denominator[k] * counts[n-k]
                   for k in range(len(denominator))) == 0
    result = {
        'status': 'PASS', 'arithmetic': 'Python exact integers and Fraction',
        'number_of_states': 8192, 'accepting_Gram_patterns': terminal_count,
        'first_sixteen_counts': counts[:16], 'counts_n0_to_last': counts,
        'universal_annihilator_ascending': universal,
        'formula_annihilator_ascending': minimal,
        'generating_function_numerator_ascending': numerator,
        'generating_function_denominator_ascending': denominator,
        'formula_at_n0_to_3': [str(conjecture(n)) for n in range(4)],
        'proof_basis': 'Quadratic character sums and four-level filtration; see paper.'
    }
    print(json.dumps(result, indent=2))
    if args.write:
        out = ROOT / 'certificates' / 'direct_verification.json'
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
