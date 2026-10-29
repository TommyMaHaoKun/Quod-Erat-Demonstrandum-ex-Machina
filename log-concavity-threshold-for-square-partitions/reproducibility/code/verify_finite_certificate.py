"""Recompute and audit a finite certificate without importing its producer.

Usage: python code/verify_finite_certificate.py certificates/finite_1000000.json
Python 3.9+ standard library only.  No checkpoint is trusted or read.
"""

import hashlib
import json
from math import isqrt
from pathlib import Path
import struct
import sys
import time


def require(condition, description):
    if not condition:
        raise ArithmeticError(description)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    cert = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    lo, upper = cert["checked_D_indices_inclusive"]
    require(lo == 1, "Unsupported starting index")
    bound = upper + 1
    require(cert["computed_coefficient_indices_inclusive"] == [0, bound],
            "Incorrect neighboring-coefficient coverage")

    began = time.perf_counter()
    # P_r(n) = P_(r-1)(n) + P_r(n-r^2), in increasing n.
    coefficients = [1] + [0] * bound
    for square in (r * r for r in range(1, isqrt(bound) + 1)):
        for n in range(square, bound + 1):
            coefficients[n] = coefficients[n] + coefficients[n - square]
    print("Fresh coin-change computation complete in %.2fs" %
          (time.perf_counter() - began), flush=True)

    # Compute b(m) by testing square divisors rather than the producer's sieve.
    start, independent_bound = cert["independent_coefficient_indices_inclusive"]
    require(start == 0 and 1043 <= independent_bound <= bound,
            "Insufficient or invalid independent coverage")
    b = [0] + [sum(r * r for r in range(1, isqrt(m) + 1) if m % (r * r) == 0)
               for m in range(1, independent_bound + 1)]
    independent = [1]
    for n in range(1, independent_bound + 1):
        numerator = sum(b[n - k] * independent[k] for k in range(n))
        quotient, remainder = divmod(numerator, n)
        require(remainder == 0, "Nonintegral recurrence at %d" % n)
        require(quotient == coefficients[n], "Algorithm mismatch at %d" % n)
        independent.append(quotient)
    require(cert["independent_coefficients_agree"] is True,
            "Certificate does not assert independent agreement")

    negatives, zeros = [], []
    sign_digest, coefficient_digest = hashlib.sha256(), hashlib.sha256()
    for value in coefficients:
        count = max(1, (value.bit_length() + 7) // 8)
        coefficient_digest.update(struct.pack("<I", count))
        coefficient_digest.update(value.to_bytes(count, "little"))
    for n in range(1, upper + 1):
        d = coefficients[n] ** 2 - coefficients[n - 1] * coefficients[n + 1]
        if d < 0:
            negatives.append(n)
            sign_digest.update(b"-")
        elif d == 0:
            zeros.append(n)
            sign_digest.update(b"0")
        else:
            sign_digest.update(b"+")
    require(negatives == cert["negative_indices"], "Negative-index mismatch")
    require(zeros == cert["zero_indices"], "Equality-index mismatch")
    require(len(negatives) == cert["negative_count"], "Negative-count mismatch")
    require(len(zeros) == cert["zero_count"], "Equality-count mismatch")
    require(upper - len(negatives) - len(zeros) == cert["positive_count"],
            "Positive-count mismatch")
    require(max(negatives, default=None) == cert["last_negative_index"],
            "Last-negative mismatch")
    require(max(negatives + zeros, default=None) == cert["last_nonpositive_index"],
            "Last-nonpositive mismatch")
    expanded = [n for first, last, step in
                cert["negative_indices_progressions_start_end_step"]
                for n in range(first, last + 1, step)]
    require(expanded == negatives, "Compressed negative-index mismatch")
    require(coefficient_digest.hexdigest() == cert["coefficient_sha256"],
            "Coefficient checksum mismatch")
    require(sign_digest.hexdigest() == cert["sign_sha256"], "Sign checksum mismatch")
    for key, row in cert["boundary"].items():
        n = int(key)
        expected = {
            "s_previous": str(coefficients[n - 1]),
            "s": str(coefficients[n]),
            "s_next": str(coefficients[n + 1]),
            "D": str(coefficients[n] ** 2 - coefficients[n - 1] * coefficients[n + 1]),
        }
        require(row == expected, "Boundary mismatch at %d" % n)
    print("PASS: D(1)..D(%d), all signs, all boundary values, both checksums," % upper)
    print("and independent recurrence for s(0)..s(%d)." % independent_bound)
    print("No statement about n > %d was checked." % upper)
    print("Elapsed %.2fs" % (time.perf_counter() - began))


if __name__ == "__main__":
    main()
