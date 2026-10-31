"""Check the unbounded query with strict cvc5 proof checking.

The native proof DAG is inspected for trusted/hole rules and saved as a
deterministic gzip stream.  This is cvc5 internal proof checking, not an
external proof-assistant formalization.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
import time
from pathlib import Path
import cvc5


PROOF_OPTIONS = {
    'produce-proofs': 'true',
    'check-proofs': 'true',
    'check-proofs-complete': 'true',
    'proof-allow-trust': 'false',
    'proof-granularity': 'dsl-rewrite-strict',
    'proof-mode': 'full-proof-strict',
    # Checking the completed proof avoids checking unused search fragments.
    'proof-check': 'lazy',
}


def configure(solver, timeout):
    solver.setLogic('QF_LIA')
    solver.setOption('tlimit-per', str(timeout))
    for key, value in PROOF_OPTIONS.items():
        solver.setOption(key, value)


def inspect_proof(proof):
    """Count unique proof nodes and reject all rule names containing TRUST."""
    seen, pending, rules = set(), [proof], Counter()
    while pending:
        node = pending.pop()
        if node in seen:
            continue
        seen.add(node)
        name = str(node.getRule()).removeprefix('ProofRule.')
        rules[name] += 1
        if 'TRUST' in name or name in {'HOLE', 'UNKNOWN'}:
            raise RuntimeError('Incomplete proof rule encountered: ' + name)
        pending.extend(node.getChildren())
    return {'unique_nodes': len(seen), 'rules': dict(sorted(rules.items())),
            'trusted_rule_nodes': 0}


def effective_options(solver):
    result = {key: solver.getOptionInfo(key)['current'] for key in PROOF_OPTIONS}
    for key in ('produce-proofs', 'check-proofs', 'check-proofs-complete'):
        assert result[key] is True, (key, result[key])
    assert result['proof-allow-trust'] is False
    assert result['proof-mode'] == 'full-proof-strict'
    assert result['proof-granularity'] == 'dsl-rewrite-strict'
    return result


def proof_bytes(solver, proof):
    printed = solver.proofToString(proof)
    # cvc5 1.3.4 Python returns bytes; other bindings may return str.
    return printed if isinstance(printed, bytes) else printed.encode('utf-8')


def solver_version(solver):
    version = solver.getVersion()
    return version.decode('utf-8') if isinstance(version, bytes) else version


def smoke_test():
    solver = cvc5.Solver()
    configure(solver, 10000)
    x = solver.mkConst(solver.getIntegerSort(), 'smoke_x')
    solver.assertFormula(solver.mkTerm(cvc5.Kind.GEQ, x, solver.mkInteger(0)))
    solver.assertFormula(solver.mkTerm(cvc5.Kind.LT, x, solver.mkInteger(0)))
    result = solver.checkSat()
    assert result.isUnsat()
    proof = solver.getProof()[0]
    report = {'result': str(result), 'solver': solver_version(solver),
              'effective_options': effective_options(solver),
              'proof_statistics': inspect_proof(proof),
              'serialized_proof_bytes': len(proof_bytes(solver, proof))}
    print(json.dumps(report, indent=2), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--timeout', type=int, default=600000)
    ap.add_argument('--proof', action='store_true',
                    help='compatibility flag; strict proof checking is always enabled')
    ap.add_argument('--smoke-test', action='store_true')
    args = ap.parse_args()
    if args.smoke_test:
        smoke_test()
        return
    root = Path(__file__).resolve().parents[1]
    path = root/'certificates'/'classification.smt2'
    data = path.read_text(encoding='utf-8')
    tm = cvc5.TermManager()
    solver = cvc5.Solver(tm)
    configure(solver, args.timeout)
    parser = cvc5.InputParser(solver)
    parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6, data, 'classification')
    sm = parser.getSymbolManager()
    while True:
        cmd = parser.nextCommand()
        if cmd.isNull():
            break
        if cmd.getCommandName() == 'check-sat':
            continue
        cmd.invoke(solver, sm)
    start = time.monotonic()
    report = {'solver': solver_version(solver),
              'formula_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'internal_proof_check': True, 'strict_proof_check': True,
              'requested_options': PROOF_OPTIONS}
    destination = root/'certificates'/'cvc5_verification.json'
    try:
        result = solver.checkSat()
        report.update({'result': str(result), 'seconds': time.monotonic()-start,
                       'effective_options': effective_options(solver)})
        print(json.dumps(report, indent=2), flush=True)
        if not result.isUnsat():
            destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
            raise SystemExit('Classification NOT verified.')
        proof = solver.getProof()[0]
        report['proof_statistics'] = inspect_proof(proof)
        printed = proof_bytes(solver, proof)
        proofpath = root/'certificates'/'classification.cvc5.proof.gz'
        with proofpath.open('wb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
                compressed.write(printed)
        # Verify that the saved archive contains the exact serialized proof.
        assert gzip.decompress(proofpath.read_bytes()) == printed
        report['proof_sha256'] = hashlib.sha256(proofpath.read_bytes()).hexdigest()
        report['proof_bytes'] = proofpath.stat().st_size
        report['uncompressed_proof_sha256'] = hashlib.sha256(printed).hexdigest()
        report['uncompressed_proof_bytes'] = len(printed)
        report['status'] = 'PASS'
        report['total_seconds'] = time.monotonic()-start
        print('Proof written: '+str(report['proof_bytes'])+' bytes.', flush=True)
    except Exception as error:
        report.update({'status': 'FAIL', 'error': str(error),
                       'total_seconds': time.monotonic()-start})
        destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        raise
    destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
