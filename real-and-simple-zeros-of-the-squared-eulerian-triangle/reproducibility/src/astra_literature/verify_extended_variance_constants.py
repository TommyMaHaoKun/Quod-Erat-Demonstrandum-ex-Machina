"""Exact scalar certificate extending the variance lemma to s <= 4 sqrt(n).

Uses only Python's standard library. All comparisons are rational, with
positive Taylor series and geometric remainder bounds.
"""
from fractions import Fraction as F
from math import factorial


def exp_lower(x, terms=100):
    assert x >= 0
    return sum((x**k / factorial(k) for k in range(terms+1)), F(0))


def exp_upper(x, terms=100):
    assert x >= 0
    ratio = x / (terms+2)
    assert ratio < 1
    return exp_lower(x, terms) + x**(terms+1) / factorial(terms+1) / (1-ratio)


def decay_upper(x):
    return 1 / exp_lower(x)


def i0_upper(x, terms=24):
    z = x*x/4
    partial = sum((z**k / factorial(k)**2 for k in range(terms+1)), F(0))
    ratio = z / (terms+2)**2
    return partial + z**(terms+1) / factorial(terms+1)**2 / (1-ratio)


def S_upper(a):
    ratio = decay_upper(8*a)
    tail = decay_upper(12*a) * (
        16/(1-ratio) + 8*ratio/(1-ratio)**2
        + ratio*(1+ratio)/(1-ratio)**3)
    return 1 + 4*decay_upper(2*a) + 9*decay_upper(6*a) + tail


def T_upper(a):
    ratio = decay_upper(8*a)
    tail = decay_upper(12*a) * (
        9/(1-ratio) + 6*ratio/(1-ratio)**2
        + ratio*(1+ratio)/(1-ratio)**3)
    return decay_upper(2*a) + 4*decay_upper(6*a) + tail


def main():
    # Parameter inequalities explained in the accompanying proof note.
    assert F(250)*7*(1+exp_lower(F(314,100)))/22 > exp_upper(F(15,2))
    assert F(253,16)**2 > 250 and F(79,5)**2 < 250
    assert exp_lower(F(7,5)) > 4
    assert F(253,4) + F(7,5) + F(1,1000) < 65
    assert (4+(F(7,5)+F(1,1000))/F(79,5))**2 < 17
    assert exp_lower(F(7,10)) > 2
    ratio_n = 1-F(1)/F(68,10)
    assert ratio_n > F(852,1000)
    assert exp_lower(F(16,100))*ratio_n > 1
    assert exp_upper(F(26,100))-1 < F(298,1000)
    assert (exp_upper(F(26,100))-1)/F(26,100) < F(115,100)
    assert ratio_n-F(1)/F(75,10) > F(719,1000)
    # (1-exp(-t))/t is decreasing. Certify its lower endpoint value.
    assert 1-1/exp_lower(F(26,100)) > F(88,100)*F(26,100)
    cmin = 1-F(16,100)/F(75,10)
    forward = cmin*cmin/(F(1298,1000)*F(215,100)) - 1/(F(719,1000)*F(75,10)**2)
    backward = (F(88,100)*cmin)**2 - 1/(F(852,1000)*F(75,10)**2)
    assert forward > F(2,7)
    assert backward > F(2,3)
    assert backward > F(1,2)
    print("PASS: parameters and tangent-envelope constants")

    # Weighted far tail for J>=3, with geometric ratio below .343.
    r = F(343,1000)
    assert decay_upper(F(15,14)) < r
    geom = r/(1-r) + F(2,3)*r/(1-r)**2 + F(1,9)*r*(1+r)/(1-r)**3
    assert geom < F(13,10)
    tail = F(13,10)*(F(250)/F(15,2))**2*decay_upper(F(3*250,56))
    assert tail < F(3,1000)
    print("PASS: weighted far tail < .003")

    # q(v)=exp(-v)I0(v) is decreasing. Each interval uses q at the left
    # endpoint and sqrt(v) at the right endpoint, compared after squaring.
    for i in range(300):
        a = F(7,10)+F(i,1000)
        b = a+F(1,1000)
        q = i0_upper(a)/exp_lower(a)
        assert b*q*q < F(47,100)**2
    assert i0_upper(F(1))/exp_lower(F(1)) < F(47,100)
    print("PASS: Fourier maximum-mass constant for v >= .7")

    # For h<=2 reuse the integral-plus-maximum bound S(a)<=2a^(-3/2).
    # The standard elementary bounds 3.14159 < pi < 355/113 suffice.
    sqrtpi_upper, sqrtpi_lower = F(177246,100000), F(177245,100000)
    sqrta, sqrtone6 = F(816497,1000000), F(408249,1000000)
    assert sqrtpi_upper**2 > F(355,113)
    assert sqrtpi_lower**2 < F(314159,100000)
    assert sqrta**2 > F(2,3) and sqrtone6**2 > F(1,6)
    erf_upper = 2*sqrtone6/sqrtpi_lower*(1-F(1,18)+F(1,360))
    integral = exp_upper(F(1,6))*sqrtpi_upper/F(4)*F(4,3)*(1+erf_upper)+sqrta/F(4)
    maximum = F(2,3)*sqrta*F(9,4)/exp_lower(F(1,2))
    assert integral < F(121,100) and maximum < F(75,100)
    assert integral+maximum < 2
    # Outward rational square-root bounds establish the strict margin.
    assert F(2646,1000)**2 > 7 and F(1733,1000)**2 > 3
    assert F(2828,1000)**2 < 8 and F(1415,1000)**2 > 2
    small = F(47,100)*2*(7*F(2646,1000)+3*F(1733,1000))
    small += F(47,100)*F(3,1000)*2*F(1415,1000)
    assert small < 8*F(2828,1000)
    print("PASS: small-h margin")

    interval_caps = [(2,3,F(2969,1000)), (3,4,F(1803,1000)),
                     (4,6,F(1298,1000)), (6,8,F(861,1000)),
                     (8,10,F(676,1000)), (10,11,F(584,1000))]
    for a,b,cap in interval_caps:
        bound = S_upper(F(a,7)) + decay_upper(F(a,2))*S_upper(F(a,3)) + F(3,1000)
        assert F(47,100)*bound < cap
        assert cap**2 < F(8,b)**3
        assert (F(47,100)*bound)**2 < F(8,b)**3, (a,b)
        print("PASS: maximum-mass h interval", a, b)

    # For h>=11 clamp L to the two adjacent integers having greatest mass.
    for i in range(22,34):
        a,b = F(i,2),F(i+1,2)
        small_adjacent = decay_upper(a/4)
        delta_right = T_upper(a/7)+small_adjacent*S_upper(a/3)
        delta_left = T_upper(a/3)+small_adjacent*S_upper(a/7)
        delta = max(delta_right,delta_left)+F(3,1000)
        gap = F(8)/b-F(1,4)-delta
        assert gap > 0 and delta < gap*gap, (a,b)
        print("PASS: two-point concentration h interval", str(a), str(b))
    print("PASS: all extended variance constants")


if __name__ == "__main__":
    main()
