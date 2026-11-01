"""Exact coefficient audit of Au (2024), Example XV, equation (5.2)."""
import sympy as s

a,b,d,e,k=s.symbols('a b d e k')
vs=(a,b,d,e)
ga,L,Z2,Z3=s.symbols('gamma log2 zeta2 zeta3')
H,J,H2,J2=s.symbols('H_k H_2k H2_k H2_2k')
q=2*k+1

def pg(x,degree):
    if degree==0:
        return {s.S.Half:-ga-2*L,s.S.One:-ga,k+s.S.Half:-ga-2*L+2*J-H,k+1:-ga+H,k+s.Rational(3,2):-ga-2*L+2*J-H+2/q}[x]
    return {s.S.Half:3*Z2,s.S.One:Z2,k+s.S.Half:3*Z2-4*J2+H2,k+1:Z2-H2,k+s.Rational(3,2):3*Z2-4*J2+H2-4/q**2}[x]

# Each tuple is (power, constant argument, linear parameter part).
gammas=[
 (1,s.S.Half,e),(1,s.S.Half,a-b+e),(1,s.S.One,a+e),
 (-1,s.S.One,d+e),(-1,s.S.Half,-d),(-1,s.S.Half,a-b-d),(-1,s.S.One,a-d),
 (1,k+s.S.Half,-d),(1,k+s.S.Half,a-b-d),(1,k+1,a-d),(1,k+1,2*a-b-2*d+e),
 (-1,k+1,a-b-d+e),(-1,k+s.Rational(3,2),a-d+e),(-1,k+s.Rational(3,2),2*a-b-d+e)]
linear=[(1,q,2*a-b-2*d+e),(-1,q,2*a-2*d+2*e),(-1,q,2*a-2*b-2*d)]
grad={v:sum(power*s.diff(ell,v)*pg(x,0) for power,x,ell in gammas)+sum(power*s.diff(ell,v)/x for power,x,ell in linear) for v in vs}
hess={(v,w):sum(power*s.diff(ell,v)*s.diff(ell,w)*pg(x,1) for power,x,ell in gammas)-sum(power*s.diff(ell,v)*s.diff(ell,w)/x**2 for power,x,ell in linear) for v in vs for w in vs}
coeffA=s.factor(8/q**3*(-grad[a]**2-hess[a,a]+grad[a]*grad[b]+hess[a,b]+grad[b]**2+hess[b,b]-grad[a]*grad[d]-hess[a,d]+grad[a]*grad[e]+hess[a,e]))
assert s.cancel(coeffA-96/q**5)==0
print('Operator applied to A(k):',coeffA)

def trunc(expr,n=2):
    return s.Add(*(c*s.prod(v**p for v,p in zip(vs,m)) for m,c in s.Poly(s.expand(expr),*vs).terms() if sum(m)<=n))
def exp_poly(expr,n):
    return trunc(sum(trunc(expr**j,n)/s.factorial(j) for j in range(n+1)),n)
def op(expr):
    p=s.Poly(s.expand(expr),*vs)
    return s.simplify(-p.coeff_monomial(a*a)+p.coeff_monomial(a*b)/2+p.coeff_monomial(b*b)-p.coeff_monomial(a*d)/2+p.coeff_monomial(a*e)/2)

# B - D Gamma(t)=D0 [Q Gamma(-t)+2^(-t) Gamma(t)], t=a-d.
t=a-d
logQ=trunc(t*(-2*ga-4*L+3*Z2*(e-b)-7*Z3*(e**2+b**2)) + t**2/2*(6*Z2-14*Z3*(e-b)) + t**3/6*(-28*Z3),3)
Q=exp_poly(logQ,3)
pow2=exp_poly(-L*t,3)
R=trunc(s.cancel((pow2-Q)/t)-ga*(Q+pow2)+(ga**2/2+Z2/2)*t*(pow2-Q)-(ga**3/6+ga*Z2/2+Z3/3)*t*t*(Q+pow2),2)
logD0=0
for power,x,ell in [(1,s.S.Half,d),(1,s.S.Half,e),(1,s.S.Half,-a+b+d),(1,s.S.Half,a-b+e),(1,s.S.One,a+e),(-1,s.S.One,a+e),(-1,s.S.One,b+e),(-1,s.S.One,d+e),(-1,s.S.One,a-b)]:
    logD0+=power*(ell*pg(x,0)+ell**2/2*pg(x,1))
