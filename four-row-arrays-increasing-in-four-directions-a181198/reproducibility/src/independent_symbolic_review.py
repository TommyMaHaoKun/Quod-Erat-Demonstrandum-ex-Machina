"""Independent proof audit from displayed formulas in SYMBOLIC_PROOF.md.

Uses whole-expression differentiation rather than the author's coefficient
checks, and normalizes directly to a(n) instead of the intermediate c(n).
"""
import sympy as S
n,t,z,Y,W,V,j=S.symbols('n t z Y W V j')

def check(v,label):
    num,den=S.fraction(S.together(v))
    assert S.expand(num)==0,(label,S.factor(num))
    print('PASS',label)

N=(n-2)*(n-1)
F=((n-2*N*z)*W**2+z*(2*n+1+2*z)*W*V+2*z*z*(1+z)*V**2)/(2*n-1)
wpp=(N*W-(n+1+2*z)*V)/(z*(1+z))
DF=S.diff(F,z)+V*S.diff(F,W)+wpp*S.diff(F,V)
check(DF-(W*V+z*(W*wpp-V*V)),'whole convolution antiderivative')

# Cancel the common formal factor (1-t)^(-2n+4) before substitution.
zt=t/(1-t); vbar=(1-t)*((n-2)*Y+(1-t)*V)
transformed=(n-2*N*zt)*Y**2+zt*(2*n+1+2*zt)*Y*vbar+2*zt**2*(1+zt)*vbar**2
H=(n+3*(n-2)*t)*Y**2+t*(2*n+1+(2*n-7)*t)*Y*V+2*t*t*(1-t)*V**2
check(transformed-H,'change of variables to quadratic H')

P=t*(1-t*t);R=n+2*(n-2)*t+(n-2)*t*t
ell=(2*n-1)/t-3/(1-t)
# Set C=1; all identities are homogeneous in (Y,C).
dy=(1-R*Y)/P
h=2*t*(t-1)**2/((4*n-1)*(t+1)**2)
g=t*((16*n**3-24*n**2+8*n)*t*t+(32*n**3-32*n**2+2*n+3)*t+16*n**3-40*n**2-14*n+3)/(n*(4*n-1)*(4*n+1)*(t+1)**2)
k=-t*((12*n*n+10*n-2)*t*t+(24*n*n+2*n-1)*t-4*n*n-12*n+1)/(2*n*(4*n-1)*(4*n+1)*(t+1)**2)
r1=-8*(n-1)*(2*n-1)*(3*n+1)/((4*n-1)*(4*n+1))
r0=(n+1)*(2*n+3)*(6*n-1)/(n*(4*n-1)*(4*n+1))
cert=h*Y*Y+g*Y+k
check(H.subs(V,dy)-(S.diff(cert,t)+dy*S.diff(cert,Y)+ell*cert+r1*Y+r0),'whole quadratic integral certificate')

f=(36*n**3+69*n*n+39*n+6)*t**3-(24*n**3+34*n*n+15*n+2)*t*t-(44*n**3+115*n*n+82*n+14)*t+16*n**3+44*n*n+38*n+10
p=t*(t-1)*f/(3*(n+1)*(3*n+2)*(3*n+4)*(4*n+1)*(t+1))
q=2*n*(2*n+1)*(4*n+5)/(3*(3*n+2)*(3*n+4)*(4*n+1))
v=-t*(t-1)*((36*n**3+69*n*n+39*n+6)*t-20*n**3-109*n*n-109*n-26)/(6*(n+1)*(n+2)*(3*n+2)*(3*n+4)*(4*n+1)*(t+1))
r=(4*n**4+33*n**3-17*n*n-60*n-20)/(3*(n+1)*(n+2)*(3*n+2)*(3*n+4)*(4*n+1))
check(S.diff(p*Y,t)+dy*S.diff(p*Y,Y)+ell*p*Y-((t*(1-t)**2-q)*Y+p/P),'whole moment integration by parts')
check(S.diff(v,t)+ell*v+r-p/P,'rational source integration by parts')

