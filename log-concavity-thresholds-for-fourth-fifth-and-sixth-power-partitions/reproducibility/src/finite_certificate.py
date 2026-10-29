"""Package exact finite reports and compact sign data; Python standard library."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from finite_bounds import bound as storage_bound

ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def tsv(path):
    return dict(line.split('\t',1) for line in path.read_text(encoding='utf-8-sig').splitlines())

def pack(directory):
    source=tsv(directory/'summary.tsv')
    check=tsv(directory/'independent_check.tsv')
    if check['result']!='PASS':
        raise ArithmeticError('Independent checker has not passed')
    k=int(source['k']); end=int(source['max_determinant_index'])
    sb=storage_bound(k,end+1)
    if not sb['fits_uint128']:
        raise ArithmeticError('A priori bound does not justify 128-bit coefficients')
    cache_record=None
    for name,file in [('coefficients','coefficients_u128le.bin'),('signs','signs_i8.bin')]:
        if name=='coefficients' and not (directory/file).exists():
            cache_record=json.loads((directory/'generator_coefficient_cache.json').read_text(encoding='utf-8-sig'))
            if (not cache_record['verified_before_removal'] or not cache_record['removed']
                or cache_record['size_bytes']!=16*(end+2)):
                raise ArithmeticError('Missing or inconsistent removed-cache evidence')
            actual=cache_record['sha256']
        else:
            actual=sha(directory/file)
        if actual!=source[name+'_sha256'] or actual!=check[name+'_sha256']:
            raise ArithmeticError(name+' digest mismatch')
    signs=(directory/'signs_i8.bin').read_bytes()
    if len(signs)!=end or any(s not in (0,1,255) for s in signs):
        raise ArithmeticError('Invalid sign stream')
    eq=[n for n,s in enumerate(signs,1) if s==0]
    negative_count=signs.count(255)
    last_negative=signs.rfind(bytes([255]))+1
    if (negative_count!=int(source['negative_count']) or len(eq)!=int(source['equality_count'])
        or last_negative!=int(source['largest_negative_index'])
        or (eq[-1] if eq else 0)!=int(source['largest_equality_index'])):
        raise ArithmeticError('Stream statistics differ')
    if eq and eq[-1]>=last_negative+1:
        raise ArithmeticError('Equality prevents the claimed strictly positive interval')
    compressed=directory.parent/('finite_k%d_%d_signs_i8.bin.gz'%(k,end))
    with compressed.open('wb') as output:
        with gzip.GzipFile(filename='',mode='wb',fileobj=output,mtime=0,compresslevel=9) as stream:
            stream.write(signs)
    record={
        'schema':'power-partition-finite-v1','k':k,
        'scope':'Finite exact result only. No infinite-tail claim is implied.',
        'coefficient_range':[0,end+1],'determinant_range':[1,end],
        'candidate_threshold':last_negative+1,
        'strictly_positive_interval':[last_negative+1,end],
        'negative_count':negative_count,'equality_count':len(eq),
        'largest_negative_index':last_negative,
        'largest_equality_index':eq[-1] if eq else None,
        'equality_indices':eq,
        'boundary_coefficients':{key[len('coefficient_'):]:value for key,value in source.items() if key.startswith('coefficient_')},
        'boundary_determinants':{key[len('determinant_'):]:value for key,value in source.items() if key.startswith('determinant_')},
        'storage_bound':sb,
        'coefficient_encoding':'16 bytes per p_k(n), unsigned little endian, n=0,...,end+1',
        'coefficients_sha256':source['coefficients_sha256'],
        'sign_encoding':'one signed byte per D_k(n), n=1,...,end: -1,0,+1',
        'signs_sha256':source['signs_sha256'],
        'compressed_sign_file':compressed.name,'compressed_sign_sha256':sha(compressed),
        'independent_verification':check,
        'removed_generator_cache':cache_record,
        'generator_implementation':'finite_disk.cs ascending two-64-bit limbs' if (directory/'disk_generate').exists() else 'finite_engine.cs ascending two-64-bit limbs',
        'source_sha256':{name:sha(ROOT/'src'/name) for name in ['finite_engine.cs','finite_checker.cs','finite_disk.cs','finite_inplace.cs','finite_migrate_inplace.py','finite_bounds.py','finite_certificate.py','finite_fast_verify.py','finite_verify.py']},
        'generation_seconds':source['elapsed_seconds'],
    }
    path=directory.parent/('finite_k%d_%d.json'%(k,end))
    path.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:record[key] for key in ['k','determinant_range','negative_count','equality_count','largest_negative_index','largest_equality_index','boundary_coefficients','boundary_determinants']},indent=2))
    return path

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('directories',nargs='+',type=Path)
    args=p.parse_args()
    for directory in args.directories:
        pack(directory)
