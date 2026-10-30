"""Independent exact transfer-matrix proof of the A172671 recurrence.

No data fitting is used. Run with Python and SymPy.
"""
from functools import lru_cache
from math import comb
import json
from pathlib import Path
import sympy as s

n = s.symbols('n')
even = (0, 2, 4, 6)

@lru_cache(None)
def reduce_moment(k, j):
    """Row representing E[x^k P_n^(6-j) (P_n')^j]."""
    if j < 0 or j > 6:
        return s.zeros(1, 4)
    if k == 0:
        return s.Matrix([[int(j == z) for z in even]])
    result = (6-j)*reduce_moment(k-1, j+1) + j*n*reduce_moment(k-1, j-1)
    if k >= 2:
        result += (k-1)*reduce_moment(k-2, j)
    return result.applyfunc(lambda x: s.expand(x/(j+1)))

def transfer():
    rows = []
    for j in even:
        row = s.zeros(1, 4)
        for ell in range(7-j):
            row += comb(6-j, ell)*reduce_moment(6-j-ell, ell)
        rows.append(row.applyfunc(lambda x: s.factor((n+1)**j*x)))
    return s.Matrix.vstack(*rows)

def target():
    p4 = 3*(n+3)*(n+4)**3*(3784*n**4+32164*n**3+100749*n**2+137862*n+69678)
    p3 = -(n+3)*(3799136*n**7+72183584*n**6+579689880*n**5+2548427912*n**4+6617561702*n**3+10141503096*n**2+8487349821*n+2991586122)
    p2 = -3*(10844944*n**8+222321352*n**7+1973930222*n**6+9916013134*n**5+30831383530*n**4+60768378830*n**3+74160044251*n**2+51243135187*n+15352797306)
    p1 = (n+2)*(29681696*n**7+504588832*n**6+3602458816*n**5+14001842392*n**4+32010306742*n**3+43078657918*n**2+31639900193*n+9799573455)
    p0 = 15435*(n+1)**3*(n+2)*(3784*n**4+47300*n**3+219945*n**2+450988*n+344237)
    return [p0,p1,p2,p3,p4]

def main():
    T = transfer()
    print('T(n) =')
    for row in T.tolist():
        print([str(x) for x in row])
    B = T/(n+1)**3
    product = s.eye(4)
    residual = s.zeros(1,4)
    for i,p in enumerate(target()):
        if i:
            product = (B.subs(n,n+i-1)*product).applyfunc(s.cancel)
        residual += p*product[0,:]
    residual = residual.applyfunc(s.cancel)
    assert residual == s.zeros(1,4), residual
    print('EXACT ALL-n TARGET ROW IDENTITY: PASS')
    vals = s.Matrix([1,0,0,0])
    initials=[]
    for i in range(8):
        initials.append(str(vals[0]))
        vals = B.subs(n,i)*vals
    print('b(0..7):', initials)
    root=Path(__file__).resolve().parents[1]
    (root/'certificates'/'transfer_matrix.json').write_text(json.dumps({'normalization':'T is the unnormalized moment transfer; B = T/(n+1)^3', 'transfer':[[str(x) for x in row] for row in T.tolist()], 'residual':[str(x) for x in residual], 'initials':initials},indent=2)+'\n')

if __name__ == '__main__':
    main()
