"""Finite obligations for ALL upper boundary splices, uniformly in m.

The mathematical reduction is in the paper, Section 6 and Appendix C. Only a finite
range of m is checked, with all larger m reduced by phase-preserving +20.
"""
from itertools import combinations
from math import ceil
from fractions import Fraction
from pathlib import Path
import json
Z='01201012';B='01012';BULK='01012323'
HS=('','01012323013','01012323010123')
MS=('01012','01012','20101')
US=('010120101201','0101201','201012010120101201')
fixed=lambda w:(w,0,1)

def templates(s,delta):
    front=[fixed(US[0]),(Z,2 if s==2 else 1,0 if s==2 else 2-s)]
    if s==0:
        V=[(Z,1,-2),(B,2,3),fixed(Z)] if delta else [(Z,1,-3),(B,2,5)]
    elif s==1:
        V=[(Z,1,-1)]+([fixed('012012')] if delta else [])+[(B,2,3)]
    else:
        V=[fixed('012'),(B,2,8),(Z,1,-3)] if delta else [fixed('012012'),(B,2,3),(Z,1,-1)]
    jres=(s-1+delta)%3;joff=-1 if s==0 and delta==0 else 0
    F=[(BULK,2,2*joff),fixed(HS[jres]),(MS[jres],2,2*joff),fixed(US[jres]),(Z,2,10)]
    return front+V,F

def length(parts):return tuple(sum(len(w)*x[i] for w,*x in parts) for i in range(2))
def ev(z,m):return z[0]*m+z[1]

def macro_ends(parts):
    cur=(0,0);out=[cur]
    for w,alpha,beta in parts:
        if not w:continue
        if alpha:
            assert len(w) in (5,8)
            cur=(cur[0]+len(w)*alpha,cur[1]+len(w)*beta);out.append(cur)
        else:
            for _ in range(beta):
                for v in w:cur=(cur[0],cur[1]+1);out.append(cur)
    return out

def bounds(s,delta):
    S,F=templates(s,delta);L=length(S);M=(L[0],L[1]-1)
    lines={M,(0,0)}
    for e in macro_ends(S):
        for shift in (0,1,4):lines.add((e[0],e[1]+shift))
    for e in macro_ends(F):lines.add((e[0],e[1]+6))
    assert all(alpha%2==0 for alpha,beta in lines)
    slopes=sorted({alpha for alpha,beta in lines})
    gap=min(y-x for x,y in zip(slopes,slopes[1:]))
    lo=min(beta for alpha,beta in lines);hi=max(beta for alpha,beta in lines)
    K=max(13,ceil(Fraction(hi-lo+40,gap)))
    assert gap*K-(hi-lo)>=40
    # F covers every third operand checked, for every m>=13.
    lf=length(F);diff=(lf[0]-M[0],lf[1]-M[1]+6)
    assert diff[0]>=0 and ev(diff,13)>=0
    return dict(K=K,lo=lo,hi=hi,slope_gap=gap,max_m=K+19)

def expand(parts,m):
    assert all(alpha*m+beta>=0 for w,alpha,beta in parts)
    return ''.join(w*(alpha*m+beta) for w,alpha,beta in parts)

def check(s,delta,m):
    SS,FF=templates(s,delta);S=expand(SS,m);F=expand(FF,m)
    assert len(F)>=len(S)-7
    for y in range(len(S)-1):
        opts=set()
        if y>=1:opts.add(int(S[y-1]))
        if y>=4:opts.add(int(S[y-4]))
        if y>=6:opts.add(int(F[y-6]))
        v=int(S[y]);assert v not in opts and all(z in opts for z in range(v)),(s,delta,m,y,v,opts)
    return len(S)-1

def main():
    out=[]
    for s in range(3):
        for delta in (0,1):
            b=bounds(s,delta);cells=0
            for m in range(13,b['max_m']+1):cells+=check(s,delta,m)
            row=dict(s=s,delta=delta,m_min=13,**b,cells=cells,passed=True);out.append(row);print(row)
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All six uniform boundary families proved;',sum(x['cells']for x in out),'positions.')

if __name__=='__main__':main()
