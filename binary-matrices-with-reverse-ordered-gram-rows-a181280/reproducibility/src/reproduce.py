"""Run all four verification routes, optionally save a JSON report.

Usage: python -B src/reproduce.py [--report report.json]
Assertions must remain enabled. This launcher never downloads anything.
"""
import argparse
import json
from pathlib import Path
import platform
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    tasks = [
        ['paper_certificate.py'],
        ['verify.py'],
        ['fourier_proof.py', '--max-n', '30', '--check-all-vectors'],
        ['independent_check.py'],
    ]
    reports = []
    for task in tasks:
        proc = subprocess.run([sys.executable, '-B', str(root / 'src' / task[0])]
                              + task[1:], cwd=root, capture_output=True,
                              text=True, check=True)
        if task[0] == 'paper_certificate.py':
            result = proc.stdout.strip()
            if not result.startswith('PASS:'):
                raise RuntimeError(result)
        else:
            result = json.loads(proc.stdout)
        reports.append({'program': task[0], 'result': result})
        print('PASS:', task[0])
    direct = reports[1]['result']['counts_n0_to_last']
    fourier = reports[2]['result']['counts']
    independent = reports[3]['result']['counts_n0_through_n15']
    if direct != fourier or direct[:16] != independent:
        raise RuntimeError('Independent counters disagree')
    report = {'status': 'PASS', 'python': platform.python_version(),
              'all_counts_agree': True, 'checks': reports}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('PASS: all-n certificate and all independent count comparisons')


if __name__ == '__main__':
    main()
