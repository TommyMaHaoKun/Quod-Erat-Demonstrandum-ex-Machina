"""Single entry point for the complete computer-assisted proof package.

Default: all exact finite reconstructions and analytic checks. The explicitly
named --analytic-only mode is a partial check and never reports full success.
Run from any directory with normal Python, without -O/PYTHONOPTIMIZE.
"""
if not __debug__:
    raise RuntimeError('Run without -O or PYTHONOPTIMIZE; all proof checks are required.')

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CASES = ((4,2000000,637855),(5,12000000,2507861),(6,180000000,35577569))


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def manifest_check():
    path = ROOT/'MANIFEST.json'
    require(path.exists(), 'MANIFEST.json missing: build the source package before the full release check.')
    data = json.loads(path.read_text(encoding='utf-8'))
    require(data['schema']=='power-partition-manifest-v1','Unknown manifest format')
    for relative, expected in data['files'].items():
        file = (ROOT/relative).resolve()
        require(ROOT in file.parents, 'Manifest path leaves package root')
        require(file.is_file(), 'Missing package input: '+relative)
        actual = hashlib.sha256(file.read_bytes()).hexdigest()
        require(actual==expected,'Package input digest differs: '+relative)
    return hashlib.sha256(path.read_bytes()).hexdigest(),len(data['files'])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--analytic-only',action='store_true')
    ap.add_argument('--python-finite',action='store_true',
                    help='Portable arbitrary-precision route; substantially slower and higher-memory.')
    args=ap.parse_args()
    require(not sys.flags.optimize,'Optimized Python disables required assertions')
    started=time.monotonic()
    manifest,count=manifest_check()
    initial_caches=[str((ROOT/'certificates'/f'finite_k{k}_{end}').relative_to(ROOT))
                    for k,end,threshold in CASES
                    if (ROOT/'certificates'/f'finite_k{k}_{end}').exists()]
    stages=[]
    def run(name,arguments):
        print('\nVERIFY '+name,flush=True)
        before=time.monotonic()
        subprocess.run([sys.executable]+arguments,cwd=str(ROOT),check=True)
        stages.append({'name':name,'result':'PASS','seconds':round(time.monotonic()-before,3)})

    run('Wright-model rational constants',['src/wright_check.py'])
    run('Mellin and contour numerical enclosures',['src/tail_bounds.py'])
    run('Uniform intermediate arcs',['src/minor_intermediate.py'])
    run('Independent complete far-arc partitions',['src/minor_far_verify.py','--write'])
    run('Infinite-tail arithmetic and endpoints',['src/tail_assembly.py'])

    if not args.analytic_only:
        for k,end,threshold in CASES:
            certificate=f'certificates/finite_k{k}_{end}.json'
            script='src/finite_verify.py' if args.python_finite or os.name!='nt' else 'src/finite_fast_verify.py'
            run(f'k={k} exact coefficients and all determinants through {end}',[script,certificate])
            record=json.loads((ROOT/certificate).read_text(encoding='utf-8'))
            require(record['k']==k,'Certificate power differs from requested case')
            require(record['coefficient_range']==[0,end+1],'Incorrect coefficient coverage')
            require(record['determinant_range']==[1,end],'Incorrect determinant coverage')
            require(record['candidate_threshold']==threshold,'Incorrect candidate convention')
            require(record['largest_negative_index']==threshold-1,'Last negative index differs')
            require(int(record['boundary_determinants'][str(threshold-1)])<0,'Missing failure witness')
            require(record['largest_equality_index']<threshold,'An equality violates claimed strict tail')
            require(record['strictly_positive_interval']==[threshold,end],'Finite positive interval mismatch')

    assembly=json.loads((ROOT/'certificates/tail_assembly.json').read_text(encoding='utf-8'))
    require(assembly['result']=='PASS','Analytic assembly failed')
    require(len(assembly['rows'])==len(CASES),'Incorrect number of analytic cases')
    for row,(k,end,threshold) in zip(assembly['rows'],CASES):
        require(row['k']==k and row['strict_tail_starts_at']<=end+1,'Finite/analytic index gap')
    report={'status':'PASS_ANALYTIC_ONLY' if args.analytic_only else 'PASS_COMPLETE_PROOF_PACKAGE',
            'scope':'Analytic checks only' if args.analytic_only else
                    'All three exact finite ranges, last failures, strict positivity, equality lists, independently checked closed arc partitions, and effective infinite-tail joins.',
            'manifest_sha256':manifest,'manifest_input_count':count,
            'finite_cache_directories_present_at_start':initial_caches,
            'python':sys.version,'platform':platform.platform(),'stages':stages,
            'seconds':round(time.monotonic()-started,3),
            'verification_boundary':'Computer-assisted arithmetic and internal mathematical review; not proof-assistant formalization or external human peer review.'}
    (ROOT/'output').mkdir(exist_ok=True)
    (ROOT/'output/verification_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('\n'+report['status'],flush=True)
    print(json.dumps({'seconds':report['seconds'],'scope':report['scope']},indent=2),flush=True)


if __name__=='__main__':
    main()
