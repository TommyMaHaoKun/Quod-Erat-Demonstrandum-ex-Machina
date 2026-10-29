"""Exact finite-domain inventory checks; infinite-case coverage is proved in the paper."""
from pathlib import Path
from fractions import Fraction as F
import json
from seam_inventory import load_tables, validate_inventory

DATA=Path(__file__).resolve().parents[1]/'certificates'

def main():
    rows,seams=load_tables(DATA)
    association=validate_inventory(rows,seams)
    for base,lo,hi in ((4,F(0),F(40,41)),(5,F(1,41),F(1))):
        rr=sorted((r for r in rows if r['base']==base),key=lambda r:F(r['lo']))
        assert F(rr[0]['lo'])==lo and F(rr[-1]['hi'])==hi
        for x,y in zip(rr,rr[1:]):assert F(x['hi'])==F(y['lo'])
        ends={F(r[z]) for r in rr for z in ('lo','hi') if 0<F(r[z])<1}
        assert ends=={F(r['t']) for r in seams if r['base']==base}
        assert all(tuple(r['p']) in ((5,0),(base+1,1)) for r in rr)
    for r in seams:
        assert r['p'] in (5,5*r['a'],r['c']+r['a'],r['c']+4*r['a'])
    out=dict(outer_cones=len(rows),outer_seams=len(seams),
             interval_partition=True,seam_inventory=association,all_outer_periods_in_proved_set=True,
             uniform_open_range='k>=41, 0<b<d, gcd(b,d)=1',
             uniform_integer_seams='d=1, a>=42',
             uncovered_admissible_parameters=0,
             proof='The paper coverage theorem proves the algebraic infinite-domain partition.')
    (DATA/'coverage_verified.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))

if __name__=='__main__':main()