B=6/((2*n)*(2*n+1)*(2*n+2)*(2*n+3))
d=n*(2*n+1)*(4*n+5)/(3*(2*n-1)*(3*n+2)*(3*n+4)*(4*n+1))
e=(2*n+1)*(28*n*n+26*n+1)/(3*(n+1)*(2*n-1)*(3*n+2)*(3*n+4)*(4*n+1))
check(d-q/(2*(2*n-1)),'moment d')
check(e-(1/(n+2)+r)/(2*(2*n-1)),'moment e')

L=3*(n-1)*(n+1)*(3*n+1)*(3*n+2)
M=8*n*(4*n-1)*(4*n+1)*(2*n+1)
Kratio=(4*n)*(4*n+1)*(4*n+2)*(4*n+3)*(2*n-1)/((2*n+1)*n*(n+1))
baseratio=Kratio*(2*n-1)/((2*n+1)*n*n)
Qbase=3*(4*n)*(4*n+1)*(4*n+2)*(7*n*n-1)/((n+1)**2*(2*n+1)**2*n**3)
check(M*r1-L*baseratio*r1.subs(n,n+1)*n*d,'direct a(n) moment cancellation')
check(L*baseratio*(r1.subs(n,n+1)*n*B*e+r0.subs(n,n+1)*B.subs(n,n+1))+M*r0*B-Qbase,'direct a(n) inhomogeneous source')

rho=(4*n+3)*(4*n+4)*(4*n+5)*(4*n+6)*(2*n-1)**2*(7*n*n+14*n+6)/((n+1)**2*(n+2)**2*(2*n+3)**2*(7*n*n-1))
p2=3*(n+1)*(2*n+3)*(3*n+4)*(3*n+5)*(7*n*n-1)*(n+2)**3
p1=-8*(n+1)*(2*n+1)*(4*n+3)*(4*n+5)*(364*n**5+84*n**4-1025*n**3-534*n*n+157*n+54)
p0=-64*(2*n-1)**2*(2*n+1)*(4*n-1)*(4*n+1)*(4*n+3)*(4*n+5)*(7*n*n+14*n+6)
factor=p2/L.subs(n,n+1)
check(factor*(M.subs(n,n+1)-rho*L)-p1,'original recurrence middle coefficient independently')
check(factor*(-rho*M)-p0,'original recurrence last coefficient independently')
check(p2.subs(n,1)*8+p1.subs(n,1)+p0.subs(n,1),'exceptional n=1')

# Polynomial coefficients y(n,j)=(-1)^j(n-2)!(j+1)/((n-2-j)!(n+j)!).
ym1=-j*(n+j)/((j+1)*(n-j-1))
ym2=(j-1)*(n+j)*(n+j-1)/((j+1)*(n-j-1)*(n-j))
ynextm1=-(n-1)*j/((j+1)*(n-j)*(n-j-1))
check((n+j)+2*(n-2)*ym1+(n-j)*ym2,'ODE coefficient identity in n,j')
check(2*(2*n-1)*ynextm1+1-2*ym1+ym2,'contiguous coefficient identity in n,j')
print('Independent all-parameter algebra checks passed.')

