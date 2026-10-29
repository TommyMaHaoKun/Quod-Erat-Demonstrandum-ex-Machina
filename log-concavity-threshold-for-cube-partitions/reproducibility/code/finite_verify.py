#!/usr/bin/env python3
"""Small exact verifier, independent of the generator module.

Usage: python code/finite_verify.py certificates/finite_200000.json
Checks the complete sequence by coin change; independently checks the stated
prefix by a different generating-function identity; checks every sign.
Python >=3.9, standard library only. Uses explicit checks, not removable asserts.
"""
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def verify(path):
    start = time.perf_counter()
    record = json.loads(path.read_text(encoding='utf-8'))
    require(record['schema'] == 'cube-partition-finite-v1', 'unknown schema')
    bound = record['max_determinant_index']
    limit = record['max_coefficient_index']
    require(bound >= 1 and limit == bound + 1, 'invalid coefficient coverage')
    values = None
    if record['sequence_file'] is not None:
        payload = (path.parent / record['sequence_file']).read_bytes()
        require(hashlib.sha256(payload).hexdigest() == record['sequence_gzip_sha256'],
                'compressed sequence hash differs')
        raw = gzip.decompress(payload)
        require(hashlib.sha256(raw).hexdigest() == record['sequence_uncompressed_sha256'],
                'uncompressed sequence hash differs')
        values = [int(line) for line in raw.decode('ascii').splitlines()]
        require(len(values) == limit + 1, 'incorrect sequence length')
    computed = [1] + [0] * limit
    j = 1
    while j * j * j <= limit:
        step = j * j * j
        for n in range(step, limit + 1):
            computed[n] += computed[n-step]
        j += 1
    if values is None:
        values = computed
    else:
        require(computed == values, 'coin-change full-range comparison failed')
    sequence_hash = hashlib.sha256()
    for value in computed:
        sequence_hash.update(('%d\n' % value).encode('ascii'))
    require(sequence_hash.hexdigest() == record['sequence_uncompressed_sha256'],
            'regenerated coefficient digest differs')
    if 'last_coefficient' in record:
        require(computed[-1] == int(record['last_coefficient']),
                'last coefficient differs')
    del computed
    independent_end = record['independent_coefficient_range'][1]
    require(record['independent_coefficient_range'][0] == 0
            and 0 <= independent_end <= limit, 'invalid cross-check range')
    # A(m) = sum_{j^3 | m} j^3; n c(n) = sum_{m=1}^n A(m)c(n-m).
    # Using verified preceding coefficients here verifies each recurrence
    # relation independently, and induction with c(0)=1 identifies the prefix.
    a = [0] * (independent_end + 1)
    j = 1
    while j ** 3 <= independent_end:
        cube = j ** 3
        for multiple in range(cube, independent_end + 1, cube):
            a[multiple] += cube
        j += 1
    require(values[0] == 1, 'incorrect constant term')
    for n in range(1, independent_end + 1):
        total = sum(a[m] * values[n-m] for m in range(1, n+1))
        require(total == n * values[n], 'divisor recurrence fails at %d' % n)
    negative, equality = [], []
    for n in range(1, bound + 1):
        d = values[n] * values[n] - values[n-1] * values[n+1]
        if d < 0:
            negative.append(n)
        if d == 0:
            equality.append(n)
    require(negative == record['negative_indices'], 'negative index set differs')
    require(equality == record['equality_indices'], 'equality index set differs')
    require(len(negative) == record['negative_count'], 'negative count differs')
    require(len(equality) == record['equality_count'], 'equality count differs')
    require((max(negative) if negative else None) == record['largest_negative_index'],
            'largest negative index differs')
    require((max(equality) if equality else None) == record['largest_equality_index'],
            'largest equality index differs')
    for key, value in record['boundary_coefficients'].items():
        require(values[int(key)] == int(value), 'boundary coefficient differs')
    for key, value in record['boundary_determinants'].items():
        n = int(key)
        require(values[n] ** 2-values[n-1]*values[n+1] == int(value),
                'boundary determinant differs')
    report = {'result': 'PASS', 'certificate': path.name,
              'coin_change_coefficient_range': [0, limit],
              'independent_recurrence_coefficient_range': [0, independent_end],
              'exact_determinant_range': [1, bound],
              'negative_count': len(negative), 'equality_count': len(equality),
              'largest_negative_index': max(negative) if negative else None,
              'largest_equality_index': max(equality) if equality else None,
              'elapsed_seconds': time.perf_counter() - start,
              'python': sys.version,
              'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python code/finite_verify.py CERTIFICATE.json')
    verify(Path(sys.argv[1]))
