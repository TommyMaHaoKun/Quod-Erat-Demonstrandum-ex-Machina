"""Exact 4sqrt(n) pole constants; uses the proved extended variance theorem."""
from fractions import Fraction as F
from math import comb
from verify_negative_bulk_variance_constants import exp_lower, exp_upper, decay_upper


def log_bounds(x,terms=40):
    x=F(x)
    if x<1:
        lo,hi=log_bounds(1/x,terms)
        return -hi,-lo
    powers=0
    while x>2:x/=2;powers+=1
    def reduced(y):
        z=(y-1)/(y+1)
        lo=2*sum((z**(2*k+1)/F(2*k+1) for k in range(terms)),F(0))
        rem=2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
        return lo,lo+rem
    lo,hi=reduced(x);l2,u2=reduced(F(2))
    return lo+powers*l2,hi+powers*u2


def Cmean(q):return max(F(q),4*log_bounds(q)[1])
def Cvar(q):return 4*log_bounds(q)[1]+F(q-1,2)
def Dlow(q,b):return log_bounds(1+F(q*q-1)*F(986,100)/(b*b+F(987,100)))[0]/2


# 0<=s<=pi, covered by rational boxes through3.15.
for i in range(63):
    a=F(i,20);b=F(i+1,20)
    Y=log_bounds(F(250)*(1+exp_lower(a))/F(355,113))[0]
    for q in [3,5,7,9]:
        D=Dlow(q,b);C=Cmean(q)
        slope=-D+C/(Y-F(7,10));intercept=C-D
        assert slope<0 and 250*slope+intercept < -12
        if q==9:
            tail_slope=slope+b*b/(2*q*q*F(986,100))
            tail_intercept=intercept+b*b/(2*q*q*F(986,100))
            assert tail_slope<0 and 250*tail_slope+tail_intercept < -12
print('PASS: 0<=s<=pi; q=3,5,7,9 and q>9 tail')

# pi<=s<=50, covered from3.14 upward in steps.1.
for i in range(469):
    a=F(314,100)+F(i,10);b=min(a+F(1,10),F(50))
    if a>=50:break
    Y=a+log_bounds(F(250)/b)[0]
    D=Dlow(3,b);slope=-(1-1/(Y-F(7,10)))*D+32*log_bounds(3)[1]/Y**2
    assert slope<0 and 250*slope < -F(39,160)
    Q=max(5,int(b))
    while Q<b or Q%2==0:Q+=1
    for q in range(5,Q+1,2):
        D=Dlow(q,b);Cm=Cmean(q);Cv=Cvar(q)
        sm=-D+Cm/(Y-F(7,10));im=Cm-D
        sv=-(1-1/(Y-F(7,10)))*D+8*Cv/Y**2
        candidates=[]
        if sm<0:candidates.append(250*sm+im)
        if sv<0:candidates.append(250*sv)
        assert candidates and min(candidates)<(-4 if q==5 else -12)
        if q==Q:
            tail=b*b/(2*q*q*F(986,100))
            candidates=[]
            if sm+tail<0:candidates.append(250*(sm+tail)+im+tail)
            if sv+tail<0:candidates.append(250*(sv+tail)+tail)
            assert candidates and min(candidates)<-12
print('PASS: pi<=s<=50; q3<.79, higher-pole sum <.021')

# Basic polynomial arithmetic, ascending coefficients.
def padd(a,b):
    return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]
def pscale(a,c):return [c*x for x in a]
def pmul(a,b):
    p=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):p[i+j]+=x*y
    return p
def ppow(a,n):
    p=[F(1)]
    for _ in range(n):p=pmul(p,a)
    return p
def pshift(a,c,scale=1):
    p=[F(0)]*len(a)
    for j,x in enumerate(a):
        for i in range(j+1):p[i]+=x*comb(j,i)*c**(j-i)*scale**i
    return p

# s>=50: q3 exponent <= -3.9n/s² <= -39/160.
s=[F(0),F(1)];s2=[F(0),F(0),F(1)]
a=F(67,100);b=F(137,100);C=F(35156,1000);M=F(3944,100);D=F(4935,100);c=F(39,10)
poly=padd(pscale(pmul(pmul([a-1,1],s2),ppow([b,1],2)),M),pscale(pmul(pmul(s2,[a,1]),[D,0,1]),-C))
poly=padd(poly,pscale(pmul(pmul([a,1],[D,0,1]),ppow([b,1],2)),-c))
assert all(x>0 for x in pshift(poly,F(50)))
assert 1/exp_lower(F(39,160))<F(79,100)
assert exp_upper(F(274,100))<F(250,16)
assert 32*log_bounds(3)[1]<C
print('PASS: s>=50, q3<.79')

# q5 exponent less than -2.53, so q5 ratio <.08.
A=F(96,100)*F(986,100);P=F(987,100)
gap=A*24/(2+P*26/2500)-8*Cvar(5)
assert gap>16*F(253,100)
assert 1/exp_lower(F(253,100))<F(8,100)

# q>=7 up to oddceil(s): exponent <= -16q n/s² <= -q.
assert log_bounds(7)[1]<F(1946,1000)
linear=[F(26272,1000),F(172,7)]
f=padd(pscale([-1,0,1],A*2500),pscale(pmul(linear,[5000+P,0,P]),-1))
scaled=pshift(f,F(7),F(45));degree=len(scaled)-1
bern=[sum(scaled[k]*F(comb(i,k),comb(degree,k)) for k in range(i+1)) for i in range(degree+1)]
assert all(x>0 for x in bern)
two=[F(-2),F(1)]
f=padd(pscale(pmul([-1,0,1],ppow(two,2)),A),pscale(pmul(linear,padd(pscale(ppow(two,2),2),[P,0,P])),-1))
assert all(x>0 for x in pshift(f,F(52)))
assert decay_upper(F(7))/(1-decay_upper(F(2)))<F(11,10000)
print('PASS: s>=50, q5<.08 and sum odd q>=7 through Q <.0011')

# Q=smallest odd integer >=s. R_Q<exp(-.8n), and the q>Q tail <.001.
assert log_bounds((1+F(986,100))/(1+F(987,100)/2500))[0]/2>F(118,100)
assert (32*log_bounds(52)[1]+204)/F(5137,100)**2<F(3,10)
assert F(96,100)*F(118,100)-F(3,10)>F(8,10)
assert F(251,250)/(2*F(986,100))<F(51,1000)
assert 750/exp_lower(F(749,1000)*250,terms=220)<F(1,1000)
assert F(79,100)+F(8,100)+F(11,10000)+F(1,1000)<F(88,100)
print('PASS: negative-s pole tail <.88 for n>=250, 0<=s<=4sqrt(n)')
