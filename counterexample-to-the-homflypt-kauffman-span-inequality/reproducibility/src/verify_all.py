"""Recompute the counterexample from its braid, using Python's standard library."""
from pathlib import Path
import hashlib
import json
import time
from independent_skein import braid, compute, homfly, kauffman

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def span(poly):
    powers = [i for i,j in poly]
    return max(powers)-min(powers)


def main():
    started = time.monotonic()
    fixtures = json.loads((ROOT/'certificates/published_polynomials.json').read_text())
    knot = next(row for row in fixtures['knots'] if row['name']=='12n_296')
    # Small known formulas exercise both signs and both smoothings.
    p,f = compute(2,[1,1,1])
    require(p=={(2,0):2,(4,0):-1,(2,2):1},'trefoil HOMFLY mismatch')
    require(span(f)==3,'trefoil Kauffman mismatch')
    base = compute(3,[1,-2,1,-2])
    require(base[0]=={(-2,0):1,(0,0):-1,(2,0):1,(0,2):-1},
            'figure-eight HOMFLY mismatch')
    require(span(base[1])==4,'figure-eight Kauffman mismatch')
    for strands,word in [(3,[1,-2,1,-2,1,-1]),(4,[1,-2,1,-2,3]),
                         (4,[1,-2,1,-2,-3]),(3,[-2,1,-2,1])]:
        require(compute(strands,word)==base,'braid or Markov invariance mismatch')
    require(compute(3,[1,2,1,-2,1])==compute(3,[2,1,2,-2,1]),
            'braid relation mismatch')
    homfly.cache_clear()
    kauffman.cache_clear()
    require(len(braid(knot['braid_strands'],knot['braid_word']))==1,
            'braid closure has more than one component')
    p,f = compute(knot['braid_strands'],knot['braid_word'])
    for label,poly in [('homfly',p),('kauffman',f)]:
        expected={(i,j):c for i,j,c in knot[label]}
        require(poly==expected,label+' polynomial differs from published coefficients')
        require(all(type(c) is int for c in poly.values()),'coefficient is not integral')
    require(span(p)==8 and span(f)==7,'span mismatch')
    report={'status':'PASS','knot':'12n_296','homfly_span':span(p),
            'kauffman_span':span(f),'homfly_states':homfly.cache_info().currsize,
            'kauffman_states':kauffman.cache_info().currsize,
            'seconds':time.monotonic()-started,
            'method':'Exact integer arithmetic; independently implemented port-pairing skein recursion from the explicit braid; full coefficient agreement with the published KnotInfo data.',
            'sha256':{str(path.relative_to(ROOT)).replace('\\','/'):
                      hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in [ROOT/'src/independent_skein.py',
                                   ROOT/'src/verify_all.py',
                                   ROOT/'certificates/published_polynomials.json']}}
    (ROOT/'output').mkdir(exist_ok=True)
    (ROOT/'output/verification_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
