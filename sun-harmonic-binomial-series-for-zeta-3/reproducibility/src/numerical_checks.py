"""Exact rational enclosures; numerical agreement is not an identity proof.

Only the Python standard library is required. Run from any working directory.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json


def target_interval(n):
    h = [Q(0)]
    for j in range(1, 3 * n):
        h.append(h[-1] + Q(1, j))
    total = Q(0)
    for k in range(1, n + 1):
        b = (21*k-8)*(2*h[3*k-1]-h[k-1])-Q(4*(27*k-11),3*(3*k-1))
        assert b > 0
        total += b / (k**3 * comb(2*k, k)**3)
    # 0 < B_k < 126 k^2 and C(2k,k) >= 4^k/(2k+1).
    # Thus 0 < term_k < 3402 k^2/64^k for every k>=1.
    r = Q(1, 64)
    m = n+1
    tail = 3402*r**m*(Q(m*m,1-r)+2*m*r/(1-r)**2+r*(1+r)/(1-r)**3)
    return total, total + tail


def three_zeta3_interval(m):
    # Euler transform: 3*zeta(3) = 4*sum_{n>=0} d_n/2^(n+1),
    # d_n = integral_0^1 (1-t)^n (-log(t))^2/2 dt
    #     = (H_(n+1)^2+H_(n+1)^(2))/(2(n+1)),  0 < d_n <= 1.
    h1 = h2 = total = Q(0)
    for j in range(1, m+1):
        h1 += Q(1,j)
        h2 += Q(1,j*j)
        total += 2*(h1*h1+h2)/ (j*2**j)
    return total, total+Q(4, 2**m)


def main():
    a,b = target_interval(80)
    c,d = three_zeta3_interval(500)
    scale = 10**120
    floor_values = [x.numerator*scale//x.denominator for x in (a,b,c,d)]
    assert len(set(floor_values)) == 1
    discrepancy_low, discrepancy_high = a-d, b-c
    assert discrepancy_low < 0 < discrepancy_high
    assert b-a < Q(1, 10**135)
    assert d-c < Q(1, 10**149)
    digits = str(floor_values[0])
    result = {
        'kind': 'exact rational numerical consistency check, not proof of equality',
        'target_terms':80, 'euler_transform_terms':500,
        'common_120_decimal_digit_truncation': digits[:-120]+'.'+digits[-120:],
        'target_interval_width_less_than':'1e-135',
        'three_zeta3_interval_width_less_than':'1e-149',
        'difference_interval_contains_zero':True,
        'target_lower':str(a), 'target_upper':str(b),
        'three_zeta3_lower':str(c), 'three_zeta3_upper':str(d),
    }
    root=Path(__file__).resolve().parents[1]
    out=root/'certificates'/'numerical_enclosures.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['common_120_decimal_digit_truncation'])
    print('PASS: independent rational enclosures agree through 120 decimal places.')
    print('This check alone does not prove the identity.')


if __name__=='__main__':
    main()
