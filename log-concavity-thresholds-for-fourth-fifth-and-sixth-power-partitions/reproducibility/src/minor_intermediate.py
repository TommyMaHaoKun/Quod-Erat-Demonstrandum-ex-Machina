"""Exact rational bounds for weighted intermediate Euler-product arcs.

This checks only the lemma in paper/minor_intermediate.md.  It is not a
coefficient or log-concavity proof.  No external dependencies are used.
"""
if not __debug__:
    raise RuntimeError("Run this proof calculation without Python -O.")
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


def bound(k, X, m, J=6, stop=100):
    assert k in (4, 5, 6) and X >= 14 and m in (0, 1, 2)
    assert J > m + 1 and stop >= 100
    # At |v| <= 1/6, sinh(v)/v <= 1 + (1/216)/(1-1/720).
    sinh_bound = 1 + F(1, 216) / (1 - F(1, 720))
    assert sinh_bound < F(201, 200)
    assert F(23, 24) / F(201, 200) > F(19, 20)
    assert 3**2 <= 2**k  # 3^(2/k) <= 2
    total = F(0)
    for j in range(J, stop):
        q = F(20, 19)**j / (j-m-1)
        if 3 * (j+1)**k <= X**k:
            total += q * F(j+1, X)**(k*(j-m-1)) * X**2
        else:
            total += q * 2 * (j+1)**2 * F(3)**(m+1-j)
    # The second branch universally majorizes the maximum, so it can be
    # used for the entire remaining tail, independent of the branch test.
    first_tail = 2 * F(3)**(m+1) * (stop+1)**2 * F(20, 57)**stop / (stop-m-1)
    ratio = F(20, 57) * F(stop+2, stop+1)**2
    assert ratio < F(9, 25)
    total += first_tail / (1-F(9, 25))
    return total


def ceiling_decimal(value, places=8):
    scale = 10**places
    return F((value.numerator*scale + value.denominator-1)//value.denominator, scale)


def result():
    data = []
    for k in (4, 5, 6):
        for X in (14, 15, 18, 20):
            row = {"k": k, "minimum_x": X, "delta": str(F(1, 6**k)), "bounds": []}
            for m in (0, 1, 2):
                exact_bound = bound(k, X, m)
                upper = ceiling_decimal(exact_bound)
                assert exact_bound <= upper
                row["bounds"].append({"moment": m, "upper_x_squared_J": str(upper),
                                      "decimal_display": float(upper)})
            data.append(row)
    return {"claim": "For x >= minimum_x, t=x^(-k), delta=6^(-k), x^2 J_m <= bound; J_m=t^(-m-1) integral_(3t)^delta theta^m rho(t,theta) dtheta.",
            "scope": "Rigorous intermediate-arc bound only; far arcs and coefficient positivity are separate obligations.",
            "method": "Exact rational series bounds, a one-variable maximum, and an infinite geometric tail.",
            "rows": data}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    obj = result()
    encoded = json.dumps(obj, indent=2) + "\n"
    if args.write:
        dest = Path(__file__).resolve().parents[1] / "certificates" / "minor_intermediate.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(encoded, encoding="utf-8")
        print("Wrote", dest)
    else:
        print(encoded, end="")
