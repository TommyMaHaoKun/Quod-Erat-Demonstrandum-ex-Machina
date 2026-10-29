#!/usr/bin/env python3
"""Exact rational certificates for the cubic transformation/minor arcs.

No third-party packages. Run from the project root:
  python code/analytic_arcs.py
The grid is a proof over CLOSED intervals, not a sampling experiment.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import argparse
import json
import time

if not __debug__:
    raise RuntimeError('Run without -O: proof checks must remain enabled.')


def exp_lower(q, degree=180):
    q = F(q)
    term = result = F(1)
    for k in range(1, degree + 1):
        term *= q / k
        result += term
    return result


def exp_upper(q, degree=80):
    q = F(q)
    assert 0 <= q < degree+2
    partial = exp_lower(q,degree)
    first = q**(degree+1)/factorial(degree+1)
    return partial + first/(1-q/F(degree+2))


def arctan_bounds(q):
    q=F(q)
    lower=sum(((-1)**k*q**(2*k+1)/F(2*k+1) for k in range(20)),F(0))
    upper=lower+q**41/F(41)
    return lower,upper


def elementary_certificate():
    lo5,hi5=arctan_bounds(F(1,5))
    lo239,hi239=arctan_bounds(F(1,239))
    pi_lo,pi_hi=16*lo5-4*hi239,16*hi5-4*lo239
    assert F(157,50)<pi_lo<pi_hi<F(22,7)
    # Transformation and trigonometric constants.
    assert (2*F(157,50))**4>F(23,2)**3
    assert F(47,100)**3>F(1,10)
    assert F(115,141)>F(4,5)
    assert 3*(1+F(3,40)+F(6,40**2)+F(6,40**3))/(1-F(1,1000))<4
    assert exp_lower(F(40))>1000
    assert 1/(1-F(4,1000))<F(101,100)
    assert F(9,5)**4>10
    assert F(216,5)**2*F(1288,1413)<42**2
    assert F(101,100)**2*F(1288,1413)<1
    assert (F(23,24)/F(261,250))**2>F(21,25)
    assert F(10,237)<F(11,250)
    # h(r) comparisons for the near arcs.
    assert F(29,20)**3>3
    assert exp_upper(F(1073,500))<F(214,25)
    assert exp_lower(F(27,10))>F(361,25)
    assert F(2016,361)-F(27,10)>F(72,25)
    assert F(32,5)**3>4**4
    assert F(8,5)**3>4
    assert exp_upper(F(8,3))<F(361,25)
    assert F(21,25)*F(11,10)**2>1
    # Four normalized minor terms at x=50; every term decreases after 50.
    x=F(50)
    B=F(161,150)
    X=B*x
    assert 7**2<50<F(71,10)**2
    term1=F(51,7)*X**7/exp_lower(F(37))
    term2=F(1,1000)*x**3*F(71,10)*X**7/exp_lower(F(75,2))
    term3=F(1,1000)*1100**9*X**7/(x**23*7)
    term4=F(22,7)*F(1,10**24)*125000**8*X**7/(x**20*7)
    assert term1+term2+term3+term4<F(1,16)
    transformation=42*F(71,10)*X**7/exp_lower(F(40))
    assert transformation<F(1,500)
    return {"minor_normalized_upper_bound":"1/16 X^-7",
            "minor_endpoint_rational_upper_float":float(term1+term2+term3+term4),
            "transform_normalized_upper_bound":"1/500 X^-7",
            "transform_endpoint_rational_upper_float":float(transformation),
            "domain":"x=t^(-1/3) >= 50; X=(A/3)x"}


def cube_root_interval(n, digits=12):
    scale = 10**digits
    target = n * scale**3
    lo, hi = 0, max(1, n) * scale + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**3 <= target:
            lo = mid
        else:
            hi = mid
    return F(lo, scale), F(hi, scale)


def constant_certificate():
    # Gamma(4/3) = integral_0^infty exp(-u^3)du. Alternating
    # exponential Taylor bounds on [0,2], with the tail at 2
    # bounded by exp(-8)/12 using convexity of u^3.
    terms = [F((-1)**k * 2**(3*k+1), factorial(k)*(3*k+1))
             for k in range(62)]
    gamma_lo = sum(terms[:62], F(0))
    gamma_hi = sum(terms[:61], F(0)) + 1/(12*exp_lower(F(8)))
    zeta_lo = zeta_hi = F(0)
    for n in range(1, 1001):
        lo, hi = cube_root_interval(n)
        zeta_lo += 1/(n*hi)
        zeta_hi += 1/(n*lo)
    lo1001, hi1001 = cube_root_interval(1001)
    zeta_lo += 3/hi1001
    zeta_hi += F(3,10)
    assert F(321,100) < gamma_lo*zeta_lo
    assert gamma_hi*zeta_hi < F(161,50)
    return {"A_lower":"321/100", "A_upper":"161/50",
            "gamma_lower_float":float(gamma_lo),
            "gamma_upper_float":float(gamma_hi),
            "zeta_lower_float":float(zeta_lo),
            "zeta_upper_float":float(zeta_hi)}


def far_arc_certificate(grid=1000000, first=159, last=500000):
    # theta >= 1/1000 implies alpha=theta/(2pi)>159/10^6,
    # since 2pi < 44/7 and 7/44000 > 159/10^6.
    assert F(7,44000) > F(first,grid)
    assert F(last,grid) == F(1,2)
    min_product = None
    min_k = None
    min_count = 51
    min_count_k = None
    cubes = [(j**3, (grid*j**3)**2) for j in range(1,51)]
    tden = 125000
    start = time.monotonic()
    for k in range(first,last):
        product = 1
        count = 0
        for j3, denominator in cubes:
            left, right = j3*k, j3*(k+1)
            if left//grid != right//grid:
                continue
            dnum = min(left % grid, grid-right % grid)
            numerator = (2*tden*dnum)**2
            factor = numerator // denominator
            product *= 1 + factor
            count += numerator >= denominator
        if min_product is None or product < min_product:
            min_product, min_k = product,k
        if count < min_count:
            min_count,min_count_k = count,k
    assert min_product >= 10**48
    assert min_count >= 16
    return {"grid":grid,"first":first,"last_exclusive":last,
            "j_max":50,"t0":"1/125000", "product_claim":"10^48",
            "count_claim":16,"minimum_product":str(min_product),
            "minimum_product_interval":min_k,
            "minimum_count":min_count,"minimum_count_interval":min_count_k,
            "seconds":time.monotonic()-start}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--skip-grid",action="store_true")
    p.add_argument("--output",default="certificates/analytic_arcs_report.json")
    args=p.parse_args()
    report={"status":"passed","constants":constant_certificate(),
            "elementary_inequalities":elementary_certificate()}
    if not args.skip_grid:
        report["far_arcs"]=far_arc_certificate()
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
