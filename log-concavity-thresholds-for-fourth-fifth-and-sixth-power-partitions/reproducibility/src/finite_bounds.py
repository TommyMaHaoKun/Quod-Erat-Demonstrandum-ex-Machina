"""Exact rational storage bounds, independent of analytic asymptotics."""
import argparse
import json
import math
from fractions import Fraction

def exp_upper(x):
    """Exact rational Taylor upper bound for exp(x), x>=0."""
    x=Fraction(x)
    terms=(x.numerator+x.denominator-1)//x.denominator+100
    total=term=Fraction(1)
    for r in range(1,terms+1):
        term*=x/r
        total+=term
    omitted=term*x/(terms+1)
    return total+omitted/(1-x/(terms+2))

def entropy_bound_k4(n):
    # log-convexity gives Gamma(5/4)<=1. By an integral test,
    # zeta(5/4) < 1+2^(-5/4)+(13/3)*3^(-1/4).
    # The rational fourth-root bounds below yield A4<19/4.
    if not (Fraction(17,20)**4>Fraction(1,2) and Fraction(19,25)**4>Fraction(1,3)):
        raise ArithmeticError('Fourth-root enclosure failed')
    zeta_upper=1+Fraction(17,40)+Fraction(13,3)*Fraction(19,25)
    if not zeta_upper<Fraction(19,4):
        raise ArithmeticError('Elementary A4 enclosure failed')
    x=18
    exponent=Fraction(n,x**4)+Fraction(19,4)*x
    return exp_upper(exponent)/x**6, {'method':'convex-midpoint entropy bound',
            'x':x,'t_numerator':1,'t_denominator':x**4,
            'A_upper_numerator':19,'A_upper_denominator':4,
            'exponent_numerator':str(exponent.numerator),
            'exponent_denominator':str(exponent.denominator),
            'zeta_upper_numerator':str(zeta_upper.numerator),
            'zeta_upper_denominator':str(zeta_upper.denominator)}

def bound(k, n):
    j = 1
    while (j+1)**k <= n:
        j += 1
    best = None
    # For coordinates 2,...,m, attach disjoint unit boxes to lattice points.
    # These boxes fit in sum j^k*x_j <= n+sum j^k. The volume is
    # (n+sum j^k)^(m-1) / ((m-1)! prod j^k). Remaining coordinates
    # independently have at most floor(n/j^k)+1 values. The coordinate
    # for the part 1 is uniquely determined by the other coordinates.
    for m in range(1,j+1):
        weights = [i**k for i in range(2,m+1)]
        upper = Fraction((n+sum(weights))**len(weights),
                         math.factorial(len(weights))*math.prod(weights))
        upper *= math.prod(n//i**k+1 for i in range(m+1,j+1))
        if best is None or upper < best[0]:
            best = upper,m
    upper,m=best
    entropy=None
    # This independent elementary bound is useful where the simplex estimate
    # is too loose. No numerical special-function library enters the proof.
    if k==4 and upper>=2**128 and n<=3400001:
        candidate,metadata=entropy_bound_k4(n)
        if candidate<upper:
            upper=candidate;entropy=metadata
    ceiling=(upper.numerator+upper.denominator-1)//upper.denominator
    record={'k': k, 'max_coefficient_index': n, 'last_base': j,
            'simplex_last_base': m, 'upper_numerator': str(upper.numerator),
            'upper_denominator': str(upper.denominator),
            'ceiling_bound': str(ceiling), 'bound_bits': ceiling.bit_length(),
            'fits_uint128': upper < 2**128}
    if entropy is not None:
        record['entropy_bound']=entropy
    return record

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--k',type=int)
    parser.add_argument('--limit',type=int)
    args=parser.parse_args()
    pairs=[(args.k,args.limit)] if args.k is not None else [(4,637866),(5,2507872),(6,35577580)]
    print(json.dumps([bound(k,n) for k,n in pairs],indent=2))
