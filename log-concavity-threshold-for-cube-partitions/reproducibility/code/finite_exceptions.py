#!/usr/bin/env python3
"""Lossless stride-eight encoding of a finite certificate's exception sets.

Usage: python code/finite_exceptions.py certificates/finite_200000.json
The output is supplementary display data, not a new counting algorithm.
"""
import json
import sys
from pathlib import Path


def runs(indices, step=8):
    members = set(indices)
    result = []
    for first in sorted(members):
        if first - step in members:
            continue
        last = first
        while last + step in members:
            last += step
        result.append([first, last, step])
    expanded = sorted(n for first, last, step in result
                      for n in range(first, last + 1, step))
    if expanded != sorted(indices):
        raise ArithmeticError('lossless expansion check failed')
    return result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python code/finite_exceptions.py CERTIFICATE.json')
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding='utf-8'))
    output = {
        'source_certificate': path.name,
        'scope': [1, data['max_determinant_index']],
        'meaning': '[a,b,s] represents {a,a+s,...,b}, including both endpoints',
        'negative_runs': runs(data['negative_indices']),
        'equality_runs': runs(data['equality_indices']),
        'negative_count': len(data['negative_indices']),
        'equality_count': len(data['equality_indices']),
        'expansion_verified': True,
    }
    target = path.with_name(path.stem + '_exception_runs.json')
    with target.open('x', encoding='utf-8') as stream:
        json.dump(output, stream, indent=2)
        stream.write('\n')
    print('%d negative runs; %d equality runs; exact expansion checked' %
          (len(output['negative_runs']), len(output['equality_runs'])))
