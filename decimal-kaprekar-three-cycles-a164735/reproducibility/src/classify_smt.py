"""Unbounded integer search for a three-cycle outside the two known families."""
import argparse
import hashlib
import json
import time
from pathlib import Path
import z3


def minimum(x, y):
    return z3.If(x <= y, x, y)


def maximum(x, y):
    return z3.If(x >= y, x, y)


def total(values):
    values = list(values)
    return values[0] if len(values) == 1 else z3.Sum(values)


def edge(solver, c, out, tag):
    lo = [total(c[:i]) if i else z3.IntVal(0) for i in range(11)]
    hi = [total(c[i + 1:]) if i < 9 else z3.IntVal(0) for i in range(10)]
    h = [z3.Int(f"h_{tag}_{j}") for j in range(10)]
    for j in range(1, 10):
        terms = []
        for low in range(10 - j):
            high = low + j
            overlap = minimum(lo[low + 1], hi[high] + c[high]) - maximum(lo[low], hi[high])
            terms.append(maximum(0, overlap))
        solver.add(h[j] == total(terms), h[j] >= 0)
    t = z3.Int(f"t_{tag}")
    solver.add(t == z3.Sum(c) - 2 * z3.Sum(h[1:]), t >= 0)
    p, q = z3.Ints(f"p_{tag} q_{tag}")
    solver.add(p >= 1, p <= 9, q >= 1, q <= p)
    for j in range(1, 10):
        solver.add(z3.Implies(z3.Or(j < q, j > p), h[j] == 0))
        solver.add(z3.Implies(z3.Or(j == p, j == q), h[j] >= 1))
    # An n-digit image fails only when its single positive difference is 1.
    solver.add(z3.Or(h[1] == 0, z3.Sum(h[1:]) >= 2))
    h[0] = z3.IntVal(0)
    for j in range(10):
        solver.add(out[j] == h[j] + h[9-j] + z3.If(j == 9, t, 0)
                   - z3.If(q == j, 1, 0) + z3.If(q - 1 == j, 1, 0)
                   - z3.If(9 - p == j, 1, 0) + z3.If(10 - p == j, 1, 0))
    return h, t, p, q


def family_x(c):
    m = c[9] - c[0]
    return z3.And(m >= 0, c[0] >= 1,
                  *[c[j] == c[9-j] for j in range(1, 5)],
                  c[1] >= m+1, c[2] >= m+1, c[3] >= m, c[4] >= m+1)


def family_y(c):
    return z3.And(c[0] == 1, c[2] == 0, c[7] == 0, c[9] == 0,
                  c[8] == c[1]+1, c[6] == c[3]+1, c[4] == c[5]+1,
                  c[3] >= 1, c[5] >= 1)


def build():
    solver = z3.Solver()
    c = [[z3.Int(f"c_{i}_{j}") for j in range(10)] for i in range(3)]
    for row in c:
        solver.add(*[v >= 0 for v in row], z3.Sum(row) >= 2)
    for row in c[1:]:
        solver.add(z3.Sum(row) == z3.Sum(c[0]))
    edges = [edge(solver, c[i], c[(i+1) % 3], str(i)) for i in range(3)]
    solver.add(z3.Or(*[c[0][j] != c[1][j] for j in range(10)]))
    solver.add(z3.Not(family_x(c[0])))
    solver.add(*[z3.Not(family_y(row)) for row in c])
    return solver, c, edges


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--timeout', type=int, default=600000)
    ap.add_argument('--export', action='store_true')
    args = ap.parse_args()
    solver, c, edges = build()
    solver.set(timeout=args.timeout)
    root = Path(__file__).resolve().parents[1]
    formula = solver.to_smt2()
    if args.export:
        with (root/'certificates'/'classification.smt2').open('w', encoding='utf-8', newline='\n') as stream:
            stream.write(formula)
    start = time.monotonic()
    result = solver.check()
    report = {'result': str(result), 'seconds': time.monotonic()-start, 'z3': z3.get_version_string(),
              'formula_sha256': hashlib.sha256(formula.encode('utf-8')).hexdigest()}
    if result == z3.sat:
        model = solver.model()
        report['histograms'] = [[model.eval(v).as_long() for v in row] for row in c]
        report['edges'] = [{'h':[model.eval(v).as_long() for v in h[1:]], 't':model.eval(t).as_long(), 'p':model.eval(p).as_long(), 'q':model.eval(q).as_long()} for h,t,p,q in edges]
    elif result == z3.unknown:
        report['reason'] = solver.reason_unknown()
    (root/'certificates'/'smt_search.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)
    if result != z3.unsat:
        raise SystemExit('Classification NOT verified.')
