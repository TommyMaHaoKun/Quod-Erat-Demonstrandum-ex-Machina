"""Exact Fourier certificate for A181280. Python 3.9+, standard library only.

This derives counts from the definition, not from the proposed formula. The
all-length bridge is the proved level-filtration annihilator documented in
notes/fourier_proof.md. No floating point or probabilistic checks are used.
"""
import argparse
from collections import Counter
from fractions import Fraction
import json

PAIRS = tuple((i, j) for i in range(4) for j in range(i, 4))


def parity(x):
    return bin(x).count('1') & 1


def dot_character(h, g):
    return 1 - 2 * parity(h & g)


def column_gram(c):
    return sum(((c >> i & 1) & (c >> j & 1)) << k
               for k, (i, j) in enumerate(PAIRS))


def accepted(g):
    rows = [0] * 4
    for k, (i, j) in enumerate(PAIRS):
        b = g >> k & 1
        rows[i] |= b << (3 - j)
        rows[j] |= b << (3 - i)
    return all(rows[i] > rows[i + 1] for i in range(3))


def next_mask(s, c):
    t = s
    for i in range(3):
        if not (s >> i & 1):
            a, b = c >> i & 1, c >> (i + 1) & 1
            if a > b:
                return None
            if a < b:
                t |= 1 << i
    return t


def weighted_transitions(h):
    rows = []
    for s in range(8):
        row = [0] * 8
        for c in range(16):
            t = next_mask(s, c)
            if t is not None:
                row[t] += dot_character(h, column_gram(c))
        rows.append(row)
    return rows


def step(v, matrix):
    return [sum(v[s] * matrix[s][t] for s in range(8)) for t in range(8)]


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


LEVEL_ROOTS = ((0, 2), (-2, 0, 2, 4), (-4, 0, 4, 8),
               (-8, -4, 0, 4, 8, 16))


def annihilator():
    p = [1]
    for roots in LEVEL_ROOTS:
        for root in roots:
            p = mul(p, [-root, 1])
    return p


def pow2(e):
    return Fraction(2**e) if e >= 0 else Fraction(1, 2**(-e))


def conjectured(n):
    if n < 4:
        return Fraction(0)
    return (pow2(2*n-11) * (6*n*n-219*n+820)/3
            - pow2(n-5) * (3*n+32)/9
            - 113*(-1)**n*pow2(3*n-14)/3
            + pow2(4*n-9)
            - (-1)**n*pow2(2*n-11)*(13*n-164)/3
            + pow2(3*n-14)*(288*n-3473)/9)


def walsh_spectrum(b):
    pairs = [(i,j) for i in range(b) for j in range(i,b)]
    spectrum = Counter()
    monomials = [sum(((c>>i&1)&(c>>j&1))<<k
                     for k,(i,j) in enumerate(pairs)) for c in range(1<<b)]
    for q in range(1<<len(pairs)):
        spectrum[sum(dot_character(q, c) for c in monomials)] += 1
    return dict(sorted(spectrum.items()))


def prove(max_n=20, check_all_vectors=False):
    good = [g for g in range(1024) if accepted(g)]
    totals = [0]*(max_n+1)
    weights = []
    observed = [set() for _ in range(4)]
    polynomial = annihilator()
    for h in range(1024):
        weight = sum(dot_character(h, g) for g in good)
        weights.append(weight)
        matrix = weighted_transitions(h)
        for s in range(8):
            level = bin(s).count('1')
            observed[level].add(matrix[s][s])
            assert matrix[s][s] in LEVEL_ROOTS[level]
            assert all(not matrix[s][t] or s & t == s for t in range(8))
        v = [1] + [0]*7
        for n in range(max_n+1):
            totals[n] += weight*v[7]
            v = step(v, matrix)
        if check_all_vectors:
            # Horner evaluation at every basis vector, so P(T_h)=0 exactly.
            for initial in range(8):
                base = [int(i==initial) for i in range(8)]
                residual = [polynomial[-1]*x for x in base]
                for coeff in reversed(polynomial[:-1]):
                    residual = [a+coeff*b for a,b in zip(step(residual,matrix),base)]
                assert residual == [0]*8, (h, initial, residual)
    assert all(x % 1024 == 0 for x in totals)
    counts = [x//1024 for x in totals]
    assert max_n >= 15
    assert all(Fraction(a) == conjectured(n) for n,a in enumerate(counts))
    assert tuple(tuple(sorted(x)) for x in observed) == LEVEL_ROOTS
    # The recurrence beyond initial 16 is a consistency check, not its proof.
    for n in range(max_n-15):
        assert sum(c*counts[n+j] for j,c in enumerate(polynomial)) == 0
    # Scalar minimal eventual denominator predicted by six terms.
    d=[1]
    for root,multiplicity in [(2,2),(4,3),(-4,2),(8,2),(-8,1),(16,1)]:
        for _ in range(multiplicity):
            d=mul(d,[1,-root])
    # P(E)a=0 implies D_all(z) A(z) has degree at most 15.
    # Compute that entire polynomial, then divide the extraneous (1+2z)
    # exactly. This is a certified GF, not rational interpolation.
    d_all=mul(d,[1,2])
    n_all=[sum(d_all[j]*counts[n-j]
               for j in range(min(n,len(d_all)-1)+1)) for n in range(16)]
    numerator=[]
    for n in range(15):
        numerator.append(n_all[n]-(2*numerator[-1] if n else 0))
    assert n_all[15] == 2*numerator[14]
    assert mul(numerator,[1,2]) == n_all
    for n in range(16,max_n+1):
        assert sum(d_all[j]*counts[n-j] for j in range(len(d_all))) == 0
    return {'method':'Fourier character decomposition and level filtration',
            'accepted_symmetric_gram_masks':good,
            'accepted_symmetric_gram_count':len(good),
            'character_weight_distribution':dict(sorted(Counter(weights).items())),
            'walsh_spectra':{str(b):walsh_spectrum(b) for b in range(1,5)},
            'annihilator_coefficients_ascending':polynomial,
            'required_initial_range':[0,15],
            'checked_range':[0,max_n],
            'counts':counts,
            'generating_function_denominator_ascending':d,
            'generating_function_numerator_ascending':numerator,
            'all_1024_matrix_polynomial_checks':check_all_vectors,
            'result':'PASS'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n',type=int,default=20)
    parser.add_argument('--check-all-vectors',action='store_true')
    args=parser.parse_args()
    print(json.dumps(prove(args.max_n,args.check_all_vectors),indent=2))
