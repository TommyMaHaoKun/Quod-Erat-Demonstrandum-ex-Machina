"""Exact rational constants for the analytic proof; no numerical libraries."""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path


def require(condition, description):
    if not condition:
        raise ArithmeticError(description)


def sqrt_bounds(q, scale=10**18):
    k = isqrt(q.numerator * scale**2 // q.denominator)
    return F(k, scale), F(k+1, scale)


def atan_bounds(x, terms=40):
    partial = sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(terms)), F(0))
    following = (-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(partial, partial+following), max(partial, partial+following)


def exp_lower(x, terms=180):
    term = result = F(1)
    for k in range(1, terms+1):
        term *= x/k
        result += term
    return result


def main():
    lo5, hi5 = atan_bounds(F(1,5))
    lo239, hi239 = atan_bounds(F(1,239))
    pi_lo, pi_hi = 16*lo5-4*hi239, 16*hi5-4*lo239
    require(F(157,50) < pi_lo < pi_hi < F(22,7), "Pi enclosure")
    sp_lo = sqrt_bounds(pi_lo)[0]
    sp_hi = sqrt_bounds(pi_hi)[1]
    z_lo = z_hi = F(0)
    N = 1000
    for k in range(1,N+1):
        lo, hi = sqrt_bounds(F(k))
        z_lo += 1/(k*hi)
        z_hi += 1/(k*lo)
    # Decreasing-function integral bounds for sum_(k>N) k^-3/2.
    z_lo += 2/sqrt_bounds(F(N+1))[1]
    z_hi += 2/sqrt_bounds(F(N))[0]
    A_lo, A_hi = sp_lo*z_lo/2, sp_hi*z_hi/2
    require(F(231,100) < A_lo < A_hi < F(58,25), "A enclosure")
    require((F(231,200))**4 > F(17,10), "Curvature constant")
    require((F(21,25))**4 < F(1,2), "Fourth-root bound")
    require(F(707,500)**2 < 2, "Square-root-of-two lower bound")
    require(1-F(500,707) > F(27,50)**2, "Angular square-root bound")
    require(F(177,100)**2 < F(157,50), "Square-root-of-pi lower bound")
    require(2*F(157,50)*F(177,100)*F(21,25)*F(27,50) > 5,
            "Complex transformed exponent b>5x")
    # On |Im z|<=t, b(z)>5/sqrt(t). At x=t^-1/2>=100,
    # E(b)<=8 exp(-5x), exp(E)-1<=16 exp(-5x).
    require(exp_lower(F(500)) > 8000, "Remainder exponential bound")
    # Major replacement error /M <=22 sqrt(x) exp(-5x).
    # Multiply by X^5 <=(29x/25)^5, and use x=100.
    # x^(11/2) exp(-5x) is decreasing for x>=100.
    major_scaled = 22*F(29,25)**5*100**5*10/exp_lower(F(500))
    require(major_scaled < F(1,1000), "Major replacement error")
    # Real-axis R is smaller; E<=1/1000 implies exp(R)<=101/100.
    require(F(1,1)/(1-F(1,1000)) < F(101,100), "Real remainder exponential")
    result = {
        'arithmetic': 'Python arbitrary-precision integers and Fraction only',
        'pi_verified_interval': ['157/50','22/7'],
        'A_verified_interval': ['231/100','58/25'],
        'A_lower_rational': str(A_lo),
        'A_upper_rational': str(A_hi),
        'zeta_partial_sum_terms': N,
        'a_power_6_lower_bound': '17/10',
        'major_replacement_bound': '(1/1000) X^-5 for x>=100',
        'all_checks_passed': True,
    }
    out=Path(__file__).resolve().parents[1]/'certificates'/'global_constants.json'
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('All exact rational global-constant checks passed.')
    print('2.31 < A < 2.32; pi in (3.14,22/7); major replacement < X^-5/1000.')


if __name__=='__main__':
    main()
