"""Independent algebra check of the final harmonic WZ pair, no Gamma differentiation."""
from pathlib import Path
import sympy as s
n,k=s.symbols('n k', integer=True, nonnegative=True)
R=(2*k**3+13*k**2*n+11*k**2+28*k*n**2+48*k*n+20*k+21*n**3+55*n**2+47*n+13)/(2*(2*n+1)*(k+2*n+2)**2)
S=(k+n+1)*(32*k**5+328*k**4*n+284*k**4+1328*k**3*n**2+2316*k**3*n+996*k**3+2646*k**2*n**3+6961*k**2*n**2+6036*k**2*n+1721*k**2+2574*k*n**4+9063*k*n**3+11855*k*n**2+6817*k*n+1451*k+972*n**5+4290*n**4+7512*n**3+6516*n**2+2796*n+474)/(6*(2*n+1)**2*(k+2*n+2)**3*(2*k+3*n+2)*(2*k+3*n+3))
rn=(n+1)**4*(n+k+1)**2/((2*n+1)*(2*n+2)*(2*n+k+2)**2*(2*n+k+3)**2)
rk=(n+k+1)**2/(2*n+k+2)**2
Dn=-s.Rational(5,3)/(n+1)+s.Rational(4,3)*(1/(2*n+1)+1/(2*n+2))+s.Rational(2,3)/(n+k+1)-s.Rational(4,3)*(1/(2*n+k+2)+1/(2*n+k+3))+sum(1/(3*n+2*k+j) for j in [2,3,4,3,4,5])
Dk=s.Rational(2,3)/(n+k+1)-s.Rational(4,3)/(2*n+k+2)+sum(1/(3*n+2*k+j) for j in [2,3,3,4])
checks={
 'coefficient_of_harmonics':s.factor(rn-1-rk*R.subs(k,k+1)+R),
 'rational_constant':s.factor(rn*Dn-rk*(R.subs(k,k+1)*Dk+S.subs(k,k+1))+S),
}
for name,value in checks.items():
 assert value==0,(name,value)
 print(name,': exact zero')
# Compare the accelerated boundary with the requested summand using formal H_{m-1}, H_{2m-1}, H_{3m-1}.
m=s.symbols('m',integer=True,positive=True)
h1,h2,h3=s.symbols('h1 h2 h3')
L0=-s.Rational(5,3)*h1+s.Rational(4,3)*(h2-1/(2*m-1))+s.Rational(2,3)*h1-s.Rational(4,3)*h2+(h3-1/(3*m-1))+h3
# Base kernel F0(m-1,0)=8*(2m-1)/(m^3 C(2m,m)^3).
B=(21*m-8)*(2*h3-h1)-4*(27*m-11)/(3*(3*m-1))
boundary=s.factor(8*(2*m-1)*(R.subs({n:m-1,k:0})*L0+S.subs({n:m-1,k:0}))-B)
assert boundary==0,boundary
print('target_boundary: exact zero')

