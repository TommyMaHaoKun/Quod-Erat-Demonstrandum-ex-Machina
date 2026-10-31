"""Adversarial regression tests for the independent proof-DAG checker."""
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from check_z3_dag import Checker


ROOT = Path(__file__).resolve().parents[1]


def node(rule, premises, conclusion):
    return {'rule': rule, 'premises': premises, 'formula_args': [conclusion]}


def fixture_cases():
    valid = {
        'root': 5,
        'nodes': [node('asserted', [], 0), node('hypothesis', [], 1),
                  node('unit-resolution', [0, 1], 2), node('lemma', [2], 0),
                  node('asserted', [], 1), node('unit-resolution', [3, 4], 2)],
        'formulas': ['a', '(not a)', 'false'], 'assertions': [0, 1],
    }
    cases = [('valid_scoped_derivation', valid, True)]
    for name, change in [
        ('open_hypothesis', lambda d: d.update(root=2)),
        ('invalid_lemma_discharge', lambda d: d['nodes'].__setitem__(3, node('lemma', [2], 1))),
        ('invented_asserted_false', lambda d: d['nodes'].__setitem__(0, node('asserted', [], 2))),
        # The original input is inconsistent, so this specifically catches
        # accidental use of global input assertions in local inference checks.
        ('global_input_leak', lambda d: d['nodes'].__setitem__(0, node('unknown-rule', [], 2))),
    ]:
        altered = json.loads(json.dumps(valid))
        change(altered)
        cases.append((name, altered, False))
    return cases


def actual_tiny_dag():
    """A real proof containing fresh ITE definitions, arithmetic and scope."""
    import z3
    z3.set_param(proof=True)
    x, y = z3.Ints('tiny_x tiny_y')
    solver = z3.Solver()
    solver.add(y == z3.If(x >= 0, x, -x), y < 0)
    assert solver.check() == z3.unsat
    proof = solver.proof()
    unique, pending = {}, [proof]
    while pending:
        item = pending.pop()
        if item.get_id() in unique:
            continue
        unique[item.get_id()] = item
        pending.extend(c for c in item.children() if str(c.sort()) == 'Proof')
    keys = sorted(unique)
    indices = {key: i for i, key in enumerate(keys)}
    formulas, formula_ids, formula_objects = [], {}, []

    def formula_id(formula):
        key = formula.get_id()
        if key not in formula_ids:
            formula_ids[key] = len(formulas)
            formulas.append(formula.sexpr())
            formula_objects.append(formula)
        return formula_ids[key]

    records = []
    for key in keys:
        item = unique[key]
        records.append({
            'rule': str(item.decl().name()),
            'premises': [indices[c.get_id()] for c in item.children() if str(c.sort()) == 'Proof'],
            'formula_args': [formula_id(c) for c in item.children() if str(c.sort()) != 'Proof'],
        })
    string_dag = {
        'root': indices[proof.get_id()], 'nodes': records, 'formulas': formulas,
        'assertions': [formula_id(a) for a in solver.assertions()],
    }
    terms, term_ids, declarations = [], {}, set()
    for formula in formula_objects:
        pending = [(formula, False)]
        while pending:
            item, finishing = pending.pop()
            if item.get_id() in term_ids:
                continue
            if not finishing:
                pending.append((item, True))
                pending.extend((child, False) for child in reversed(item.children()))
                continue
            record = {'op': str(item.decl().name()), 'sort': str(item.sort()),
                      'args': [term_ids[c.get_id()] for c in item.children()]}
            if z3.is_int_value(item):
                record.update(op='numeral', value=item.as_string())
            elif item.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                record.update(op='symbol', name=str(item.decl().name()))
                declarations.add(item.decl().sexpr())
            term_ids[item.get_id()] = len(terms)
            terms.append(record)
    shared_dag = {key: value for key, value in string_dag.items() if key != 'formulas'}
    shared_dag.update(format='logical-term-dag-v1', terms=terms,
                      formula_roots=[term_ids[f.get_id()] for f in formula_objects],
                      declarations=sorted(declarations))
    return solver.to_smt2(), string_dag, shared_dag


def main():
    destination = (ROOT/'tmp'/'proof-checker-regressions').resolve()
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination) as name:
        folder = Path(name).resolve()
        assert folder.is_relative_to(destination)
        ordinary = '(declare-fun a () Bool)\n(assert a)\n(assert (not a))\n(check-sat)\n'
        cases = [(name, ordinary, dag, expected) for name, dag, expected in fixture_cases()]
        for name, dag, expected in fixture_cases():
            shared = {key: value for key, value in dag.items() if key != 'formulas'}
            shared.update(format='logical-term-dag-v1', declarations=['(declare-fun a () Bool)'],
                          formula_roots=[0, 1, 2], terms=[
                              {'op': 'symbol', 'name': 'a', 'sort': 'Bool', 'args': []},
                              {'op': 'not', 'sort': 'Bool', 'args': [0]},
                              {'op': 'false', 'sort': 'Bool', 'args': []}])
            cases.append(('shared_'+name, ordinary, shared, expected))
        query, dag, shared = actual_tiny_dag()
        cases.append(('real_fresh_definition_proof', query, dag, True))
        cases.append(('real_shared_fresh_definition_proof', query, shared, True))
        corrupted = json.loads(json.dumps(shared))
        corrupted['terms'][0]['sort'] = 'unsupported'
        cases.append(('shared_wrong_sort', query, corrupted, False))
        for name, query, dag, expected in cases:
            query_path, dag_path = folder/(name+'.smt2'), folder/(name+'.json.gz')
            query_path.write_text(query, encoding='utf-8')
            with gzip.open(dag_path, 'wt', encoding='utf-8') as stream:
                json.dump(dag, stream)
            run = subprocess.run(
                [sys.executable, str(ROOT/'src/check_z3_dag.py'), '--query', str(query_path),
                 '--dag', str(dag_path), '--report', str(folder/(name+'.report.json'))],
                capture_output=True, text=True, timeout=60)
            if (run.returncode == 0) != expected:
                raise AssertionError((name, run.stdout, run.stderr))
            print('PASS: '+name)
    checker = Checker('(declare-fun x () Int)',
                      ['(= (+ x 0) x)', '(> x 0)'], {}, 1000)
    checker.local_implication([], checker.formulas[0])
    try:
        checker.local_implication([], checker.formulas[1])
    except ValueError:
        pass
    else:
        raise AssertionError('Accepted a false standalone arithmetic assertion.')
    print('PASS: strict local arithmetic and invalid inference rejection.')
    equality = Checker('(declare-fun x () Int) (declare-fun y () Int) (declare-fun z () Int)',
                       ['(= x y)', '(= y z)', '(= x z)',
                        '(= (+ x 1) (+ y 1))', '(= (+ x 1) (+ z 1))'], {}, 1000)
    f = equality.formulas
    assert equality.syntactic('trans', f[:2], f[2])
    assert not equality.syntactic('trans', f[:1], f[2])
    assert equality.syntactic('monotonicity', f[:1], f[3])
    assert not equality.syntactic('monotonicity', f[:1], f[4])
    print('PASS: equality/congruence fast paths accept valid and reject invalid steps.')


if __name__ == '__main__':
    main()
