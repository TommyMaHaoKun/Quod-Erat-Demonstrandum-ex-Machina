"""Uncertified high-precision normalization diagnostic, NOT part of proof.

Uses an existing exact DP checkpoint; does not rerun the coefficient table.
Requires mpmath. All rigorous certificates use standard-library arithmetic.
"""

import json
from math import isqrt
from pathlib import Path
from fractions import Fraction
import mpmath as mp

from finite_verify import load_checkpoint


def main():
    root = Path(__file__).resolve().parents[1]
    bound = 1200001
    coefficients, next_root = load_checkpoint(root / "certificates/dp_1200000.bin", bound)
    if next_root != isqrt(bound) + 1:
        raise ValueError("Diagnostic requires a completed exact checkpoint")
    mp.mp.dps = 100
    A = mp.sqrt(mp.pi) * mp.zeta(mp.mpf(3) / 2) / 2
    a = (A / 2) ** (mp.mpf(2) / 3)
    major = json.loads((root / "certificates/major_arc.json").read_text())
    c = []
    for entry in major["coefficients_c_r"]:
        q = Fraction(entry)
        c.append(mp.mpf(q.numerator) / q.denominator)

    def model(n):
        X = a * mp.root(n, 3)
        M = a * mp.exp(3 * X) / (2 * mp.sqrt(3) * mp.pi ** mp.mpf("1.5")
                                 * mp.mpf(n) ** (mp.mpf(7) / 6))
        P = mp.fsum(c[r] / X ** r for r in range(len(c)))
        return X, M, P

    cases = []
    for n in (1042, 10000, 100000, 1000000, 1200000):
        X, M, P = model(n)
        coefficient_error = mp.mpf(coefficients[n]) / M - P
        D = coefficients[n] ** 2 - coefficients[n - 1] * coefficients[n + 1]
        exact_ratio = mp.mpf(D) / (coefficients[n - 1] * coefficients[n + 1])
        log_curvature = mp.log1p(exact_ratio)
        logQ = []
        for m in (n - 1, n, n + 1):
            _, Mm, Pm = model(m)
            logQ.append(mp.log(Mm * Pm))
        q_curvature = 2 * logQ[1] - logQ[0] - logQ[2]
        row = {
            "n": n,
            "X": str(X),
            "s_over_M": str(mp.mpf(coefficients[n]) / M),
            "P": str(P),
            "coefficient_error_times_X5": str(coefficient_error * X ** 5),
            "actual_log_curvature": str(log_curvature),
            "model_log_curvature": str(q_curvature),
            "actual_log_curvature_times_X5": str(log_curvature * X ** 5),
            "model_log_curvature_times_X5": str(q_curvature * X ** 5),
            "model_curvature_lower_bound": str(mp.mpf(3) / 5 * a * mp.mpf(n + 1) ** (-mp.mpf(5) / 3)),
        }
        cases.append(row)
    result = {
        "scope": "Uncertified numerical diagnostic only; not a proof or a uniform error bound",
        "digits": mp.mp.dps,
        "mpmath_version": mp.__version__,
        "checkpoint": "certificates/dp_1200000.bin",
        "cases": cases,
    }
    output = root / "certificates/model_diagnostic.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for row in cases:
        print("n=%d; coefficient error*X^5=%s; actual/model log curvature*X^5=%s/%s" % (
            row["n"], mp.nstr(mp.mpf(row["coefficient_error_times_X5"]), 14),
            mp.nstr(mp.mpf(row["actual_log_curvature_times_X5"]), 14),
            mp.nstr(mp.mpf(row["model_log_curvature_times_X5"]), 14)))
    print("Uncertified diagnostic only:", output)


if __name__ == "__main__":
    main()
