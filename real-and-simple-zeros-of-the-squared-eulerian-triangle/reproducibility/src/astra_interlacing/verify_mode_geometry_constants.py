"""Exact scalar certificate for the shifted-mode bridge.

Only standard-library rational arithmetic is used.  Structural inequalities
are proved in the paper; this script checks their numerical constants.
"""
from fractions import Fraction as F
from math import comb, factorial


def exp_lower(x, terms=100):
    x = F(x)
    assert x >= 0
    return sum((x**j / factorial(j) for j in range(terms + 1)), F(0))


def exp_upper(x, terms=100):
    x = F(x)
    ratio = x / (terms + 2)
    assert 0 <= ratio < 1
    return exp_lower(x, terms) + x**(terms + 1) / factorial(terms + 1) / (1-ratio)


def shift(poly, a):
    return [sum((poly[j]*comb(j, i)*a**(j-i)
                 for j in range(i, len(poly))), F(0))
            for i in range(len(poly))]


def main():
    # Eight-unit band: the numerator of delta_h-12 is four times
    # v^4-41v^3+18v^2+192v-192. It is positive for v>=41.
    poly = [F(-192), F(192), F(18), F(-41), F(1)]
    assert all(c > 0 for c in shift(poly, F(41)))
    assert F(41**2, 4*41-8) < 11
    assert F(1600-10, 121) > 12
    # General mode coordinates have sum S<3v/5; n-S>S^2 for v>40.
    assert F(16,25)*40-F(3,5) > 0
    print('PASS: eight-unit band, curvature >12, and diagonal dominance')

    # Outer separator: log n>25/4, L<=sqrt(n)/5, and L>=7.
    assert exp_upper(F(25,4)) < 1600
    assert exp_lower(F(8)) > 1600
    assert F(1600, 32) > 49
    assert exp_lower(F(40,3)-2) > 24
    assert F(2,5)/24 < F(1,3)
    assert F(37,9) > 4
    assert exp_upper(F(4)) < 1000
    print('PASS: outer separator lies beyond 4sqrt(n), with four small neighbors')

    # Global joint and single-vertex descents.
    eps = F(1,10000)
    assert exp_lower(12-F(202,100)-F(1,3)) > 1/eps
    assert exp_upper(F(404,100)) < 57
    weighted = ((1+eps)/(1-eps)**2)**2-1
    assert weighted < 7*eps
    assert 57*weighted < F(4,100)
    assert exp_lower(F(11,6)) > F(25,4)
    r = F(4,25)
    off = 4*r/(1-r)**2
    assert off == F(400,441)
    assert off < 1-F(1,1000)
    assert F(7,8)-F(8,100)-F(1,1000) > F(79,100)
    print('PASS: weighted tail <.04AB, vertex dominance, and paired sign margin')

    # Uniform actual-versus-ideal error, evaluated at the decreasing endpoints.
    near = 456*F(12)*1601/(1-eps)**2/exp_lower(F(64))
    far = 456*7*eps**7/(1-eps)**2
    assert near+far < F(1,1000)
    assert F(40**2,5)-F(69,10)*40-3 > 0
    print('PASS: Eulerian replacement error <AB/(1000H)')

    # General separator phase constants.
    assert F(118,100)/exp_lower(F(2)) < F(1,6)
    assert exp_lower(F(120)) > 1000
    assert F(10,120**2) < F(1001,1000)**2-1
    assert F(1601*10,3*120**3) < F(4,1000)
    assert F(1,120) < F(9,1000)
    assert F(604,1000)*F(22,7)+F(42,100) < F(3,4)*F(314,100)
    print('PASS: shifted-separator phase error <3pi/4')


if __name__ == '__main__':
    main()
