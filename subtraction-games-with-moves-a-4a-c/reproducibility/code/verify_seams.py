"""Independent finite-word verification; no call to the state solver."""
import json
from pathlib import Path
from math import gcd
from fractions import Fraction as Q
from seam_inventory import load_tables, validate_record

def verify(z):
    validate_record(z)
    a,c,p,q=[z[k]for k in('a','c','p','q')];H=z['prefix'];W=z['block']
    assert a>=2 and c>4*a and gcd(a,c)==1 and p>0 and q>0
    assert (len(H),len(W))==(q,p)
    assert H[-1]!=W[-1]
    for d in range(1,p):
        if p%d==0:assert any(W[i]!=W[i%d] for i in range(p))
    F=H+(W*((c+p+p-1)//p))
    assert len(F)>=q+c+p
    for n in range(q+c+p):
        opts={int(F[n-s])for s in(a,4*a,c)if s<=n}
        v=int(F[n]);assert v not in opts and all(i in opts for i in range(v)),(a,c,n)
    assert (z['state_first'],z['state_repeat'])==(q,q+p)
    assert F[q:q+c]==F[q+p:q+p+c]
    return dict(a=a,c=c,p=p,q=q,positions=q+c+p)

if __name__=='__main__':
    here=Path(__file__).resolve().parents[1]/'certificates'
    atlas,seams=load_tables(here)
    ans=[verify(z)for z in seams]
    (here/'seams_verified.json').write_text(json.dumps(ans,indent=2)+'\n')
    print('Verified',len(ans),'seams and',sum(z['positions']for z in ans),'recurrence positions.')
