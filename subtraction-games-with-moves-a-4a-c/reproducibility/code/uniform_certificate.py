"""Standalone exact proof checker for the interval 0, 2, 3 word formulas.
Python 3 standard library only. This is NOT a state-repeat search.
Lengths are affine pairs (b,g), meaning b+g*t, where t=r/a.
A segment (word,m,b) repeats that word m*k+b times.
"""
from fractions import Fraction as Q
from itertools import combinations
from bisect import bisect_right
from math import ceil
import json
from pathlib import Path

add=lambda x,y:tuple(a+b for a,b in zip(x,y))
sub=lambda x,y:tuple(a-b for a,b in zip(x,y))
ev=lambda x,t:x[0]+x[1]*t
unit=(1,0);r=(0,1);s=(1,-1)
B=[(0,unit),(1,unit),(0,unit),(1,unit),(2,unit)]
U=[(0,unit),(1,unit)]
F=lambda x:[(0,x),(2,sub(unit,x)),(1,x)]
R=F(r);S=F(s);D=[(3,r)];E=[(3,(-1,2))]
one=lambda w:(w,0,1)

def template(tag):
    """Return F, prefix segment count, move intercept d, min k, period type."""
    if tag[0]=='0':
        C=[(0,r),(3,s),(1,r)];D0=C+[(2,s)]+C+S+C
        H=[(B,1,0),one(D0)]
        if tag=='0l':W=[(U+S+R,1,-1),one(U+R+S+R)]
        else:
            H += [(U+S+R,1,-1),one(U+S)]
            V=F((2,-2));X=R+R+V
            W=[(X,1,0),one(R)] if tag=='0m' else [one(X)]
        d=0;kmin=2;short=tag=='0h'
    elif tag[0]=='2':
        if tag[1]=='l':
            H=[(B,1,0),one(U+R+S+D+S+R),(U+S+R,1,-1),
               (U+R+S,1,0),one(U+R)]
            V=F((0,2));X=S+V+S
            W=[(X,1,0),one(S+V)] if tag=='2ll' else [one(X)]
        else:
            H=[(B,1,0),one(U+R+S+D+S+R),(U+S+R,1,0),
               one(U+S+E+S),(U+R+S,1,1),one(E)]
            V=F((2,-2));X=V+R+R
            W=[(X,1,1),one(V+[(3,(-2,3))])] if tag=='2ul' else [one(X)]
        d=2;kmin=1;short=tag in ('2ls','2us')
    else:
        H=[(B,1,1),one([(0,r),(3,s)])]
        if tag=='3l':
            X=[(0,unit),(1,unit),(2,r),(0,unit),(1,unit),(2,s)]
            W=[one([(1,r),(2,s)]),(X,1,1),
               one([(0,(0,2)),(3,(1,-2)),(1,r)])]
        else:
            X=[(1,r),(2,s),(0,unit),(1,unit),(2,r),(0,unit),(1,s)]
            W=[one(X)]
        d=3;kmin=1;short=tag=='3h'
    result=H+[(X,1,2)] if short else H+W+W
    # 0/2 lower long: P=c+1. 2 upper long/3 lower: P=c+4.
    ptype=0 if short else 4 if tag in ('2ul','3l') else 1
    return result,len(H),d,kmin,ptype

# left, right, include left, include right
domains={
 '0l':(Q(0),Q(1,2),False,True),'0m':(Q(1,2),Q(2,3),False,False),
 '0h':(Q(2,3),Q(1),True,False),
 '2ll':(Q(0),Q(1,3),False,False),'2ls':(Q(1,3),Q(1,2),True,False),
 '2us':(Q(1,2),Q(2,3),False,True),'2ul':(Q(2,3),Q(1),False,False),
 '3l':(Q(0),Q(1,2),False,False),'3h':(Q(1,2),Q(1),True,False)}

