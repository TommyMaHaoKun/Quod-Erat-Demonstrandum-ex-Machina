"""Direct word evaluator for the uniform neighbourhood of c=5a.

Explicit powers and modular coordinates only: no mex or state search.
"""
from math import gcd

O='01012323';R='01201012';A='012';B='01012'
UH=('', '01012323013', '01012323010123')
UM=('01012','01012','20101')
UK=('010120101201','0101201','201012010120101201')

def upper_front(j,y):
    m,s=divmod(j,3)
    for w,num in ((O,2*m),(UH[s],1),(UM[s],2*m),(UK[s],1)):
        width=len(w)*num
        if y<width:return w[y%len(w)]
        y-=width
    return R[y%8]

def lower_front(j,y):
    m,s=divmod(j,3)
    parts=(((O,2*m),(B,2*m),('01',1)),
           ((O,2*m+1),('013',1),(B,2*m+1)),
           ((O,2*m+1),('0101232',1),(B,2*m+1),('01',1)))[s]
    for w,num in parts:
        width=len(w)*num
        if y<width:return w[y%len(w)]
        y-=width
    return R[y%8]

def upper_towers(k):
    m,s=divmod(k,3)
    if s==0:return R*(m-2)+B*(2*m+3)+R,R*(m-3)+B*(2*m+5)
    if s==1:return R*(m-1)+A+A+B*(2*m+3),R*(m-1)+B*(2*m+3)
    return A+B*(2*m+8)+R*(m-3),A+A+B*(2*m+3)+R*(m-1)

def upper(a,d):
    if d==1:return upper_seam(a)
    k,b=divmod(a,d);m,s=divmod(k,3);P=6*a+d
    assert k>=41 and 0<b<d and gcd(a,d)==1
    X,Y=upper_towers(k)
    necklace=''.join(X if (i+1)*b//d>i*b//d else Y for i in range(d))
    assert len(necklace)==P
    inv=pow(a,-1,P);D=(8*m+28,8*m+20,16*m+12)[s]
    q=((26*m+13)*a+3*m*d,(26*m-1)*a+(3*m-1)*d,(26*m+40)*a)[s]
    def symbol(n):
        y,x=divmod(n,a);j=x//d
        return upper_front(j,y) if y-6*j<D else necklace[(inv*n-D)%P]
    return P,q,symbol

def upper_seam(a):
    m,s=divmod(a,3);P=6*a+1
    assert a>=42
    E=8*m+(20,12,12)[s];gamma=10*m+(-27,-13,-7)[s]
    N=(R*(m-3)+B*(2*m+5),R*(m-1)+B*(2*m+3),R*(m-1)+A+A+B*(2*m+3))[s]
    assert len(N)==P
    q=((26*a*a+42*a)//3,(26*a*a-26*a)//3-2,(26*a*a-52*a)//3-3)[s]
    def symbol(n):
        y,x=divmod(n,a);z=y-6*x
        return upper_front(x,y) if z<E else N[(z+gamma)%P]
    return P,q,symbol

def lower_seam(a):
    h,s=divmod(a,3);P=6*a-1
    assert a>=42
    D=16*h+(4,12,15)[s];shift=10*h+(-19,-5,1)[s]
    N=(R*(h-2)+B*(2*h+3),R*h+B*(2*h+1),R*h+A+A+B*(2*h+1))[s]
    assert len(N)==P
    q=((26*a*a+9*a)//3+1,(26*a*a-59*a)//3+3,(26*a*a-85*a)//3+4)[s]
    def symbol(n):
        y,t=divmod(n,a);x=a-1-t;z=y-6*x
        return lower_front(x,y) if z<D else N[(z+shift)%P]
    return P,q,symbol

def lower_towers(k):
    m,s=divmod(k,3)
    if s==0:return R*(m-1)+B*(2*m+1)+R,R*(m-2)+B*(2*m+3)
    if s==1:return R*m+A+A+B*(2*m+1),R*m+B*(2*m+1)
    return A+B*(2*m+6)+R*(m-2),A+A+B*(2*m+1)+R*m

def lower_open(a,d):
    k,b=divmod(a,d);m,s=divmod(k,3);P=6*a-d
    assert k>=41 and d>1 and 0<b<d and gcd(a,d)==1
    X,Y=lower_towers(k)
    N=''.join(X if (i+1)*b//d>i*b//d else Y for i in range(d))
    assert len(N)==P
    inv=pow(a,-1,P);D=(8*m+18,8*m+10,16*m+10)[s]
    q=((26*m+3)*a+d,(26*m-10)*a-(3*m-2)*d,(26*m+30)*a-(3*m+2)*d)[s]
    def symbol(n):
        y,t=divmod(n,a);i=a-1-t;j=i//d;z=y-6*j
        return lower_front(j,y) if z<D else N[(y-inv*i-D)%P]
    return P,q,symbol

def formula(a,c):
    d=abs(c-5*a)
    assert a>=2 and c>4*a and gcd(a,c)==1 and 0<41*d<a
    if c>5*a:return upper(a,d)
    if d==1:return lower_seam(a)
    return lower_open(a,d)

def classify(a,c):
    p,q,symbol=formula(a,c)
    return dict(a=a,c=c,p=p,q=q,prefix=''.join(symbol(n) for n in range(q)),
                block=''.join(symbol(n) for n in range(q,q+p)),family='uniform_near_5a')
