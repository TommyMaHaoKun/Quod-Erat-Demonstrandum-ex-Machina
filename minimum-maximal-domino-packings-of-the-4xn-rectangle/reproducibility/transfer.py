"""Exact column model for maximal domino packings on the four-row strip."""
from collections import defaultdict

FULL = 15

def independent(u):
    return not (u & (u << 1))

def vertical_pairs(mask):
    pairs = []
    while mask:
        bit = mask & -mask
        if not (mask & (bit << 1)):
            return None
        pairs.append((bit.bit_length()-1, bit.bit_length()))
        mask ^= bit | (bit << 1)
    return tuple(pairs)

STATES = tuple((h,u) for h in range(16) for u in range(16)
               if not (h & u) and independent(u))
INDEX = {s:i for i,s in enumerate(STATES)}
START = INDEX[(0,0)]
TERMINAL = tuple(i for i,(h,u) in enumerate(STATES) if h == 0)

def make_edges():
    edges = []
    for i,(h,p) in enumerate(STATES):
        for j,(k,u) in enumerate(STATES):
            if h & (k | u) or p & u:
                continue
            pairs = vertical_pairs(FULL ^ (h | k | u))
            if pairs is not None:
                edges.append((i,j,bin(k).count('1')+len(pairs)))
    return tuple(edges)

EDGES = make_edges()
OUT = tuple(tuple((j,c) for a,j,c in EDGES if a == i) for i in range(len(STATES)))

def minimum_table(nmax):
    cur = {START:(0,1)}
    result = []
    vectors = [cur]
    for n in range(1,nmax+1):
        nxt = {}
        for i,(v,a) in cur.items():
            for j,c in OUT[i]:
                w=v+c
                if j not in nxt or w<nxt[j][0]:
                    nxt[j]=(w,a)
                elif w==nxt[j][0]:
                    nxt[j]=(w,nxt[j][1]+a)
        best=min(nxt[j][0] for j in TERMINAL if j in nxt)
        count=sum(nxt[j][1] for j in TERMINAL if j in nxt and nxt[j][0]==best)
        result.append((n,best,count))
        cur=nxt
        vectors.append(cur)
    return result,vectors

if __name__=='__main__':
    import json
    print('states',len(STATES),'edges',len(EDGES))
    print(json.dumps(minimum_table(40)[0],indent=2))
