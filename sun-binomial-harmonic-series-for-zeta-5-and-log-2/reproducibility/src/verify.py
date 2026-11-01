"""Exact arithmetic checks and independent enclosures for Sun's equation (3.15).

Run from any working directory: python path/to/src/verify.py
The mathematical proof is in paper/main.tex. Interval overlap is a consistency
check; the proof uses Au's stated identities and analytic differentiation.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json
import sys

import sympy as s

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def symbolic_checks():
    n, h, h2, z3, z5, p2, ell = s.symbols("n h h2 z3 z5 p2 ell")
    P = 21*n**3 - 22*n**2 + 8*n - 1
    # h=H_(n-1), h2=H_(2n-1). Differentiate every Pochhammer
    # factor separately before simplifying the logarithmic derivative.
    hn = h + 1/n
    h2n = h2 + 1/(2*n)
    logderiv = 14*hn - 14*(2*h2n-hn) - 14/n
    assert s.expand(logderiv + 28*(h2-h)) == 0
    sprime_term = 2*s.diff(P, n) + P*logderiv
    target_term = 14*P*(h2-h) - 63*n*n + 44*n - 8
    assert s.expand(sprime_term+2*target_term) == 0
    # The gamma logarithmic derivative of C at zero.
    psi_half, psi_one = s.symbols("psi_half psi_one")
    c_logderiv = -psi_half+8*psi_half+2*psi_one-psi_half-4*psi_one-4*psi_one
    assert s.expand(c_logderiv.subs(psi_half, psi_one-2*ell)+12*ell) == 0
    U = 7*z3/4-p2*ell/4
    W = 7*z3/16
    Bprime = -6*W+2*U-9*7*z3/8
    assert s.expand(Bprime+7*z3+p2*ell/2) == 0
    A0 = (93*z5-7*p2*z3)/4
    Sprime = (-12*p2*ell)*(p2/8)+p2*Bprime-4*A0
    assert s.expand(Sprime+93*z5+2*p2*p2*ell) == 0
    # Exact shift n=k+1 in Au's Example XV sum: its term is 4 A_(n-1).
    # (1)_(n-1)/(1/2)_(n-1) = ((n-1/2)/n) (1)_n/(1/2)_n.
    a_shift = (4*n-1)*((n-Q(1,2))/n)**4/((2*n-1)**5*n)
    au_term = (4*n-1)/(4*n**5*(2*n-1))
    assert s.cancel(4*a_shift-au_term) == 0
    return 6


def atan_interval(q, terms):
    partial = sum((Q((-1)**j, (2*j+1)*q**(2*j+1)) for j in range(terms)), Q(0))
    following = Q((-1)**terms, (2*terms+1)*q**(2*terms+1))
    return min(partial, partial+following), max(partial, partial+following)


def pi_interval():
    lo5, hi5 = atan_interval(5, 180)
    lo239, hi239 = atan_interval(239, 60)
    return 16*lo5-4*hi239, 16*hi5-4*lo239


def log2_interval():
    terms = 220
    partial = 2*sum((Q(1, (2*j+1)*3**(2*j+1)) for j in range(terms)), Q(0))
    tail = Q(2, (2*terms+1)*3**(2*terms+1))*Q(9, 8)
    return partial, partial+tail


def zeta5_interval():
    terms = 600
    diffs = [Q(1, j**5) for j in range(1, terms+1)]
    partial = Q(0)
    for k in range(terms):
        assert 0 < diffs[0] <= 1
        partial += diffs[0]/2**(k+1)
        diffs = [diffs[j]-diffs[j+1] for j in range(len(diffs)-1)]
    # Euler's transformation of eta(5); its forward differences lie in [0,1].
    return partial*Q(16,15), (partial+Q(1,2**terms))*Q(16,15)


def target_interval(terms=100):
    H = [Q(0)]
    for j in range(1,2*terms):
        H.append(H[-1]+Q(1,j))
    partial = Q(0)
    for k in range(1, terms+1):
        P = 21*k**3-22*k*k+8*k-1
        numerator = 14*P*(H[2*k-1]-H[k-1])-63*k*k+44*k-8
        partial += Q(256**k, k**7*comb(2*k,k)**7)*numerator
    # C(2k,k) >= 4^k/(2k+1), |numerator| <= 843 k^3.
    # Successive k^3/64^k terms have ratio <= 1/8 for k>=1.
    tail = Q(843*3**7*(terms+1)**3,64**(terms+1))*Q(8,7)
    return partial-tail, partial+tail, tail


def decimal_bound(x, digits, upper=False):
    scale = 10**digits
    value = x.numerator*scale//x.denominator
    if upper and Q(value,scale)<x:
        value += 1
    sign = "-" if value<0 else ""
    value = abs(value)
    return f"{sign}{value//scale}.{value%scale:0{digits}d}"


def run():
    checks = symbolic_checks()
    lo, hi, tail = target_interval()
    plo, phi = pi_interval()
    llo, lhi = log2_interval()
    zlo, zhi = zeta5_interval()
    rlo, rhi = Q(93,2)*zlo+plo**4*llo, Q(93,2)*zhi+phi**4*lhi
    assert lo<=rhi and rlo<=hi, "Independent exact intervals are disjoint"
    assert hi-lo<Q(1,10**160) and rhi-rlo<Q(1,10**175)
    report = {
        "status":"PASS",
        "symbolic_checks":checks,
        "target_terms":100,
        "target_enclosure":[decimal_bound(lo,160),decimal_bound(hi,160,True)],
        "constant_enclosure":[decimal_bound(rlo,160),decimal_bound(rhi,160,True)],
        "target_tail_upper_bound":decimal_bound(tail,180,True),
        "zeta5_euler_terms":600,
        "pi_machin_terms":[180,60],
        "log2_atanh_terms":220,
        "interpretation":"Exact independent enclosures agree; the analytic proof is in the paper."
    }
    destination = Path(__file__).resolve().parents[1]/"certificates"/"verification.json"
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    run()
