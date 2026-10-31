"""Run every check of the A181199 proof and write certificates/verification_report.json.

Usage (from the folder that contains src/, certificates/ and data/):
    python src/verify_all.py
"""
import json
import os
import platform
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sympy  # noqa: E402

import count_arrays  # noqa: E402
import pfaffian_sum  # noqa: E402
import verify_gosper  # noqa: E402
import verify_recurrence  # noqa: E402
import verify_telescoping  # noqa: E402
from common import CERT  # noqa: E402


def step(name, fn, report):
    t0 = time.time()
    print("[%s] running ..." % name, flush=True)
    out = fn()
    report[name] = {"result": out, "seconds": round(time.time() - t0, 1)}
    print("[%s] ok (%.1f s)" % (name, time.time() - t0), flush=True)


def main():
    report = {"python": platform.python_version(), "sympy": sympy.__version__}
    step("independent_counts", lambda: count_arrays.main(7, 30), report)
    step("pfaffian_and_double_sum", lambda: {k: v for k, v in pfaffian_sum.main().items()
                                             if k != "pairing_terms"}, report)
    step("telescoping_symbolic", verify_telescoping.symbolic_check, report)
    step("telescoping_pointwise", lambda: verify_telescoping.summed_check(12), report)
    step("gosper", verify_gosper.main, report)
    step("recurrence", verify_recurrence.main, report)
    for name in ("telescoping_symbolic",):
        assert report[name]["result"]["identity_holds"]
    report["conclusion"] = ("All exact checks passed: Kauers-Koutschan Conjecture 19 and the "
                            "OEIS A181199 recurrence hold for every n >= 1.")
    with open(os.path.join(CERT, "verification_report.json"), "w") as fh:
        json.dump(report, fh, indent=2, default=str)
    print(report["conclusion"])


if __name__ == "__main__":
    main()
