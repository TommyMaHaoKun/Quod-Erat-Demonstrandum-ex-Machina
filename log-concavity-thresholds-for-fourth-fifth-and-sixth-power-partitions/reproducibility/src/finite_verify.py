"""Portable standard-library finite checker, requires no C# runtime.

It regenerates counts with Python arbitrary-precision integers, checks every
determinant sign, all equality indices and exact witnesses, and an independent
logarithmic-derivative recurrence prefix. The original k=6 range of 36 million
needs about 2 GB RAM; the enlarged 180 million range can require about 10 GB.
Prefer finite_fast_verify.py, which selects the bounded-memory disk checker
for the enlarged range. This Python alternative is not the executed full k=6
checker.
"""
import argparse
import gzip
import hashlib
import json
import time
from pathlib import Path
from finite_bounds import bound as storage_bound

def verify(path, prefix=2048):
    start=time.perf_counter()
    record=json.loads(path.read_text(encoding='utf-8'))
    if record['schema']!='power-partition-finite-v1':
        raise ValueError('Unknown certificate')
    k=record['k'];begin,end=record['determinant_range']
    if begin!=1 or record['coefficient_range']!=[0,end+1]:
        raise ArithmeticError('Coverage mismatch')
    if storage_bound(k,end+1)!=record['storage_bound']:
        raise ArithmeticError('Storage proof mismatch')
    payload=(path.parent/record['compressed_sign_file']).read_bytes()
    if hashlib.sha256(payload).hexdigest()!=record['compressed_sign_sha256']:
        raise ArithmeticError('Compressed sign digest mismatch')
    signs=gzip.decompress(payload)
    if len(signs)!=end or hashlib.sha256(signs).hexdigest()!=record['signs_sha256']:
        raise ArithmeticError('Sign digest mismatch')
    coins=[];j=1
    while j**k<=end+1:
        coins.append(j**k);j+=1
    counts=[1]+[0]*(end+1)
    for coin in reversed(coins):
        for n in range(coin,end+2):
            counts[n]+=counts[n-coin]
        print('independent coin',coin,'seconds',round(time.perf_counter()-start,3),flush=True)
    digest=hashlib.sha256()
    for value in counts:
        digest.update(value.to_bytes(16,'little'))
    if digest.hexdigest()!=record['coefficients_sha256']:
        raise ArithmeticError('Full coefficient digest mismatch')
    eq=[];negative_count=0;last_negative=None
    for n in range(1,end+1):
        d=counts[n]**2-counts[n-1]*counts[n+1]
        sign=(d>0)-(d<0)
        if sign%256!=signs[n-1]:
            raise ArithmeticError('Determinant sign mismatch at %d'%n)
        if sign<0:
            negative_count+=1;last_negative=n
        elif sign==0:
            eq.append(n)
    if eq!=record['equality_indices'] or negative_count!=record['negative_count'] or last_negative!=record['largest_negative_index']:
        raise ArithmeticError('Exception set mismatch')
    for n,value in record['boundary_coefficients'].items():
        if counts[int(n)]!=int(value):
            raise ArithmeticError('Coefficient witness mismatch')
    for n,value in record['boundary_determinants'].items():
        n=int(n)
        if counts[n]**2-counts[n-1]*counts[n+1]!=int(value):
            raise ArithmeticError('Determinant witness mismatch')
    prefix=min(prefix,end+1);divisor=[0]*(prefix+1)
    for coin in coins:
        for n in range(coin,prefix+1,coin):
            divisor[n]+=coin
    independent=[1]
    for n in range(1,prefix+1):
        numerator=sum(divisor[m]*independent[n-m] for m in range(1,n+1))
        quotient,remainder=divmod(numerator,n)
        if remainder or quotient!=counts[n]:
            raise ArithmeticError('Divisor recurrence mismatch')
        independent.append(quotient)
    report={'result':'PASS','k':k,'coefficient_range':[0,end+1],
            'determinant_range':[1,end],'independent_divisor_prefix':[0,prefix],
            'seconds':time.perf_counter()-start}
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate',type=Path)
    parser.add_argument('--prefix',type=int,default=2048)
    args=parser.parse_args()
    verify(args.certificate,args.prefix)
