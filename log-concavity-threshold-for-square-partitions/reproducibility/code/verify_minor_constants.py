"""Pure-rational audit of constants in the uniform minor-arc argument.

Python 3.9+ standard library only. All comparisons use fractions or integers.
The analytic reduction and monotonicity proof are in research/minor_arcs.md
and research/review_finite_and_minor.md. The assumed A enclosure is 2.31<A<2.32.
"""

from fractions import Fraction as Q
import json
from pathlib import Path


def require(condition, description):
    if not condition:
        raise ArithmeticError(description)


def log_bounds(q, terms=160):
    """For q>1, log(q)=2*sum z^(2k+1)/(2k+1), z=(q-1)/(q+1).

    The positive tail after terms is at most
    2*z^(2*terms+1)/((2*terms+1)*(1-z*z)).
    """
    require(q > 1 and terms >= 1, "Invalid log-bound arguments")
    z = (q - 1) / (q + 1)
    power = z
    partial = Q(0)
    for k in range(terms):
        partial += 2 * power / (2 * k + 1)
        power *= z * z
    remainder = 2 * power / ((2 * terms + 1) * (1 - z * z))
    return partial, partial + remainder


def exp_negative_upper(a, terms=240):
    """exp(-a) <= 1 / sum_(k=0)^terms a^k/k!, for a>0."""
    require(a > 0 and terms >= 1, "Invalid exponential-bound arguments")
    term = Q(1)
    partial = term
    for k in range(1, terms + 1):
        term *= a / k
        partial += term
    return 1 / partial


def outward_decimal(q, upper, digits=15):
    scale = 10 ** digits
    scaled = q * scale
    integer = ((scaled.numerator + scaled.denominator - 1) // scaled.denominator
               if upper else scaled.numerator // scaled.denominator)
    return str(Q(integer, scale))


def main():
    c = Q(21, 25)
    require((Q(23, 24) / Q(261, 250)) ** 2 > c,
            "Sine/sinh squared-ratio bound")
    require(Q(1, 24) / (1 - Q(1, 80)) == Q(10, 237),
            "Sinh geometric-tail identity")
    require(Q(10, 237) < Q(11, 250), "Sinh rational upper bound")

    l46, u46 = log_bounds(Q(46, 25))
    l361, u361 = log_bounds(Q(361, 25))
    l4, u4 = log_bounds(Q(4))
    require(l46 / 2 > Q(38, 125), "Near-arc exponential rate")
    require(u361 / 2 < Q(67, 50), "Near-arc floor-loss logarithm")
    require(l4 > Q(67, 50), "exp(1.34)<4")
    require(4 * c / (1 + c) - u46 > 1, "h derivative at r=1")
    v4 = 16 * c
    require(4 * v4 / (1 + v4) - u361 > 1, "h derivative at r=4")
    require(Q(9, 40) * l361 > Q(3, 5), "Intermediate-arc rate")
    require(10000 / c < 110 ** 2, "100/sqrt(c)<110")

    # pi>3 follows from the alternating polynomial lower bound for
    # 4*integral_0^1 1/(1+x^2) dx; eight terms give a lower bound.
    pi_lower = 4 * sum((Q((-1) ** k, 2 * k + 1) for k in range(8)), Q(0))
    require(pi_lower > 3, "Elementary pi lower bound")
    # pi<22/7 follows from integral_0^1 x^4(1-x)^4/(1+x^2) dx=22/7-pi>0.
    pi_upper = Q(22, 7)
    require(2 * pi_upper < Q(629, 100), "Far-arc grid coverage")
    a_upper = Q(58, 25)
    require(3 * (a_upper / 2) / 3 < Q(11, 10) ** 2,
            "sqrt(3X/pi)<=1.1 sqrt(x)")

    # At real t<=1/10000, x>=100 and b=2*pi^(3/2)*x>1000.
    require(4 * 3 ** 3 * 100 ** 2 > 1000 ** 2, "b>1000")
    # exp(1000)>1+1000+1000^2/2>10000.
    require(1 + 1000 + Q(1000 ** 2, 2) > 10000, "exp(-1000)<1/10000")
    e_upper = (2 * Q(1, 10000) / (1 - Q(1, 10000))
               * (1 + Q(2, 1000) + Q(2, 1000 ** 2)))
    require(e_upper < Q(1, 1000), "Real transformed remainder <1/1000")
    # For 0<=u<1, exp(u)<=1/(1-u) follows termwise from its series.
    require(1 / (1 - Q(1, 1000)) < Q(101, 100), "exp(R(t))<=1.01")

    # Multiply the normalized minor-arc bound by X^5 and use X<=1.16x.
    # Each term decreases for x>=100. For x^p exp(-d*x), its logarithmic
    # derivative p/x-d is negative, as checked exactly below.
    require(Q(9, 2) - Q(38, 125) * 100 < 0, "Near weighted term decreases")
    require(Q(15, 2) - Q(3, 5) * 100 < 0, "Middle weighted term decreases")
    require(Q(-21, 2) < 0 and Q(-17, 2) < 0, "Power terms decrease")
    prefactor = Q(1111, 1000) * Q(29, 25) ** 5
    exp_near = exp_negative_upper(Q(152, 5))
    exp_middle = exp_negative_upper(Q(60))
    require(exp_near < Q(63, 10 ** 15), "exp(-30.4)<6.3e-14")
    require(exp_middle < Q(9, 10 ** 27), "exp(-60)<9e-27")
    terms = {
        "near": prefactor * 128 * 10 ** 9 * exp_near,
        "middle_exponential": prefactor * Q(1, 100) * 10 ** 15 * exp_middle,
        "middle_power": prefactor * Q(1, 100) * 110 ** 9 / 10 ** 21,
        "far": prefactor * pi_upper * Q(1, 10 ** 25) * 10000 ** 8 / 10 ** 17,
    }
    total = sum(terms.values(), Q(0))
    require(total < Q(1, 40), "Uniform minor bound <=X^-5/40")
    result = {
        "scope": "Exact rational checks of explicit minor-arc constants and uniform normalization",
        "domain": "x=t^(-1/2)>=100; X=A*x/2; 2.31<A<2.32",
        "assumption": "The transformed product identity and finite far-arc certificate are established separately",
        "log_enclosures": {
            "log(46/25)": [outward_decimal(l46, False), outward_decimal(u46, True)],
            "log(361/25)": [outward_decimal(l361, False), outward_decimal(u361, True)],
            "log(4)": [outward_decimal(l4, False), outward_decimal(u4, True)],
        },
        "weighted_term_upper_bounds_at_x_100":
            {name: outward_decimal(value, True) for name, value in terms.items()},
        "weighted_total_upper_bound": outward_decimal(total, True),
        "weighted_target": "1/40",
        "conclusion": "Normalized absolute minor-arc contribution <= (1/40)*X^(-5) for every real x>=100",
        "arithmetic": "Python arbitrary-precision integers and fractions only",
    }
    output = Path(__file__).resolve().parents[1] / "certificates" / "minor_constants.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
