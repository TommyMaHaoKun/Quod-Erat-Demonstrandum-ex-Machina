from fractions import Fraction as F
from math import factorial

def require(condition, description):
    if not condition:
        raise ArithmeticError(description)

def binom(a,k):
    out=F(1)
    for j in range(k): out=out*(a-j)/(j+1)
    return out

def poch_half(r):
    out=F(1)
    for j in range(r): out*=F(2*j+1,2)
    return out

cs=[]
for r in range(11):
    v=sum((binom(F(2*r+5,2),j)*binom(F(-2*r-1,2),2*r-j)/3**(2*r-j) for j in range(2*r+1)),F(0))
    c=(-1)**r*poch_half(r)*v/3**r
    cs.append(c)
    print('c',r,str(c),float(c))
S0=sum((76*poch_half(r)/115**r for r in range(1,11)),F(0))
S1=sum((76*r*poch_half(r)/115**r for r in range(1,11)),F(0))
S2=sum((76*r*(r+1)*poch_half(r)/115**r for r in range(1,11)),F(0))
require(S0<F(34,100), "S0 bound")
require(S1<F(35,100), "S1 bound")
require(S2<F(72,100), "S2 bound")
curv=(S2/(1-S0)+S1*S1/(1-S0)**2+2*S1/(1-S0))/9
require(curv<F(1,2), "Exact polynomial curvature bound")
B=210*poch_half(11)
require(B<1410000000, "Gaussian remainder constant")
# B X^-11 <= (1/1000) X^-5 for X>=115
require(1000*B<115**6, "Gaussian remainder endpoint")
print('S0,S1,S2,curvature',*[float(x) for x in (S0,S1,S2,curv)])
print('B',str(B),float(B))
print('All rational inequalities passed.')
# Exact positive-term lower bounds for exp at the endpoint; no floating point.
def exp_lower(x, terms=160):
    term=F(1)
    out=term
    for k in range(1,terms+1):
        term=term*x/k
        out+=term
    return out
require(exp_lower(F(16*115,25)) > 10000*180*115**5,
        "Gaussian exponential tail endpoint")
require(exp_lower(F(11*115,25)) > 10000*5*115**5,
        "Horizontal exponential tail endpoint")
# Because X^(9/2)<=X^5 and X^5 exp(-cX) decreases for X>=115,
# each exponential error is <(1/10000) X^-5 throughout the domain.
print('All exponential endpoint certificates passed.')
from pathlib import Path
import json
crude_curvature=(F(72,100)/F(66,100)+F(35,100)**2/F(66,100)**2+2*F(35,100)/F(66,100))/9
require(crude_curvature<F(1,2), "Coarse polynomial curvature bound")
cert={
    'scope':'Exact rational checks for the explicit major-arc model and its curvature; the analytic lemmas are proved in paper/major_arc.tex.',
    'domain_X_min':115,
    'coefficients_c_r':[str(c) for c in cs],
    'rational_sums':{'S0':str(S0),'S1':str(S1),'S2':str(S2),'curvature_bound':str(curv),'crude_curvature_bound':str(crude_curvature)},
    'B':str(B),
    'gaussian_exponential_lower_bound_terms':160,
    'horizontal_exponential_lower_bound_terms':160,
    'all_checks_passed':True
}
out_path=Path(__file__).resolve().parents[1]/'certificates'/'major_arc.json'
out_path.parent.mkdir(exist_ok=True)
out_path.write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
print('Certificate written:',out_path)
