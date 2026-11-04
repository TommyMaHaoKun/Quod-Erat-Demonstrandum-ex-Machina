"""Exact rational checks for the Weibull counterexample's one-point bound.

The analytic proof is in the accompanying paper.
No floating-point quadrature, optimization, or third-party package is used.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import factorial
from pathlib import Path

if not __debug__:
    raise RuntimeError('Run without -O or PYTHONOPTIMIZE; assertions are required.')


def moment(k):
    """Integral from 0 to 1 of (1-u/2)*u**(2*k)."""
    return Q(1, 2*k+1) - Q(1, 4*k+4)


def weighted_taylor(t, degree, moment_shift=0):
    return sum(((-t)**k / factorial(k)) * moment(k+moment_shift)
               for k in range(degree+1))


def exponential_taylor(t, degree):
    return sum(t**k / factorial(k) for k in range(degree+1))


def rational(value):
    return {'numerator': str(value.numerator), 'denominator': str(value.denominator)}


def verify():
    t = Q(41, 20)
    lower_f = weighted_taylor(t, 5)
    upper_m2 = weighted_taylor(t, 6, 1)
    lower_exp_positive = exponential_taylor(t, 6)
    # Odd/even Taylor remainder signs supply the analytic inequality direction.
    assert lower_f > Q(482, 1000)
    assert upper_m2 < Q(78, 1000)
    coarse_derivative_margin = Q(482, 1000) - 3*t*Q(78, 1000)
    assert coarse_derivative_margin == Q(23, 10000) > 0
    derivative_margin = lower_f - 3*t*upper_m2
    assert derivative_margin > coarse_derivative_margin
    assert lower_exp_positive > Q(100, 13)

    # A second, longer pair of alternating truncations checks the same point.
    lower_f_15 = weighted_taylor(t, 15)
    upper_m2_16 = weighted_taylor(t, 16, 1)
    upper_exp_negative_16 = exponential_taylor(-t, 16)
    assert lower_f_15 - 3*t*upper_m2_16 > Q(1, 100)
    assert upper_exp_negative_16 < Q(13, 100)

    stationary_f_bound = Q(3, 4)*((2 - 1/t)*Q(13, 100) + 1/t)
    bound = Q(99, 28)*t*stationary_f_bound**3
    assert bound == Q(7381964831571, 7530880000000)
    assert 0 < bound < 1
    return {
        'status': 'PASS_EXACT_RATIONAL_ONE_POINT_CERTIFICATE',
        'arithmetic': 'Python standard-library Fraction; all decisions exact',
        't0': rational(t),
        'lower_F_Taylor5': rational(lower_f),
        'upper_second_moment_Taylor6': rational(upper_m2),
        'derivative_margin_lower_bound': rational(derivative_margin),
        'coarse_derivative_margin': rational(coarse_derivative_margin),
        'lower_exp_positive_Taylor6': rational(lower_exp_positive),
        'exp_reciprocal_comparison': 'lower_exp_positive_Taylor6 > 100/13',
        'longer_derivative_margin': rational(lower_f_15-3*t*upper_m2_16),
        'upper_exp_negative_Taylor16': rational(upper_exp_negative_16),
        'stationary_F_bound': rational(stationary_f_bound),
        'global_normalized_ratio_cubed_bound': rational(bound),
        'strict_gap_below_one': rational(1-bound),
        'analytic_dependencies': [
            'Weibull survival exp(-x^(3/2)) and mean Gamma(5/3)',
            'The tail event splits into two disjoint integrals up to a null boundary',
            'The symmetric exponent is at least 3*u^2/4',
            'sqrt(1-u) <= 1-u/2 for 0 <= u <= 1',
            'Gamma log-convexity gives Gamma(5/3)^3 <= pi/4',
            'pi < 22/7',
            'Rescaled positive densities have increasing likelihood ratio',
            'The stationary majorant G is decreasing for t >= 2',
            'Taylor remainders have the stated global signs'
        ],
        'claim': 'For every z>0, the mean-normalized Weibull tail ratio is strictly below one.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = verify()
    report['checker_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    destination = args.report or Path(__file__).resolve().parents[1] / 'certificates' / 'one_point_bound.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
