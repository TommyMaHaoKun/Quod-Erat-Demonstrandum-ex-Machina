"""Self-contained finite certificate printed in the paper; Python 3.9+."""
from fractions import Fraction as F

pairs = [(i, j) for i in range(4) for j in range(i, 4)]
def gram_rows(g):
    rows = [0] * 4
    for k, (i, j) in enumerate(pairs):
        if (g >> k) & 1:
            rows[i] |= 1 << (3-j)
            rows[j] |= 1 << (3-i)
    return rows

good = []
for g in range(1024):
    r = gram_rows(g)
    if r[0] > r[1] > r[2] > r[3]:
        good.append(g)
assert len(good) == 48

edges = [[] for _ in range(8)]
for s in range(8):
    for c in range(16):
        b = [(c >> (3-i)) & 1 for i in range(4)]
        if any(not ((s >> i) & 1) and b[i] > b[i+1]
               for i in range(3)):
            continue
        t = s
        for i in range(3):
            if b[i] < b[i+1]:
                t |= 1 << i
        h = sum((b[i]*b[j]) << k
                for k, (i, j) in enumerate(pairs))
        edges[s].append((t, h))

v = [[0]*1024 for _ in range(8)]
v[0][0] = 1
counts = []
for n in range(16):
    counts.append(sum(v[7][g] for g in good))
    w = [[0]*1024 for _ in range(8)]
    for s in range(8):
        for t, h in edges[s]:
            for g, value in enumerate(v[s]):
                w[t][g ^ h] += value
    v = w

def formula(n):
    return (F(4**n*(6*n*n-219*n+820), 6144)
            - F(2**n*(3*n+32), 288)
            - F(113*(-8)**n, 49152) + F(16**n, 512)
            - F((-4)**n*(13*n-164), 6144)
            + F(8**n*(288*n-3473), 147456))

assert counts == [0, 0, 0, 0, 58, 1629, 28924, 507052,
    8211776, 133693904, 2140571200, 34361115072,
    549587348992, 8798356254976, 140744002571264,
    2252082614856704]
assert all(counts[n] == (0 if n < 4 else formula(n))
           for n in range(16))
print('PASS: exact initial values n=0..15; 48 Gram patterns')
