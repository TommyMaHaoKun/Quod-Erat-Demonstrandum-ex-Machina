"""Exact rational finite certificate for all far arcs and all 0<t<=1/10000.

This verifies an analytic inequality, not partition coefficients. No floating
point or external packages are used. See research/minor_arcs.md for its proof.
"""
import json
from pathlib import Path

B = 100000
J = 40
START = B // 629
TARGET = 10**50


def verify():
    worst_product = None
    worst_index = None
    min_strong = J
    for k in range(START, B // 2):
        product = 1
        strong = 0
        for j in range(1, J + 1):
            square = j*j
            left, right = square*k, square*(k+1)
            if left // B != right // B:
                distance_numerator = 0
            else:
                distance_numerator = min(left % B, B - right % B)
            numerator = (20000 * distance_numerator)**2
            denominator = (B * square)**2
            lower_factor = 1 + numerator // denominator
            product *= lower_factor
            strong += numerator >= denominator
        if product < TARGET:
            raise ValueError("Insufficient far-arc product", k, product)
        if strong < 16:
            raise ValueError("Insufficient strong far-arc factors", k, strong)
        if worst_product is None or product < worst_product:
            worst_product, worst_index = product, k
        min_strong = min(min_strong, strong)
    result = {
        "scope": "Uniform far-arc bound for square-partition generating product",
        "grid_denominator": B,
        "grid_start_numerator": START,
        "grid_end_numerator": B//2,
        "factors": J,
        "t0": "1/10000",
        "verified_product_lower_bound": str(TARGET),
        "observed_minimum_product": str(worst_product),
        "minimum_product_interval_numerator": worst_index,
        "verified_strong_factors_lower_bound": 16,
        "observed_minimum_strong_factors": min_strong,
        "conclusion": "|F(exp(-t+i theta))|/F(exp(-t)) <= 10^-25 (10000 t)^8 for 1/100 <= |theta| <= pi and 0<t<=1/10000",
    }
    out = Path(__file__).resolve().parents[1] / "certificates" / "minor_arcs.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    verify()
