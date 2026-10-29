"""Exact rational certificate checks for the all-n proof of A181198.

Requires SymPy. Every check is an identity in Q(n,t), not a finite-n test.
"""
import sympy as s

n,t,z = s.symbols('n t z')

def zero(expr, label):
    numerator = s.cancel(expr).as_numer_denom()[0]
    assert numerator == 0, (label, s.factor(numerator))
    print('PASS:',label)

# W satisfies z(1+z)W''+(n+1+2z)W'-(n-2)(n-1)W=0.
L=(n-2)*(n-1)
Pw=(n+1+2*z)/(z*(1+z))
Qw=L/(z*(1+z))
f0=(n-2*L*z)/(2*n-1)
f1=z*(2*n+1+2*z)/(2*n-1)
f2=2*z*z*(1+z)/(2*n-1)
zero(s.diff(f0,z)+Qw*f1-z*Qw,'F derivative: W squared coefficient')
zero(2*f0+s.diff(f1,z)-Pw*f1+2*Qw*f2-(1-z*Pw),'F derivative: W Wprime coefficient')
zero(f1+s.diff(f2,z)-2*Pw*f2+z,'F derivative: Wprime squared coefficient')

# Y'=C/P-RY/P. Constants C=1/(n-1)! and w=t^(2n-1)(1-t)^3.
P=t*(1-t*t)
R=n+2*(n-2)*t+(n-2)*t*t
ell=(2*n-1)/t-3/(1-t)  # w'/w
A=n+3*(n-2)*t
B=t*(2*n+1+(2*n-7)*t)
D=2*t*t*(1-t)
Q2=A-B*R/P+D*R*R/P**2
Q1=B/P-2*D*R/P**2
Q0=D/P**2

h=2*t*(t-1)**2/((4*n-1)*(t+1)**2)
g=t*(16*n**3*t**2+32*n**3*t+16*n**3
     -24*n**2*t**2-32*n**2*t-40*n**2
     +8*n*t**2+2*n*t-14*n+3*t+3)/(n*(4*n-1)*(4*n+1)*(t+1)**2)
k=-t*(12*n**2*t**2+24*n**2*t-4*n**2
      +10*n*t**2+2*n*t-12*n-2*t**2-t+1)/(2*n*(4*n-1)*(4*n+1)*(t+1)**2)
r1=-8*(n-1)*(2*n-1)*(3*n+1)/((4*n-1)*(4*n+1))
r0=(n+1)*(2*n+3)*(6*n-1)/(n*(4*n-1)*(4*n+1))
zero(s.diff(h,t)+(ell-2*R/P)*h-Q2,'quadratic reduction')
zero(s.diff(g,t)+(ell-R/P)*g+r1-(Q1-2*h/P),'linear reduction')
zero(s.diff(k,t)+ell*k+r0-(Q0-g/P),'constant reduction')

# Moment telescoper. p below certifies t(1-t)^2 minus q.
F=(36*n**3*t**3-24*n**3*t**2-44*n**3*t+16*n**3
   +69*n**2*t**3-34*n**2*t**2-115*n**2*t+44*n**2
   +39*n*t**3-15*n*t**2-82*n*t+38*n
   +6*t**3-2*t**2-14*t+10)
p=t*(t-1)*F/(3*(n+1)*(3*n+2)*(3*n+4)*(4*n+1)*(t+1))
q=2*n*(2*n+1)*(4*n+5)/(3*(3*n+2)*(3*n+4)*(4*n+1))
v=-t*(t-1)*(36*n**3*t-20*n**3+69*n**2*t-109*n**2
            +39*n*t-109*n+6*t-26)/(6*(n+1)*(n+2)*(3*n+2)*(3*n+4)*(4*n+1)*(t+1))
r=(4*n**4+33*n**3-17*n**2-60*n-20)/(3*(n+1)*(n+2)*(3*n+2)*(3*n+4)*(4*n+1))
zero(s.diff(p,t)+(ell-R/P)*p-(t*(1-t)**2-q),'moment reduction')
zero(s.diff(v,t)+ell*v+r-p/P,'moment rational source')

# Normalized polynomial moment T=n! integral wY; Tnext+dT=e.
d=n*(n+1)*(2*n+1)*(4*n+5)/(3*(2*n-1)*(3*n+2)*(3*n+4)*(4*n+1))
e=(28*n*n+26*n+1)/(2*(n+1)*(2*n-1)*(2*n+3)*(3*n+2)*(3*n+4)*(4*n+1))
beta=3/(2*n*(n+1)*(2*n+1)*(2*n+3))
zero(d-(n+1)*q/(2*(2*n-1)),'moment homogeneous coefficient')
zero(e-n*(n+1)*beta*(1/(n+2)+r)/(2*(2*n-1)),'moment source coefficient')

U=-2*n*(3*n+1)/((2*n-1)*(4*n+1))
V=3*(6*n-1)/(8*(n-1)*(2*n-1)**2*(2*n+1)*(4*n+1))
An=3*(3*n+1)*(3*n+2)
Bn=(n+1)**2
Cn=3*(7*n*n-1)/(4*n*(n-1)*(2*n-1)**2*(2*n+1)**2)
zero(-An*U.subs(n,n+1)*d+Bn*U,'normalized target moment cancellation')
zero(An*(U.subs(n,n+1)*e+V.subs(n,n+1))+Bn*V-Cn,'normalized target source')

# Eliminate the hypergeometric source, then undo c_n normalization.
# c_n=(4n-1)/(n-1) * (n!)^4/(4n)! * a_n.
scale_ratio=(4*n+3)*(n-1)/(n*(4*n-1))*(n+1)**4/((4*n+1)*(4*n+2)*(4*n+3)*(4*n+4))
source_ratio=s.factor(Cn.subs(n,n+1)/Cn)
coef2=s.factor(An.subs(n,n+1)*scale_ratio*scale_ratio.subs(n,n+1))
coef1=s.factor((Bn.subs(n,n+1)-source_ratio*An)*scale_ratio)
coef0=s.factor(-source_ratio*Bn)
target2=3*(n+1)*(2*n+3)*(3*n+4)*(3*n+5)*(7*n*n-1)*(n+2)**3
target1=-8*(n+1)*(2*n+1)*(4*n+3)*(4*n+5)*(364*n**5+84*n**4-1025*n**3-534*n*n+157*n+54)
target0=-64*(2*n-1)**2*(2*n+1)*(4*n-1)*(4*n+1)*(4*n+3)*(4*n+5)*(7*n*n+14*n+6)
zero(coef1*target2-coef2*target1,'original target middle coefficient')
zero(coef0*target2-coef2*target0,'original target trailing coefficient')

print('All rational identities proved by exact numerator cancellation.')