coeffR=s.factor(op(trunc(exp_poly(logD0,2)*R,2)))
assert coeffR==7*Z3
print('Operator applied to (B - D Gamma(t)) divided by pi^2:',coeffR)

# Regulating summand: D Gamma(1+t)(1+t)_n/[(n+t)n!]
# = -2^(-t) D0 Gamma(n+t)/(n!); differential operator will annihilate it.
X,Y=s.symbols('psi_n trigamma_n')
reglog=trunc(logD0-L*t+X*t+Y*t*t/2,2)
coeff_reg=s.factor(op(exp_poly(reglog,2)))
assert coeff_reg==0
print('Operator applied to regulator divided by its constant term:',coeff_reg)
print('All three exact coefficient assertions passed.')

# The missing polynomial from Au's C(n), specialized at c=0, was
# independently recovered by a rational degree-2 Gosper ansatz.
n=s.symbols('n')
P=(4*a*a*d+4*a*a*n-2*a*a-4*a*b*d-4*a*b*n+2*a*b
   +8*a*d*e+12*a*d*n-2*a*d+8*a*e*n-4*a*e+12*a*n*n-8*a*n+a
   -4*b*d*e-4*b*d*n+2*b*e+4*d*e*e+16*d*e*n-2*d*e+12*d*n*n-4*d*n
   +8*e*e*n-2*e*e+24*e*n*n-12*e*n+e+16*n**3-12*n*n+2*n)
zero={v:0 for v in vs}
P0=P.subs(zero)
assert s.expand(P0-2*n*(2*n-1)*(4*n-1))==0
X0,Y0,X1,Y1=s.symbols('psi_n psi_n_half trigamma_n trigamma_n_half')
def pgc(x,degree):
    if x in (s.S.Half,s.S.One):
        return pg(x,degree)
    if degree==0:
        return {n:X0,n+s.S.Half:Y0,2*n-1:(X0+Y0)/2+L-1/(2*n-1),2*n+1:(X0+Y0)/2+L+1/(2*n)}[x]
    return {n:X1,n+s.S.Half:Y1,2*n-1:(X1+Y1)/4+1/(2*n-1)**2,2*n+1:(X1+Y1)/4-1/(2*n)**2}[x]
gammasC=[(1,n,a+e),(1,n,b+e),(1,2*n-1,d+e),(1,n,a-b),
 (-1,n+s.S.Half,d),(-1,n+s.S.Half,e),(-1,n+s.S.Half,-a+b+d),(-1,n+s.S.Half,a-b+e),(-1,2*n+1,a+e),
 (1,s.S.Half,d),(1,s.S.Half,e),(1,s.S.Half,-a+b+d),(1,s.S.Half,a-b+e),
 (-1,s.S.One,b+e),(-1,s.S.One,d+e),(-1,s.S.One,a-b)]
gC={v:sum(power*s.diff(ell,v)*pgc(x,0) for power,x,ell in gammasC)+s.diff(P,v).subs(zero)/P0 for v in vs}
hC={(v,w):sum(power*s.diff(ell,v)*s.diff(ell,w)*pgc(x,1) for power,x,ell in gammasC)+s.diff(P,v,w).subs(zero)/P0-s.diff(P,v).subs(zero)*s.diff(P,w).subs(zero)/P0**2 for v in vs for w in vs}
ratioC=s.factor((-gC[a]**2-hC[a,a]+gC[a]*gC[b]+hC[a,b]+gC[b]**2+hC[b,b]-gC[a]*gC[d]-hC[a,d]+gC[a]*gC[e]+hC[a,e])/2)
assert s.cancel(ratioC+1/(n*(2*n-1)))==0
print('Operator applied to C(n) divided by its constant term:',ratioC)
print('All four exact coefficient assertions passed.')
