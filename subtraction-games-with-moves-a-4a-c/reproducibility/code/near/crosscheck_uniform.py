"""Independent direct recurrence comparisons (corroboration, not a proof)."""
from uniform_classification import formula
from pathlib import Path
import json

def one(a,c):
    p,q,symbol=formula(a,c);N=q+c+p;g=bytearray(N)
    for n in range(N):
        mask=0
        for t in (a,4*a,c):
            if n>=t:mask|=1<<g[n-t]
        v=0
        while mask&(1<<v):v+=1
        g[n]=v
        assert ord(symbol(n))-48==v,(a,c,n,v,symbol(n))
    assert g[q-1]!=g[q+p-1]
    # Independently check the primitive block by its border array.
    W=g[q:q+p];pi=[0]*p
    for i in range(1,p):
        j=pi[i-1]
        while j and W[i]!=W[j]:j=pi[j-1]
        if W[i]==W[j]:j+=1
        pi[i]=j
    t=p-pi[-1]
    assert t==p or p%t!=0
    return dict(a=a,c=c,p=p,q=q,terms=N)

if __name__=='__main__':
    cases=[]
    for a in (42,43,44,75,100,101,200,201,202):
        for sign in (-1,1):cases.append((a,5*a+sign))
    for k,d,b in ((41,2,1),(42,2,1),(43,2,1),(44,3,1),(45,3,2),
                  (46,5,1),(47,5,4),(60,7,3),(101,2,1),(201,2,1)):
        a=k*d+b
        for sign in (-1,1):cases.append((a,5*a+sign*d))
    out=[]
    for a,c in cases:
        row=one(a,c);out.append(row);print(row,flush=True)
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All independent comparisons passed:',len(out),'games,',sum(r['terms'] for r in out),'terms.')
