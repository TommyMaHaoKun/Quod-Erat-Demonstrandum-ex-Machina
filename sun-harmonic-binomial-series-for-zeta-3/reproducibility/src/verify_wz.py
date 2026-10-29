"""Exact verification of the harmonic WZ pair (no numerical assumptions)."""
from pathlib import Path
import sympy as s
n,k=s.symbols('n k', nonnegative=True)
R=(2*k**3+13*k**2*n+11*k**2+28*k*n**2+48*k*n+20*k+21*n**3+55*n**2+47*n+13)/(2*(2*n+1)*(k+2*n+2)**2)
Q=(32*k**5+328*k**4*n+284*k**4+1328*k**3*n**2+2316*k**3*n+996*k**3+2646*k**2*n**3+6961*k**2*n**2+6036*k**2*n+1721*k**2+2574*k*n**4+9063*k*n**3+11855*k*n**2+6817*k*n+1451*k+972*n**5+4290*n**4+7512*n**3+6516*n**2+2796*n+474)
S=(k+n+1)*Q/(6*(2*n+1)**2*(k+2*n+2)**3*(2*k+3*n+2)*(2*k+3*n+3))
a=(n+1)**4*(n+k+1)**2/((2*n+1)*(2*n+2)*(2*n+k+2)**2*(2*n+k+3)**2)
b=(n+k+1)**2/(2*n+k+2)**2
third=s.Rational(1,3)
dn=-5*third/(n+1)+4*third*(1/(2*n+1)+1/(2*n+2))+2*third/(n+k+1)-4*third*(1/(2*n+k+2)+1/(2*n+k+3))+sum(1/(3*n+2*k+j) for j in (2,3,4))+sum(1/(3*n+2*k+j) for j in (3,4,5))
dk=2*third/(n+k+1)-4*third/(2*n+k+2)+sum(1/(3*n+2*k+j) for j in (2,3))+sum(1/(3*n+2*k+j) for j in (3,4))
coefficient=s.factor(a-1-b*R.subs(k,k+1)+R)
constant=s.factor(a*dn-b*R.subs(k,k+1)*dk-b*S.subs(k,k+1)+S)
assert coefficient==constant==0
# At k=0 the harmonic terms reduce to 2H_{3n+2}-H_n
# after multiplication by R plus S. Exact rational correction:
r0=R.subs(k,0); s0=S.subs(k,0)
# L(n,0)=2H_{3n+2}-H_n -4/[3(2n+1)]-1/(3n+2)
# The target is multiplied by F(n,0)*R(n,0) = (21n+13)/[(n+1)^3 C(2n+2,n+1)^3].
corr=-4*third/(2*n+1)-1/(3*n+2)+s0/r0
expected=-4*(27*n+16)/(3*(3*n+2)*(21*n+13))
assert s.factor(corr-expected)==0
print('Exact harmonic WZ identity: PASS')
print('Exact target boundary correction: PASS')
(Path(__file__).resolve().parents[1]/'certificates'/'wz_verification.txt').write_text('Exact rational coefficient identity: 0\nExact rational constant identity: 0\nExact target correction residual: 0\n')
