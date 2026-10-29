"""Validate the mathematical identity of every rational seam before use."""
import json
from fractions import Fraction
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'certificates'


def validate_record(record):
    base = record['base']
    t = Fraction(record['t'])
    if base not in (4, 5) or not 0 < t < 1:
        raise ValueError('Invalid seam identifier')
    pair = (t.denominator, base * t.denominator + t.numerator)
    if (record['a'], record['c']) != pair:
        raise ValueError('Seam label does not identify its primitive parameter pair')
    return (base, t), pair


def validate_inventory(atlas, seams):
    expected = set()
    cone_ids = set()
    for row in atlas:
        base, lo, hi = row['base'], Fraction(row['lo']), Fraction(row['hi'])
        key = (base, lo, hi)
        if base not in (4, 5) or not 0 <= lo < hi <= 1 or key in cone_ids:
            raise ValueError('Invalid or duplicate atlas interval')
        cone_ids.add(key)
        expected.update((base, t) for t in (lo, hi) if 0 < t < 1)
    # Verify the complete prescribed outer interval partition, independently
    # of the supplied seam list. Missing/extra cones cannot redefine coverage.
    for base, start, stop in ((4, Fraction(0), Fraction(40, 41)),
                              (5, Fraction(1, 41), Fraction(1))):
        intervals = sorted((lo, hi) for b, lo, hi in cone_ids if b == base)
        cursor = start
        for lo, hi in intervals:
            if lo != cursor:
                raise ValueError('Atlas partition has a gap or overlap')
            cursor = hi
        if cursor != stop:
            raise ValueError('Atlas partition has an incorrect outer endpoint')
    identifiers, pairs = set(), set()
    for record in seams:
        key, pair = validate_record(record)
        if key in identifiers or pair in pairs:
            raise ValueError('Duplicate seam identifier or parameter pair')
        identifiers.add(key)
        pairs.add(pair)
    expected_pairs = {(t.denominator, base*t.denominator+t.numerator)
                      for base, t in expected}
    if identifiers != expected or pairs != expected_pairs:
        raise ValueError('Missing or unexpected seam identifier or parameter pair')
    return {'identifiers': len(identifiers), 'pairs': len(pairs),
            'association': True, 'unique': True, 'complete': True}


def load_tables(directory=DATA):
    atlas = json.loads((directory / 'atlas.json').read_text(encoding='utf-8'))
    seams = json.loads((directory / 'seams.json').read_text(encoding='utf-8'))
    validate_inventory(atlas, seams)
    return atlas, seams
