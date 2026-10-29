"""Independent adversarial checks using cell masks and rational polynomials.

No conjectured recurrence is used to generate the array counts.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial as fac
import json
from pathlib import Path

def count_cells(n):
    pred=[]
    for i in range(4):
        for j in range(n):
            cells=[(i,j-1),(i-1,j),(i-1,j-1),(i-1,j+1)]
            pred.append(sum(1<<(r*n+c) for r,c in cells if 0<=r<4 and 0<=c<n))
    full=(1<<(4*n))-1
    @lru_cache(None)
    def rec(mask):
        if mask==full:return 1
        total=0
        for c,p in enumerate(pred):
            if not (mask>>c)&1 and p&mask==p:
                total+=rec(mask|(1<<c))
        return total
    return rec(0)

def y(n):
    assert n>=2
    return [F((-1)**k*fac(n-2)*(k+1),fac(n-2-k)*fac(n+k)) for k in range(n-1)]

def add(*polys):
    out=[F(0)]*max(map(len,polys))
    for p in polys:
        for i,v in enumerate(p):out[i]+=v
    while len(out)>1 and out[-1]==0:out.pop()
    return out

def scale(p,a):return [a*x for x in p]
def mul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return out
def deriv(p):return [i*x for i,x in enumerate(p)][1:] or [F(0)]
def integral(p):return sum(v/F(i+1) for i,v in enumerate(p))
def moment(n):return integral([F(0)]*(2*n-1)+mul([1,-3,3,-1],y(n)))
def beta(n):return F(6*fac(2*n-1),fac(2*n+3))
def via_moment(n):
    C=F(1,fac(n-1));K=F(fac(4*n-1),(2*n-1)*fac(n)*fac(n-1))
    r1=F(-8*(n-1)*(2*n-1)*(3*n+1),(4*n-1)*(4*n+1))
    r0=F((n+1)*(2*n+3)*(6*n-1),n*(4*n-1)*(4*n+1))
    return K/F(2*n-1)*(C*r1*moment(n)+C*C*r0*beta(n))

def run():
    report={'description':'Independent finite checks, not an all-n proof','counts':{},'polynomial_identity_n':[],'moment_recurrence_n':[]}
    for n in range(2,31):
        p=y(n)
        ode=add(mul([0,1,0,-1],deriv(p)),mul([n,2*(n-2),n-2],p),[-F(1,fac(n-1))])
        assert all(v==0 for v in ode),(n,'ODE',ode)
        cont=add(mul([0,2*(2*n-1)],y(n+1)),mul([1,-2,1],p),[-F(1,fac(n))])
        assert all(v==0 for v in cont),(n,'contiguity',cont)
        report['polynomial_identity_n'].append(n)
        d=F(n*(2*n+1)*(4*n+5),3*(2*n-1)*(3*n+2)*(3*n+4)*(4*n+1))
        e=F((2*n+1)*(28*n*n+26*n+1),3*(n+1)*(2*n-1)*(3*n+2)*(3*n+4)*(4*n+1))
        assert moment(n+1)+d*moment(n)==F(1,fac(n-1))*beta(n)*e,(n,'moment recurrence')
        report['moment_recurrence_n'].append(n)
        if n<=14:
            cells=count_cells(n)
            result=via_moment(n)
            assert result.denominator==1 and result.numerator==cells,(n,result,cells)
            report['counts'][n]=str(cells)
    assert count_cells(1)==1
    report['counts'][1]='1'
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':run()
