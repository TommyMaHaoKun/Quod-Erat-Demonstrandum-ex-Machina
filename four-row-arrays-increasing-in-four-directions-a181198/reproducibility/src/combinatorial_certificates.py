"""Independent exact rational checks of the linear-moment IBP certificate."""
import sympy as s

n,t=s.symbols('n t')
D=3*(n+1)*(3*n+2)*(3*n+4)*(4*n+1)
alpha=2*n*(2*n+1)*(4*n+5)/(3*(3*n+2)*(3*n+4)*(4*n+1))
r0=-2*(2*n+1)*(4*n+5)/(3*(3*n+2)*(3*n+4)*(4*n+1))
r1=(11*n*n+26*n+14)/(3*(n+1)*(3*n+2)*(3*n+4))
r2=(2*n+1)/(3*(n+1)*(3*n+4))
r3=-1/(3*n+4)
R=(r0+r1*t+r2*t*t+r3*t**3)/(1+t)**2
L=t*(1-t*t)*s.diff(R,t)+(n-(2*n-1)*t-3*(n+1)*t*t)*R
assert s.cancel(L-t*(1-t)**2+alpha)==0
H=(2*n*(1-t)-4*t)/(1+t)-t*(1-t)/(1+t)**2
g=-(28*n*n+33*n+8)/D
d0=2*(20*n**3+11*n*n-11*n-5)/D
d1=-1/(3*n+4)
assert s.cancel(R-d0-d1*t-g*H)==0
beta=(4*n**4+33*n**3-17*n*n-60*n-20)/(3*(n+1)*(n+2)*(3*n+2)*(3*n+4)*(4*n+1))
assert s.cancel(d0+d1*n/(n+2)-beta)==0
r=n*(2*n+1)*(4*n+5)/(3*(2*n-1)*(3*n+2)*(3*n+4)*(4*n+1))
f=(2*n+1)*(28*n*n+26*n+1)/(3*(n+1)*(2*n-1)*(3*n+2)*(3*n+4)*(4*n+1))
assert s.cancel(alpha/(2*(2*n-1))-r)==0
assert s.cancel((1/(n+2)+beta)/(2*(2*n-1))-f)==0
assert s.Rational(1,4320)+r.subs(n,2)*s.Rational(1,280)==s.Rational(1,140)*f.subs(n,2)
print('All five rational identities and the n=2 moment check passed.')
