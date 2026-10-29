"""Exact, resumable finite verification for square-partition log-concavity.

Python 3.9+ standard library only.  This program establishes statements only on
the finite interval recorded in its certificate; it proves no infinite tail.

Coin-change invariant: after square r*r is processed, a[n] counts partitions
of n using the squares 1,4,...,r*r.  Increasing n permits repeated copies of
the current square.  The coefficient bound is limit+1, because D(limit) needs
the next coefficient.
"""

import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path
import struct
import time


MAGIC = b"SQPART1\n"


def encoded_integer(value):
    """Canonical unsigned encoding, prefixed by a four-byte LE byte count."""
    raw = value.to_bytes(max(1, (value.bit_length() + 7) // 8), "little")
    return struct.pack("<I", len(raw)) + raw


def save_checkpoint(path, a, next_root):
    """Write an atomic checksum-protected checkpoint of the exact DP state."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    digest = hashlib.sha256()
    with temporary.open("wb") as stream:
        stream.write(MAGIC)
        header = struct.pack("<QQ", len(a) - 1, next_root)
        stream.write(header)
        digest.update(header)
        for value in a:
            raw = encoded_integer(value)
            stream.write(raw)
            digest.update(raw)
        stream.write(digest.digest())
    temporary.replace(path)


def load_checkpoint(path, bound):
    """Read only the simple numeric format; no executable deserialization."""
    with path.open("rb") as stream:
        if stream.read(len(MAGIC)) != MAGIC:
            raise ValueError("Invalid checkpoint magic")
        header = stream.read(16)
        saved_bound, next_root = struct.unpack("<QQ", header)
        if saved_bound != bound or not (1 <= next_root <= isqrt(bound) + 1):
            raise ValueError("Checkpoint bound or next square does not match")
        digest = hashlib.sha256(header)
        a = []
        for _ in range(bound + 1):
            size_bytes = stream.read(4)
            if len(size_bytes) != 4:
                raise ValueError("Truncated coefficient length")
            size = struct.unpack("<I", size_bytes)[0]
            if not 1 <= size <= 1_000_000:
                raise ValueError("Invalid coefficient size")
            raw = stream.read(size)
            if len(raw) != size or (size > 1 and raw[-1] == 0):
                raise ValueError("Invalid or noncanonical coefficient")
            digest.update(size_bytes)
            digest.update(raw)
            a.append(int.from_bytes(raw, "little"))
        if stream.read(32) != digest.digest() or stream.read(1):
            raise ValueError("Checkpoint checksum mismatch or trailing data")
    if a[0] != 1:
        raise ValueError("Invalid constant coefficient")
    return a, next_root


def coin_change(bound, checkpoint=None, resume=False, checkpoint_every=50):
    if resume and checkpoint and checkpoint.exists():
        a, start = load_checkpoint(checkpoint, bound)
        print("Resuming before square root", start, flush=True)
    else:
        a = [0] * (bound + 1)
        a[0] = 1
        start = 1
    began = time.perf_counter()
    last = began
    for root in range(start, isqrt(bound) + 1):
        square = root * root
        for n in range(square, bound + 1):
            a[n] += a[n - square]
        now = time.perf_counter()
        if checkpoint and root % checkpoint_every == 0:
            save_checkpoint(checkpoint, a, root + 1)
        if now - last >= 10 or root == isqrt(bound):
            print("DP square root %d/%d; elapsed %.1fs" %
                  (root, isqrt(bound), now - began), flush=True)
            last = now
    if checkpoint:
        save_checkpoint(checkpoint, a, isqrt(bound) + 1)
    return a


def logarithmic_derivative(bound):
    """Independent recurrence with exact divisibility checked at every n.

    q F'(q)/F(q) = sum_j j^2 q^(j^2)/(1-q^(j^2))
                 = sum_(m>=1) b(m) q^m,
    b(m) = sum_(j^2|m) j^2.
    Coefficients in q F'(q) = F(q) sum b(m)q^m give
    n*s(n) = sum_(m=1)^n b(m)*s(n-m).
    """
    weights = [0] * (bound + 1)
    for root in range(1, isqrt(bound) + 1):
        square = root * root
        for multiple in range(square, bound + 1, square):
            weights[multiple] += square
    a = [0] * (bound + 1)
    a[0] = 1
    for n in range(1, bound + 1):
        numerator = sum(weights[m] * a[n - m] for m in range(1, n + 1))
        a[n], remainder = divmod(numerator, n)
        if remainder:
            raise ArithmeticError("Nonintegral recurrence at n=%d" % n)
    return a


def compress_progressions(values):
    """Lossless human-readable disjoint runs, not an unverified pattern claim."""
    runs = []
    index = 0
    while index < len(values):
        if index + 2 < len(values):
            step = values[index + 1] - values[index]
            end = index + 1
            while end + 1 < len(values) and values[end + 1] - values[end] == step:
                end += 1
            if end - index >= 2:
                runs.append([values[index], values[end], step])
                index = end + 1
                continue
        runs.append([values[index], values[index], 1])
        index += 1
    rebuilt = [n for lo, hi, step in runs for n in range(lo, hi + 1, step)]
    if rebuilt != values:
        raise ArithmeticError("Progression encoding mismatch")
    return runs


def summarize(a, limit, independent_through, timings):
    failures = []
    equalities = []
    signs = hashlib.sha256()
    coefficients = hashlib.sha256()
    for value in a:
        coefficients.update(encoded_integer(value))
    for n in range(1, limit + 1):
        difference = a[n] * a[n] - a[n - 1] * a[n + 1]
        if difference < 0:
            failures.append(n)
            signs.update(b"-")
        elif difference == 0:
            equalities.append(n)
            signs.update(b"0")
        else:
            signs.update(b"+")
    boundary_indices = sorted(set(n for n in [1, 2, 3, 1040, 1041, 1042, 1043, limit]
                                  if 1 <= n <= limit))
    return {
        "format_version": 1,
        "scope": "Exact finite verification only; no infinite-tail claim",
        "checked_D_indices_inclusive": [1, limit],
        "computed_coefficient_indices_inclusive": [0, limit + 1],
        "method": "square-coin increasing-index dynamic programming",
        "independent_method": "logarithmic-derivative recurrence",
        "independent_coefficient_indices_inclusive": [0, independent_through],
        "independent_coefficients_agree": True,
        "negative_count": len(failures),
        "negative_indices": failures,
        "negative_indices_progressions_start_end_step": compress_progressions(failures),
        "zero_count": len(equalities),
        "zero_indices": equalities,
        "positive_count": limit - len(failures) - len(equalities),
        "last_negative_index": max(failures, default=None),
        "last_nonpositive_index": max(failures + equalities, default=None),
        "boundary": {str(n): {"s_previous": str(a[n - 1]), "s": str(a[n]),
                               "s_next": str(a[n + 1]),
                               "D": str(a[n] ** 2 - a[n - 1] * a[n + 1])}
                     for n in boundary_indices},
        "coefficient_sha256": coefficients.hexdigest(),
        "coefficient_hash_encoding": "concatenation of 4-byte LE byte lengths and minimal unsigned LE integers; zero is one zero byte",
        "sign_sha256": signs.hexdigest(),
        "sign_hash_encoding": "one ASCII -, 0, or + per D(n), in increasing n from 1 through limit",
        "timings_seconds": timings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100000)
    parser.add_argument("--independent-through", type=int, default=5001)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--checkpoint-every", type=int, default=50)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.limit < 1042 or args.independent_through < 1043:
        parser.error("limit must be >=1042 and independent-through must be >=1043")
    if args.checkpoint_every < 1:
        parser.error("checkpoint-every must be positive")
    began = time.perf_counter()
    a = coin_change(args.limit + 1, args.checkpoint, args.resume, args.checkpoint_every)
    dp_finished = time.perf_counter()
    independent_through = min(args.independent_through, args.limit + 1)
    independent = logarithmic_derivative(independent_through)
    for n, value in enumerate(independent):
        if a[n] != value:
            raise ArithmeticError("Independent methods disagree at n=%d" % n)
    independent_finished = time.perf_counter()
    certificate = summarize(a, args.limit, independent_through, {
        "dp_this_run_including_checkpoints": dp_finished - began,
        "independent_recurrence": independent_finished - dp_finished,
    })
    certificate["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: certificate[k] for k in (
        "scope", "checked_D_indices_inclusive", "negative_count", "zero_indices",
        "last_negative_index", "last_nonpositive_index", "coefficient_sha256",
        "independent_coefficient_indices_inclusive", "timings_seconds")}, indent=2))
    print("Certificate written:", args.output.resolve(), flush=True)


if __name__ == "__main__":
    main()
