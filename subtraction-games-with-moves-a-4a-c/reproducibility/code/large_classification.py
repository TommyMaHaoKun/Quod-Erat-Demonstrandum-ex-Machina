"""Proved structural classification for c>6a, and for every a=2.

No search for a repeated state. Returns a displayed prefix, a displayed
periodic word, the least period, and the least preperiod. The displayed
prefix can extend past the least preperiod, and W can be a word power.
"""
import argparse
import json
from math import gcd

def theorem(a,c):
    if not (a>=2 and c>4*a and gcd(a,c)==1):
        raise ValueError('inadmissible parameters')
    k,rem=divmod(c,5*a);j,r=divmod(rem,a)
    B='0'*a+'1'*a+'0'*a+'1'*a+'2'*a
    U='0'*a+'1'*a
    F=lambda t:'0'*t+'2'*(a-t)+'1'*t
    R,S=F(r),F(a-r)
    if j==0 and k>=2:
        s=a-r;C='0'*r+'3'*s+'1'*r;D0=C+'2'*s+C+S+C
        A=B*k+D0
        if 2*r<=a:
            W=(U+S+R)*(k-1)+U+R+S+R;p=c+a;q=(5*k+6)*a
        else:
            A+=(U+S+R)*(k-1)+U+S;V=F(2*s)
            W=(R+R+V)*k+R if 3*r<2*a else R+R+V
            p=c+a if 3*r<2*a else 5*a//3 if 3*r==2*a else 5*a
            q=(10*k+4)*a+r
        return A,W,p,q,'interval_0'
    if j==1 and k>=1:
        X=U+'2'*r;Y=U+'2'*(a-r)
        if 2*r<=a:
            W=X+Y;p=5*a if 2*r<a else 5*a//2;q=5*k*a-a+r
        else:
            W=(X+Y)*k+X;p=c+a;q=5*k*a-r
        return B*k,W,p,q,'interval_1'
    if j==2 and k>=1 and 2*r!=a:
        if 2*r<a:
            A=B*k+U+R+S+'3'*r+S+R+(U+S+R)*(k-1)+(U+R+S)*k+U+R
            V=F(2*r);W=(S+V+S)*k+S+V if 3*r<a else S+V+S
            p=c+a if 3*r<a else 5*a//3 if 3*r==a else 5*a
            q=(15*k+6)*a+r
        else:
            E='3'*(2*r-a)
            A=B*k+U+R+S+'3'*r+S+R+(U+S+R)*k+U+S+E+S+(U+R+S)*(k+1)+E
            V=F(2*a-2*r);W=V+R+R if 3*r<=2*a else (V+R+R)*(k+1)+V+'3'*(3*r-2*a)
            p=5*a if 3*r<2*a else 5*a//3 if 3*r==2*a else c+4*a
            q=(15*k+17)*a+3*r if 3*r<=2*a else (15*k+19)*a
        return A,W,p,q,'interval_2'
    if j==3 and k>=1:
        T=U+'2'*r+U+'2'*(a-r);A=B*(k+1)+'0'*r+'3'*(a-r)
        if 2*r<a:
            W='1'*r+'2'*(a-r)+T*(k+1)+'0'*(2*r)+'3'*(a-2*r)+'1'*r;p=c+4*a
        else:
            W='1'*r+'2'*(a-r)+U+'2'*r+'0'*a+'1'*(a-r)
            p=5*a if 2*r>a else 5*a//2
        return A,W,p,(5*k+6)*a,'interval_3'
    if j==4 and k>=1:
        D='3'*r+'0'*(a-r)+'2'*r+'1'*(a-r)+'3'*r+U+'2'*(a-r)+'3'*r
        W=B*k+U+'2'*r+U+'2'*a
        return B*(k+1)+D,W,c+a,c+6*a,'interval_4'
    if a==2:
        k,t=divmod(c,10);B='0011001122';E='0011021021'
        A,W,p,q={
            1:(B*k+'031203102103','1'+E*k+'02',c+2,c+11),
            3:(B*(k-1)+'001100112','20011',5,c-4),
            5:(B*k+'00110210213','0210210011',10,c+6),
            7:(B*(k+1)+'03','12001',5,c+5),
            9:(B*(k+1)+'30213001123',B*k+'00112001122',c+2,c+12),
        }[t]
        return A,W,p,q,'a2'
    return None

def classify(a,c):
    result=theorem(a,c)
    if result is None:raise NotImplementedError('Outside the large-range evaluator; use classify.py for the complete classification.')
    A,W,p,q,name=result
    def symbol(n):return A[n] if n<len(A) else W[(n-len(A))%len(W)]
    return dict(a=a,c=c,p=p,q=q,prefix=''.join(symbol(n) for n in range(q)),
                block=''.join(symbol(n) for n in range(q,q+p)),family=name)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('a',type=int);parser.add_argument('c',type=int)
    args=parser.parse_args();print(json.dumps(classify(args.a,args.c),indent=2))
