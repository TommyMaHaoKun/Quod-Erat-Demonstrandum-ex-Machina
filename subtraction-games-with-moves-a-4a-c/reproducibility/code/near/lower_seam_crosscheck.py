"""Candidate lower d=1 splice; numerical discovery checks, not uniform proof."""
from halfstrip_certificate import prefix,value

def candidate(a):
    h,s=divmod(a,3)
    assert a>=9
    A='01012';C='012';T=C+A
    W=T*(h-2)+A*(2*h+3) if s==0 else T*h+A*(2*h+1) if s==1 else T*h+C+C+A*(2*h+1)
    P=6*a-1;D=16*h+(4,12,15)[s];shift=10*h+(-19,-5,1)[s]
    assert len(W)==P
    V=[prefix(*divmod(x,3)) for x in range(a)]
    def at(n):
        y,i=divmod(n,a);x=a-1-i;z=y-6*x
        return value(V[x],y) if z<D else int(W[(z+shift)%P])
    return at,(D+6*(a-1)+1)*a,P

if __name__=='__main__':
    total=0
    for a in range(10,81):
        at,N,P=candidate(a);c=5*a-1
        g=[at(n) for n in range(N+c+P)]
        for n,v in enumerate(g):
            opts={g[n-d] for d in(a,4*a,c) if n>=d}
            assert v not in opts and all(j in opts for j in range(v)),(a,n,v,opts)
        q=max(n+1 for n in range(len(g)-P) if g[n]!=g[n+P])
        h,s=divmod(a,3)
        want=((26*a*a+(9,-59,-85)[s]*a)//3+(1,3,4)[s])
        assert q==want,(a,q,want)
        total+=len(g)
    print('All lower seam splice candidates a10..80 satisfy mex and predicted q:',total,'positions.')
