#!/usr/bin/env python3
"""Exact counts for the labeled arrays of OEIS A195806.

Python standard library only. Run `python src/counting.py` from any cwd;
the certificate location is resolved relative to this saved source file.
All calculations use integers. This script checks counts, not by itself
the all-n proof; the paper supplies the parameterization and generating
function proof.
"""
import argparse
import itertools
import json
from pathlib import Path


def count_lattice(n):
    """Count the integral parameterization by its two difference coordinates."""
    total = 0
    for p in range(-n, n + 1):
        for q in range(-n, n + 1):
            a = max(abs(p), abs(p + q), abs(2*p + q))
            b = max(abs(q), abs(3*p + q), abs(3*p + 2*q))
            if a <= n and b <= n:
                total += (n + 1 - a)**2 * (n + 1 - b)**2
    return total


def count_chamber(n):
    """Independent loop shape using the dihedral fundamental chamber."""
    total = 0
    for h in range(n // 3 + 1):
        for k in range((n - 3*h) // 2 + 1):
            orbit = 1 if h == k == 0 else 6 if h == 0 or k == 0 else 12
            total += orbit * (n + 1 - 2*h - k)**2 * (n + 1 - 3*h - 2*k)**2
    return total


def count_original(n):
    """Exhaustively enumerate the original 12 noncorner entries.

    Uses only the original equal-line-sum equations, independently of
    the parameterization. Intended for n <= 3, not large instances.
    The entry order is lexicographic (i,j,k), i+j+k=4, excluding corners.
    """
    total = 0
    for u in itertools.product(range(n + 1), repeat=12):
        if not u[2]+u[6] == u[10]+u[11] == u[0]+u[3]:
            continue
        if not u[7]+u[8]+u[9] == u[1]+u[5]+u[9] == u[1]+u[4]+u[7]:
            continue
        if not u[3]+u[4]+u[5]+u[6] == u[0]+u[4]+u[8]+u[11] == u[2]+u[5]+u[8]+u[10]:
            continue
        if not u[0]+u[1]+u[2] == u[3]+u[7]+u[10] == u[6]+u[9]+u[11]:
            continue
        total += 1
    return total


COEFFICIENTS = (
    (1,25,158,650,2275,4680,4680),
    (16,198,1133,3900,8125,9360,4680),
    (105,1087,4922,12350,17875,14040,4680),
    (496,4148,14783,28600,31525,18720,4680),
    (1759,12121,35258,55250,49075,23400,4680),
    (5052,29474,72197,94900,70525,28080,4680),
)


def stated_formula(n):
    m, r = divmod(n, 6)
    return sum(c * m**i for i, c in enumerate(COEFFICIENTS[r]))


def verify_geometry(radius=12):
    """Finite sanity check of exact group/orbit descriptions; not a proof."""
    def norms(x,y):
        return max(abs(x),abs(y),abs(x+y)), max(abs(y-x),abs(2*x+y),abs(x+2*y))
    def orbit(x,y):
        result = set()
        for _ in range(6):
            result.add((x,y))
            result.add((y,x))
            x,y = -y,x+y
        return result
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            points = orbit(x,y)
            assert all(norms(*v)==norms(x,y) for v in points)
            representatives = [(a,b) for a,b in points if a>=b>=0]
            assert len(representatives)==1
            a,b = representatives[0]
            size = 1 if a==0 else 6 if b==0 or a==b else 12
            assert len(points)==size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n',type=int,default=41)
    parser.add_argument('--write',action='store_true',help='write certificates/counts.json')
    args = parser.parse_args()
    if args.max_n < 0:
        parser.error('--max-n must be nonnegative')
    verify_geometry()
    counts = []
    for n in range(args.max_n + 1):
        lattice = count_lattice(n)
        chamber = count_chamber(n)
        predicted = stated_formula(n)
        assert lattice == chamber == predicted, (n,lattice,chamber,predicted)
        counts.append(lattice)
    brute = [count_original(n) for n in range(4)]
    assert brute == [1,16,105,496]
    assert all(count_lattice(n)==brute[n] for n in range(4))
    report = {
        'arithmetic':'exact Python integers',
        'n_min':0,'n_max':args.max_n,'counts':counts,
        'methods':['integral difference-coordinate double sum','dihedral chamber double sum'],
        'original_constraint_exhaustive_counts':brute,
        'all_stated_formulas_agree':True,
        'scope':'Finite arithmetic checks; the manuscript proves the all-n generating-function identity.'
    }
    if args.write:
        destination=Path(__file__).resolve().parents[1]/'certificates'/'counts.json'
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
