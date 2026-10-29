#!/usr/bin/env python3
"""Exact cube partition certificates; Python >=3.9, standard library only.

Run from the package root:
  python code/finite_generate.py --benchmark
  python code/finite_generate.py --max-index 200000

The generated sequence includes c(max_index+1), which is needed to test
D_3(max_index). No floating point arithmetic enters any count or sign.
"""
import argparse
import gzip
import hashlib
import json
import platform
import sys
import time
from pathlib import Path


def cube_partitions(limit):
    counts = [0] * (limit + 1)
    counts[0] = 1
    j = 1
    while j ** 3 <= limit:
        cube = j ** 3
        for n in range(cube, limit + 1):
            counts[n] += counts[n - cube]
        j += 1
    return counts


def logarithmic_derivative_counts(limit):
    divisor_sums = [0] * (limit + 1)
    j = 1
    while j ** 3 <= limit:
        cube = j ** 3
        for n in range(cube, limit + 1, cube):
            divisor_sums[n] += cube
        j += 1
    counts = [1]
    for n in range(1, limit + 1):
        numerator = sum(divisor_sums[k] * counts[n-k]
                        for k in range(1, n + 1))
        quotient, remainder = divmod(numerator, n)
        if remainder:
            raise ArithmeticError('nonintegral recurrence at %d' % n)
        counts.append(quotient)
    return counts


def benchmark():
    results = []
    for algorithm, function, sizes in (
            ('cube_coin_change', cube_partitions, (20000, 100000, 200000)),
            ('divisor_recurrence', logarithmic_derivative_counts, (1000, 3000, 6000))):
        for limit in sizes:
            start = time.perf_counter()
            result = function(limit)
            results.append({'algorithm': algorithm, 'coefficient_limit': limit,
                            'seconds': time.perf_counter() - start,
                            'last_coefficient_digits': len(str(result[-1]))})
            print(json.dumps(results[-1]), flush=True)
    return results


def generate(max_index, crosscheck_limit, destination):
    destination.mkdir(parents=True, exist_ok=True)
    stem = 'finite_%d' % max_index
    certificate_path = destination / (stem + '.json')
    sequence_path = destination / (stem + '_coefficients.txt.gz')
    if certificate_path.exists() or sequence_path.exists():
        raise FileExistsError('Refusing to overwrite an existing finite certificate')
    start = time.perf_counter()
    counts = cube_partitions(max_index + 1)
    dp_seconds = time.perf_counter() - start
    print('Coin-change calculation complete in %.3f s' % dp_seconds, flush=True)
    negatives, equalities = [], []
    for n in range(1, max_index + 1):
        determinant = counts[n] ** 2 - counts[n - 1] * counts[n + 1]
        if determinant < 0:
            negatives.append(n)
        elif determinant == 0:
            equalities.append(n)
    start = time.perf_counter()
    independent = logarithmic_derivative_counts(crosscheck_limit)
    if independent != counts[:crosscheck_limit + 1]:
        raise ArithmeticError('Independent coefficient cross-check failed')
    recurrence_seconds = time.perf_counter() - start
    print('Independent recurrence agrees through %d in %.3f s' %
          (crosscheck_limit, recurrence_seconds), flush=True)
    raw_sequence = ''.join('%d\n' % value for value in counts).encode('ascii')
    # mtime=0 makes this gzip payload deterministic across runs.
    sequence_path.write_bytes(gzip.compress(raw_sequence, mtime=0))
    record = {
        'schema': 'cube-partition-finite-v1',
        'claim_scope': 'finite only; this does not prove the infinite tail',
        'max_determinant_index': max_index,
        'max_coefficient_index': max_index + 1,
        'coefficient_generator': 'cube coin-change dynamic programming',
        'independent_crosscheck': 'logarithmic derivative divisor recurrence',
        'independent_coefficient_range': [0, crosscheck_limit],
        'negative_indices': negatives,
        'equality_indices': equalities,
        'negative_count': len(negatives),
        'equality_count': len(equalities),
        'largest_negative_index': max(negatives) if negatives else None,
        'largest_equality_index': max(equalities) if equalities else None,
        'boundary_coefficients': {str(n): str(counts[n]) for n in range(15654, 15658)
                                  if n <= max_index + 1},
        'boundary_determinants': {str(n): str(counts[n] ** 2-counts[n-1]*counts[n+1])
                                  for n in (15655, 15656) if n <= max_index},
        'sequence_file': sequence_path.name,
        'sequence_format': 'ASCII c(0), c(1), ..., one decimal integer per line',
        'sequence_uncompressed_sha256': hashlib.sha256(raw_sequence).hexdigest(),
        'sequence_gzip_sha256': hashlib.sha256(sequence_path.read_bytes()).hexdigest(),
        'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'runtime': {'python': sys.version, 'platform': platform.platform(),
                    'coin_change_seconds': dp_seconds,
                    'divisor_recurrence_seconds': recurrence_seconds},
    }
    certificate_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: record[k] for k in ('negative_count', 'equality_count',
          'largest_negative_index', 'largest_equality_index',
          'boundary_coefficients', 'boundary_determinants')}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark', action='store_true')
    parser.add_argument('--max-index', type=int, default=200000)
    parser.add_argument('--crosscheck-limit', type=int, default=15657)
    parser.add_argument('--output-dir', type=Path, default=Path('certificates'))
    args = parser.parse_args()
    if args.benchmark:
        report = {'python': sys.version, 'results': benchmark()}
        args.output_dir.mkdir(parents=True, exist_ok=True)
        target = args.output_dir / 'finite_benchmark.json'
        if target.exists():
            raise FileExistsError('Refusing to overwrite the benchmark report')
        target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    else:
        if not 0 <= args.crosscheck_limit <= args.max_index + 1:
            parser.error('crosscheck limit must lie in [0, max-index+1]')
        generate(args.max_index, args.crosscheck_limit, args.output_dir)


if __name__ == '__main__':
    main()
