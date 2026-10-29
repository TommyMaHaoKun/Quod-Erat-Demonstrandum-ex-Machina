"""Reproduce exact proof checks and independent counting from this directory."""
from pathlib import Path
import json
import platform
import subprocess
import sys
import time

if not __debug__:
    raise SystemExit('Do not run verification with python -O: assertions are required.')
root=Path(__file__).resolve().parents[1]
dest=root/'certificates'
dest.mkdir(exist_ok=True)
start=time.monotonic()
jobs=[
    ('symbolic_certificate_checks.txt','symbolic_certificates.py',[]),
    ('independent_symbolic_checks.txt','independent_symbolic_review.py',[]),
    ('independent_moment_certificates.txt','combinatorial_certificates.py',[]),
    ('independent_cell_checks.json','independent_cell_review.py',[]),
    ('pfaffian_checks.json','symbolic_pfaffian.py',['--max-n','20']),
    ('combinatorial_sum_checks.json','combinatorial_formula.py',['--max-n','100','--dp-max','30']),
]
for output,script,args in jobs:
    result=subprocess.run([sys.executable,str(root/'src'/script),*args],cwd=root,
                          capture_output=True,text=True)
    if result.returncode:
        print(result.stdout);print(result.stderr)
        raise SystemExit(f'FAILED: {script}')
    (dest/output).write_text(result.stdout,encoding='utf-8')
    print('PASS',script,flush=True)

data=json.loads((dest/'combinatorial_sum_checks.json').read_text())
values={int(k):int(v) for k,v in data['finite_sum_values'].items()}
oeis={int(row.split()[0]):int(row.split()[1])
      for row in (root/'data'/'OEIS_b181198.txt').read_text().splitlines()
      if row.strip() and not row.startswith('#')}
if len(values)!=100 or any(oeis[n]!=v for n,v in values.items()):
    raise SystemExit('OEIS table comparison failed.')
pf=json.loads((dest/'pfaffian_checks.json').read_text())
if not pf['all_residuals_zero'] or any(int(v)!=values[int(n)] for n,v in pf['values'].items()):
    raise SystemExit('Independent Pfaffian comparison failed.')
cells=json.loads((dest/'independent_cell_checks.json').read_text())
if any(int(v)!=values[int(n)] for n,v in cells['counts'].items()):
    raise SystemExit('Independent cell comparison failed.')
import sympy
report={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,
        'all_parameter_symbolic_verifiers':3,'positive_sum_terms':100,
        'oeis_terms_matched':100,'profile_dp_max_n':30,'cell_bitmask_max_n':14,
        'pfaffian_max_n':20,'target_recurrence_residual_zero_n':[1,98],
        'seconds':round(time.monotonic()-start,3),
        'scope':'Exact rational identities support the all-n written proof; finite counts are independent implementation checks.'}
(dest/'verification_summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
