"""Independent rational checks for the shifted-rectangle tail/error lemmas."""
from fractions import Fraction as F
from math import factorial


def exp_lower(x, terms=160):
    assert x >= 0
    return sum((x**j / factorial(j) for j in range(terms+1)), F(0))


def exp_upper(x, terms=160):
    assert x >= 0
    ratio = x / (terms+2)
    assert ratio < 1
    return exp_lower(x, terms)+x**(terms+1)/factorial(terms+1)/(1-ratio)


epsilon = F(1,10000)
assert exp_lower(12-F(202,100)-F(1,3)) > 10000
assert exp_upper(F(404,100)) < 57
weighted = ((1+epsilon)/(1-epsilon)**2)**2-1
assert weighted < 7*epsilon
assert 57*weighted < F(4,100)
assert F(8,100)*F(8,7) < F(1,10)
print("PASS: descent, weighted lattice sum, and central mixed margin")

single_ratio = 1/exp_lower(F(11,6))
assert 4*single_ratio/(1-single_ratio)**2 < F(907,1000)
print("PASS: single-vertex off-mode ideal mass < .907")

# At t=sqrt(n)=40, H<=t/4+2=12. The logarithmic derivative of
# (t/4+2)(t^2+1) is <3/t, proving the near expression decreases.
# This includes the eight-unit overlap band below 4 sqrt(n).
near = F(456)*12*1601/exp_lower(F(64))/(1-epsilon)**2
# H epsilon^H decreases for integral H>=7.
far = F(456)*7*epsilon**7/(1-epsilon)**2
assert near < F(1,10**20)
assert far < F(1,10**23)
assert near+far < F(1,1000)
print("PASS: actual Eulerian approximation error < AB/(1000 H)")
