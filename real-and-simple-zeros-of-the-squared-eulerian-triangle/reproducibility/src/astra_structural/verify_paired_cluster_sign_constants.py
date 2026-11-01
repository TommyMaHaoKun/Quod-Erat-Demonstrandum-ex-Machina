"""Rational constants for the paired-cluster independent-root/sign lemma."""
from fractions import Fraction as F
from verify_negative_bulk_variance_constants import exp_lower, exp_upper

epsilon=1/exp_lower(F(12))
t=F(1,1000);E=exp_upper(t);r=E*epsilon
value_tail=epsilon*(E+E*E)/(1-r)
assert value_tail<F(2,100000)
assert value_tail<t/(1+t)

T=F(202,100);E=exp_upper(T);r=E*epsilon
weighted_tail=epsilon*(E+E*E*(2-r))/(1-r)**2
assert weighted_tail<F(1,1000)
assert E<F(100,13)
assert F(13,100)-F(1,1000)>F(128,1000)
assert F(2)+F(1,1000)<T
assert F(7,8)-F(8,100)-F(1,1000)>F(79,100)
print('PASS: independent roots within .001, positive derivatives on 2.02-neighborhoods, paired actual sign margin .79 AB/H')
