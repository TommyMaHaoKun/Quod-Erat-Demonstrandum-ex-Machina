"""Exact edge-fusion square recurrence; standalone standard-library validation.

The construction here is ABSTRACT. A graph is extended along an existing edge
uv by adding new vertices a,b and edges ua,ab,bv. No other identifications are
made. This code does not certify that arbitrary words are geometric chains.
"""
from fractions import Fraction as F
from itertools import product
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    N: int
    r: F
    T: F
    D: F
    Q: F
    K: F


INITIAL = State(4, F(3,4), F(5), F(0), F(5,4), F(5))


def extend(s, c=0):
    """c=-1,0,1 chooses oriented exit ua,ab,bv, respectively."""
    assert c in (-1, 0, 1)
    N,r,T,D,Q,K = s.N,s.r,s.T,s.D,s.Q,s.K
    h = r+3
    A = N-r-1
    rr = (r+2)/h
    DD = (D+2*A*c)/h
    QQ = (Q+4*c*D+4*A*c*c+2*(r+2)**2)/h**2
    TT = T + (-(Q+N*r*r)/2+4*N+2*r+4-2*c*D-2*A*c*c)/h
    KK = K+T - ((N+2)*Q-D*D+2*N*r*r-16*N-4*r-8)/(4*h)
    return State(N+2,rr,TT,DD,QQ,KK)


def attach(edges, boundary, c):
    u,v = boundary
    a = 1+max(max(e) for e in edges)
    b = a+1
    return edges+[(u,a),(a,b),(b,v)], ((u,a),(a,b),(b,v))[c+1]


def inverse(matrix):
    """Gauss-Jordan over fractions, with no numerical approximation."""
    n = len(matrix)
    a = [[F(x) for x in row]+[F(i==j) for j in range(n)]
         for i,row in enumerate(matrix)]
    for k in range(n):
        pivot = next(i for i in range(k,n) if a[i][k])
        a[k],a[pivot] = a[pivot],a[k]
        factor = a[k][k]
        a[k] = [x/factor for x in a[k]]
        for i in range(n):
            if i != k and a[i][k]:
                factor = a[i][k]
                a[i] = [x-factor*y for x,y in zip(a[i],a[k])]
    return [row[n:] for row in a]


def from_graph(edges, boundary):
    N = 1+max(max(e) for e in edges)
    lap = [[0]*N for _ in range(N)]
    for u,v in edges:
        lap[u][u] += 1; lap[v][v] += 1
        lap[u][v] -= 1; lap[v][u] -= 1
    inv = inverse([row[:-1] for row in lap[:-1]])
    inv = [row+[F(0)] for row in inv]+[[F(0)]*N]
    R = [[inv[i][i]+inv[j][j]-2*inv[i][j] for j in range(N)]
         for i in range(N)]
    u,v = boundary
    d = [R[x][u]-R[x][v] for x in range(N)]
    return State(N,R[u][v],sum(R[x][u]+R[x][v] for x in range(N)),
                 sum(d),sum(z*z for z in d),
                 sum(R[i][j] for i in range(N) for j in range(i)))


def validate(max_cells=5):
    start_edges = [(0,1),(1,2),(2,3),(3,0)]
    assert from_graph(start_edges,(0,1)) == INITIAL
    count = 1
    for length in range(1,max_cells):
        for word in product((-1,0,1),repeat=length):
            edges,boundary,s = start_edges,(0,1),INITIAL
            for c in word:
                edges,boundary = attach(edges,boundary,c)
                s = extend(s,c)
            assert s == from_graph(edges,boundary), (word,s,from_graph(edges,boundary))
            count += 1
    print(f'Exact full-state validations: {count}; cells <= {max_cells}.')
    print('C4:', INITIAL.K)
    print('Domino:', extend(INITIAL).K)
    print('Straight triomino:', extend(extend(INITIAL,0),0).K)
    print('L triomino:', extend(extend(INITIAL,-1),0).K)


def symbolic_objective(n):
    """Optional SymPy display of the exact quadratic turn polynomial."""
    import sympy as sp
    c = sp.symbols(f'c0:{max(0,n-2)}')
    s = INITIAL
    for i in range(n-1):
        # Symbolic analogue of extend; its final exit never affects K.
        choice = c[i] if i < len(c) else 0
        N,r,T,D,Q,K = s.N,s.r,s.T,s.D,s.Q,s.K
        h,A = r+3,N-r-1
        s = State(N+2,(r+2)/h,
            sp.expand(T+(-(Q+N*r*r)/2+4*N+2*r+4-2*choice*D-2*A*choice**2)/h),
            sp.expand((D+2*A*choice)/h),
            sp.expand((Q+4*choice*D+4*A*choice**2+2*(r+2)**2)/h**2),
            sp.expand(K+T-((N+2)*Q-D**2+2*N*r*r-16*N-4*r-8)/(4*h)))
    return c,sp.factor(s.K),sp.Poly(s.K,*c) if c else s.K


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-cells',type=int,default=5)
    parser.add_argument('--symbolic',type=int,default=0)
    args=parser.parse_args()
    validate(args.max_cells)
    if args.symbolic:
        c,p,_=symbolic_objective(args.symbolic)
        print('Turn variables:',c)
        print('K:',p)