def bound(tag):
    segs,nh,d,kmin,ptype=template(tag);cur=(0,0,0);ends=[cur]
    for w,m,b in segs:
        if m:
            length=(0,0)
            for _,x in w:length=add(length,x)
            assert length==(5,0)
            cur=add(cur,(5*m,5*b,0));ends.append(cur)
        else:
            for _ in range(b):
                for _,x in w:cur=add(cur,(0,*x));ends.append(cur)
    shifted={add(x,v) for x in ends for v in ((0,0,0),(0,1,0),(0,4,0),(5,d,1))}
    assert all(x[0]%5==0 for x in shifted)
    lo=min(min(b,b+g) for m,b,g in shifted)
    hi=max(max(b,b+g) for m,b,g in shifted)
    K=max(kmin,ceil(Q(hi-lo+5,5)))
    assert 5*K-(hi-lo)>=5
    return K,lo,hi

def check(tag,k):
    segs,nh,d,kmin,ptype=template(tag);cur=(0,0);runs=[]
    for j,(w,m,b) in enumerate(segs):
        if j==nh:prefix=cur
        assert m*k+b>=0
        for _ in range(m*k+b):
            for v,x in w:
                end=add(cur,x);runs.append((cur,end,v));cur=end
    total=cur;c=(5*k+d,1);moves=[(0,0),(1,0),(4,0),c]
    ends={add(x,v) for l,h,_ in runs for x in (l,h) for v in moves}
    left,right,il,ir=domains[tag];cuts={left,right}
    for (b,g),(bb,gg) in combinations(ends,2):
        if g!=gg:
            t=Q(bb-b,g-gg)
            if left<=t<=right:cuts.add(t)
    cuts=sorted(cuts)
    tests={(x+y)/2 for x,y in zip(cuts,cuts[1:])}
    tests.update(t for t in cuts if left<t<right or(t==left and il)or(t==right and ir))
    count=0;options_seen={v:set() for v in range(4)}
    for t in sorted(tests):
        assert all(ev(h,t)>=ev(l,t) for l,h,_ in runs)
        rr=[(ev(l,t),ev(h,t),v) for l,h,v in runs if ev(h,t)>ev(l,t)]
        assert rr[0][0]==0 and rr[-1][1]==ev(total,t)
        assert all(x[1]==y[0] for x,y in zip(rr,rr[1:]))
        starts=[l for l,h,v in rr];M=ev(total,t);C=ev(c,t)
        P=5 if ptype==0 else C+ptype
        assert M>=ev(prefix,t)+C+P
        boundaries=sorted({Q(0),M}|{ev(x,t) for x in ends if 0<=ev(x,t)<=M})
        def at(x):
            assert 0<=x<M
            return rr[bisect_right(starts,x)-1][2]
        for l,h in zip(boundaries,boundaries[1:]):
            x=(l+h)/2;v=at(x)
            opts={at(x-m) for m in (Q(1),Q(4),C) if m<=x}
            assert v not in opts and all(j in opts for j in range(v)),(tag,k,t,l,h,v,opts)
            options_seen[v].add(tuple(sorted(opts)));count+=1
    return dict(k=k,cuts=list(map(str,cuts)),tests=list(map(str,sorted(tests))),cells=count,
                options={v:sorted(x) for v,x in options_seen.items()})

def main():
    output={}
    for tag in domains:
        K,lo,hi=bound(tag);kmin=template(tag)[3]
        checks=[check(tag,k) for k in range(kmin,K+1)]
        output[tag]=dict(K=K,lo=lo,hi=hi,cells=sum(x['cells'] for x in checks),checks=checks)
        print(tag,'K=',K,'bounds=',(lo,hi),'cells=',output[tag]['cells'])
    for tag,count in {'2ll':1010,'2ls':2232,'2us':4168,'2ul':3339,'3l':1029,'3h':765}.items():
        assert output[tag]['cells']==count
    Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
    print('All exact uniform-family certificates passed.')

if __name__=='__main__':main()
