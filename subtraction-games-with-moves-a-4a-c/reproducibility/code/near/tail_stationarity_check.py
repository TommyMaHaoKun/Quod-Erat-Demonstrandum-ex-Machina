"""Finite local obligations proving every cyclic A/B word is a mex solution.

This is a proof checker for the universal local lemma, not an instance grid.
"""
from itertools import product
import json
from pathlib import Path
A='012';B='01012';count=0
for parts in product((A,B),repeat=4):
    word=''.join(parts);start=len(parts[0])+len(parts[1])
    for j in range(start,start+len(parts[2])):
        v=int(word[j]);opts={int(word[j-1]),int(word[j+1]),int(word[j-4])}
        assert v not in opts and all(x in opts for x in range(v)),(parts,j,v,opts)
        count+=1
assert count==64
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(
    contexts=16,positions=64,proved='Every bi-infinite concatenation of A=012 and B=01012 satisfies f(j)=mex(f(j-1),f(j+1),f(j-4)).'),indent=2)+'\n')
print('All 64 universal local obligations passed.')
