"""Run the packaged proof checkers without invoking any discovery routine."""
import sys,subprocess,json,time
from pathlib import Path
from classify import classify
here=Path(__file__).resolve().parent;report=[]
if not __debug__:
    raise RuntimeError('Run without -O: mathematical assertions must be enabled.')
for script in('test_seam_inventory.py','verify_atlas.py','verify_seams.py','pure_obstruction_certificate.py','uniform_certificate.py','a2_certificate.py','band4_tables.py','verify_coverage.py',
 'near/tail_stationarity_check.py','near/upper_splice_certificate.py',
 'near/upper_boundary_uniform.py','near/upper_minimality.py',
 'near/halfstrip_certificate.py','near/lower_seam_uniform_certificate.py',
 'near/lower_open_boundary_uniform.py','near/lower_open_minimality.py',
 'near/crosscheck_uniform.py','crosscheck_atlas.py','near/lower_open_crosscheck.py','near/lower_seam_crosscheck.py','check_examples.py'):
    begin=time.monotonic()
    r=subprocess.run([sys.executable,str(here/script)],cwd=here.parent,capture_output=True,text=True)
    print(script,r.returncode,r.stdout.splitlines()[-1] if r.stdout else r.stderr,flush=True)
    assert r.returncode==0,(script,r.stdout,r.stderr)
    report.append(dict(script=script,exit_code=r.returncode,seconds=time.monotonic()-begin,output=r.stdout))
for a,c,p,q in[(3,14,15,47),(41,204,245,13411),(41,206,247,13855),(2,9,11,21),(3,19,15,13),(3,32,5,74)]:
    z=classify(a,c);assert(z['p'],z['q'])==(p,q)
for a,c,p,q in [(50,251,301,20797),(83,413,496,30462),(83,417,500,31374),(44,219,263,15536)]:
    z=classify(a,c);assert(z['p'],z['q'])==(p,q)
(here.parent/'certificates/release_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('All packaged theorem checks and classifier checks passed.')
