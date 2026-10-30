"""Independent exact checks of A172671, using only Python's standard library.

The finite tests here are corroboration, not an all-index proof.
No transfer-matrix code is imported by this checker.
"""
from fractions import Fraction
from functools import lru_cache
from math import factorial
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


@lru_cache(None)
def count_rows(capacities):
    """Coefficient of the row polynomial raised to sum(capacities)/2.

    Column permutations preserve this count, so sorted residual capacities
    may share a cache entry.  The 21 choices remain separately counted.
    """
    if not any(capacities):
        return 1
    if sum(capacities) % 2:
        return 0
    answer = 0
    for i in range(6):
        for j in range(i, 6):
            c = list(capacities)
            c[i] -= 1
            c[j] -= 1
            if min(c) >= 0:
                answer += count_rows(tuple(sorted(c, reverse=True)))
    return answer


def multiply(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def gaussian_moment(p):
    value = 0
    even_moment = 1
    for degree in range(0, len(p), 2):
        if degree:
            even_moment *= degree - 1
        value += p[degree] * even_moment
    return value


def hermite_plus(n):
    """Explicit coefficients of exp(xt+t^2/2), with factorial scaling."""
    p = [0] * (n + 1)
    for j in range(n // 2 + 1):
        p[n - 2*j] = factorial(n) // (2**j * factorial(j) * factorial(n - 2*j))
    return p


def hermite_values(n):
    p = hermite_plus(n)
    sixth = [1]
    for _ in range(6):
        sixth = multiply(sixth, p)
    moment = gaussian_moment(sixth)
    a = Fraction(moment * factorial(3*n), factorial(n)**6)
    assert a.denominator == 1
    b = Fraction(moment, factorial(n)**3)
    return int(a), b


def recurrence_coefficients(n):
    # Independently transcribed directly from literature/target_formula.tex.
    return [
        15435*(n+1)**3*(n+2)*(3784*n**4+47300*n**3+219945*n**2+450988*n+344237),
        (n+2)*(29681696*n**7+504588832*n**6+3602458816*n**5+14001842392*n**4+32010306742*n**3+43078657918*n**2+31639900193*n+9799573455),
        -3*(10844944*n**8+222321352*n**7+1973930222*n**6+9916013134*n**5+30831383530*n**4+60768378830*n**3+74160044251*n**2+51243135187*n+15352797306),
        -(n+3)*(3799136*n**7+72183584*n**6+579689880*n**5+2548427912*n**4+6617561702*n**3+10141503096*n**2+8487349821*n+2991586122),
        3*(n+3)*(n+4)**3*(3784*n**4+32164*n**3+100749*n**2+137862*n+69678),
    ]


def check_source_transcription():
    target = (ROOT / "literature/target_formula.tex").read_text(encoding="utf-8")
    source_path = ROOT / "literature/kout4.tex"
    start = target.index("  If ")
    excerpt = target[start:].strip()
    canonical = re.sub(r"\s+", "", excerpt)
    assert hashlib.sha256(canonical.encode()).hexdigest() == "7c7e083590996f30ecbd1489dcc98ce1c645674bf06949704a2126aa6e5d520b"
    report = {"target_excerpt_integrity": "canonical SHA-256 verified"}
    if source_path.exists():
        source = source_path.read_text(encoding="utf-8")
        assert canonical in re.sub(r"\s+", "", source)
        report["optional_full_source_comparison"] = "exact after removing whitespace"
        report["source_sha256"] = hashlib.sha256(source_path.read_bytes()).hexdigest()
    return report


def main():
    max_n = 40
    values = [hermite_values(n) for n in range(max_n + 1)]
    dp = []
    for n in range(9):
        a = count_rows((n,) * 6)
        assert a == values[n][0], (n, a, values[n][0])
        dp.append({"n": n, "a": str(a)})
    for n in range(max_n - 3):
        residual = sum(c * values[n+j][1] for j, c in enumerate(recurrence_coefficients(n)))
        assert residual == 0, (n, residual)
    assert [v[1] for v in values[:4]] == [1, 15, 2249, 444975]
    report = {
        "status": "PASS",
        "interpretation": "Independent exact finite checks; the all-index theorem requires the symbolic proof.",
        "source_transcription": check_source_transcription(),
        "direct_row_coefficient_dp": {"indices": [0, 8], "values": dp, "cache_states": count_rows.cache_info().currsize},
        "hermite_polynomial_exact_evaluation": {"indices": [0, max_n]},
        "target_recurrence_exact_residuals": {"indices": [0, max_n-4], "all_zero": True},
        "initial_b": [str(v[1]) for v in values[:4]],
        "all_values": [{"n": n, "a": str(a), "b": str(b)} for n, (a, b) in enumerate(values)],
    }
    out = ROOT / "certificates/independent_checks.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "all_values"}, indent=2))


if __name__ == "__main__":
    main()
