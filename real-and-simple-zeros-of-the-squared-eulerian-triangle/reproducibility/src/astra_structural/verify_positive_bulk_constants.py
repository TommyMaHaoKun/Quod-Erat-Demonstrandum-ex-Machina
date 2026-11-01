"""Exact constants for positive-s pole dominance on [0,3sqrt(n)]."""
from fractions import Fraction as F
from verify_negative_bulk_variance_constants import exp_lower, exp_upper

n=250
for q,threshold,cap in [(3,F(60,100),F(55,100)),(5,F(170,100),F(19,100)),(7,F(311,100),F(45,1000)),(9,F(460,100),F(1,81))]:
    E=F(7*n*(n-1)*(q*q-1))*F(986,100)/(6*(9*n+q*q*F(987,100))*(16*n+F(987,100)))
    assert E>threshold
    assert 1/exp_lower(threshold)<cap
threshold=F(16*n)/F(986,100)/(F(7*(n-1),54)-1)
assert threshold<13
odd_tail=F(987,100)/8-1-F(1,9)-F(1,25)-F(1,49)
assert odd_tail<F(63,1000)
assert F(55,100)+F(19,100)+F(45,1000)+F(63,1000)<F(85,100)
assert 16*exp_upper(F(1))**2<250
print('PASS: positive-s pole sum <.85 for n>=250, 0<=s<=3sqrt(n)')
