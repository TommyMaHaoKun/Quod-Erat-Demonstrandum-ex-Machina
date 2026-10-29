"""Independent final-shape enumeration audit and exact spectral cross-check.

Enumerates ALL connected free polyominoes first, then filters by final-plane
properties. This does not use the endpoint-extension method under audit.
Run: python src/enumeration_audit.py --max-n 8
"""
from __future__ import annotations
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import sympy as sp
import exact_chains as target
import recurrence_check as recurrence


def canon(squares):
    variants = []
    for reflected in (False, True):
        p = [(y,x) if reflected else (x,y) for x,y in squares]
        for _ in range(4):
            x0 = min(x for x,y in p)
            y0 = min(y for x,y in p)
            variants.append(tuple(sorted((x-x0,y-y0) for x,y in p)))
            p = [(-y,x) for x,y in p]
    return min(variants)


def corners(s):
    x,y = s
    return [(x,y),(x+1,y),(x+1,y+1),(x,y+1)]


def shape_graph(squares):
    G = nx.Graph()
    for s in squares:
        p = corners(s)
        G.add_edges_from((p[k],p[(k+1)%4]) for k in range(4))
    return G


def final_chain_test(squares):
    # The cell dual is computed pairwise from Manhattan distance, not growth.
    n = len(squares)
    cell_graph = nx.Graph()
    cell_graph.add_nodes_from(squares)
    cell_graph.add_edges_from((a,b) for a,b in itertools.combinations(squares,2)
                             if abs(a[0]-b[0])+abs(a[1]-b[1]) == 1)
    if not nx.is_tree(cell_graph) or max(dict(cell_graph.degree()).values()) > 2:
        return False
    incident = Counter(p for s in squares for p in corners(s))
    if max(incident.values()) > 3:
        return False
    G = shape_graph(squares)
    # For connected lattice edge unions, Euler counts all bounded faces.
    # Each chosen unit square is already one face. Equality excludes extras.
    return nx.is_biconnected(G) and G.number_of_edges()-G.number_of_nodes()+1 == n


def pseudo_k(squares):
    G = shape_graph(squares)
    vs = list(G)
    n = len(vs)
    L = sp.zeros(n)
    for i,u in enumerate(vs):
        L[i,i] = G.degree[u]
        for j,v in enumerate(vs):
            if G.has_edge(u,v):
                L[i,j] = -1
    J = sp.ones(n)/n
    plus = (L+J).inv()-J
    return n*sp.trace(plus)


def abstract_degree_test(n):
    count = 0
    invalid_embeddings = []
    embedded_shapes = set()
    for word in itertools.product((-1,0,1),repeat=max(0,n-2)):
        es,boundary = [(0,1),(1,2),(2,3),(3,0)],(0,1)
        for c in tuple(word)+(0,)*(n>1):
            es,boundary = recurrence.attach(es,boundary,c)
        degrees = Counter(v for e in es for v in e)
        admissible = all(a != b or a == 0 for a,b in zip(word,word[1:]))
        assert (max(degrees.values()) <= 4) == admissible, (n,word,degrees)
        count += admissible
        if admissible:
            cells = [(0,0)] if n == 1 else [(0,0),(1,0)]
            direction = 0
            for c in word:
                direction = (direction+c)%4
                dx,dy = ((1,0),(0,1),(-1,0),(0,-1))[direction]
                x,y = cells[-1]
                cells.append((x+dx,y+dy))
            if len(set(cells)) != n or not final_chain_test(cells):
                invalid_embeddings.append(list(word))
            else:
                embedded_shapes.add(canon(cells))
    return count,invalid_embeddings,embedded_shapes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-n',type=int,default=8)
    ap.add_argument('--output',default='data/enumeration_independent_audit.json')
    args = ap.parse_args()
    all_shapes = {((0,0),)}
    target_shapes = {((0,0),)}
    rows = []
    for n in range(1,args.max_n+1):
        filtered = {s for s in all_shapes if final_chain_test(s)}
        assert filtered == target_shapes, (n,filtered-target_shapes,target_shapes-filtered)
        for shape in all_shapes:
            assert canon(shape) == target.canonical(shape)
            for dx,dy in ((3,-2),(-8,7)):
                translated = [(x+dx,y+dy) for x,y in shape]
                assert canon(translated) == target.canonical(translated) == shape
        exact_checks = 0
        if n <= 5:
            for shape in filtered:
                assert str(pseudo_k(shape)) == str(target.kirchhoff(shape)), shape
                exact_checks += 1
        abstract_count,bad_words,embedded_shapes = abstract_degree_test(n)
        assert embedded_shapes == filtered
        row = dict(n=n,all_free_polyominoes=len(all_shapes),geometric_chains=len(filtered),
                   exact_pseudoinverse_checks=exact_checks,
                   admissible_oriented_abstract_words=abstract_count,
                   geometrically_invalid_abstract_words=bad_words)
        print(json.dumps(row),flush=True)
        rows.append(row)
        if n < args.max_n:
            grown = set()
            for shape in all_shapes:
                used = set(shape)
                for x,y in shape:
                    for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                        if q not in used:
                            grown.add(canon((*shape,q)))
            all_shapes = grown
            target_shapes = {t for s in target_shapes for t in target.extensions(s)}
    out = Path(args.output)
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(dict(status='passed',results=rows),indent=2),encoding='utf-8')


if __name__ == '__main__':
    main()
