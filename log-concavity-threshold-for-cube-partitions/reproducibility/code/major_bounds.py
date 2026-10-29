"""Exact rational certificates for the cubic saddle model. Python >= 3.9."""
from fractions import Fraction as F
from math import factorial
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if not __debug__:
    raise RuntimeError('Run without -O: proof checks must remain enabled.')

def rising(a, k):
    v = F(1)
    for i in range(k):
        v *= a+i
    return v

def binom(a, k):
    v=F(1)
    for j in range(k):
        v *= (a-j)/(j+1)
    return v

def coefficient(r):
    # [z^(2r)] (1+z)^(r+4)(1+2z/3+z^2/6)^(-r-1/2)
    degree=2*r
    total=F(0)
    for k in range(degree+1):
        outer=binom(-F(2*r+1,2),k)
        for b in range(k+1):
            d=k+b
            if d<=degree:
                total += (outer*binom(F(k),b)*F(2,3)**(k-b)*F(1,6)**b
                          *binom(F(r+4),degree-d))
    return (-1)**r*rising(F(1,2),r)*total/6**r

def exp_lower(q, terms=500):
    term=F(1); total=term
    for j in range(1,terms+1):
        term *= q/j
        total += term
    return total

def main():
    X0=F(50)
    cs=[coefficient(r) for r in range(25)]
    assert cs[0]==1 and cs[1]==-F(67,144)
    S=[sum((abs(cs[r])*([1,r,r*(r+1)][j])/X0**r for r in range(1,25)),F(0)) for j in range(3)]
    assert S[0]<F(1,100) and S[1]<F(1,100) and S[2]<F(1,50)
    curv=(S[2]/(1-S[0])+S[1]**2/(1-S[0])**2+3*S[1]/(1-S[0]))/16
    assert curv<F(1,100)
    # The analytic Rouché and Cauchy bounds in the manuscript.
    assert 2*F(6,5)**2<3
    assert F(2,9)*23*10<52
    assert 52/(1-F(10,11)**2)<300
    B=750*rising(F(1,2),25)*F(10,11)**50
    local=B/X0**18
    # Replace sqrt(X) by 1 when upper bounding X^(-1/2) at X>=50.
    gaussian=1000*X0**7/exp_lower(X0)
    horizontal=10*X0**7/exp_lower(F(9,10)*X0)
    assert local<F(1,100000)
    assert gaussian<F(1,100000)
    assert horizontal<F(1,10000)
    assert local+gaussian+horizontal<F(1,1000)
    # Curvature: 3X/4-5/4-1/100 >= 7X/10 for X>=50.
    assert F(3,4)*X0-F(5,4)-F(1,100)>=F(7,10)*X0
    report={
      'status':'PASS','domain':'X >= 50','order':24,
      'coefficients':[str(c) for c in cs],
      'S0_S1_S2':[str(x) for x in S],
      'diagnostic_floats':{'local_times_X7':float(local),'gaussian_times_X7':float(gaussian),'horizontal_times_X7':float(horizontal),'curvature_error':float(curv)},
      'conclusion':'|V/M - P| < X^(-7)/1000; curvature >= (7/10) X/m^2',
      'arithmetic':'All decisions above use Fraction; floats are display only.'}
    path=ROOT/'certificates'/'major_bounds.json'
    path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'diagnostic_floats':report['diagnostic_floats']}))

if __name__=='__main__': main()
