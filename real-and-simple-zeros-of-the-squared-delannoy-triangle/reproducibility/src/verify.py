"""Reproduce exact finite checks accompanying the analytic all-n proof.

Run from the project root with ``python src/verify.py``.  ``--write`` regenerates
the deterministic certificate; ``--independent`` also runs the separately
written exploratory checker.  No finite bound here is an all-index proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "exact_checks.json"
MAX_N = 50
IDENTITY_MAX_N = 12


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add_scaled(target, source, scalar, shift=0):
    """Add scalar*x**shift*source to an ascending integer coefficient list."""
    for k, value in enumerate(source):
        target[k + shift] += scalar * value


def recurrence_rows(max_n):
    rows = [[1], [2, 1], [5, 6, 1], [12, 25, 10, 1]]
    for n in range(4, max_n + 1):
        row = [0] * (n + 1)
        for distance, constant in ((1, 3), (2, -1), (3, -1), (4, 0)):
            add_scaled(row, rows[n - distance], 1, shift=1)
            add_scaled(row, rows[n - distance], constant)
        rows.append(row)
    return rows[:max_n + 1]


def path_rows(max_n):
    """Delannoy triangle from the three allowed path steps, not from G_n."""
    rows = [[1]]
    for n in range(1, max_n + 1):
        row = []
        for k in range(n + 1):
            value = 0
            if k < n:
                value += rows[n - 1][k]
            if k:
                value += rows[n - 1][k - 1]
            if n >= 2 and 1 <= k <= n - 1:
                value += rows[n - 2][k - 1]
            row.append(value)
        rows.append(row)
    return rows


def square_rows(rows):
    return [[sum(rows[n][j] * rows[j][k] for j in range(k, n + 1))
             for k in range(n + 1)] for n in range(len(rows))]


def expression(row, variable):
    return sum(coefficient * variable**k for k, coefficient in enumerate(row))


def variations(signs):
    nonzero = [value for value in signs if value]
    return sum(a != b for a, b in zip(nonzero, nonzero[1:]))


def symbolic_identities(rows):
    x, t, r = sp.symbols("x t r")
    denominator = 1 - (x + 3)*t + (1 - x)*t**2 + (1 - x)*t**3 - x*t**4
    initial = sum(expression(rows[n], x)*t**n for n in range(4))
    coefficients = sp.Poly(sp.expand(denominator * initial), t)
    initial_numerator = sum(coefficients.nth(n)*t**n for n in range(4))
    require(sp.expand(initial_numerator - (1 - t)) == 0,
            "The initial polynomials do not produce numerator 1-t.")

    g = lambda z: 1 / (1 - z)
    f = lambda z: z*(1 + z)/(1 - z)
    matrix_gf = g(t)*g(f(t))/(1 - x*f(f(t)))
    require(sp.cancel(matrix_gf - (1 - t)/denominator) == 0,
            "Matrix-square generating function disagrees with the recurrence.")

    d = [sp.Integer(1), 1 + x]
    for n in range(2, IDENTITY_MAX_N + 1):
        d.append(sp.expand((1 + x)*d[-1] + x*d[-2]))
    s = (1 - r)/(1 + r)
    target_x = r*(r - 1)/(r + 1)
    for n in range(IDENTITY_MAX_N + 1):
        quotient = (r*d[n].subs(x, r) - s*d[n].subs(x, s))/(r - s)
        require(sp.cancel(quotient - expression(rows[n], target_x)) == 0,
                f"Divided-difference identity failed at n={n}.")
    return {
        "initial_numerator_is_1_minus_t": True,
        "matrix_square_generating_function_identity": True,
        "divided_difference_identity_checked_through_n": IDENTITY_MAX_N,
        "identity_arithmetic": "exact rational-function simplification over Q(r)",
    }


def compute_certificate():
    rows = recurrence_rows(MAX_N)
    independently_squared = square_rows(path_rows(MAX_N))
    require(rows == independently_squared,
            "Independent Delannoy path recursion and matrix square disagree.")
    identities = symbolic_identities(rows)
    x = sp.Symbol("x")
    checks = []
    for n, row in enumerate(rows):
        polynomial = sp.Poly.from_list(list(reversed(row)), x, domain=sp.QQ)
        require(polynomial.degree() == n and polynomial.LC() == 1,
                f"Degree or monicity failed at n={n}.")
        require(all(coefficient > 0 for coefficient in row),
                f"Coefficient positivity failed at n={n}.")
        coefficient_hash = hashlib.sha256(
            json.dumps(row, separators=(",", ":")).encode("ascii")
        ).hexdigest()
        if n == 0:
            signs_minus, signs_zero = [1], [1]
            gcd_degree = 0
        else:
            gcd_degree = int(sp.gcd(polynomial, polynomial.diff()).degree())
            require(gcd_degree == 0, f"Repeated root detected at n={n}.")
            sturm = polynomial.sturm()
            signs_minus = [int(sp.sign(p.LC())) * (-1)**p.degree() for p in sturm]
            signs_zero = [int(sp.sign(p.eval(0))) for p in sturm]
        v_minus, v_zero = variations(signs_minus), variations(signs_zero)
        require(v_minus - v_zero == n,
                f"Sturm chain does not certify n negative roots at n={n}.")
        checks.append({
            "n": n,
            "degree": n,
            "coefficient_sha256": coefficient_hash,
            "all_coefficients_positive": True,
            "monic": True,
            "derivative_gcd_degree": gcd_degree,
            "sturm_signs_at_negative_infinity": signs_minus,
            "sturm_signs_at_zero": signs_zero,
            "variations_at_negative_infinity": v_minus,
            "variations_at_zero": v_zero,
            "distinct_negative_real_roots": n,
        })
        print(f"n={n:2d}: path-square equality, positivity, and {n} distinct negative roots",
              flush=True)
    return {
        "schema": 1,
        "scope": "Finite exact checks only; the manuscript supplies the all-n analytic proof.",
        "max_n": MAX_N,
        "path_square_equality_through_n": MAX_N,
        "sturm_arithmetic": "exact rational polynomial remainder sequence over Q",
        "symbolic_identities": identities,
        "polynomials": checks,
    }


def independent_check():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "src" / "explore_independent.py"),
         "--max-n", str(MAX_N)],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    records = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    require([record["n"] for record in records] == list(range(1, MAX_N + 1)),
            "Independent checker did not cover the required indices.")
    require(all(record["negative_real_roots"] == record["n"] and record["squarefree"]
                for record in records), "Independent checker reported a failure.")
    print(f"Independent companion passed n=1..{MAX_N}.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="Regenerate the checked-in deterministic certificate.")
    parser.add_argument("--independent", action="store_true",
                        help="Also run the separately written exact exploratory checker.")
    args = parser.parse_args()
    certificate = compute_certificate()
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
        print("Wrote certificates/exact_checks.json.", flush=True)
    else:
        expected = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        require(certificate == expected, "Computed checks differ from the saved certificate.")
        print("Saved certificate matches all recomputed exact checks.", flush=True)
    if args.independent:
        independent_check()
    print("PASS. These finite checks support, but do not replace, the analytic proof.", flush=True)


if __name__ == "__main__":
    main()
