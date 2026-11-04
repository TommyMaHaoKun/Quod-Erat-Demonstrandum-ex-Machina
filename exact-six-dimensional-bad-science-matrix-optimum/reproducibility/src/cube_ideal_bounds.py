"""Exact squared centroid maxima over all Boolean-cube order ideals."""
import argparse
import json
from pathlib import Path
from time import monotonic

import numpy as np


def ideals(d):
    result=[0,1]
    for k in range(d):
        half=1<<k
        result=[lo | (hi<<half) for lo in result for hi in result if not hi & ~lo]
    return result


def enumerate_six():
    start=monotonic()
    smaller=ideals(5)
    assert len(smaller)==7581
    masks=np.array(smaller,dtype=np.uint64)
    cardinality=np.array([bin(x).count('1') for x in smaller],dtype=np.int64)
    coord_masks=[sum(1<<v for v in range(32) if v&(1<<j)) for j in range(5)]
    sums=np.array([[m-2*bin(x&cm).count('1') for cm in coord_masks]
                   for x,m in zip(smaller,cardinality)],dtype=np.int64)
    maxima=np.full(65,-1,dtype=np.int64)
    witnesses=[None]*65
    seen=0
    for index,lo in enumerate(smaller):
        choices=np.flatnonzero((masks & np.uint64((1<<32)-1-lo))==0)
        sizes=cardinality[index]+cardinality[choices]
        merged=sums[index]+sums[choices]
        values=np.sum(merged*merged,axis=1)+(cardinality[index]-cardinality[choices])**2
        seen+=len(choices)
        for m in np.unique(sizes):
            slots=np.flatnonzero(sizes==m)
            best=slots[int(np.argmax(values[slots]))]
            score=int(values[best])
            if score>maxima[m]:
                maxima[m]=score
                witnesses[m]=hex(lo | (smaller[int(choices[best])]<<32))
    assert seen==7828354
    assert list(maxima)==list(maxima[::-1])
    # L(m)=(2sqrt(3)-2)m+16-8sqrt(3)=a+b sqrt(3).
    # Exact comparisons L(m)^2 >= maxima[m], with a=16-2m,b=2m-8.
    checks=[]
    for m,score in enumerate(maxima[:33]):
        a,b=16-2*m,2*m-8
        u,v=a*a+3*b*b-int(score),2*a*b
        gap_positive=(u>=0 and (v>=0 or u*u>=3*v*v)) or (u<0 and v>0 and 3*v*v>=u*u)
        checks.append({'m':m,'max_squared_centroid':int(score),'witness_mask':witnesses[m],
                       'affine_bound_holds':bool(gap_positive),'gap':{'rational':u,'sqrt3':v}})
    return {'dimension':6,'ideals_dimension_five':len(smaller),'ideals_enumerated':seen,
            'maxima':list(map(int,maxima)),'checks':checks,'seconds':monotonic()-start}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('certificates/cube6_ideal_bounds.json'))
    args=parser.parse_args()
    report=enumerate_six()
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
