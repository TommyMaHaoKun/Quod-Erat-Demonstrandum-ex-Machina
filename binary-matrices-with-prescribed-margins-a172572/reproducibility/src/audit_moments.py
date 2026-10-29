"""Independent exact polynomial audit of the Hermite-moment proof.

This implementation does not import the symbolic moment-reduction code.
It constructs Hermite polynomials coefficient by coefficient and integrates
their products using the elementary Gaussian moments (2r-1)!!.
"""
from fractions import Fraction as Q
from math import comb, factorial


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def power(a, exponent):
    out = [1]
    for _ in range(exponent):
        out = mul(out, a)
    return out


def hermite(n):
    return [0 if (n-j) % 2 else
            (-1)**((n-j)//2) * factorial(n)
            // (factorial(j)*factorial((n-j)//2)*2**((n-j)//2))
            for j in range(n+1)]


def gaussian(poly):
    return sum(a*factorial(j)//(2**(j//2)*factorial(j//2))
               for j, a in enumerate(poly) if j % 2 == 0)


def moment(n, j, k):
    return gaussian([0]*j + mul(power(hermite(n), 6-k),
                               power(hermite(n-1), k)))


def f(n): return 102*n**4+204*n**3+145*n**2+43*n+5
def g(n): return 62*n**2+93*n+36
def h(n): return 62*n**2+31*n+5


def matrix(n):
    return [[Q(3*n*f(n), (n+1)*(2*n+1)),
             Q(-9*n**4*g(n), 2*(n+1)*(2*n+1)),
             Q(-5*n**6, 2*(n+1))],
            [Q(n*h(n), 2*n+1), Q(-60*n**4, 2*n+1), 0],
            [5*n, 0, 0]]


def normalized_b(n):
    return Q(factorial(2*n), factorial(n)**5)*gaussian(power(hermite(n), 6))


def auxiliary_c(n):
    return 5*n**3*Q(factorial(2*n), factorial(n)**5)*moment(n, 0, 4)


def numeric_audit():
    checked = 0
    for n in range(1, 7):
        v = [moment(n, 0, k) for k in (2, 4, 6)]
        actual_next = [moment(n+1, 0, k) for k in (2, 4, 6)]
        predicted = [sum(a*b for a,b in zip(row, v)) for row in matrix(n)]
        assert predicted == actual_next, (n, predicted, actual_next)
        assert moment(n, 0, 0) == 5*n*moment(n, 0, 2)
        for j in range(1, 7):
            for k in range(7):
                lhs = (k-1)*moment(n, j, k)
                rhs = (k*moment(n, j-1, k-1) if k else 0)
                rhs -= n*(6-k)*moment(n, j-1, k+1) if k < 6 else 0
                rhs -= (j-1)*moment(n, j-2, k) if j >= 2 else 0
                assert lhs == rhs, (n,j,k)
                checked += 1
        # Independently test the exceptional k=1 reduction, including odd j.
        for j in range(1, 7, 2):
            lhs = (j+1+4*n)*moment(n, j, 1)
            rhs = j*moment(n,j-1,0)+5*n*j*moment(n,j-1,2)+20*n*n*moment(n,j,3)
            assert lhs == rhs, (n,j)
        assert ((n+1)**4*normalized_b(n+1)
                == 6*f(n)*normalized_b(n)-9*n*g(n)*auxiliary_c(n)
                -50*n*n*(4*n*n-1)*normalized_b(n-1))
        assert ((n+1)*auxiliary_c(n+1)
                == 2*h(n)*normalized_b(n)-120*n*auxiliary_c(n))
    initial = [normalized_b(n) for n in range(4)]
    assert initial == [1,30,4530,1074900]
    print(f'PASS: {checked} exact integration-by-parts checks; six transfer '
          'matrices; exceptional reductions; both scalar equations; initial data.')


def symbolic_elimination_audit():
    # Independent coefficient-array arithmetic; no symbolic-algebra package.
    # Arrays are in increasing powers of the formal variable n.
    def add(*polys):
        ans = [0]*max(map(len, polys))
        for p in polys:
            for i, a in enumerate(p):
                ans[i] += a
        while len(ans)>1 and ans[-1] == 0:
            ans.pop()
        return ans

    def scale(c, p):
        return [c*a for a in p]

    def product(*polys):
        ans = [1]
        for p in polys:
            ans = mul(ans, p)
        return ans

    def shift(p, c):
        ans = [0]*len(p)
        for i, a in enumerate(p):
            for j in range(i+1):
                ans[j] += a*comb(i,j)*c**(i-j)
        return ans

    ff = [5,43,145,204,102]
    gg = [36,93,62]
    hh = [5,31,62]
    fp, gp = shift(ff,1), shift(gg,1)
    np1, np2 = [1,1], [2,1]
    # Coefficients after eliminating c_n,c_(n+1), multiplied by G(n).
    # The order is b(n-1),b(n),b(n+1),b(n+2).
    actual = [
        scale(6000, product([0,0,1],[-1,0,4],gp)),
        add(scale(18,product(gg,gp,hh)),
            scale(50,product(gg,power(np1,2),add(scale(4,power(np1,2)),[-1]))),
            scale(-720,product(gp,ff))),
        add(scale(-6,product(gg,fp)),scale(120,product(gp,power(np1,4)))),
        product(gg,power(np2,4))
    ]
    pp = [601185,1653960,1884032,1137319,383756,68634,5084]
    qq = [827860,2220988,2354425,1227805,313720,31372]
    # Published target with its index m replaced by n-1.
    target = [
        scale(6000,product([0,0,1],[-1,2],[1,2],shift([470,341,62],-1))),
        scale(-4,product([1,2],shift(qq,-1))),
        scale(-6,shift(pp,-1)),
        product(power(np2,4),shift([191,217,62],-1))
    ]
    for i, (a,b) in enumerate(zip(actual,target)):
        assert add(a,scale(-1,b)) == [0], (i,a,b)
    print('PASS: independent exact symbolic elimination equals the target '
          'recurrence coefficient by coefficient, with m=n-1.')


if __name__ == '__main__':
    numeric_audit()
    symbolic_elimination_audit()
