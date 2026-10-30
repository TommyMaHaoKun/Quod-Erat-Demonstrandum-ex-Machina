"""Exact polynomial certificate checker. Python standard library only.

Independently implements rational-polynomial arithmetic, derives the transfer
matrix from integration by parts, parses the published TeX target, and proves
the cleared row identity coefficient by coefficient. No sample fitting.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ZERO = (F(0),)
ONE = (F(1),)
N = (F(0), F(1))

def norm(a):
    a = list(map(F, a))
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a) if a else ZERO

def const(a):
    return (F(a),)

def add(a, b):
    return norm([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])

def scale(a, c):
    return norm([x*c for x in a])

def mul(a, b):
    c = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return norm(c)

def power(a, k):
    r = ONE
    for _ in range(k):
        r = mul(r, a)
    return r

def shift(a, h):
    r = ZERO
    for i, x in enumerate(a):
        r = add(r, scale(power((F(h), F(1)), i), x))
    return r

def parse(expr):
    """Parse only integer polynomial arithmetic with implicit multiplication."""
    expr = expr.replace('\\qquad', '').replace('\\', '').replace('&', '')
    expr = expr.replace('{', '').replace('}', '')
    expr = re.sub(r'\s+', '', expr)
    tokens = re.findall(r'\d+|n|[+\-*/^()]', expr)
    assert ''.join(tokens) == expr, expr
    pos = 0
    def atom():
        nonlocal pos
        t = tokens[pos]
        pos += 1
        if t == '-':
            a = scale(atom(), -1)
        elif t == '+':
            a = atom()
        elif t == '(':
            a = summation()
            assert tokens[pos] == ')'
            pos += 1
        elif t == 'n':
            a = N
        else:
            a = const(int(t))
        if pos < len(tokens) and tokens[pos] == '^':
            pos += 1
            k = int(tokens[pos])
            pos += 1
            a = power(a, k)
        return a
    def product():
        nonlocal pos
        a = atom()
        while pos < len(tokens) and tokens[pos] not in ('+', '-', ')'):
            if tokens[pos] == '*':
                pos += 1
                a = mul(a, atom())
            elif tokens[pos] == '/':
                pos += 1
                b = atom()
                assert len(b) == 1
                a = scale(a, 1/b[0])
            else:
                a = mul(a, atom())
        return a
    def summation():
        nonlocal pos
        a = product()
        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            sign = 1 if tokens[pos] == '+' else -1
            pos += 1
            a = add(a, scale(product(), sign))
        return a
    result = summation()
    assert pos == len(tokens)
    return result

def matrix_mul(a, b):
    return [[sum_poly(mul(a[i][k], b[k][j]) for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def sum_poly(items):
    r = ZERO
    for item in items:
        r = add(r, item)
    return r

@lru_cache(None)
def reduction(k, j):
    if not 0 <= j <= 6:
        return (ZERO,)*4
    if k == 0:
        return tuple(const(j == 2*r) for r in range(4))
    a, b = reduction(k-1, j+1), reduction(k-1, j-1)
    c = reduction(k-2, j) if k >= 2 else (ZERO,)*4
    return tuple(scale(add(add(scale(a[r], 6-j), scale(mul(N, b[r]), j)),
                           scale(c[r], k-1)), F(1, j+1)) for r in range(4))

def main():
    target_bytes = (ROOT/'literature'/'target_formula.tex').read_bytes()
    target = target_bytes.decode('utf-8')
    body = '\n'.join(line for line in target.splitlines() if not line.startswith('%'))
    canonical = re.sub(r'\s+', '', body)
    assert hashlib.sha256(canonical.encode()).hexdigest() == '7c7e083590996f30ecbd1489dcc98ce1c645674bf06949704a2126aa6e5d520b'
    source_path = ROOT/'literature'/'kout4.tex'
    source_comparison = 'not rerun; original article is not required by the public certificate'
    if source_path.exists():
        source = source_path.read_text(encoding='utf-8')
        assert canonical in re.sub(r'\s+', '', source)
        source_comparison = 'exact after removing whitespace and excerpt comments'
    align = target.split('\\begin{align*}')[1].split('\\end{align*}')[0]
    terms = re.findall(r'(.*?)\\tilde\{a\}_(?:\{n\+([1-4])\}|n)', align, re.S)
    assert len(terms) == 5
    p = [None]*5
    for expr, j in terms:
        p[int(j or 0)] = parse(expr)

    paper = (ROOT/'paper'/'main.tex').read_text(encoding='utf-8')
    paper_terms = re.findall(r'p_([0-4])\(n\)=\{\}&(.*?)(?=p_[0-4]\(n\)|\\end\{align\*\})', paper, re.S)
    assert len(paper_terms) == 5
    for j, expr in paper_terms:
        expr = re.sub(r'\\hspace\{[^}]*\}', '', expr)
        for command in ('\\bigl', '\\bigr', '\\quad'):
            expr = expr.replace(command, '')
        expr = expr.replace(',', '').replace('.', '')
        assert parse(expr) == p[int(j)], ('paper target mismatch', j)

    forms = [
        ['3(2n+1)(29n^2+29n+5)', '15(76n^2+95n+28)', '75(4n+3)', '7'],
        ['(n+1)^2(76n^2+57n+9)/3', '241(n+1)^2(2n+1)/3', '35(n+1)^2', '0'],
        ['(n+1)^4(4n+1)', '21(n+1)^4', '0', '0'],
        ['(n+1)^6', '0', '0', '0']]
    A = [[parse(x) for x in row] for row in forms]
    for r, j in enumerate((0, 2, 4, 6)):
        derived = [ZERO]*4
        for ell in range(7-j):
            reduced = reduction(6-j-ell, ell)
            derived = [add(derived[t], scale(reduced[t], comb(6-j, ell))) for t in range(4)]
        derived = [mul(power(add(N, ONE), j), x) for x in derived]
        assert A[r] == derived, (r, A[r], derived)

    product = [[const(i == j) for j in range(4)] for i in range(4)]
    residual = [ZERO]*4
    summand_degrees = []
    for j in range(5):
        if j:
            product = matrix_mul([[shift(x, j-1) for x in row] for row in A], product)
        multiplier = p[j]
        for t in range(j+1, 5):
            multiplier = mul(multiplier, power((F(t), F(1)), 3))
        summands = [mul(multiplier, x) for x in product[0]]
        summand_degrees.append([len(x)-1 if x != ZERO else -1 for x in summands])
        residual = [add(residual[t], summands[t]) for t in range(4)]
    assert residual == [ZERO]*4, residual
    report = {
        'status': 'PASS', 'arithmetic': 'standard-library fractions.Fraction polynomial arithmetic',
        'target_excerpt_integrity': 'canonical SHA-256 matches the excerpt checked against the original article',
        'optional_full_source_comparison': source_comparison,
        'paper_target_coefficients': 'all five equal to parsed source polynomials',
        'transfer_entries_verified': 16,
        'identity': 'sum_j p_j(n)*prod_{t=j+1}^4(n+t)^3*e0*A(n+j-1)*...*A(n)=0',
        'summand_degrees_by_j': summand_degrees,
        'residual_coefficients_low_to_high': [[str(x) for x in row] for row in residual],
        'target_sha256': hashlib.sha256(target_bytes).hexdigest(),
    }
    output = ROOT/'certificates'/'polynomial_identity.json'
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
