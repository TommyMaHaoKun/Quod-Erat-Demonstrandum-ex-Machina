"""Complete structural classifier for every admissible pair. No state-search fallback."""
import json,argparse
from fractions import Fraction as Q
from pathlib import Path
from math import gcd
from seam_inventory import load_tables
from large_classification import classify as large
from near.uniform_classification import classify as near
DATA=Path(__file__).resolve().parents[1]/'certificates'

def classify(a,c):
    if not(a>=2 and c>4*a and gcd(a,c)==1):raise ValueError('inadmissible parameters')
    if c>6*a or a==2:return large(a,c)
    if 0<41*abs(c-5*a)<a:return near(a,c)
    base,r=divmod(c,a);t=Q(r,a)
    atlas,seams=load_tables(DATA)
    for z in seams:
        if(a,c)==(z['a'],z['c']):return dict(z,family='atlas_seam')
    for z in atlas:
        if z['base']==base and Q(z['lo'])<t<Q(z['hi']):
            word=lambda w:''.join(str(v)*(b*a+g*r) for v,(b,g) in w)
            prefix,block=word(z['prefix']),word(z['period'])
            p=z['p'][0]*a+z['p'][1]*r;q=z['q'][0]*a+z['q'][1]*r
            assert(len(prefix),len(block))==(q,p)
            return dict(a=a,c=c,p=p,q=q,prefix=prefix,block=block,family='affine_atlas',interval=[z['lo'],z['hi']])
    raise AssertionError('Coverage invariant failed for an admissible pair')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('a',type=int);ap.add_argument('c',type=int);args=ap.parse_args()
    print(json.dumps(classify(args.a,args.c),indent=2))
