"""Rebuild and run the bounded-memory exact checker from a compact certificate.

Windows: uses the installed .NET Framework C# compiler. Only Python's standard
library is required. The C# source is compiled freshly, rather than trusting a
packaged executable. The large coefficient arrays are regenerated locally.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from finite_bounds import bound as storage_bound

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate',type=Path)
    parser.add_argument('--disk',action='store_true')
    args=parser.parse_args()
    path=args.certificate.resolve()
    record=json.loads(path.read_text(encoding='utf-8'))
    if record['schema']!='power-partition-finite-v1':
        raise ValueError('Unknown certificate schema')
    k=record['k'];start,end=record['determinant_range']
    if start!=1 or record['coefficient_range']!=[0,end+1]:
        raise ArithmeticError('Coverage mismatch')
    if storage_bound(k,end+1)!=record['storage_bound'] or not record['storage_bound']['fits_uint128']:
        raise ArithmeticError('A priori exact size bound failed')
    directory=path.parent/('finite_k%d_%d'%(k,end))
    directory.mkdir(exist_ok=True)
    compressed=path.parent/record['compressed_sign_file']
    if hashlib.sha256(compressed.read_bytes()).hexdigest()!=record['compressed_sign_sha256']:
        raise ArithmeticError('Compressed sign digest mismatch')
    digest=hashlib.sha256();count=0;equalities=[];negative_count=0;last_negative=0
    with gzip.open(compressed,'rb') as inp, (directory/'signs_i8.bin').open('wb') as out:
        for data in iter(lambda:inp.read(4*1024*1024),b''):
            if any(s not in (0,1,255) for s in data):
                raise ArithmeticError('Invalid sign encoding')
            equalities.extend(count+i+1 for i,s in enumerate(data) if s==0)
            negative_count+=data.count(255)
            last=data.rfind(bytes([255]))
            if last>=0:
                last_negative=count+last+1
            digest.update(data);count+=len(data);out.write(data)
    if count!=end or digest.hexdigest()!=record['signs_sha256']:
        raise ArithmeticError('Decompressed sign digest mismatch')
    if equalities!=record['equality_indices'] or negative_count!=record['negative_count'] or last_negative!=record['largest_negative_index']:
        raise ArithmeticError('Exact exception-set mismatch')
    source={
        'k':k,'max_determinant_index':end,'max_coefficient_index':end+1,
        'negative_count':record['negative_count'],'equality_count':record['equality_count'],
        'largest_negative_index':record['largest_negative_index'],
        'largest_equality_index':record['largest_equality_index'] or 0,
        'coefficients_sha256':record['coefficients_sha256'],
        'signs_sha256':record['signs_sha256'],
    }
    source.update({'coefficient_'+n:v for n,v in record['boundary_coefficients'].items()})
    source.update({'determinant_'+n:v for n,v in record['boundary_determinants'].items()})
    summary=''.join('%s\t%s\n'%(key,value) for key,value in source.items())
    # Preserve the original generator timing; the verification metadata do not
    # modify an existing summary that already has identical substantive fields.
    summary_path=directory/'summary.tsv'
    if summary_path.exists():
        existing=dict(line.split('\t',1) for line in summary_path.read_text(encoding='utf-8-sig').splitlines())
        if any(existing.get(key)!=str(value) for key,value in source.items()):
            raise ArithmeticError('Existing summary disagrees with the requested certificate')
    else:
        summary_path.write_text(summary,encoding='utf-8')
    compiler=Path(os.environ.get('WINDIR','C:/Windows'))/'Microsoft.NET'/'Framework64'/'v4.0.30319'/'csc.exe'
    if not compiler.exists():
        raise SystemExit('The fast route requires a C# compiler. Use finite_verify.py for the portable Python arbitrary-precision route.')
    disk=args.disk or end>100000000
    names=['finite_inplace','finite_disk'] if disk else ['finite_checker']
    for name in names:
        executable=ROOT/'src'/(name+'.exe')
        subprocess.run([str(compiler),'/nologo','/optimize+','/checked-','/platform:x64','/r:System.Numerics.dll','/out:'+str(executable),str(ROOT/'src'/(name+'.cs'))],check=True)
    if disk:
        subprocess.run([str(ROOT/'src'/'finite_inplace.exe'),str(k),str(end),str(directory)],check=True)
    executable=ROOT/'src'/('finite_disk.exe' if disk else 'finite_checker.exe')
    command=[str(executable)]+(['verify',str(k),str(end),str(directory)] if disk else [str(directory)])
    subprocess.run(command,check=True)
    print('PASS: exact exception set, a priori storage bound, independently regenerated coefficients, all determinant signs, witnesses and divisor recurrence prefix.')

if __name__=='__main__':
    main()
