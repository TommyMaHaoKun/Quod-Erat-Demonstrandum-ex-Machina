"""Exact geometric polyomino chain enumeration and grounded-Laplacian checks.

Requires python-flint (rational matrix inversion); networkx only for isomorphism.
Run from the project root: python src/exact_chains.py --max-n 10
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from time import perf_counter
from flint import fmpq_mat

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))

def vertices(c):
    x, y = c
    return {(x,y), (x+1,y), (x,y+1), (x+1,y+1)}

def canonical(cells):
    """D4 and translation quotient; cell ordering forgotten, hence reversal too."""
    forms = []
    for swap in (False, True):
        for sx in (-1, 1):
            for sy in (-1, 1):
                pts = [(sx*(y if swap else x), sy*(x if swap else y)) for x,y in cells]
                mx, my = min(x for x,y in pts), min(y for x,y in pts)
                forms.append(tuple(sorted((x-mx,y-my) for x,y in pts)))
    return min(forms)

def neighbors(c):
    return [(c[0]+dx,c[1]+dy) for dx,dy in DIRS]

def extensions(cells):
    occupied = set(cells)
    verts = set().union(*(vertices(c) for c in cells))
    ends = [c for c in cells if sum(t in occupied for t in neighbors(c)) <= 1]
    for end in ends:
        for new in neighbors(end):
            if new in occupied:
                continue
            if set(neighbors(new)) & occupied != {end}:
                continue
            shared = vertices(end) & vertices(new)
            if vertices(new) & verts != shared:
                continue
            yield canonical((*cells, new))

def graph(cells):
    verts = sorted(set().union(*(vertices(c) for c in cells)))
    ids = {v:i for i,v in enumerate(verts)}
    edges = set()
    for x,y in cells:
        cyc = [(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        for a,b in zip(cyc,cyc[1:]+cyc[:1]):
            edges.add(tuple(sorted((ids[a],ids[b]))))
    return verts, sorted(edges)

def kirchhoff(cells, pair_check=False):
    verts, edges = graph(cells)
    N = len(verts)
    assert N == 2*len(cells)+2 and len(edges) == 3*len(cells)+1
    A = [[0]*(N-1) for _ in range(N-1)]
    for u,v in edges:
        if u < N-1: A[u][u] += 1
        if v < N-1: A[v][v] += 1
        if max(u,v) < N-1:
            A[u][v] -= 1
            A[v][u] -= 1
    M = fmpq_mat(A).inv()
    K = N*sum(M[i,i] for i in range(N-1))-sum(M[i,j] for i in range(N-1) for j in range(N-1))
    if pair_check:
        # Ground pairs contribute diagonal entries; other pairs are dipole energies.
        pairs = sum(M[i,i] for i in range(N-1))
        pairs += sum(M[i,i]+M[j,j]-2*M[i,j] for i in range(N-1) for j in range(i+1,N-1))
        assert pairs == K
    return K

def path_order(cells):
    occupied = set(cells)
    start = min(c for c in cells if sum(t in occupied for t in neighbors(c)) <= 1)
    path = [start]
    while len(path) < len(cells):
        path.append(next(t for t in neighbors(path[-1]) if t in occupied and t not in path))
    return path

def turn_word(cells):
    p = path_order(cells)
    ds = [DIRS.index((b[0]-a[0],b[1]-a[1])) for a,b in zip(p,p[1:])]
    return ''.join({0:'S',1:'L',3:'R'}[(b-a)%4] for a,b in zip(ds,ds[1:]))

def graph_classes(shapes):
    import networkx as nx
    reps = []
    classes = []
    for s in shapes:
        vs, es = graph(s)
        G = nx.Graph()
        G.add_nodes_from(range(len(vs)))
        G.add_edges_from(es)
        for i,H in enumerate(reps):
            if nx.is_isomorphic(G,H):
                classes[i].append(s)
                break
        else:
            reps.append(G)
            classes.append([s])
    return classes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-n',type=int,default=10)
    ap.add_argument('--output',default='data/exhaustive_geometric.json')
    args = ap.parse_args()
    level = {((0,0),)}
    results = []
    for n in range(1,args.max_n+1):
        start = perf_counter()
        low = high = None
        minimizers = []
        for cells in sorted(level):
            K = kirchhoff(cells, pair_check=n<=5)
            if low is None or K < low:
                low, minimizers = K, [cells]
            elif K == low:
                minimizers.append(cells)
            if high is None or K > high:
                high = K
        item = dict(n=n,embeddings=len(level),minimum=str(low),maximum=str(high),
                    minimizers=minimizers,turn_words=[turn_word(s) for s in minimizers],
                    minimizing_graph_classes=len(graph_classes(minimizers)),seconds=round(perf_counter()-start,3))
        print(json.dumps(item),flush=True)
        results.append(item)
        out = Path(args.output)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(dict(arithmetic='exact rational FLINT',quotient='D4+translation; unlabelled cell sets',results=results),indent=2),encoding='utf-8')
        if n < args.max_n:
            level = {ext for cells in level for ext in extensions(cells)}

if __name__ == '__main__':
    main()
