"""Exact affine-endpoint proof tables for c=(5k+4)a+r, k>=1, 0<r<a.

Endpoints are represented by (A,R), meaning A*a+R*r.  Their ordering
is proved on the whole cone a>0, 0<r<a by endpoint inequalities.
No sampled parameter value is used to establish an inequality.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def add(x,y):return tuple(i+j for i,j in zip(x,y))
def neg(x):return tuple(-i for i in x)
def sub(x,y):return add(x,neg(y))
def scale(x,t):return tuple(i*t for i in x)
def positive(x):
    # A+R*t >= 0 on [0,1], with strict positivity on (0,1).
    A,R=x
    return A>=0 and A+R>=0 and (A>0 or A+R>0)
def less(x,y):return positive(sub(y,x))
def key(x):return x[0]*F(1)+x[1]*F(1,3)
def word(items,start=(0,0)):
    out=[];pos=start
    for value,length in items:
        end=add(pos,length)
        assert less(pos,end)
        out.append((pos,end,value));pos=end
    return out
def shifted(runs,delta):
    # Function x -> runs(x+delta).
    return [(sub(l,delta),sub(r,delta),v) for l,r,v in runs]
def value(runs,x):
    found=[v for l,r,v in runs if less(l,x) and less(x,r)]
    assert len(found)==1,(x,found)
    return found[0]
def tex(x):
    A,R=x
    if x==(0,0):return '0'
    text=''
    for coefficient,symbol in ((A,'a'),(R,'r')):
        if not coefficient:continue
        if text and coefficient>0:text+='+'
        if coefficient==-1:text+='-'
        elif coefficient!=1:text+=str(coefficient)
        text+=symbol
    return text
def table(name,domain,functions):
    lo,hi=domain
    endpoints={lo,hi}
    for runs in functions:
        for l,r,_ in runs:
            for e in (l,r):
                if (e==lo or less(lo,e)) and (e==hi or less(e,hi)):
                    endpoints.add(e)
    endpoints=sorted(endpoints,key=key)
    rows=[]
    for l,r in zip(endpoints,endpoints[1:]):
        assert less(l,r),('order not valid throughout cone',l,r)
        midpoint=scale(add(l,r),F(1,2))
        vals=[value(f,midpoint) for f in functions]
        expected=0
        while expected in vals[1:]:expected+=1
        assert vals[0]==expected,(name,l,r,vals)
        rows.append([tex(l),tex(r),*vals])
    return rows

Bitems=[(0,(1,0)),(1,(1,0)),(0,(1,0)),(1,(1,0)),(2,(1,0))]
Ditems=[(3,(0,1)),(0,(1,-1)),(2,(0,1)),(1,(1,-1)),(3,(0,1)),
        (0,(1,0)),(1,(1,0)),(2,(1,-1)),(3,(0,1))]
Aitems=[(0,(1,0)),(1,(1,0)),(2,(0,1)),(0,(1,0)),(1,(1,0)),(2,(1,0))]
B=[]
for m in range(-3,5):B+=word(Bitems,(5*m,0))
D=word(Ditems)
left_and_D=word(Bitems,(-5,0))+D
early=shifted(D,(5,1))+word(Bitems)+word(Bitems,(5,0))
H=word(Bitems,(-5,0))+word(Aitems)+word(Bitems,(5,1))
tables={
 'Transient':table('D',((0,0),(5,1)),[D,shifted(left_and_D,(-1,0)),shifted(left_and_D,(-4,0)),shifted(B,(1,-1))]),
 'Early tail':table('early',((0,0),(4,0)),[B,shifted(early,(-1,0)),shifted(early,(-4,0)),shifted(B,(1,0))]),
 'Late tail':table('late',((0,0),(5,1)),[shifted(H,(-1,0)),shifted(H,(-2,0)),shifted(H,(-5,0)),D]),
}

def main():
    dest=Path('data');dest.mkdir(exist_ok=True)
    (dest/'affine_tables.json').write_text(json.dumps(tables,indent=2),encoding='utf-8')
    out=[]
    for name,rows in tables.items():
        out.append('\\subsection*{'+name+'}')
        out.append('\\begin{longtable}{cc|c|ccc}\\toprule')
        out.append('$\\ell$ & $h$ & $F(n)$ & $F(n-a)$ & $F(n-4a)$ & $F(n-c)$\\\\ \\midrule\\endhead')
        for l,r,*vals in rows:
            out.append(f'${l}$ & ${r}$ & '+' & '.join(map(str,vals))+r'\\')
        out.append('\\bottomrule\\end{longtable}')
    (dest/'affine_tables.tex').write_text('\n'.join(out),encoding='utf-8')
    print({name:len(rows) for name,rows in tables.items()})
if __name__=='__main__':main()
