"""Exact constants for positive-s pole dominance on [3sqrt(n),4sqrt(n)]."""
from fractions import Fraction as F
from verify_negative_bulk_variance_constants import exp_lower, exp_upper, decay_upper

# B=pi²/s²<.005, and phi(3)=.75-.5log4>.05.
assert F(987,100)/2250<F(5,1000)
assert exp_lower(F(14,10))>4
assert F(75,100)-F(7,10)>F(5,1000)/2

# Q>=25 and Q*pi/s>1.6, taking Q the largest odd <=sqrt(3)s/pi.
assert 3*2250>25*25*F(987,100)
assert 3*F(25,27)**2>F(16,10)**2

# First four pole bounds.
first=F(0)
for q in [3,5,7,9]:
    E=F(q*q-1)*F(986,100)/(64+2*F(q*q+1)*F(987,100)/250)
    first+=decay_upper(E)
assert first<F(326,1000)

# Remaining finite poles q>=11 use a Gaussian tail.
alpha=F(986,100)/F(16016,100)
finite_tail=decay_upper(120*alpha)/(1-decay_upper(48*alpha))
assert finite_tail<F(1,1000)

# D_Q>.62, so R_Q<exp(-.31n). The far tail adds exponent <.197n.
assert exp_upper(F(124,100))<F(356,100)/F(1005,1000)
assert F(251,250)/(2*F(16,10)**2)<F(197,1000)
assert 500/exp_lower(F(113,1000)*250)<F(1,1000)
assert F(326,1000)+F(1,1000)+F(1,1000)<F(33,100)
print('PASS: positive-s pole sum <.33 for n>=250, 3sqrt(n)<=s<=4sqrt(n)')
