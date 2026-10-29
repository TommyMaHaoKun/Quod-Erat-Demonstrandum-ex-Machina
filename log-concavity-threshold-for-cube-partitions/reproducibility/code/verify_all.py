"""Full portable reproduction: run from anywhere using Python >= 3.9."""
import json
import subprocess
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if not __debug__:
    raise RuntimeError('Run without -O: proof checks must remain enabled.')

def main():
    started=time.monotonic()
    commands=[
      ['code/finite_verify.py','certificates/finite_10000000.json'],
      ['code/major_bounds.py'],
      ['code/analytic_arcs.py'],
      ['code/exception_table.py'],
    ]
    results=[]
    for args in commands:
        print('Running '+' '.join(args),flush=True)
        begin=time.monotonic()
        result=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True)
        if result.returncode:
            print(result.stdout);print(result.stderr,file=sys.stderr)
            raise RuntimeError('Verification failed: '+args[0])
        results.append({'command':[sys.executable,*args],'status':'PASS',
          'seconds':time.monotonic()-begin,'stdout':result.stdout,'stderr':result.stderr})
        print('PASS '+args[0],flush=True)
    # Exact coverage and final comparison, independent of display-only reports.
    from fractions import Fraction as F
    if not (10_000_000>F(161,150)*50**4 and F(321,100)>3 and F(63,100)>F(4,9)):
        raise ArithmeticError('coverage or curvature combination failed')
    report={'status':'PASS','python':sys.version,'checks':results,
      'elapsed_seconds':time.monotonic()-started,
      'coverage':{'finite_determinants':[1,10000000],
        'analytic_coefficients_begin':10000000,'analytic_determinants_begin':10000001},
      'scope':'Executable certificates; analytic arguments require reading the accompanying proof.'}
    target=ROOT/'certificates/reproduction_report.json'
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: all certificate checks and exact coverage; report at '+str(target))

if __name__=='__main__':main()
