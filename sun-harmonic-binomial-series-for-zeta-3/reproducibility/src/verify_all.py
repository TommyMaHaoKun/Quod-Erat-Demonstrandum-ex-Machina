"""Run all mathematical checks from paths relative to this source file."""
from pathlib import Path
import json
import platform
import subprocess
import sys
import sympy


def main():
    root=Path(__file__).resolve().parents[1]
    reports=[]
    for name in ('verify_wz.py', 'verify_independent.py', 'numerical_checks.py'):
        p=subprocess.run([sys.executable, str(root/'src'/name)],
                         cwd=root,capture_output=True,text=True)
        print(p.stdout,end='')
        if p.returncode:
            print(p.stderr)
            raise SystemExit(p.returncode)
        reports.append({'script':name,'exit_code':p.returncode,'output':p.stdout})
    report={'status':'PASS','python':platform.python_version(),
            'sympy':sympy.__version__,'checks':reports,
            'scope':'Exact rational identities and independent numerical enclosures; analytic proofs are in the paper.'}
    out=root/'certificates'/'verification_report.json'
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: all supplied mathematical checks.')


if __name__=='__main__':
    main()
