"""Generate rational median brackets and a convexity-based finite certificate.

Exploratory generation uses Arb (python-flint). The released certificate is
checked independently using only integer arithmetic by rational_verify.py.
All paths are relative to this project; no network calls are made.
"""
from fractions import Fraction as Q
from pathlib import Path
import csv
import json
import time
from flint import arb, ctx

ROOT = Path(__file__).resolve().parents[1]
ctx.prec = 160
C = arb(2).log()
CACHE = {}
SCALE = 10**22


def ball(q):
    q = Q(q)
    return arb(q.numerator) / q.denominator


def median(k):
    if k in CACHE:
        return CACHE[k]
    kb = ball(k)
    lo, hi = Q(0), k
    for _ in range(86):
        mid = (lo + hi) / 2
        p = ball(mid).gamma_lower(kb, regularized=1)
        if p < arb(1)/2:
            lo = mid
        elif p > arb(1)/2:
            hi = mid
        else:
            raise ArithmeticError("CDF sign unresolved at generation precision")
    lo = Q((lo.numerator*SCALE)//lo.denominator, SCALE)
    hi = Q((hi.numerator*SCALE)//hi.denominator+1, SCALE)
    assert ball(lo).gamma_lower(kb, regularized=1) < arb(1)/2
    assert ball(hi).gamma_lower(kb, regularized=1) > arb(1)/2
    CACHE[k] = lo, hi
    return lo, hi


def cell(a, b):
    c = b + min(b-a, Q(1,100))
    la, _ = median(a)
    lb, _ = median(b)
    _, uc = median(c)
    d = (uc-lb)/(c-b)
    bracket = ball(d)-C*ball(la)/ball(b*b)
    value = (C/ball(a)).exp()*bracket
    return c, value


def main():
    start = time.time()
    cells = []
    pending = [(Q(1,10), Q(7))]
    while pending:
        a,b = pending.pop()
        c,v = cell(a,b)
        # Require visible slack, so small changes in arithmetic precision do
        # not affect the result. v is an enclosure, not a point estimate.
        if v < arb("0.99999"):
            cells.append((a,b,c))
        else:
            mid=(a+b)/2
            pending.extend([(mid,b),(a,mid)])
        if len(cells) and len(cells)%250==0:
            print(f"accepted={len(cells)} nodes={len(CACHE)} elapsed={time.time()-start:.1f}s",flush=True)
    cells.sort()
    needed=sorted({x for row in cells for x in row})
    dest=ROOT/'certificates'
    dest.mkdir(exist_ok=True)
    with (dest/'median_brackets.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['k','lower','upper'])
        for k in needed:
            lo,hi=median(k);w.writerow([str(k),str(lo),str(hi)])
    with (dest/'intervals.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['a','b','c'])
        w.writerows([[str(x) for x in row] for row in cells])
    worst=max((cell(a,b)[1].upper(),a,b) for a,b,c in cells)
    result={'intervals':len(cells),'median_nodes':len(needed),
            'domain':['1/10','7'],'max_c':str(max(x[2] for x in cells)),
            'worst_upper':str(worst[0]),'worst_cell':[str(worst[1]),str(worst[2])],
            'arb_bits':ctx.prec,'generation_seconds':round(time.time()-start,3)}
    (dest/'generation_summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
