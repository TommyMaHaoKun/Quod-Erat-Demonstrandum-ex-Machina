"""Independent bounded validation of the unbounded histogram encoding.

Uses actual decimal integer subtraction as the reference operation. This
script is a model check on finite examples, not an all-length proof.
"""
import json
from collections import Counter
from itertools import combinations_with_replacement
from pathlib import Path
from random import Random


def histogram(number):
    counts = Counter(str(number))
    return tuple(counts[str(i)] for i in range(10))


def integer_image(counts):
    digits = ''.join(str(i) * counts[i] for i in range(10))
    return int(digits[::-1]) - int(digits)


def ordinary_step(number):
    digits = ''.join(sorted(str(number)))
    return int(digits[::-1]) - int(digits)


def algebraic_edge(counts):
    n = sum(counts)
    h = [0] * 10
    for small in range(10):
        left = sum(counts[:small])
        for large in range(small + 1, 10):
            right = sum(counts[large + 1:])
            h[large - small] += max(
                0, min(left + counts[small], right + counts[large])
                - max(left, right))
    support = [j for j in range(1, 10) if h[j]]
    if not support:
        return None
    p, q = max(support), min(support)
    t = n - 2 * sum(h)
    out = [h[j] + h[9 - j] + (t if j == 9 else 0) for j in range(10)]
    out[q] -= 1
    out[q - 1] += 1
    out[9 - p] -= 1
    out[10 - p] += 1
    width_preserved = not (sum(h) == 1 and p == 1)
    return tuple(h), t, p, q, tuple(out), width_preserved


def check_one(counts):
    value = integer_image(counts)
    edge = algebraic_edge(counts)
    if edge is None:
        assert value == 0
        return False
    h, t, p, q, out, width = edge
    digits = [i for i in range(10) for _ in range(counts[i])]
    direct = Counter(digits[-1 - i] - digits[i] for i in range(len(digits) // 2))
    assert h[1:] == tuple(direct[i] for i in range(1, 10))
    assert t == len(digits) - 2 * sum(direct[i] for i in range(1, 10))
    assert t >= 0 and min(out) >= 0 and sum(out) == sum(counts)
    assert width == (len(str(value)) == sum(counts))
    actual = histogram(value)
    if width:
        assert out == actual
    else:
        nominal = list(actual)
        nominal[0] += 1
        assert out == tuple(nominal)
    return width


def check_z3(samples):
    import z3
    from classify_smt import edge as symbolic_edge
    count = 0
    for c in samples:
        numerical = algebraic_edge(c)
        if numerical is None:
            continue
        solver = z3.Solver()
        out = [z3.Int('review_out_' + str(j)) for j in range(10)]
        h, t, p, q = symbolic_edge(solver, [z3.IntVal(v) for v in c], out, 'review')
        got = solver.check()
        if not numerical[-1]:
            assert got == z3.unsat
        else:
            assert got == z3.sat
            model = solver.model()
            assert tuple(model.eval(v).as_long() for v in out) == numerical[4]
            assert tuple(model.eval(v).as_long() for v in h) == numerical[0]
            assert model.eval(t).as_long() == numerical[1]
            assert model.eval(p).as_long() == numerical[2]
            assert model.eval(q).as_long() == numerical[3]
            solver.add(z3.Or(*[out[j] != numerical[4][j] for j in range(10)]))
            assert solver.check() == z3.unsat
        count += 1
    return count


def main():
    exhaustive_count = 0
    cycle_counts = {}
    samples = []
    for n in range(1, 9):
        images = {}
        for digits in combinations_with_replacement(range(10), n):
            c = tuple(digits.count(j) for j in range(10))
            check_one(c)
            exhaustive_count += 1
            images[c] = integer_image(c)
            if exhaustive_count % 997 == 0:
                samples.append(c)
        cycles = set()
        for c, image in images.items():
            c1 = histogram(image)
            if sum(c1) != n:
                continue
            c2 = histogram(images[c1])
            if sum(c2) != n:
                continue
            c3 = histogram(images[c2])
            if c3 == c and c1 != c:
                x0, x1, x2 = images[c2], image, images[c1]
                assert len({x0, x1, x2}) == 3
                assert histogram(x0) == c
                assert ordinary_step(x0) == x1
                assert ordinary_step(x1) == x2
                assert ordinary_step(x2) == x0
                cycles.add(min((x0, x1, x2), (x1, x2, x0), (x2, x0, x1)))
        cycle_counts[n] = len(cycles)
    assert cycle_counts == {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1}
    random = Random(164735)
    for i in range(2000):
        n = random.randrange(9, 301)
        c = [0] * 10
        for _ in range(n):
            c[random.randrange(10)] += 1
        c = tuple(c)
        check_one(c)
        if i % 101 == 0:
            samples.append(c)
    # Explicit width-loss and repeated-digit corner cases.
    for n in (2, 3, 8, 101):
        c = (n - 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)
        check_one(c)
        samples.append(c)
    checked_z3 = check_z3(samples)
    report = {
        'status': 'PASS',
        'scope': 'bounded validation; not a proof of all-length classification',
        'all_histograms_lengths': [1, 8],
        'exhaustive_histograms': exhaustive_count,
        'deterministic_random_cases': 2000,
        'random_digit_lengths': [9, 300],
        'random_seed': 164735,
        'symbolic_edge_cases': checked_z3,
        'exact_three_cycle_counts': cycle_counts,
        'checks': ['positive-difference overlap', 'central length', 'borrow corrections',
                   'ordinary non-padded width', 'integer-cycle reconstruction',
                   'symbolic constraints and output uniqueness'],
    }
    root = Path(__file__).resolve().parents[1]
    destination = root / 'certificates' / 'model_verification.json'
    destination.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
