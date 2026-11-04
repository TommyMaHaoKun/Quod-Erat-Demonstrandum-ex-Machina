"""Independent exact proof checks using only Python's standard library.

This enumerates small order ideals by increasing vertex insertion, not by
the nested-slice enumeration used in cube_ideal_bounds.py. All comparisons
and all matrix evaluations use integer or rational arithmetic.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
import sys
from pathlib import Path
from time import monotonic

EXPECTED = [0,6,20,38,64,86,116,150,192,214,244,278]


def verify():
    if sys.flags.optimize:
        raise RuntimeError('Run this exact verifier without Python optimization flags.')
    started=monotonic()
    predecessors=[sum(1 << (v ^ (1 << j)) for j in range(6) if v & (1 << j))
                  for v in range(64)]
    signs=[tuple(1-2*((v >> j)&1) for j in range(6)) for v in range(64)]
    maxima=[-1]*12
    counts=[0]*12
    witnesses=[None]*12

    def visit(mask,last,m,centroid):
        counts[m]+=1
        square=sum(value*value for value in centroid)
        if square>maxima[m]:
            maxima[m]=square
            witnesses[m]=hex(mask)
        if m==11:return
        for v in range(last+1,64):
            if predecessors[v] & mask == predecessors[v]:
                visit(mask | (1<<v),v,m+1,
                      tuple(x+y for x,y in zip(centroid,signs[v])))

    visit(0,-1,0,(0,)*6)
    assert maxima==EXPECTED,(maxima,EXPECTED)
    assert counts==[1,1,6,15,35,75,156,306,605,1110,2045,3512]
    for m in range(12):
        initial_sum=tuple(sum(signs[v][j] for v in range(m)) for j in range(6))
        assert sum(z*z for z in initial_sum)==maxima[m]

    # The upper majorant is L(m)=a+b sqrt(3), a=16-2m,b=2m-8.
    # sqrt(3) lies strictly between 5/3 and 7/4, by integer squaring.
    assert 25 < 27 and 48 < 49
    gaps=[]
    for m,square in enumerate(maxima):
        a,b=16-2*m,2*m-8
        u,v=a*a+3*b*b-square,2*a*b
        lower=Fraction(u)+v*(Fraction(5,3) if v>=0 else Fraction(7,4))
        assert lower>=0,(m,u,v)
        assert (lower>0 or v!=0)==(m not in (4,8))
        gaps.append({'m':m,'u':u,'v':v,'certified_lower':str(lower)})

    # For m >=12, antipodal-free orthogonality gives ||centroid||^2<=32m.
    # At12 the squared-majorant gap is448-256sqrt3>0; its derivative
    # is96(2-sqrt3)>0, and its second derivative is2(2sqrt3-2)^2>0.
    assert 448-256*Fraction(7,4)==0
    assert 2-Fraction(7,4)>0

    # Each row is integer_vector / sqrt(squared_denominator).
    rows=[((-1,0,1,-1,0,-1),4),((1,0,-1,1,0,-1),4),
          ((1,0,1,1,0,1),4),((1,-1,0,-1,0,0),3),
          ((-1,0,-1,-1,0,1),4),((1,1,0,-1,0,0),3)]
    assert all(sum(v*v for v in row)==denom for row,denom in rows)
    values=Counter()
    for vertex in product((-1,1),repeat=6):
        squared=max(Fraction(sum(a*x for a,x in zip(row,vertex))**2,denom)
                    for row,denom in rows)
        values[str(squared)]+=1
    assert values=={'3':32,'4':32},values
    return {'status':'PASS','method':'Independent increasing-vertex enumeration of every order ideal of size at most 11',
            'dimension':6,'ideal_counts_by_size':counts,'ideals_checked':sum(counts),
            'max_squared_centroids':maxima,'witness_masks':witnesses,
            'exact_majorant_comparisons':gaps,
            'large_cells':'Orthogonality bound 32m and positive increasing quadratic gap for m>=12',
            'matrix_row_squared_norms':[1]*6,'matrix_squared_sup_norm_counts':dict(values),
            'exact_optimum':'1 + sqrt(3)/2','seconds':monotonic()-started,
            'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=verify()
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
