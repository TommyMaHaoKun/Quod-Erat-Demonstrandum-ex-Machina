"""Uniform interval-domain contradiction certificates under pure-period constraints.
No SG term generation. Endpoints are exact affine functions b+g*t.
"""
from fractions import Fraction as Q
from itertools import product
from functools import lru_cache
from bisect import bisect_right
import json
Z=(Q(0),Q(0)); A=(Q(1),Q(0))
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def neg(x):return(-x[0],-x[1])
def sub(x,y):return add(x,neg(y))
def ev(x,t):return x[0]+x[1]*t
def const(x):return(Q(x),Q(0))
MEX=[]
for opts in product(range(4),repeat=3):
 v=0
 while v in opts:v+=1
 MEX.append((v,*opts))
TABLES={'mex':MEX,'fer':[(x,y)for x in range(4)for y in range(4)if(x==0)==(y==1)],'ne':[(x,y)for x in range(4)for y in range(4)if x!=y]}
@lru_cache(None)
def support(kind,masks):
 out=[0]*len(masks)
 for tup in TABLES[kind]:
  if all(d&(1<<v)for d,v in zip(masks,tup)):
   for i,v in enumerate(tup):out[i]|=1<<v
 return tuple(out)

class Trace:
 """Validate every ordering on a complete parameter interval or singleton."""
 def __init__(self,left,right):
  self.lower=Q(left);self.upper=Q(right);self.t=(self.lower+self.upper)/2
  self.point=self.lower==self.upper;self.comparisons=0
 def ordered(self,ends):
  ends=sorted(set(ends),key=lambda e:(ev(e,self.t),e))
  ans=[]
  for e in ends:
   if ans:
    d=sub(e,ans[-1]);v=ev(d,self.t);self.comparisons+=1
    if v==0:
     assert self.point, ('unresolved crossing',self.lower,self.upper,ans[-1],e)
     continue
    assert v>0
    if not self.point:
     dl=ev(d,self.lower);du=ev(d,self.upper)
     assert dl>=0 and du>=0 and (dl>0 or du>0), ('invalid uniform order',self.lower,self.upper,d)
   ans.append(e)
  return ans

def refine(dom,kind,offsets,tr):
 t=tr.t;lo=dom[0][0];hi=dom[-1][1]
 ends=[e for l,h,m in dom for e in(l,h)]
 cuts=tr.ordered([sub(e,s)for e in ends for s in offsets])
 starts=[ev(l,t)for l,h,m in dom]
 def at(x):return dom[bisect_right(starts,ev(x,t))-1][2]
 updates=[]
 for l,h in zip(cuts,cuts[1:]):
  if any(ev(add(l,s),t)<ev(lo,t) or ev(add(h,s),t)>ev(hi,t)for s in offsets):continue
  mid=((l[0]+h[0])/2,(l[1]+h[1])/2)
  masks=tuple(at(add(mid,s))for s in offsets)
  supported=support(kind,masks)
  for s,old,new in zip(offsets,masks,supported):
   if old!=new:updates.append((add(l,s),add(h,s),new))
 if not updates:return dom,None
 cuts=tr.ordered(ends+[e for l,h,m in updates for e in(l,h)])
 newdom=[]
 for l,h in zip(cuts,cuts[1:]):
  if ev(l,t)<ev(lo,t)or ev(h,t)>ev(hi,t):continue
  mid=((l[0]+h[0])/2,(l[1]+h[1])/2);x=ev(mid,t)
  mask=at(mid)
  for p,q,m in updates:
   if ev(p,t)<=x<ev(q,t):mask &=m
  if mask==0:return dom,dict(kind=kind,interval=[l,h],original_mask=at(mid),updates=len(updates))
  if newdom and newdom[-1][2]==mask:newdom[-1]=(newdom[-1][0],h,mask)
  else:newdom.append((l,h,mask))
 return newdom,None

def prove(left,right,band=5,window=8,passes=3):
 tr=Trace(left,right);t=tr.t;c=(Q(band),Q(1))
 dom=[(const(-window),Z,15)]+[(const(i),const(i+1),1<<v)for i,v in enumerate([0,1,0,1,2])]
 if band==5:dom.append((const(5),c,1))
 relations=[('fer',[Z,A])]+[('ne',[Z,s])for s in(A,const(4),c)]+[('mex',[Z,neg(A),const(-4),neg(c)])]
 counts=[]
 for p in range(passes):
  old=dom
  for kind,offs in relations:
   dom,bad=refine(dom,kind,offs,tr)
   if bad:
    return dict(t=str(t),band=band,window=window,proved=True,passes=p+1,relation=kind,
      contradiction=[[str(x)for x in e]for e in bad['interval']],
      valid=(str(t),str(t))if tr.point else(str(tr.lower),str(tr.upper)),point=tr.point,comparisons=tr.comparisons,cells=len(dom))
  counts.append(len(dom))
  if dom==old:break
 return dict(t=str(t),band=band,window=window,proved=False,passes=p+1,valid=(str(t),str(t))if tr.point else(str(tr.lower),str(tr.upper)),point=tr.point,comparisons=tr.comparisons,cells=len(dom),counts=counts)

def main():
 cases=[]
 for band,parts in [
   (4,[(Q(1,2),Q(1,2)),(Q(1,2),Q(2,3)),(Q(2,3),Q(2,3)),(Q(2,3),Q(1))]),
   (5,[(Q(0),Q(1,3)),(Q(1,3),Q(1,3)),(Q(1,3),Q(1,2)),
       (Q(1,2),Q(1,2)),(Q(1,2),Q(2,3)),(Q(2,3),Q(2,3)),(Q(2,3),Q(1))])]:
  for left,right in parts:
   result=prove(left,right,band)
   assert result['proved'],result
   cases.append(result)
   print(result)
 from pathlib import Path
 Path(__file__).with_suffix('.json').write_text(json.dumps(dict(
  window='[-8,c) in band5; [-8,5) in band4',
  proved_domains={'4':'[1/2,1)','5':'(0,1)'},cases=cases),indent=2)+'\n')
 print('All 11 affine contradiction certificates passed.')

if __name__=='__main__':main()
