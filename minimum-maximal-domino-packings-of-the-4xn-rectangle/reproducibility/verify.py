"""Small exact certificate verifier; Python 3.9+, standard library only.

No optimization oracle, symbolic algebra, or numerical approximation is used.
The potential is the explicit table in the paper. All graphs are regenerated.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

HOLES = (0, 1, 2, 4, 5, 8, 9, 10)
POTENTIAL = (
    (0,0,0,0,0,0,-1,0),
    (3,None,1,3,None,2,None,1),
    (3,2,None,3,2,2,2,None),
    (4,None,None,4,None,4,None,None),
    (3,2,3,None,None,2,2,2),
    (4,None,3,None,None,4,None,2),
    (4,3,None,None,None,3,2,None),
    (4,None,None,None,None,4,None,None),
    (3,2,3,1,1,None,None,None),
    (4,None,4,4,None,None,None,None),
    (4,4,None,3,2,None,None,None),
    (4,None,None,4,None,None,None,None),
    (4,4,4,None,None,None,None,None),
    (4,None,4,None,None,None,None,None),
    (4,4,None,None,None,None,None,None),
    (4,None,None,None,None,None,None,None),
)

def pop(x):
    return bin(x).count('1')

def closure(seeds, adjacency):
    seen=set(seeds); stack=list(seeds)
    while stack:
        for target in adjacency[stack.pop()]:
            if target not in seen:
                seen.add(target); stack.append(target)
    return seen

def count_formula(n):
    k,r=divmod(n,3)
    if r==0:
        return (None,7,10)[k] if k<3 else 8
    if r==1:
        return (1,100,663,1892,3652,5796)[k] if k<6 else 226*k*k+106*k-392
    return (6,51,124,178)[k] if k<4 else 50*k+24

def build_certificate():
    states=[(h,u) for h in range(16) for u in HOLES if not h&u]
    potential={s:POTENTIAL[s[0]][HOLES.index(s[1])] for s in states}
    assert all((POTENTIAL[h][a] is None)==bool(h&u)
               for h in range(16) for a,u in enumerate(HOLES))
    edges=[]
    for h,u in states:
        for k,v in states:
            if h&(k|v) or u&v: continue
            rem=15^(h|k|v)
            if rem not in (0,3,6,12,15): continue
            cost=pop(k)+pop(rem)//2
            defect=3*cost-4+potential[h,u]-potential[k,v]
            assert defect>=0
            edges.append(((h,u),(k,v),defect))
    assert (len(states),len(edges))==(60,304)
    histogram=[sum(d==k for s,t,d in edges) for k in range(5)]
    assert histogram==[111,99,59,20,15]
    start=(0,0)
    zero=defaultdict(list); reverse_zero=defaultdict(list)
    for s,t,d in edges:
        if d==0:zero[s].append(t);reverse_zero[t].append(s)
    bridge=closure([start],zero)&closure([(0,9)],reverse_zero)
    assert bridge=={(0,0),(0,9)}
    assert [(s,t) for s in sorted(bridge) for t in zero[s] if t in bridge]==[((0,0),(0,9))]
    cycles=[]; unseen=set(states)
    while unseen:
        s=min(unseen)
        component=closure([s],zero)&closure([s],reverse_zero)
        unseen-=component
        if len(component)>1 or s in zero[s]:
            assert len(component)==3
            assert all(sum(t in component for t in zero[x])==1 for x in component)
            cycle=[min(component)]
            cycle.append(next(t for t in zero[cycle[-1]] if t in component))
            cycle.append(next(t for t in zero[cycle[-1]] if t in component))
            assert cycle[0] in zero[cycle[-1]]
            cycles.append(cycle)
    assert len(cycles)==8
    adj=defaultdict(list); reverse=defaultdict(list)
    for s,t,d in edges:
        for b in range(4-d):
            source=(*s,b); target=(*t,b+d)
            adj[source].append(target); reverse[target].append(source)
    accepted={(h,u,b) for h,u in states if h==0 for b in range(4)
              if 0<=b+potential[h,u]<=2}
    initial=(0,0,0)
    active=closure([initial],adj)&closure(accepted,reverse)
    order=sorted(active,key=lambda x:(x[2],x[0],x[1]))
    index={s:i for i,s in enumerate(order)}
    arcs=[(index[s],index[t]) for s in order for t in adj[s] if t in active]
    finals=[index[s] for s in order if s in accepted]
    assert (len(order),len(arcs))==(114,327)
    # Cyclic-component structure: finite acyclic junctions between 3-cycles.
    components=[];unseen=set(active)
    while unseen:
        s=min(unseen)
        comp=closure([s],adj)&closure([s],reverse)&active
        unseen-=comp;components.append(comp)
    owner={s:i for i,comp in enumerate(components) for s in comp}
    cyclic={i for i,comp in enumerate(components) if len(comp)>1 or next(iter(comp)) in adj[next(iter(comp))]}
    assert len(cyclic)==16
    for i in cyclic:
        assert len(components[i])==3
        assert all(sum(t in components[i] for t in adj[s])==1 for s in components[i])
    dag=defaultdict(set)
    for s in active:
        for t in adj[s]:
            if t in active and owner[s]!=owner[t]:dag[owner[s]].add(owner[t])
    from functools import lru_cache
    @lru_cache(None)
    def most_cycles(i):
        return int(i in cyclic)+max((most_cycles(j) for j in dag[i]),default=0)
    assert most_cycles(owner[initial])==3
    vectors=[]; counts=[]
    current=[0]*len(order); current[index[initial]]=1
    for n in range(27):
        vectors.append(current); counts.append(sum(current[i] for i in finals))
        nxt=[0]*len(order)
        for i,j in arcs:nxt[j]+=current[i]
        current=nxt
    residual=[vectors[26][i]-3*vectors[23][i]+3*vectors[20][i]-vectors[17][i]
              for i in range(len(order))]
    assert residual==[0]*114
    assert counts[0]==1 and counts[1]==1
    assert all(counts[n]==count_formula(n) for n in range(1,27))
    # The proposed closed forms satisfy the same recurrence for all n>=26:
    # n-9>=17, and all four terms then belong to the same polynomial regime
    # (r=0: n>=9; r=1: n>=19; r=2: n>=14). At n=26,27 this is immediate;
    # at n=28 the earliest r=1 term is19. A third finite difference is zero.
    denominator={0:1,3:-3,6:3,9:-1}
    actual_counts=[0]+counts[1:]
    numerator=[sum(coef*actual_counts[n-j] for j,coef in denominator.items() if j<=n)
               for n in range(26)]
    return dict(states=[list(s) for s in states], potential=[potential[s] for s in states],
                state_count=60, transition_count=304, defect_histogram=histogram, zero_cycles=cycles,
                active_cyclic_components=16, maximum_cycles_on_path=3,
                active_states=order, active_edges=arcs, accepting_indices=finals,
                start_index=index[initial], active_count=114, active_edge_count=327,
                ceiling_counts_0_to_26=counts,
                vectors={str(n):vectors[n] for n in (17,20,23,26)},
                recurrence_residual=residual, numerator=numerator)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate',action='store_true')
    parser.add_argument('--independent',action='store_true',help='run graph recursion through40 and raw enumeration through9')
    args=parser.parse_args()
    cert=build_certificate()
    # Normalize tuples for exact comparison with JSON.
    cert=json.loads(json.dumps(cert))
    path=Path(__file__).with_name('certificate.json')
    if args.write_certificate:
        path.write_text(json.dumps(cert,indent=2)+'\n',encoding='utf-8')
    else:
        assert json.loads(path.read_text(encoding='utf-8'))==cert
    from structure_construction import construction, verify
    for n in range(1,201):verify(n,construction(n))
    if args.independent:
        from independent_check import rectangular_grid,minimum_maximal_matchings
        for raw,limit in ((False,40),(True,9)):
            for n in range(1,limit+1):
                m,a,_=minimum_maximal_matchings(rectangular_grid(4,n),memoize=not raw)
                assert m==(1 if n==1 else (4*n+2)//3)
                assert a==count_formula(n)
        print('Independent graph recursion: n=1..40; raw exhaustive enumeration: n=1..9: PASS')
    print('60 states; 304 transitions; nonnegative defects; 8 three-cycles: PASS')
    print('114 active states; 327 arcs; 114 exact recurrence identities: PASS')
    print('All initial values and certificate data: PASS')
    print('Explicit constructions at n=1..200: PASS')
    print('All-length bridge: vector identity persists under multiplication by the transition matrix.')

if __name__=='__main__':main()
