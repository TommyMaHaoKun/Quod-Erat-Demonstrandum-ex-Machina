"""Independent algebra check of the final harmonic WZ pair, no Gamma differentiation."""
from fractions import Fraction
from functools import lru_cache
from math import factorial
import sympy as s
n,k=s.symbols('n k', integer=True, nonnegative=True)
R=(2*k**3+13*k**2*n+11*k**2+28*k*n**2+48*k*n+20*k+21*n**3+55*n**2+47*n+13)/(2*(2*n+1)*(k+2*n+2)**2)
S=(k+n+1)*(32*k**5+328*k**4*n+284*k**4+1328*k**3*n**2+2316*k**3*n+996*k**3+2646*k**2*n**3+6961*k**2*n**2+6036*k**2*n+1721*k**2+2574*k*n**4+9063*k*n**3+11855*k*n**2+6817*k*n+1451*k+972*n**5+4290*n**4+7512*n**3+6516*n**2+2796*n+474)/(6*(2*n+1)**2*(k+2*n+2)**3*(2*k+3*n+2)*(2*k+3*n+3))
rn=(n+1)**4*(n+k+1)**2/((2*n+1)*(2*n+2)*(2*n+k+2)**2*(2*n+k+3)**2)
rk=(n+k+1)**2/(2*n+k+2)**2
# Derive harmonic increments from their affine indices, independently of the printed u,v.
harmonic_specs = [
    (s.Rational(-5,3),1,0,0), (s.Rational(4,3),2,0,0),
    (s.Rational(2,3),1,1,0), (s.Rational(-4,3),2,1,1),
    (s.Integer(1),3,2,1), (s.Integer(1),3,2,2),
]
Dn=sum(c*sum(1/(an*n+ak*k+b+j) for j in range(1,an+1))
       for c,an,ak,b in harmonic_specs)
Dk=sum(c*sum(1/(an*n+ak*k+b+j) for j in range(1,ak+1))
       for c,an,ak,b in harmonic_specs)
checks={
 'coefficient_of_harmonics':s.factor(rn-1-rk*R.subs(k,k+1)+R),
 'rational_constant':s.factor(rn*Dn-rk*(R.subs(k,k+1)*Dk+S.subs(k,k+1))+S),
}
for name,value in checks.items():
 if value!=0: raise AssertionError((name,value))
 print(name,': exact zero')
# Compare the accelerated boundary with the requested summand using formal H_{m-1}, H_{2m-1}, H_{3m-1}.
m=s.symbols('m',integer=True,positive=True)
h1,h2,h3=s.symbols('h1 h2 h3')
L0=-s.Rational(5,3)*h1+s.Rational(4,3)*(h2-1/(2*m-1))+s.Rational(2,3)*h1-s.Rational(4,3)*h2+(h3-1/(3*m-1))+h3
# Base kernel F0(m-1,0)=8*(2m-1)/(m^3 C(2m,m)^3).
B=(21*m-8)*(2*h3-h1)-4*(27*m-11)/(3*(3*m-1))
boundary=s.factor(8*(2*m-1)*(R.subs({n:m-1,k:0})*L0+S.subs({n:m-1,k:0}))-B)
if boundary!=0: raise AssertionError(boundary)
print('target_boundary: exact zero')



# A separate standard-library implementation evaluates actual harmonic numbers,
# factorials, and the printed rational functions, without symbolic substitution.
@lru_cache(None)
def harmonic(j):
    return sum((Fraction(1,i) for i in range(1,j+1)), Fraction())

@lru_cache(None)
def rational_pair(a,b):
    kernel=Fraction(factorial(a)**4*factorial(a+b)**2,
                    factorial(2*a)*factorial(2*a+b+1)**2)
    ell=(Fraction(-5,3)*harmonic(a)+Fraction(4,3)*harmonic(2*a)
         +Fraction(2,3)*harmonic(a+b)-Fraction(4,3)*harmonic(2*a+b+1)
         +harmonic(3*a+2*b+1)+harmonic(3*a+2*b+2))
    p=(2*b**3+(13*a+11)*b**2+(28*a*a+48*a+20)*b
       +21*a**3+55*a*a+47*a+13)
    q=(32*b**5+(328*a+284)*b**4
       +(1328*a*a+2316*a+996)*b**3
       +(2646*a**3+6961*a*a+6036*a+1721)*b*b
       +(2574*a**4+9063*a**3+11855*a*a+6817*a+1451)*b
       +972*a**5+4290*a**4+7512*a**3+6516*a*a+2796*a+474)
    rr=Fraction(p,2*(2*a+1)*(b+2*a+2)**2)
    ss=Fraction((a+b+1)*q,
                6*(2*a+1)**2*(b+2*a+2)**3*(2*b+3*a+2)*(2*b+3*a+3))
    return kernel*ell, kernel*(rr*ell+ss)

for a in range(8):
    for b in range(8):
        local=(rational_pair(a+1,b)[0]-rational_pair(a,b)[0]
               -rational_pair(a,b+1)[1]+rational_pair(a,b)[1])
        if local: raise AssertionError(('local harmonic WZ',a,b,local))
print('64 exact local harmonic-pair checks: passed')

for top in range(8):
    for right in range(8):
        horizontal=sum((rational_pair(top+1,b)[0]-rational_pair(0,b)[0]
                        for b in range(right+1)),Fraction())
        vertical=sum((rational_pair(a,right+1)[1]-rational_pair(a,0)[1]
                      for a in range(top+1)),Fraction())
        if horizontal!=vertical:
            raise AssertionError(('finite rectangle',top,right,horizontal-vertical))
print('64 exact finite telescoping rectangles: passed')
