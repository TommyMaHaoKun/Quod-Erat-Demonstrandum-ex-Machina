"""Generate an independent integer recurrence near both ends of each cone."""
from pathlib import Path
from fractions import Fraction as Q
import json
from solver import primitive_period
here=Path(__file__).resolve().parents[1]/'certificates'
out=[]
for row in json.loads((here/'atlas.json').read_text()):
    l,h=Q(row['lo']),Q(row['hi'])
    for name,x,y in (('left',l,h),('right',h,l)):
        t=Q(17*x.numerator+y.numerator,17*x.denominator+y.denominator)
        assert l<t<h
        a,r=t.denominator,t.numerator;c=row['base']*a+r
        def expand(w):return bytes(v for v,(b,g) in w for _ in range(b*a+g*r))
        H,W=expand(row['prefix']),expand(row['period']);p,q=len(W),len(H)
        assert p==row['p'][0]*a+row['p'][1]*r and q==row['q'][0]*a+row['q'][1]*r
        N=q+c+p;g=bytearray()
        for n in range(N):
            opts={g[n-s] for s in(a,4*a,c) if s<=n}
            v=next(v for v in range(4) if v not in opts);g.append(v)
            assert v==(H[n] if n<q else W[(n-q)%p]),(a,c,n)
        assert primitive_period(W)==p and H[-1]!=W[-1]
        out.append(dict(base=row['base'],lo=row['lo'],hi=row['hi'],side=name,a=a,c=c,p=p,q=q,terms=N))
(here/'atlas_crosschecks.json').write_text(json.dumps(out,indent=2)+'\n')
assert len(out)==178 and sum(z['terms']for z in out)==15164928
print('All 178 integer comparisons passed; 15164928 recurrence terms.')
