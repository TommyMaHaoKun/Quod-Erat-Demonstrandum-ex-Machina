"""High-precision supporting checks; the mathematical proof is independent.

Run with Python 3 and mpmath installed. No files outside this project are used.
"""

import json
import random

import mpmath as mp


mp.mp.dps = 60


def beta_cdf(x, t):
    a = (1 - t) / 2
    return mp.betainc(a, a, 0, x, regularized=True)


def beta_quantile(p, t):
    lo, hi = mp.mpf(0), mp.mpf(1)
    for _ in range(170):
        mid = (lo + hi) / 2
        if beta_cdf(mid, t) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def interval_energy(t):
    return (
        mp.gamma((1 + t) / 2)
        * mp.gamma(1 - t / 2)
        / mp.sqrt(mp.pi)
        / 2**t
    )


def distance_matrix(points, t):
    return mp.matrix([[abs(x - y) ** t for y in points] for x in points])


def equilibrium(points, t):
    matrix = distance_matrix(points, t)
    ones = mp.matrix([1] * len(points))
    solution = mp.lu_solve(matrix, ones)
    energy = 1 / sum(solution)
    masses = solution * energy
    assert min(masses) > 0
    assert abs(sum(masses) - 1) < mp.mpf("1e-50")
    assert max(abs(v - energy) for v in matrix * masses) < mp.mpf("1e-50")
    return energy, masses


def finite_transport_check(points, r, s):
    er, masses = equilibrium(points, r)
    es, _ = equilibrium(points, s)
    partial = mp.mpf(0)
    cuts = []
    for mass in list(masses)[:-1]:
        partial += mass
        cuts.append(beta_quantile(partial, r))
    fs = [mp.mpf(0)] + [beta_cdf(x, s) for x in cuts] + [mp.mpf(1)]
    test_masses = mp.matrix([fs[i + 1] - fs[i] for i in range(len(points))])
    test_energy = (test_masses.T * distance_matrix(points, s) * test_masses)[0]
    transport_margin = mp.log(test_energy / interval_energy(s)) / s - mp.log(
        er / interval_energy(r)
    ) / r
    main_margin = mp.log(es / interval_energy(s)) / s - mp.log(
        er / interval_energy(r)
    ) / r
    assert test_energy <= es + mp.mpf("1e-45")
    assert transport_margin > 0
    assert main_margin >= transport_margin - mp.mpf("1e-45")
    return transport_margin, main_margin


def normalization_check(alpha, count=2000):
    # Direct improper quadrature is separate from the exponential series.
    integral = mp.quad(lambda z: z / mp.sinh(z) ** alpha, [0, 1, mp.inf])
    closed = 2 ** (alpha - 2) * mp.beta(alpha / 2, 1 - alpha) * (
        mp.digamma(1 - alpha / 2) - mp.digamma(alpha / 2)
    )
    assert abs(integral - closed) < mp.mpf("1e-45")
    coefficient, partial = mp.mpf(1), mp.mpf(0)
    for n in range(count):
        if n:
            coefficient *= (alpha + n - 1) / n
        partial += coefficient / (2 * n + alpha) ** 2
    # For alpha in (0,1), (alpha)_n/n! <= 1. A decreasing-integrand
    # bound gives a rigorous (deliberately coarse) bound for the series tail.
    tail_bound = 1 / (2 * (2 * (count - 1) + alpha))
    total = integral / 2**alpha
    assert 0 < total - partial < tail_bound
    return total - partial


def main():
    rng = random.Random(20261102)
    results = []
    parameters = [("0.15", "0.45"), ("0.35", "0.75"), ("0.6", "0.9")]
    for index in range(12):
        n = 3 + index % 5
        coordinates = [0] + sorted(rng.sample(range(1, 1000), n - 2)) + [1000]
        points = [mp.mpf(i) / 1000 for i in coordinates]
        r, s = map(mp.mpf, parameters[index % len(parameters)])
        transport, target = finite_transport_check(points, r, s)
        results.append(
            {
                "points_times_1000": coordinates,
                "r": str(r),
                "s": str(s),
                "transport_log_margin": mp.nstr(transport, 25),
                "target_log_margin": mp.nstr(target, 25),
            }
        )
    tails = {
        alpha: mp.nstr(normalization_check(mp.mpf(alpha)), 25)
        for alpha in ["0.2", "0.5", "0.8"]
    }
    print(
        json.dumps(
            {
                "status": "PASS",
                "precision_decimal_digits": mp.mp.dps,
                "finite_transport_cases": results,
                "mixing_series_tail_after_2000_terms": tails,
                "proof_dependency": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
