"""Verify the exact bridge from the full query to the reduced query.

Only the 28 constraints justified in the paper's reduction appendix may be
added. Each original assertion must imply its corresponding reduced-query
assertion, independently of all other assertions. These local implications
use the same strict cvc5 proof settings as the proof-DAG checker.
"""
import hashlib
import json
from pathlib import Path
import time

from check_z3_dag import Checker, print_sexpr, sexprs


ROOT = Path(__file__).resolve().parents[1]


def expected_additions():
    formulas = []
    for i in range(3):
        formulas.append('(<= c_%d_0 1)' % i)
        for j in range(1, 5):
            a, b = 'c_%d_%d' % (i, j), 'c_%d_%d' % (i, 9-j)
            formulas.extend(['(<= (- %s %s) 3)' % (a, b),
                             '(<= (- %s %s) 3)' % (b, a)])
    formulas.append('(or (distinct p_0 9) (distinct q_0 1))')
    return formulas


def main():
    started = time.monotonic()
    source = ROOT/'certificates/classification.smt2'
    reduced = ROOT/'certificates/classification_builder_reduced.smt2'
    source_text, reduced_text = [p.read_text(encoding='utf-8') for p in (source, reduced)]
    source_expr, reduced_expr = sexprs(source_text), sexprs(reduced_text)
    declarations = lambda expressions: {print_sexpr(e) for e in expressions
                                        if isinstance(e, list) and e
                                        and e[0] in ('declare-fun', 'declare-const')}
    if declarations(source_expr) != declarations(reduced_expr):
        raise ValueError('Reduced query declarations differ from the full query.')
    allowed = {'declare-fun', 'declare-const', 'assert', 'check-sat', 'set-info', 'set-logic'}
    if any(not isinstance(e, list) or not e or e[0] not in allowed for e in reduced_expr):
        raise ValueError('Unexpected reduced query command.')
    formulas = [print_sexpr(e[1]) for e in reduced_expr if e[0] == 'assert']
    additions = expected_additions()
    checker = Checker(source_text, formulas+additions, {}, 10000)
    count = len(checker.original_assertions)
    if len(formulas) != count + len(additions):
        raise ValueError('Unexpected number of reduced constraints.')
    for original, transformed in zip(checker.original_assertions, checker.formulas[:count]):
        if original != transformed:
            checker.local_implication([original], transformed)
    for actual, expected in zip(checker.formulas[count:len(formulas)],
                                checker.formulas[len(formulas):]):
        if actual != expected:
            checker.local_implication([expected], actual)
            checker.local_implication([actual], expected)
    report = {
        'result': 'PASS',
        'scope': 'full-query assertion bridge and exact list of analytic reduction constraints',
        'full_assertions': count,
        'analytic_reduction_constraints': len(additions),
        'full_query_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'reduced_query_sha256': hashlib.sha256(reduced.read_bytes()).hexdigest(),
        'stats': dict(checker.stats),
        'seconds': time.monotonic()-started,
    }
    (ROOT/'certificates/query_verification.json').write_text(
        json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
