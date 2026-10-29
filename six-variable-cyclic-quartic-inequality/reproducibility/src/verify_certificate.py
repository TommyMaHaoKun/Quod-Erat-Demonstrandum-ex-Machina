"""Verify the exact Gram certificate using only Python's standard library.

Run from any working directory: python path/to/src/verify_certificate.py
Optional --report PATH changes the report destination.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations_with_replacement
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def matrix(values):
    require(isinstance(values, list) and values, 'Expected nonempty matrix')
    require(all(isinstance(row, list) and len(row) == len(values[0]) for row in values), 'Matrix is not rectangular')
    return [[Fraction(v) for v in row] for row in values]

def transpose(a):
    return [list(row) for row in zip(*a)]

def multiply(a, b):
    require(len(a[0]) == len(b), 'Incompatible matrix dimensions')
    bt = transpose(b)
    return [[sum((x*y for x,y in zip(row,col)), Fraction(0)) for col in bt] for row in a]

def add_term(poly, exp, value):
    exp = tuple(exp)
    poly[exp] = poly.get(exp, Fraction(0)) + value

def target_polynomial():
    poly = {}
    for i in range(6):
        for j in range(6):
            exp = [0]*6
            exp[i] += 2
            exp[j] += 2
            add_term(poly, exp, Fraction(1))
            exp = [0]*6
            exp[i] += 1
            exp[j] += 1
            exp[(j+1)%6] += 2
            add_term(poly, exp, Fraction(-1))
    return poly

def verify(certificate_path):
    raw = certificate_path.read_bytes()
    data = json.loads(raw)
    mons = data['monomials']
    require(len(mons) == 21 and len({tuple(e) for e in mons}) == 21, 'Expected 21 distinct monomials')
    require(all(len(e) == 6 and all(isinstance(v,int) and v >= 0 for v in e) and sum(e)==2 for e in mons), 'Invalid degree-two monomial')
    B = matrix(data['basis'])
    H = matrix(data['reduced_gram'])
    L = matrix(data['ldl_lower'])
    diagonal = [Fraction(v) for v in data['ldl_diagonal']]
    require((len(B),len(B[0])) == (21,18), 'Wrong B dimensions')
    require((len(H),len(H[0])) == (18,18), 'Wrong H dimensions')
    require((len(L),len(L[0])) == (18,18), 'Wrong L dimensions')
    require(len(diagonal) == 18, 'Wrong D dimensions')
    require(H == transpose(H), 'H is not symmetric')
    require(all(diagonal[i] > 0 for i in range(18)), 'Nonpositive LDL pivot')
    require(all(L[i][i] == 1 for i in range(18)), 'L is not unit diagonal')
    require(all(L[i][j] == 0 for i in range(18) for j in range(i+1,18)), 'L is not lower triangular')
    LD = [[L[i][j]*diagonal[j] for j in range(18)] for i in range(18)]
    require(multiply(LD,transpose(L)) == H, 'LDL identity failed')
    G = multiply(multiply(B,H),transpose(B))
    actual = {}
    for i,e in enumerate(mons):
        for j,f in enumerate(mons):
            add_term(actual,[a+b for a,b in zip(e,f)],G[i][j])
    expected = target_polynomial()
    exponents = set(actual) | set(expected)
    for exp in sorted(exponents):
        require(actual.get(exp,0) == expected.get(exp,0), 'Coefficient mismatch: '+str(exp))
    require(len(exponents) == 126, 'Did not check all 126 degree-four monomials')
    # Independently establish the three-dimensional kernel and equality case.
    u = [2,1,-1,-2,-1,1]
    v = [0,1,1,0,-1,-1]
    kernel = [[Fraction(1),sum(e[i]*u[i] for i in range(6)),sum(e[i]*v[i] for i in range(6))] for e in mons]
    require(all(value == 0 for row in multiply(transpose(B),kernel) for value in row), 'B does not annihilate the stated kernel')
    # Exact row reduction checks rank B = 18; no floating point is used.
    rows = [row[:] for row in B]
    rank = 0
    for col in range(18):
        pivot = next((i for i in range(rank,21) if rows[i][col]),None)
        if pivot is None:
            continue
        rows[rank],rows[pivot] = rows[pivot],rows[rank]
        factor = rows[rank][col]
        rows[rank] = [x/factor for x in rows[rank]]
        for i in range(rank+1,21):
            factor = rows[i][col]
            rows[i] = [x-factor*y for x,y in zip(rows[i],rows[rank])]
        rank += 1
    require(rank == 18, 'B has insufficient rank')
    # Kernel columns independent: on square monomials they are 1,2u,2v;
    # their pairwise inner products vanish, and their norms are positive.
    vectors = [[Fraction(1)]*6,[Fraction(t) for t in u],[Fraction(t) for t in v]]
    require(all(sum(x*y for x,y in zip(vectors[i],vectors[j])) == 0 for i in range(3) for j in range(i)), 'Kernel witnesses are not orthogonal')
    require(all(sum(x*x for x in row)>0 for row in vectors), 'Zero kernel witness')
    lookup = {tuple(e):i for i,e in enumerate(mons)}
    for i,j in combinations_with_replacement(range(6),2):
        ei=[0]*6;ei[i]=2
        ej=[0]*6;ej[j]=2
        eij=[0]*6;eij[i]+=1;eij[j]+=1
        for k in range(3):
            require(kernel[lookup[tuple(ei)]][k]+kernel[lookup[tuple(ej)]][k]-2*kernel[lookup[tuple(eij)]][k] == 0, 'Equality functional failed')
    return {
        'status':'PASS',
        'arithmetic':'Python standard-library fractions.Fraction; exact rational arithmetic only',
        'certificate_sha256':hashlib.sha256(raw).hexdigest(),
        'target':'(sum x_i^2)^2 - (sum x_i)(sum x_i x_(i+1)^2), with six cyclic variables',
        'domain':'all real six-tuples',
        'quartic_coefficients_checked':len(exponents),
        'reduced_gram_dimension':18,
        'positive_ldl_pivots':18,
        'basis_rank':rank,
        'equality':'x_1 = x_2 = x_3 = x_4 = x_5 = x_6',
        'checks':['polynomial identity','symmetric reduced Gram matrix','exact LDL identity','strictly positive LDL pivots','basis rank','kernel dimension and basis','all pairwise equality functionals'],
        'qualification':'Exact algebraic verification, not a formal proof-assistant check or external peer review.'
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,default=ROOT/'certificates/verification_report.json')
    args=parser.parse_args()
    report=verify(ROOT/'certificates/exact_gram.json')
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
