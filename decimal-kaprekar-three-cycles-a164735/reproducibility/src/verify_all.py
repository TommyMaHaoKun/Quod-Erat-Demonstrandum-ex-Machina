"""Run the published verification procedure without regenerating the proof."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-paper', action='store_true',
                        help='Also rebuild local paper sources using pdfLaTeX.')
    args = parser.parse_args()
    started = time.monotonic()
    commands = [
        ['src/test_proof_checker.py'],
        ['src/verify_model.py'],
        ['src/families.py', '--symbolic'],
        ['src/verify_query.py'],
        ['src/check_z3_dag.py',
         '--bridge-assertions',
         '--dag', 'certificates/classification_builder_reduced_arith2_terms.z3.dag.json.gz',
         '--query', 'certificates/classification_builder_reduced.smt2',
         '--report', 'certificates/z3_dag_reduced_verification.json'],
    ]
    if args.build_paper:
        commands.append(['src/build_paper.py'])
    runs = []
    for command in commands:
        print('Running: '+ ' '.join(command), flush=True)
        before = time.monotonic()
        result = subprocess.run([sys.executable]+command, cwd=ROOT)
        runs.append({'command': command, 'exit_code': result.returncode,
                     'seconds': time.monotonic()-before})
        if result.returncode:
            raise SystemExit(result.returncode)
    files = sorted((ROOT/'src').glob('*.py')) + [
        ROOT/'requirements.txt',
        ROOT/'literature/target_formula.tex',
        ROOT/'certificates/classification.smt2',
        ROOT/'certificates/classification_builder_reduced.smt2',
        ROOT/'certificates/classification_builder_reduced_arith2_terms.z3.dag.json.gz',
    ]
    report = {
        'result': 'PASS', 'python': sys.version.split()[0],
        'runs': runs, 'seconds': time.monotonic()-started,
        'sha256': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in files},
    }
    (ROOT/'certificates/release_verification.json').write_text(
        json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('PASS: every published computational verification completed.')


if __name__ == '__main__':
    main()
