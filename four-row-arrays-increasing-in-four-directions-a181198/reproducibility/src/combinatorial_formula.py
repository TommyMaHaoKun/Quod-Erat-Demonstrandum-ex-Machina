"""Exact all-n finite sums from a cut at the completion of the second row.

Only Python's standard library is required.  Running this file checks the
combinatorial sum against an independently implemented ideal-lattice DP.
The recurrence checks are evidence only; this script is not a proof of it.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import factorial, comb
import argparse
import json


def shifted_count(parts):
    """Shifted hook formula for a strict partition, with trailing zeros ignored."""
    parts = tuple(x for x in parts if x)
    assert all(x > 0 for x in parts)
    assert all(x > y for x, y in zip(parts, parts[1:]))
    result = Fraction(factorial(sum(parts)), 1)
    for x in parts:
        result /= factorial(x)
    for x, y in combinations(parts, 2):
        result *= Fraction(x-y, x+y)
    assert result.denominator == 1
    return result.numerator


def two_row_suffix(n, b, c):
    if b == c == 0:
        return comb(2*n-2, n-1)//n
    assert 0 <= c < b < n
    result = Fraction(factorial(2*n-b-c-1)*(b-c),
                      factorial(n-b)*factorial(n-c))
    assert result.denominator == 1
    return result.numerator


def cut_sum(n):
    if n == 1:
        return 1
    result = (comb(2*n-2, n-1)//n)**2
    for b in range(1, n-1):
        for c in range(b):
            result += shifted_count((n,n-1,b,c))*two_row_suffix(n,b,c)
    return result


def ideal_dp(n):
    """DP from cell predecessors, without the shifted-hook formula."""
    @lru_cache(None)
    def f(s):
        if s == (n,n,n,n):
            return 1
        out = 0
        for i, v in enumerate(s):
            if v == n:
                continue
            # Place cell (i,v+1). Its strongest predecessor above has
            # column min(n,v+2), owing to the down-left comparison.
            if i and s[i-1] < min(n,v+2):
                continue
            t = list(s)
            t[i] += 1
            out += f(tuple(t))
        return out
    return f((0,0,0,0))


def recurrence_residual(n, a):
    p2 = 3*(n+1)*(2*n+3)*(3*n+4)*(3*n+5)*(7*n*n-1)*(n+2)**3
    p1 = 8*(n+1)*(2*n+1)*(4*n+3)*(4*n+5)*(364*n**5+84*n**4-1025*n**3-534*n*n+157*n+54)
    p0 = 64*(2*n-1)**2*(2*n+1)*(4*n-1)*(4*n+1)*(4*n+3)*(4*n+5)*(7*n*n+14*n+6)
    return p2*a[n+2]-p1*a[n+1]-p0*a[n]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=20)
    parser.add_argument('--dp-max', type=int, default=15)
    args=parser.parse_args()
    a={n:cut_sum(n) for n in range(1,args.max_n+1)}
    checks=[]
    for n in range(1,min(args.dp_max,args.max_n)+1):
        direct=ideal_dp(n)
        assert a[n] == direct, (n,a[n],direct)
        checks.append(n)
    residuals={n:recurrence_residual(n,a) for n in range(1,args.max_n-1)}
    assert all(v==0 for v in residuals.values())
    print(json.dumps({'finite_sum_values':a,'dp_matched_indices':checks,
                      'recurrence_residuals':residuals}, indent=2))


if __name__ == '__main__':
    main()
