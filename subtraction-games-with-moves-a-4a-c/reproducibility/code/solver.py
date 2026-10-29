"""Exact Sprague--Grundy solver; complete recurrence-state certificates.

No external dependencies.  Run `python solver.py --help`.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
import time

def primitive_period(word):
    pi = [0] * len(word)
    for i in range(1, len(word)):
        j = pi[i-1]
        while j and word[i] != word[j]:
            j = pi[j-1]
        if word[i] == word[j]:
            j += 1
        pi[i] = j
    p = len(word) - pi[-1]
    return p if len(word) % p == 0 else len(word)

def solve(a: int, c: int, cap: int = 200000):
    if not (a >= 2 and c > 4*a and math.gcd(a,c) == 1):
        raise ValueError('inadmissible parameters')
    g = bytearray()
    seen = {}
    state = 0
    mask = (1 << (2*c)) - 1
    for n in range(cap):
        used = 0
        for s in (a,4*a,c):
            if s <= n:
                used |= 1 << g[n-s]
        v = 0
        while used & (1 << v):
            v += 1
        g.append(v)
        state = ((state << 2) | v) & mask
        if n < c-1:
            continue
        start = n-c+1
        if state in seen:
            first = seen[state]
            d = start-first
            assert g[first:first+c] == g[start:start+c]
            p = primitive_period(g[first:first+d])
            q = first
            while q and g[q-1] == g[q-1+p]:
                q -= 1
            assert (p,q) == (d,first), 'first complete-state repeat must be minimal'
            assert all(g[k] == g[k+p] for k in range(q,len(g)-p))
            return dict(a=a,c=c,p=p,q=q,c_mod_5a=c%(5*a),c_div_5a=c//(5*a),
                        prefix=''.join(map(str,g[:q])),
                        block=''.join(map(str,g[q:q+p])),
                        state_first=first,state_repeat=start,terms=len(g),status='certified')
        seen[state] = start
    return dict(a=a,c=c,status='incomplete',terms=len(g))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--a-max',type=int,default=12)
    parser.add_argument('--c-max',type=int,default=150)
    parser.add_argument('--cap',type=int,default=200000)
    parser.add_argument('--output',default='data/survey')
    args=parser.parse_args()
    start=time.monotonic()
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for a in range(2,args.a_max+1):
        for c in range(4*a+1,args.c_max+1):
            if math.gcd(a,c)==1:
                rows.append(solve(a,c,args.cap))
    out.with_suffix('.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    fields=['a','c','p','q','c_div_5a','c_mod_5a','terms','status']
    with out.with_suffix('.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
        w.writeheader();w.writerows(rows)
    good=[r for r in rows if r['status']=='certified']
    meta=dict(a_max=args.a_max,c_max=args.c_max,cap=args.cap,total=len(rows),
              certified=len(good),incomplete=len(rows)-len(good),
              max_p=max((r['p'] for r in good),default=0),
              max_q=max((r['q'] for r in good),default=0),
              pure=[(r['a'],r['c']) for r in good if r['q']==0],
              elapsed_seconds=time.monotonic()-start)
    out.with_name(out.name+'_summary.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(json.dumps(meta,indent=2))

if __name__=='__main__':main()
