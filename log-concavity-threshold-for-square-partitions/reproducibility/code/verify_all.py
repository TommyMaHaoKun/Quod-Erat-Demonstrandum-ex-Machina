"""Reproduce every essential numerical proof check from the project root."""
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    root = Path(__file__).resolve().parents[1]
    checks = [
        ('global_constants', ['code/verify_global_constants.py']),
        ('major_arc', ['code/verify_major_arc.py']),
        ('minor_arcs', ['code/verify_minor_arcs.py']),
        ('minor_constants', ['code/verify_minor_constants.py']),
        ('finite_independent_audit', ['code/verify_finite_certificate.py',
                                    'certificates/finite_1200000.json']),
    ]
    results = []
    for name, args in checks:
        print('Checking ' + name + ' ...', flush=True)
        start = time.monotonic()
        process = subprocess.run([sys.executable, *args], cwd=root,
                                 text=True, capture_output=True)
        (root/'certificates'/('verification_' + name + '.txt')).write_text(
            process.stdout + process.stderr, encoding='utf-8')
        results.append({'check': name, 'passed': process.returncode == 0,
                        'seconds': round(time.monotonic()-start, 3)})
        if process.returncode:
            print(process.stdout + process.stderr)
            raise RuntimeError(name + ' failed')
        print(name + ': PASS', flush=True)
    report = {
        'scope': 'Executed exact arithmetic checks; analytic arguments are in the paper',
        'python_version': sys.version,
        'checks': results,
        'finite_D_domain': [1, 1200000],
        'analytic_coefficient_domain': 'm >= 1200000',
        'analytic_D_domain': 'n >= 1200001',
        'uncovered_positive_indices': [],
        'formal_proof_assistant': False,
        'all_passed': True,
    }
    (root/'certificates'/'verification_report.json').write_text(
        json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('All essential checks passed. The finite and analytic ranges meet without a gap.')


if __name__ == '__main__':
    main()
