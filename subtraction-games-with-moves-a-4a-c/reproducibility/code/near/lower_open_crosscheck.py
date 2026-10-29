"""Supplementary direct checks of the proved lower open construction.

The uniform proof is the paper, Section 7 and Appendix C; this finite computation is
independent validation, not its all-parameter justification.
"""
from pathlib import Path
from math import gcd
import json
from halfstrip_certificate import prefix,value

def candidate(k,d,b):
    a=k*d+b;P=6*a-d;m,s=divmod(k,3)
    alpha='012';beta='01012';rho=alpha+beta
    if s==0:X=rho*(m-1)+beta*(2*m+1)+rho;Y=rho*(m-2)+beta*(2*m+3)
    elif s==1:X=rho*m+alpha*2+beta*(2*m+1);Y=rho*m+beta*(2*m+1)
    else:X=alpha+beta*(2*m+6)+rho*(m-2);Y=alpha*2+beta*(2*m+1)+rho*m
    T=''.join(X if ((j+1)*b)//d>(j*b)//d else Y for j in range(d))
    assert len(T)==P
    inv=pow(a,-1,P);D=(8*m+18,8*m+10,16*m+10)[s]
    V=[prefix(*divmod(x,3)) for x in range(k+1)]
    def at(n):
        y,t=divmod(n,a);i=a-1-t;x,e=divmod(i,d);z=y-6*x
        return value(V[x],y) if z<D else int(T[(y-inv*i-D)%P])
    q=((26*m+3)*a+d,(26*m-10)*a-(3*m-2)*d,(26*m+30)*a-(3*m+2)*d)[s]
    N=(D+6*k+1)*a
    return at,q,N,P

def main():
    out=[]
    for k in (41,42,43,44,59,60,61,80,121):
        for d,b in ((2,1),(3,1),(3,2),(7,1),(7,3),(7,6)):
            assert gcd(d,b)==1
            a=k*d+b;c=5*a-d;at,q,N,P=candidate(k,d,b)
            g=[at(n) for n in range(N+c+P)]
            for n,v in enumerate(g):
                opts={g[n-t] for t in (a,4*a,c) if n>=t}
                assert v not in opts and all(t in opts for t in range(v)),(k,d,b,n,v,opts)
            got=max(n+1 for n in range(len(g)-P) if g[n]!=g[n+P])
            assert got==q,(k,d,b,got,q)
            out.append(dict(k=k,d=d,b=b,a=a,q=q,P=P,positions=len(g)))
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All',len(out),'complete constructions passed mex and exact q:',sum(x['positions'] for x in out),'positions.')

if __name__=='__main__':main()
