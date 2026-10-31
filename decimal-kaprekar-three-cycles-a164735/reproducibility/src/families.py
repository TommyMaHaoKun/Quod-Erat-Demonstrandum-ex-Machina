"""Exact X/Y family algebra; this script does not prove exhaustiveness."""
from math import comb
import argparse


def step(d, eps):
    """Subtraction histogram followed by outside-in sorted-digit pairing."""
    positive = [j for j in range(1, 10) if d[j]]
    if not positive:
        return None
    m, M = positive[0], positive[-1]
    if sum(d[1:]) == 1 and M == 1:
        return None  # The non-padded map loses a digit.
    c = [0] * 10
    for j in positive:
        c[j] += d[j]
        c[9-j] += d[j]
    c[9] += 2*d[0] + eps
    c[m] -= 1
    c[m-1] += 1
    c[9-M] -= 1
    c[10-M] += 1
    assert min(c) >= 0
    ans = [0] * 10
    lo, hi = 0, 9
    while lo < hi:
        if not c[lo]:
            lo += 1
            continue
        if not c[hi]:
            hi -= 1
            continue
        count = min(c[lo], c[hi])
        ans[hi-lo] += count
        c[lo] -= count
        c[hi] -= count
    if lo == hi:
        ans[0] = c[lo] // 2
    return tuple(ans)


def family_x(s, x, y, z, w, e, eps):
    assert s >= 0 and y >= 0 and min(x, z, w, e) >= 1
    assert eps in (0, 1)
    t = 2*s + eps
    return (s, x, t, y, t, z, t, w, t, e)


def family_y(b, u, v):
    assert min(b, u) >= 1 and v >= 0
    return ((0, 0, 0, b, 0, u, 1, v, 1, 0),
            (0, u, 0, b, 1, v, 1, 0, 0, 0),
            (0, v+1, 1, b, 0, 0, 0, u-1, 1, 0))


def family_count(n):
    h, eps = divmod(n, 2)
    x_count = 0
    for s in range(h // 9 + 1):
        L = h - 9*s - 4*eps
        if L < 4:
            continue
        fixed = sum(L-3*j for j in range(1, (L-1)//3 + 1))
        numerator = comb(L, 4)-fixed
        assert numerator % 3 == 0
        x_count += numerator // 3
    y_count = comb(h-2, 2) if eps == 0 and h >= 4 else 0
    return x_count+y_count


def target_polynomials(k):
    """The eighteen numerators in Kauers--Koutschan Conjecture 23."""
    return [
        3*(243*k**5+405*k**4+35*k**3+395*k**2-318*k+40),
        k*(729*k**4-405*k**3-615*k**2+225*k+106),
        729*k**5+1620*k**4+735*k**3+1320*k**2-684*k+40,
        k*(729*k**4-705*k**2+136),
        3*k*(243*k**4+675*k**3+515*k**2+565*k-118),
        k*(729*k**4+405*k**3-615*k**2-225*k+106),
        3*k*(243*k**4+810*k**3+845*k**2+790*k+32),
        3*k*(k+1)*(243*k**3+27*k**2-142*k+12),
        729*k**5+2835*k**4+3705*k**3+3405*k**2+726*k+40,
        3*k*(k+1)*(243*k**3+162*k**2-127*k-18),
        729*k**5+3240*k**4+5055*k**3+4860*k**2+1636*k+160,
        3*k*(k+1)*(243*k**3+297*k**2-52*k-48),
        729*k**5+3645*k**4+6585*k**3+6795*k**2+2926*k+400,
        3*k*(k+1)*(243*k**3+432*k**2+83*k-58),
        729*k**5+4050*k**4+8295*k**3+9270*k**2+4696*k+800,
        3*k*(k+1)*(243*k**3+567*k**2+278*k-28),
        3*(k+3)*(243*k**4+756*k**3+1127*k**2+734*k+160),
        3*k*(k+1)*(243*k**3+702*k**2+533*k+62),
    ]


def symbolic_verification():
    import sympy as sp
    from pathlib import Path
    import re
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    q, z, k = sp.symbols('q z k')
    # Compare the program's polynomials with the attributed source excerpt,
    # independently of the generating-function calculation below.
    target = (Path(__file__).resolve().parents[1]/'literature/target_formula.tex').read_text(encoding='utf-8')
    rows = re.findall(r'^\s*([^\n]+?),\s*&\s*i=(\d+)[;.]', target, re.M)
    assert len(rows) == 18 and {int(i) for _, i in rows} == set(range(18))
    transformations = standard_transformations + (implicit_multiplication_application,)
    for expression, residue in rows:
        assert re.fullmatch(r'[0-9k^+*()\s-]+', expression)
        expected = parse_expr(expression.replace('^', '**'),
                              local_dict={'k': k}, transformations=transformations)
        assert sp.expand(expected-target_polynomials(k)[int(residue)]) == 0
    print('PASS: all eighteen program polynomials match the source excerpt.')
    X = q**8/(3*(1-q**9)) * (1/(1-q**2)**5
                             -1/((1-q**2)**2*(1-q**6)))
    Y = q**8/(1-q**2)**3
    G = q*(-q**24+q**22+q**18-q**16+q**15-q**13+q**7) / (
        (q-1)**6*(q+1)**5*(q*q-q+1)*(q*q+q+1)**2*(q**6+q**3+1))
    assert sp.cancel(X+Y-G) == 0
    power_sums = [1/(1-z)]
    for j in range(1, 6):
        power_sums.append(sp.cancel(z*sp.diff(power_sums[-1], z)))
    common_denominator = (1-z)**6
    power_numerators = [sp.cancel(S*common_denominator) for S in power_sums]
    conjectured_numerator = 0
    for i, P in enumerate(target_polynomials(k)):
        numerator = sum(coefficient*power_numerators[degree[0]]
                        for degree, coefficient in sp.Poly(P, k).terms())/40
        conjectured_numerator += q**i * numerator.subs(z, q**18)
    # Conjecture 23 starts at n=3. The polynomial extensions give 3 at
    # n=0 and 1 at n=2; both must be removed, while n=1 already gives 0.
    conjectured_numerator -= (3+q**2)*(1-q**18)**6
    g_num, g_den = sp.fraction(G)
    # Clear denominators as polynomials to avoid an expensive expansion of
    # an unreduced sum of eighteen rational functions.
    left = sp.Poly(conjectured_numerator, q)*sp.Poly(g_den, q)
    right = sp.Poly(g_num, q)*sp.Poly((1-q**18)**6, q)
    assert left == right
    print('PASS: exact rational-function identity for all eighteen branches.')


def finite_checks():
    from itertools import product
    for s, y, eps in product(range(3), range(4), range(2)):
        for x, z, w, e in product(range(1, 4), repeat=4):
            a = family_x(s, x, y, z, w, e, eps)
            assert step(a, eps) == family_x(s, z, y, w, x, e, eps)
    for b, u, v in product(range(1, 7), range(1, 7), range(7)):
        A, B, C = family_y(b, u, v)
        assert step(A, 0) == B and step(B, 0) == C and step(C, 0) == A
    assert family_count(1) == family_count(2) == 0
    for n in range(3, 1001):
        k, i = divmod(n, 18)
        numerator = target_polynomials(k)[i]
        assert numerator % 40 == 0
        assert family_count(n) == numerator // 40
    print('PASS: family transitions and counts through n=1000.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--symbolic', action='store_true')
    args = parser.parse_args()
    finite_checks()
    if args.symbolic:
        symbolic_verification()
