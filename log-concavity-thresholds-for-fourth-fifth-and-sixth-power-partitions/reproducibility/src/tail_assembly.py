"""Exact rational assembly of the explicit infinite-tail inequalities.

Run tail_bounds.py and the independent far-arc certificate checker as well.
This program verifies the final arithmetic, regenerates the intermediate
bound, and reads exact rational far moments (never display floats). It does
not replace the mathematical far-cell checker or the analytic proofs.
"""
if not __debug__:
    raise RuntimeError('Assertions are required; do not run this checker with -O.')

from fractions import Fraction as F
from math import factorial
from pathlib import Path
import gzip
import hashlib
import json
from minor_intermediate import bound as intermediate_bound

ROOT = Path(__file__).resolve().parents[1]
CONFIG = {
    4: {'x0':18, 'B':2000000, 'sqrt_upper':F(87,20),
        'I': [F('7.864705e-17'),F('3.574880e-18'),F('1.5e-18')]},
    5: {'x0':15, 'B':12000000, 'sqrt_upper':F(4),
        'I': [F('2.111634e-18'),F('4.059085e-21'),F('5e-21')]},
    6: {'x0':15, 'B':180000000, 'sqrt_upper':F(4),
        'I': [F('2.380075e-21'),F('9.299098e-25'),F('1.2e-24')]},
}


def ceil_decimal(value, places=12):
    scale = 10**places
    return F((value.numerator*scale+value.denominator-1)//value.denominator,scale)


def real_transform_bound():
    # The separately certified B(0)>2 gives b(t)>=30 when x>=15.
    # A positive Taylor sum is a lower bound for e^30.
    exp_lower = sum((F(30)**r/factorial(r) for r in range(61)), F(0))
    q = 1/exp_lower
    polynomial = sum((F(factorial(6),factorial(6-j)*30**j)
                      for j in range(7)),F(0))
    E = 6*q*polynomial/(1-q)
    assert E < F(1,101)
    assert 1/(1-E) < F(101,100)
    return E


def assemble(k, config):
    x0 = config['x0']
    Xu = F(21*x0,20)
    root_u = config['sqrt_upper']
    assert root_u*root_u > Xu
    path = ROOT/'certificates'/f'minor_far_sharp_k{k}_x{x0}.json.gz'
    content = path.read_bytes()
    obj = json.loads(gzip.decompress(content))
    assert obj['k'] == k and obj['X'] == x0
    assert obj['method_version'] == 3
    assert obj['success'] is True and obj['bad_scaling_cells'] == 0
    assert F(obj['scaling_exponent']) == F(7,2)
    actual = [F(s) for s in obj['moments']]
    I = config['I']
    assert all(a <= b for a,b in zip(actual,I))

    C = [ceil_decimal(intermediate_bound(k,x0,j),8) for j in range(3)]
    factor = F(101,50)*F(101,100)*Xu*root_u
    # B_j denotes an upper bound for X times the OUTER relative error.
    # Intermediate: X sqrt(X) C_j/x^2, decreasing as x^(-1/2).
    # Far: X sqrt(X) x^[k(j+1)](x0/x)^[7k/2] I_j,
    # decreasing as x^[3/2-k(5/2-j)]. All powers are negative.
    exponents = [F(3,2)-k*(F(5,2)-j) for j in range(3)]
    assert all(e < 0 for e in exponents)
    outer = [factor*(C[j]/x0**2 + x0**(k*(j+1))*I[j]) for j in range(3)]
    # Central errors a_j have X(4a0+4a1+a2+a0a2)<1/2000.
    # Therefore Xa0<1/8000 and Xa2<1/2000. The following explicitly
    # retains all cross terms after adding the outer errors.
    cost = (F(1,2000)+4*outer[0]+4*outer[1]+outer[2]
            +outer[0]*outer[2]/x0
            +outer[2]/(8000*x0)+outer[0]/(2000*x0))
    eps0 = (F(1,8000)+outer[0])/x0
    assert eps0 < 1
    assert cost < F(3,5)
    c = -F(1,504) if k==5 else F(0)
    assert config['B']+c > F(21,20)*x0**(k+1)
    return {
        'k':k,'x0':x0,'strict_tail_starts_at':config['B'],
        'far_certificate':str(path.relative_to(ROOT)),
        'far_certificate_sha256':hashlib.sha256(content).hexdigest(),
        'far_moments_exact':[str(v) for v in actual],
        'far_moments_upper':[str(v) for v in I],
        'intermediate_x_squared_J':[str(v) for v in C],
        'X_times_outer_eps_upper':[str(v) for v in outer],
        'X_times_outer_eps_decimal_upper':[str(ceil_decimal(v)) for v in outer],
        'far_monotonicity_exponents':[str(v) for v in exponents],
        'normalized_total_cost_exact':str(cost),
        'normalized_total_cost_decimal_upper':str(ceil_decimal(cost,8)),
        'required_upper_bound':'3/5',
        'positivity_eps0_upper':str(eps0),
        'join_sufficient_upper_m':str(F(21,20)*x0**(k+1)),
    }


def main():
    E = real_transform_bound()
    rows = [assemble(k,cfg) for k,cfg in CONFIG.items()]
    report = {
        'method':'Exact Fraction arithmetic and analytic monotonicity',
        'real_axis_E6_30_upper':str(E),
        'real_axis_exp_R_upper':'101/100',
        'central_normalized_budget':'1/2000',
        'rows':rows,
        'scope':'Arithmetic assembly, conditional on the separately proved analytic lemmas and independently checked far-cell certificates.',
        'result':'PASS',
    }
    path = ROOT/'certificates'/'tail_assembly.json'
    path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    for row in rows:
        print(json.dumps({key:row[key] for key in
              ('k','x0','strict_tail_starts_at','X_times_outer_eps_decimal_upper',
               'normalized_total_cost_decimal_upper','required_upper_bound')},indent=2))
    print('PASS: exact assembly inequalities and all three analytic joins.')


if __name__=='__main__':
    main()
