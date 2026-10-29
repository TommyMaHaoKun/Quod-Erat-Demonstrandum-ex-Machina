"""Complete exact arithmetic audit. Python 3.9+, standard library only.

Run from any working directory: python path/to/src/verify.py
No external CAS, floating point, network, or precomputed answers are needed.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import runpy
from counting import count_lattice, count_chamber, count_original, COEFFICIENTS, verify_geometry
from vertices import audit


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += x
    return trim(c)


def scale(a, x): return trim([x*t for t in a])


def mul(a, b):
    c = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    return trim(c)


def power(a, n):
    c = [1]
    for _ in range(n): c = mul(c, a)
    return c


def subst_power(a, k):
    c = [0] * ((len(a)-1)*k+1)
    for i, x in enumerate(a): c[i*k] = x
    return trim(c)


class Rat:
    def __init__(self, num, den=(1,)):
        self.num, self.den = trim(num), trim(den)
    def __add__(self, b):
        return Rat(add(mul(self.num,b.den),mul(b.num,self.den)),mul(self.den,b.den))
    def __mul__(self, b):
        return Rat(mul(self.num,b.num),mul(self.den,b.den))
    def times(self, x): return Rat(scale(self.num,x),self.den)
    def equals(self, b): return mul(self.num,b.den) == mul(b.num,self.den)


def rational_audit():
    z = [0,1]
    def P(k):
        t = [0]*k+[1]
        d = add([1],scale(t,-1))
        return (Rat(add([1],t),d),Rat(scale(t,2),power(d,2)),
                Rat(scale(mul(t,add([1],t)),2),power(d,3)))
    p, q = P(3), P(2)
    r2 = Rat([1,1],power([1,-1],3))
    r3 = Rat([1,4,1],power([1,-1],4))
    r4 = Rat([1,11,11,1],power([1,-1],5))
    derived = ((p[2]*q[0]+(p[1]*q[1]).times(2)+p[0]*q[2])*r2
              +(p[1]*q[0]+p[0]*q[1])*r3.times(2)+p[0]*q[0]*r4).times(3)+r4.times(-2)
    numerator = [1,13,59,212,471,753,882,753,471,212,59,13,1]
    denominator = mul(mul(power([1,-1],7),[1,1]),power([1,1,1],3))
    target = Rat(numerator,denominator)
    assert derived.equals(target), 'Chamber generating function identity'

    # Independent partial-fraction identity used in the paper.
    b = [Q(-2521,7776),Q(-737,432),Q(2687,216),Q(-2275,36),
         Q(325,2),Q(-1625,9),Q(650,9)]
    partial = Rat([0])
    polynomial_part = [0]
    for j, c in enumerate(b,1):
        partial = partial + Rat([c],power([1,-1],j))
        term = [1]
        for k in range(1,j): term = scale(mul(term,[k,1]),Q(1,k))
        polynomial_part = add(polynomial_part,scale(term,c))
    expected_p = [Q(c,7776) for c in [10745,33552,33936,23400,13650,4680,780]]
    assert polynomial_part == expected_p
    H = [-70,92,-52,86,86,-220,92,-70,56]
    partial = partial + Rat([Q(-3,32)],[1,1]) + Rat(scale(H,Q(1,243)),power([1,0,0,-1],3))
    assert partial.equals(target), 'Partial fractions'
    # Extract each residue of H/(243(1-z^3)^3) as a polynomial in k.
    expected_r = [[Q(-70,243),Q(-36,243),Q(6,243)],
                  [Q(26,243),Q(60,243),Q(6,243)],
                  [Q(44,243),Q(-24,243),Q(-12,243)]]
    for r in range(3):
        in_k = [0]
        for i in range(r,len(H),3):
            j = i//3
            in_k = add(in_k,scale(mul([1-j,1],[2-j,1]),Q(H[i],486)))
        in_n = [0]
        for j,c in enumerate(in_k):
            in_n = add(in_n,scale(power([Q(-r,3),Q(1,3)],j),c))
        assert in_n == expected_r[r]

    # Verify the six claimed polynomials by an identity of generating functions.
    # S_j(t)=sum m^j t^m=A_j(t)/(1-t)^(j+1).
    # Recurrence follows by t*d/dt; S_0 includes m=0.
    euler = [[1]]
    for j in range(6):
        a = euler[-1]
        deriv = [(i+1)*a[i+1] for i in range(len(a)-1)] or [0]
        euler.append(mul(z,add(mul([1,-1],deriv),scale(a,j+1))))
    common_numerator = [0]
    for r, coeffs in enumerate(COEFFICIENTS):
        one_residue = [0]
        for j,c in enumerate(coeffs):
            one_residue = add(one_residue,scale(mul(euler[j],power([1,-1],6-j)),c))
        common_numerator = add(common_numerator,[0]*r+subst_power(one_residue,6))
    assert Rat(common_numerator,power([1,0,0,0,0,0,-1],7)).equals(target)
    assert sum(numerator) == 3900
    assert sum(c*(-1)**i for i,c in enumerate(numerator)) == -12
    # Polynomial remainder modulo z^2+z+1 is the nonzero constant 12.
    rem = numerator[:]
    while len(rem)>2:
        c,k=rem[-1],len(rem)-3
        for j in range(3): rem[k+j] -= c
        rem=trim(rem)
    assert rem == [12]
    return {'chamber_rational_identity':True,'partial_fractions':True,
            'six_constituents_as_rational_identity':True,'minimal_period':6}


def main():
    root = Path(__file__).resolve().parents[1]
    structure = audit()
    algebra = rational_audit()
    verify_geometry()
    counts = []
    for n in range(42):
        m,r=divmod(n,6)
        predicted=sum(c*m**j for j,c in enumerate(COEFFICIENTS[r]))
        value=count_lattice(n)
        assert value == count_chamber(n) == predicted
        counts.append(value)
    saved=json.loads((root/'certificates/counts.json').read_text(encoding='utf-8'))
    assert saved['counts'] == counts and saved['n_min']==0 and saved['n_max']==41
    assert [count_original(n) for n in range(4)] == [1,16,105,496]
    runpy.run_path(str(root/'src/verify_source_index.py'),run_name='__main__')
    report={'status':'PASS','exact_arithmetic_only':True,'structure':structure,
            'algebra':algebra,'count_range':[0,41],
            'original_constraint_brute_force':[1,16,105,496]}
    print(json.dumps(report,indent=2))


if __name__ == '__main__': main()
