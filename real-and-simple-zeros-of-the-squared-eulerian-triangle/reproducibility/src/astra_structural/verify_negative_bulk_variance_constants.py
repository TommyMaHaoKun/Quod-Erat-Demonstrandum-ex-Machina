"""Rational certification of scalar constants in the negative-bulk variance lemma."""
from fractions import Fraction as F
from math import factorial


def exp_lower(x, terms=80):
    return sum((x**k/F(factorial(k)) for k in range(terms+1)),F(0))


def exp_upper(x, terms=80):
    assert x>=0
    partial=exp_lower(x,terms)
    next_term=x**(terms+1)/factorial(terms+1)
    ratio=x/F(terms+2)
    assert ratio<1
    return partial+next_term/(1-ratio)


def decay_upper(x):return 1/exp_lower(x)


def i0_upper(x, terms=20):
    z=x*x/4
    partial=sum((z**k/F(factorial(k)**2) for k in range(terms+1)),F(0))
    next_term=z**(terms+1)/factorial(terms+1)**2
    ratio=z/F((terms+2)**2)
    assert ratio<1
    return partial+next_term/(1-ratio)


def S_upper(a):
    # Terms j=1,2,3; for j=4+r, j(j-1)>=12+8r.
    t=decay_upper(8*a)
    tail=decay_upper(12*a)*(16/(1-t)+8*t/(1-t)**2+t*(1+t)/(1-t)**3)
    return 1+4*decay_upper(2*a)+9*decay_upper(6*a)+tail


# sqrt(v) exp(-v) I_0(v) < .47 on [.8,1], using 200 rational boxes.
for i in range(200):
    a=F(4,5)+F(i,1000);b=a+F(1,1000)
    q=i0_upper(a)/exp_lower(a)
    assert b*q*q<F(47,100)**2
assert i0_upper(F(1))/exp_lower(F(1))<F(47,100)
print('PASS: Poisson-binomial maximum-mass constant on [.8,1]')

# Elementary parameter bounds, using Y>=7.5 and Y/n<=.2.
r0=F(1)-F(1)/F(68,10)
assert r0>F(852,1000)
assert exp_lower(F(16,100))*r0>1
assert exp_upper(F(1,5))-1<F(222,1000)
assert 5*(exp_upper(F(1,5))-1)<F(111,100)
right_gap=1-F(1)/F(68,10)-F(1)/F(75,10)
assert right_gap>F(719,1000)
cmin=1-F(16,100)/F(75,10)
forward=cmin*cmin/(2*F(211,100)*F(1222,1000))-F(1)/(2*F(719,1000)*F(75,10)**2)
assert forward>F(1,6)
backward=(F(9,10)*cmin)**2-F(1)/(F(852,1000)*F(75,10)**2)
assert backward>F(2,3)
assert 1-1/exp_upper(F(1,5))>=F(18,100)
print('PASS: forward, backward and adjacent-ratio constants')

# Finite h intervals. For h<=2 a separate integral-plus-maximum estimate applies.
for a,b,cap in [(2,4,F(542,100)),(4,6,F(240,100)),(6,8,F(162,100)),(8,10,F(131,100))]:
    bound=S_upper(F(a,6))+decay_upper(F(a,2))*S_upper(F(a,3))+F(1,10**7)
    assert bound<cap
    assert (F(47,100)*cap)**2<(F(8,b))**3
    print('PASS: h interval',a,b,'coupled sum <',str(cap))

# Weighted tail, decreasing in n>=250.
tail=F(2,5)*(F(250)/F(75,10))**2/exp_lower(F(5*250,54))
assert tail<F(1,10**7)
print('PASS: geometric tail < 1e-7')

# S(a)<=2 a^(-3/2), 0<a<=2/3: scaled integral and maximum.
# erf(sqrt(a)/2)<=sqrt(a/pi), and pi<22/7 suffice.
# Certified with squared rational comparisons to avoid irrational arithmetic.
# Integral exact at a=2/3 is below 1.21 and maximum below .75.
# Use erf(sqrt(1/6)) <= (2/sqrt(pi))*sqrt(1/6)*(1-1/18+1/360).
# Replacing square roots by rational outward bounds.
sqrtpi=F(177246,100000); sqrta=F(816497,1000000); sqrtone6=F(408249,1000000)
assert sqrtpi*sqrtpi>F(355,113) # elementary pi upper bound 355/113
assert sqrta*sqrta>F(2,3)
assert sqrtone6*sqrtone6>F(1,6)
erf_upper=2*sqrtone6/F(177245,100000)*(1-F(1,18)+F(1,360))
integ=exp_upper(F(1,6))*sqrtpi/F(4)*F(4,3)*(1+erf_upper)+sqrta/F(4)
assert integ<F(121,100)
maximum=(F(2,3)*sqrta)*F(9,4)/exp_lower(F(1,2))
assert maximum<F(75,100)
assert integ+maximum<2
# .47*2*(6^(3/2)+3^(3/2)) < 8^(3/2), using outward roots.
assert F(47,100)*2*(6*F(245,100)+3*F(174,100))<8*F(282,100)
print('PASS: small-h integral bound')
