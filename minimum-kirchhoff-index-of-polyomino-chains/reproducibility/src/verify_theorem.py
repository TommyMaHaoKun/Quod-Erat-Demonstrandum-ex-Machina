"""Exact finite checks of the paper's formulas and spectral certificates.

These checks support, but do not replace, the universal proofs. They do not
verify the match between an external source definition and the graph class.
No proof assistant is used. Only the Python standard library is required.
"""
from fractions import Fraction as F
from itertools import product
from recurrence_check import INITIAL, extend, validate


def sequences(n):
    q=[1,4]
    for _ in range(n):
        q.append(4*q[-1]-q[-2])
    B=[0]+[2*i*q[i]+q[i-1] for i in range(1,n+1)]
    return q,B


def straight_value(n,q):
    return F((n+1)**3,3)+F((n+1)**2*(q[n+1]-q[n-1]),6*q[n])


def kernel_value(word,n,q,B):
    gain=sum(B[i+1]*B[n-2-i]*c*c for i,c in enumerate(word))
    gain+=2*sum(B[i+1]*B[n-2-j]*word[i]*word[j]
                for i in range(len(word)) for j in range(i+1,len(word)))
    return straight_value(n,q)-F(gain,q[n])


def matvec(a,v):
    return [sum(x*y for x,y in zip(row,v)) for row in a]


def psd_exact(a):
    """Exact symmetric elimination; no floating-point eigenvalue test."""
    a=[row[:] for row in a]
    n=len(a)
    for k in range(n):
        pivot=a[k][k]
        assert pivot>=0,('negative pivot',k,pivot)
        if pivot==0:
            assert all(a[k][j]==0 for j in range(k,n)),('zero pivot nonzero row',k)
            continue
        for i in range(k+1,n):
            for j in range(i,n):
                a[j][i]=a[i][j]=a[i][j]-a[i][k]*a[j][k]/pivot


def verify_certificate(n,q,B):
    m=n-2
    H=[[F(B[min(i,j)]*B[n-1-max(i,j)],q[n])
        for j in range(1,m+1)] for i in range(1,m+1)]
    alt=[F((-1)**i) for i in range(1,m+1)]
    h=[v*w for v,w in zip(alt,matvec(H,alt))]
    assert all(x>0 for x in h)
    # Independent inverse from H=diag(v) C diag(delta) C^T diag(v)/q[n].
    v=[B[n-1-i] for i in range(1,m+1)]
    t=[F(B[i],B[n-1-i]) for i in range(1,m+1)]
    delta=[t[0]]+[t[i]-t[i-1] for i in range(1,m)]
    assert all(x>0 for x in delta)
    T=[[F(0) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        T[i][i]=q[n]*(1/delta[i]+(1/delta[i+1] if i+1<m else 0))/v[i]**2
        if i+1<m:
            T[i][i+1]=T[i+1][i]=-q[n]/(delta[i+1]*v[i]*v[i+1])
    for i in range(m):
        for j in range(m):
            assert sum(T[i][k]*H[k][j] for k in range(m))==int(i==j)
    assert all(T[i][i]*h[i]>F(2,3) for i in range(m))
    J=[[4*h[i]*int(i==j)-3*h[i]*T[i][j]*h[j]
        for j in range(m)] for i in range(m)]
    assert matvec(J,alt)==matvec(H,alt)
    lam=[-6*h[i]*T[i][i+1]*h[i+1] for i in range(m-1)]
    mu=[h[i]*(3*T[i][i]*h[i]-2) for i in range(m)]
    assert all(x>0 for x in lam+mu)
    for i in range(m):
        assert J[i][i]==mu[i]+(lam[i-1] if i else 0)+(lam[i] if i+1<m else 0)
        if i+1<m:
            assert 2*J[i][i+1]==lam[i]
    psd_exact([[J[i][j]-H[i][j] for j in range(m)] for i in range(m)])


def verify(max_n=24,word_n=8,laplacian_n=5):
    validate(laplacian_n)
    q,B=sequences(max(max_n,word_n)+1)
    straight=INITIAL
    for n in range(1,max_n+1):
        assert straight.K==straight_value(n,q)
        if n>=3:
            verify_certificate(n,q,B)
        straight=extend(straight,0)
    words_checked=0
    for n in range(3,word_n+1):
        best=None; winners=[]
        for word in product((-1,0,1),repeat=n-2):
            s=INITIAL
            for c in word:
                s=extend(s,c)
            s=extend(s,0)
            value=kernel_value(word,n,q,B)
            assert s.K==value,(n,word,s.K,value)
            words_checked+=1
            if any(word[i]==word[i+1]!=0 for i in range(n-3)):
                continue
            if best is None or value<best:
                best=value;winners=[word]
            elif value==best:
                winners.append(word)
        alt=tuple((-1)**i for i in range(n-2))
        assert set(winners)=={alt,tuple(-c for c in alt)},(n,winners)
    print(f'Straight values verified for 1 <= n <= {max_n}.')
    print(f'Exact matrix certificates, including PSD elimination: 3 <= n <= {max_n}.')
    print(f'Quadratic formula verified on {words_checked} abstract words, n <= {word_n}.')
    print(f'Relaxed minimizers classified exactly for 3 <= n <= {word_n}.')
    print('All checks passed. Universal proofs and source-domain audit are separate.')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=24)
    parser.add_argument('--word-n',type=int,default=8)
    parser.add_argument('--laplacian-n',type=int,default=5)
    a=parser.parse_args()
    verify(a.max_n,a.word_n,a.laplacian_n)