# Final manuscript transcription audit (paper/main.tex). These formulas use a
# different certificate representation from the original symbolic proof.
alpha=2*n*(2*n+1)*(4*n+5)/(3*(3*n+2)*(3*n+4)*(4*n+1))
s0=-2*(2*n+1)*(4*n+5)/(3*(3*n+2)*(3*n+4)*(4*n+1))
s1=(11*n*n+26*n+14)/(3*(n+1)*(3*n+2)*(3*n+4))
s2=(2*n+1)/(3*(n+1)*(3*n+4))
s3=-1/(3*n+4)
Scert=(s0+s1*t+s2*t*t+s3*t**3)/(1+t)**2
check(P*S.diff(Scert,t)+(n-(2*n-1)*t-3*(n+1)*t*t)*Scert-t*(1-t)**2+alpha,'manuscript S certificate')
check(S.diff(P,t)+ell*P-R-(n-(2*n-1)*t-3*(n+1)*t*t),'manuscript S bracket')
D=3*(n+1)*(3*n+2)*(3*n+4)*(4*n+1)
Haux=(2*n*(1-t)-4*t)/(1+t)-t*(1-t)/(1+t)**2
gamma=-(28*n*n+33*n+8)/D
d0=2*(20*n**3+11*n*n-11*n-5)/D
d1=-1/(3*n+4)
check(Scert-d0-d1*t-gamma*Haux,'manuscript S rational decomposition')
vaux=t*(1-t)/(1+t)
check(S.diff(vaux,t)+ell*vaux-Haux,'manuscript H total derivative')
beta=(4*n**4+33*n**3-17*n*n-60*n-20)/(3*(n+1)*(n+2)*(3*n+2)*(3*n+4)*(4*n+1))
check(d0+d1*n/(n+2)-beta,'manuscript beta integration')
check(d-alpha/(2*(2*n-1)),'manuscript moment r')
check(e-(1/(n+2)+beta)/(2*(2*n-1)),'manuscript moment f')

U=-2*n*(3*n+1)/((2*n-1)*(4*n+1))
Vn=3*(6*n-1)/(8*(n-1)*(2*n-1)**2*(2*n+1)*(4*n+1))
# q_n*K_n/(2n-1)*C/n! = n*(4n-1)/[4*(n-1)*(2n-1)^2].
# q_n*K_n/(2n-1)*C^2 = n^2*(4n-1)/[4*(n-1)*(2n-1)^2].
check(n*(4*n-1)*r1/(4*(n-1)*(2*n-1)**2)-U,'manuscript c_n coefficient U')
check(n*n*(4*n-1)*r0*B/(4*(n-1)*(2*n-1)**2)-Vn,'manuscript c_n constant V')
dt=n*(n+1)*(2*n+1)*(4*n+5)/(3*(2*n-1)*(3*n+2)*(3*n+4)*(4*n+1))
et=(28*n*n+26*n+1)/(2*(n+1)*(2*n-1)*(2*n+3)*(3*n+2)*(3*n+4)*(4*n+1))
check(dt-(n+1)*d,'manuscript T recurrence coefficient')
check(et-n*(n+1)*B*e,'manuscript T recurrence source')
A=3*(3*n+1)*(3*n+2);E=(n+1)**2
G=3*(7*n*n-1)/(4*n*(n-1)*(2*n-1)**2*(2*n+1)**2)
check(-A*U.subs(n,n+1)*dt+E*U,'manuscript c recurrence cancellation')
check(A*(U.subs(n,n+1)*et+Vn.subs(n,n+1))+E*Vn-G,'manuscript c recurrence source')
rhoc=(n-1)*(2*n-1)**2*(7*n*n+14*n+6)/((n+1)*(2*n+3)**2*(7*n*n-1))
check(G.subs(n,n+1)-rhoc*G,'manuscript G ratio')
sn=(n-1)*(n+1)**3/(8*n*(4*n-1)*(4*n+1)*(2*n+1))
rawratio=(4*n+3)*(n-1)/(n*(4*n-1))*(n+1)**4/((4*n+1)*(4*n+2)*(4*n+3)*(4*n+4))
check(rawratio-sn,'manuscript q ratio')
mult=64*(2*n+1)*(2*n+3)**2*(4*n-1)*(4*n+1)*(4*n+3)*(4*n+5)*(7*n*n-1)/((n-1)*(n+1))
check(mult*A.subs(n,n+1)*sn*sn.subs(n,n+1)-p2,'manuscript target leading coefficient')
check(mult*(E.subs(n,n+1)-rhoc*A)*sn-p1,'manuscript target middle coefficient')
check(mult*(-rhoc*E)-p0,'manuscript target last coefficient')
print('Final manuscript transcription checks passed.')
