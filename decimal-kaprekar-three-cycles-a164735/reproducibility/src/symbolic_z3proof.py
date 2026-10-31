"""Produce and inventory a Z3 proof of the exact exported classification query.

This generator does not independently validate Z3's proof.  The inventory
supports development of a separate local-inference verifier.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import time

import z3


ROOT = Path(__file__).resolve().parents[1]


def compressed_write(path, data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('wb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0,
                          compresslevel=6) as compressed:
            compressed.write(data)
    temporary.replace(path)
    return {'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'uncompressed_bytes': len(data),
            'uncompressed_sha256': hashlib.sha256(data).hexdigest()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--timeout', type=int, default=600000)
    ap.add_argument('--builder', action='store_true',
                    help='construct the identical query directly with classify_smt.build')
    ap.add_argument('--reduced', action='store_true',
                    help='direct reduced query; depends on the separately proved reduction lemmas')
    ap.add_argument('--arith-solver', type=int, choices=[2,6])
    ap.add_argument('--simplify', action='store_true',
                    help='normalize assertions first; retain explicit source assertion bridges')
    ap.add_argument('--text-proof', action='store_true',
                    help='also serialize the full native proof text; DAG alone is sufficient')
    ap.add_argument('--term-dag', action='store_true', default=True,
                    help='serialize logical terms with global sharing; never print formula text')
    args = ap.parse_args()
    if args.reduced:
        args.builder = True
    z3.set_param(proof=True)
    path = ROOT / 'certificates' / 'classification.smt2'
    data = path.read_bytes()
    original_query_sha256 = hashlib.sha256(data).hexdigest()
    if args.builder:
        from classify_smt import build
        solver, histograms, edges = build()
        # Build first, before parsing, to retain the direct-builder AST order.
        source_solver = z3.Solver()
        source_solver.from_string(data.decode('utf-8'))
        source_assertions = list(source_solver.assertions())
        assert len(solver.assertions()) == len(source_assertions)
        assert all(z3.eq(z3.simplify(a), z3.simplify(b))
                   for a,b in zip(source_assertions, solver.assertions()))
        # This is a preliminary normalization check, not an independent
        # proof of the bridges. The standalone checker must verify them.
        builder_data = solver.to_smt2().encode('utf-8')
        if args.reduced:
            for row in histograms:
                solver.add(row[0] <= 1)
                for j in range(1,5):
                    solver.add(row[j]-row[9-j] <= 3, row[9-j]-row[j] <= 3)
            solver.add(z3.Or(edges[0][2] != 9, edges[0][3] != 1))
            builder_data = solver.to_smt2().encode('utf-8')
            data = builder_data
            source_assertions = list(solver.assertions())
        builder_name = 'classification_builder_reduced.smt2' if args.reduced else 'classification_builder.smt2'
        (ROOT/'certificates'/builder_name).write_bytes(builder_data)
    else:
        source_solver = z3.Solver()
        source_solver.from_string(data.decode('utf-8'))
        source_assertions = list(source_solver.assertions())
        solver = source_solver
    if args.simplify:
        original_solver = solver
        solver = z3.Solver()
        for assertion in original_solver.assertions():
            solver.add(z3.simplify(assertion))
    solver.set(timeout=args.timeout)
    if args.arith_solver is not None:
        solver.set('smt.arith.solver', args.arith_solver)
    started = time.monotonic()
    result = solver.check()
    report = {'solver': z3.get_version_string(), 'result': str(result),
              'query_sha256': hashlib.sha256(data).hexdigest(),
              'solve_seconds': time.monotonic()-started,
              'construction': 'direct builder' if args.builder else 'SMT-LIB parser',
              'reduced': args.reduced,
              'arithmetic_solver': args.arith_solver,
              'assertions_simplified': args.simplify,
              'independent_proof_checked': False}
    print(json.dumps(report), flush=True)
    suffix = '_builder' if args.builder else ''
    if args.reduced:
        suffix += '_reduced'
        report['original_query_sha256'] = original_query_sha256
        report['reduction_dependencies'] = [
            'zero-count monotonicity lemma', 'regular-cycle classification',
            'orbit rotation and X closure', 'inner imbalance bounded by three']
    if args.arith_solver is not None:
        suffix += '_arith' + str(args.arith_solver)
    if args.simplify:
        suffix += '_simp'
    if args.term_dag:
        suffix += '_terms'
    destination = ROOT / 'certificates' / ('z3proof_summary'+suffix+'.json')
    if args.builder:
        report['builder_query_sha256'] = hashlib.sha256(builder_data).hexdigest()
    # Save the solver result before the potentially substantial DAG traversal.
    destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    if result != z3.unsat:
        report['reason'] = solver.reason_unknown() if result == z3.unknown else 'SAT'
        destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        raise SystemExit('No UNSAT proof obtained.')
    proof = solver.proof()
    pending = [proof]
    unique = {}
    rules = Counter()
    samples = {}
    while pending:
        node = pending.pop()
        key = node.get_id()
        if key in unique:
            continue
        unique[key] = node
        name = str(node.decl().name())
        rules[name] += 1
        if name not in samples:
            # Never stringify a proof subtree here: sharing can make its
            # expanded textual representation exponentially larger.
            samples[name] = {'node_id': key, 'argument_count': node.num_args()}
        pending.extend(child for child in node.children() if child.sort().kind() == 1000)
        if len(unique) % 10000 == 0:
            print('Inventoried proof nodes: '+str(len(unique)), flush=True)
    ordered = sorted(unique)
    node_ids = {key: i for i, key in enumerate(ordered)}
    formulas = {}
    formula_text = []
    formula_refs = []
    declarations = {}
    formula_subterms_seen = set()

    def formula_id(formula):
        key = formula.get_id()
        if key not in formulas:
            formulas[key] = len(formula_refs)
            formula_refs.append(formula)
            if args.term_dag:
                return formulas[key]
            formula_text.append(formula.sexpr())
            pending_terms = [formula]
            while pending_terms:
                term = pending_terms.pop()
                if term.get_id() in formula_subterms_seen:
                    continue
                formula_subterms_seen.add(term.get_id())
                if z3.is_app(term):
                    declaration = term.decl()
                    if declaration.kind() == z3.Z3_OP_UNINTERPRETED:
                        declarations[declaration.get_id()] = declaration.sexpr()
                    pending_terms.extend(term.children())
                elif z3.is_quantifier(term):
                    pending_terms.append(term.body())
        return formulas[key]

    records = []
    for key in ordered:
        node = unique[key]
        children = node.children()
        premise_ids, formula_ids = [], []
        for child in children:
            if child.sort().kind() == 1000:
                premise_ids.append(node_ids[child.get_id()])
            else:
                formula_ids.append(formula_id(child))
        records.append({
            'rule': str(node.decl().name()), 'kind': node.decl().kind(),
            'premises': premise_ids, 'formula_args': formula_ids,
        })
        if len(records) % 20000 == 0:
            print('Exported proof records: '+str(len(records)), flush=True)
    inventory = {'root': node_ids[proof.get_id()], 'nodes': records,
                 'formulas': formula_text,
                 'assertions': [formula_id(a) for a in solver.assertions()]}
    inventory['source_assertions'] = [formula_id(a) for a in source_assertions]
    inventory['assertion_bridges'] = [
        [formula_id(a), formula_id(b)]
        for a,b in zip(source_assertions,solver.assertions())]
    inventory['source_query_sha256'] = hashlib.sha256(data).hexdigest()
    if args.term_dag:
        term_ids, term_records = {}, []
        operators = Counter()
        for formula in formula_refs:
            stack = [(formula, False, None)]
            while stack:
                term, expanded, children = stack.pop()
                term_key = term.get_id()
                if term_key in term_ids:
                    continue
                if not z3.is_app(term):
                    raise RuntimeError('Only quantifier-free application terms are supported.')
                if not expanded:
                    children = term.children()
                    stack.append((term, True, children))
                    stack.extend((child, False, None) for child in reversed(children)
                                 if child.get_id() not in term_ids)
                    continue
                declaration = term.decl()
                kind = declaration.kind()
                sort = str(term.sort())
                record = {'sort': sort, 'kind': kind,
                          'args': [term_ids[child.get_id()] for child in children]}
                parameters = declaration.params()
                if parameters:
                    if not all(isinstance(value, (int, str)) for value in parameters):
                        raise RuntimeError('Unsupported declaration parameter type.')
                    record['params'] = parameters
                if z3.is_int_value(term) or z3.is_rational_value(term):
                    record.update(op='numeral', value=term.as_string())
                elif kind == z3.Z3_OP_UNINTERPRETED or (
                        not children and kind not in (z3.Z3_OP_TRUE, z3.Z3_OP_FALSE)):
                    if children:
                        raise RuntimeError('Uninterpreted functions are not supported.')
                    record.update(op='symbol', name=str(declaration.name()))
                    declarations[declaration.get_id()] = declaration.sexpr()
                else:
                    record['op'] = str(declaration.name())
                operators[(record['op'], sort)] += 1
                term_ids[term_key] = len(term_records)
                term_records.append(record)
                if len(term_records) % 20000 == 0:
                    print('Exported shared logical terms: '+str(len(term_records)), flush=True)
        inventory.pop('formulas')
        inventory['format'] = 'logical-term-dag-v1'
        inventory['terms'] = term_records
        inventory['formula_roots'] = [term_ids[formula.get_id()] for formula in formula_refs]
        report['logical_terms'] = len(term_records)
        report['operators'] = {op+':'+sort: count for (op,sort),count in sorted(operators.items())}
        print('Operator inventory: '+json.dumps(report['operators']), flush=True)
    inventory['declarations'] = sorted(declarations.values())
    # formula_text can grow while recording assertions; the shared list remains current.
    report['proof_nodes'] = len(unique)
    report['formula_nodes'] = len(formula_refs)
    report['rules'] = dict(sorted(rules.items()))
    report['samples'] = samples
    report['dag'] = compressed_write(ROOT/'certificates'/('classification'+suffix+'.z3.dag.json.gz'),
                                     json.dumps(inventory, separators=(',', ':')))
    if args.text_proof:
        report['proof'] = compressed_write(ROOT/'certificates'/('classification'+suffix+'.z3.proof.gz'),
                                           proof.sexpr())
    report['total_seconds'] = time.monotonic()-started
    destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'samples'},
                     indent=2), flush=True)


if __name__ == '__main__':
    main()
