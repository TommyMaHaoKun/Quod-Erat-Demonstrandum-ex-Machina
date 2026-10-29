"""Independent exact checker of open affine cones, using sorted boundaries.

For each proposed open cone, every adjacent boundary-order inequality is
checked at both endpoints. Linearity proves the entire arrangement is fixed.
Mex, least period, and the final prefix mismatch are then checked exactly.
The source is a proposed word; no ordering assertions from discovery are used.
"""
from fractions import Fraction as Q
from bisect import bisect_right
from pathlib import Path
import json

def add(x,y):return (x[0]+y[0],x[1]+y[1])
def sub(x,y):return (x[0]-y[0],x[1]-y[1])
def ev(x,t):return x[0]+x[1]*t

def check(row):
    lo,hi=Q(row['lo']),Q(row['hi']);t=(lo+hi)/2
    assert lo<hi and not row.get('singleton',False)
    H=[(v,tuple(x)) for v,x in row['prefix']]
    W=[(v,tuple(x)) for v,x in row['period']]
    q,P=tuple(row['q']),tuple(row['p']);c=(row['base'],1)
    def length(word):
        out=(0,0)
        for _,z in word:out=add(out,z)
        return out
    assert length(H)==q and length(W)==P
    assert all(isinstance(i,int) for v,x in H+W for i in x)
    assert all(0<=v<=3 for v,x in H+W)
    assert ev(q,lo)>0 and ev(q,hi)>0
    copies=2 if P[0]>c[0] else 3
    runs=[];cur=(0,0)
    for v,z in H+W*copies:
        assert ev(z,lo)>=0 and ev(z,hi)>=0 and ev(z,t)>0
        end=add(cur,z);runs.append((cur,end,v));cur=end
    M=cur
    for x in (lo,hi):assert ev(M,x)>=ev(add(add(q,c),P),x)
    moves=((0,0),(1,0),(4,0),c)
    lines={(0,0),M}
    for l,h,_ in runs:
        for x in (l,h):
            for s in moves:lines.add(add(x,s))
    lines=sorted(lines,key=lambda x:(ev(x,t),x))
    for a,b in zip(lines,lines[1:]):
        for x in (lo,hi):assert ev(a,x)<=ev(b,x),((row['base'],row['lo'],row['hi']),'crossing',a,b,x)
    # Distinct affine lines cannot tie at an interior point after this check.
    assert len({ev(x,t) for x in lines})==len(lines)
    starts=[ev(l,t) for l,h,v in runs];end=ev(M,t)
    boundaries=[ev(x,t) for x in lines if 0<=ev(x,t)<=end]
    def at(x):
        assert 0<=x<end
        return runs[bisect_right(starts,x)-1][2]
    cells=0
    for a,b in zip(boundaries,boundaries[1:]):
        x=(a+b)/2;v=at(x)
        opts={at(x-ev(s,t)) for s in moves[1:] if ev(s,t)<=x}
        assert v not in opts and all(i in opts for i in range(v)),((row['base'],row['lo'],row['hi']),a,b,v,opts)
        cells+=1
    # Circular runs: merge the seam if the first and last labels agree.
    circle=list(W)
    if circle[0][0]==circle[-1][0]:
        circle[0]=(circle[0][0],add(circle[0][1],circle[-1][1]));circle.pop()
    assert all(circle[i][0]!=circle[(i+1)%len(circle)][0] for i in range(len(circle)))
    exceptions=set();identity_shifts=[];n=len(circle)
    assert n>1
    for shift in range(1,n):
        if any(circle[i][0]!=circle[(i+shift)%n][0] for i in range(n)):continue
        root=None;possible=True
        for i in range(n):
            b,g=sub(circle[i][1],circle[(i+shift)%n][1])
            if not g:
                if b:possible=False;break
            else:
                z=Q(-b,g)
                if root is None:root=z
                elif root!=z:possible=False;break
        if possible:
            if root is None:identity_shifts.append(shift)
            elif lo<root<hi:exceptions.add(root)
    assert not identity_shifts and not exceptions,((row['base'],row['lo'],row['hi']),identity_shifts,exceptions)
    # H is cut at its exact earliest index: preceding letters differ from
    # the backward periodic extension throughout this open cone.
    assert H and H[-1][0]!=W[-1][0]
    return dict(lo=str(lo),hi=str(hi),p=P,q=q,cells=cells,
                prefix_runs=len(H),period_runs=len(W),
                recurrence=True,primitive=True,earliest=True)

if __name__=='__main__':
    here=Path(__file__).resolve().parents[1]/'certificates'
    out=[]
    for row in json.loads((here/'atlas.json').read_text()):
        ans=check(row);ans['base']=row['base'];out.append(ans)
    (here/'atlas_verified.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All',len(out),'open cones proved;',sum(x['cells'] for x in out),'position cells.')
