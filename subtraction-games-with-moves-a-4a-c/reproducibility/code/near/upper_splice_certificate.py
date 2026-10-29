"""Exact finite obligations for the upper integer seams c=5a+1.
Includes a self-contained certificate for the upper half-strip column formula.
No state search and no game recurrence sampling replaces the affine proof.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

BULK='01012323'; R='01201012'; B='01012'; A='012'
H=['','01012323013','01012323010123']
M=['01012','01012','20101']
K=['010120101201','0101201','201012010120101201']
Q=[12,18,32]
assert [len(H[r])+len(K[r]) for r in range(3)]==Q

def front_value(x,y):
    if y<0:return None
    m,r=divmod(x,3)
    blocks=[(BULK,2*m),(H[r],1),(M[r],2*m),(K[r],1)]
    for w,n in blocks:
        if y<len(w)*n:return int(w[y%len(w)])
        y-=len(w)*n
    return int(R[y%8])

def fnear(r,u,s,delta):
    # x=3m+r, a=3j+s, u=j-m. At y=6x+H_a+delta.
    h=20 if s==0 else 12
    off=8*u+6*r+h+delta-Q[r]
    assert off>=-len(K[r]),(r,u,s,delta,off)
    return int(K[r][off] if off<0 else R[off%8])

def mex(values):
    z=0
    while z in values:z+=1
    return z

def interface_checks():
    count=0
    for s,r,u in product(range(3),range(3),range(4)):
        # x<a iff 3u+s-r>=1. x>0 can be arranged with large j.
        if 3*u+s-r<1:continue
        for d in range(-1,4):
            def val(r0,u0,delta):
                return fnear(r0,u0,s,delta) if delta<0 else int(B[(-8+delta)%5])
            got=val(r,u,d)
            opts=[val(r,u,d-1),val(r,u,d-4)]
            pr,pu=(r-1,u) if r else (2,u+1)
            opts.append(val(pr,pu,d+1))
            assert got==mex(opts),(s,r,u,d,got,opts)
            count+=1
    # For u>=3 all fnear offsets are >=0, and adding one to u adds8:
    # therefore u=3 checks every larger u too.
    for s,r,d in product(range(3),range(3),range(-5,5)):
        assert 8*3+6*r+(20 if s==0 else 12)+d-Q[r]>=0
    return count

# Affine endpoints are (coefficient of j, constant).
def add(x,y):return x[0]+y[0],x[1]+y[1]
def at(x,j):return x[0]*j+x[1]
def shift(x,v):return x[0],x[1]+v

def segments(parts):
    # A part (word, affine repetition count), constant words are expanded
    # into single-character cells so all segment periods divide40.
    ans=[];pos=(0,0)
    for w,(u,v) in parts:
        if not w:continue
        if (u,v)==(0,1):
            for ch in w:
                end=add(pos,(0,1));ans.append((pos,end,ch));pos=end
        else:
            end=add(pos,(len(w)*u,len(w)*v));ans.append((pos,end,w));pos=end
    return ans,pos

def templates(s):
    # Z is the spliced column0 through y<H_a+6a, with 9 unused extra chars.
    zparts=[(K[0],(0,1)),(R,(2,-1 if s==0 else 0))]
    if s==2:zparts.append((A+A,(0,1)))
    zparts.append((B,(2,5 if s==0 else 3)))
    Z,Zend=segments(zparts)
    # x=a-1 -> (m,r)=(j-1,2),(j,0),(j,1).
    dr,r=[(-1,2),(0,0),(0,1)][s]
    fparts=[(BULK,(2,2*dr)),(H[r],(0,1)),(M[r],(2,2*dr)),(K[r],(0,1)),(R,(10,10))]
    F,Fend=segments(fparts)
    stop=(26,[20,18,24][s])
    assert Zend==add(stop,(0,9))
    return Z,F,stop

def lookup(ss,n,j):
    for l,r,w in ss:
        if at(l,j)<=n<at(r,j):return int(w[(n-at(l,j))%len(w)])
    raise AssertionError(('missing',n,j))

def ordered_endpoints(s):
    Z,F,stop=templates(s)
    cuts={(0,0),(0,1),(0,4),(0,6),stop}
    for ss,ds in ((Z,(0,1,4)),(F,(6,))):
        for l,r,w in ss:
            assert 40%len(w)==0
            for d in ds:cuts.add(shift(l,d));cuts.add(shift(r,d))
    # Clip at0/stop. F's artificial far end is safely past stop for all j>=3.
    cuts=[x for x in cuts if 0<=at(x,20)<=at(stop,20)]
    cuts.sort(key=lambda x:at(x,20))
    assert cuts[0]==(0,0) and cuts[-1]==stop
    for l,r in zip(cuts,cuts[1:]):
        da,db=r[0]-l[0],r[1]-l[1]
        assert da>=0 and at(r,20)>at(l,20),(s,l,r)
        if da:assert at(r,20)-at(l,20)>=40,(s,l,r)
    # Clipping is stable: every omitted cut is below0 or above stop at j20
    # with slope difference preserving that order thereafter.
    allcuts={(0,0),(0,1),(0,4),(0,6),stop}
    for ss,ds in ((Z,(0,1,4)),(F,(6,))):
        for l,r,w in ss:
            for d in ds:allcuts|={shift(l,d),shift(r,d)}
    for p in allcuts-set(cuts):
        if at(p,20)<0:assert p[0]<=0
        else:assert at(p,20)>at(stop,20) and p[0]>=stop[0]
    # All slopes relevant to covered word patterns are multiples of2, so
    # changing j by20 changes every affine endpoint by a multiple of40.
    assert all(p[0]%2==0 for p in allcuts)
    return cuts

def check_wrap_point(s,j,n):
    Z,F,stop=templates(s)
    got=lookup(Z,n,j);opts=[]
    for d in (1,4):
        if n>=d:opts.append(lookup(Z,n-d,j))
    if n>=6:opts.append(lookup(F,n-6,j))
    assert got==mex(opts),(s,j,n,got,opts)

def wrap_checks():
    count=0
    for s in range(3):
        low=4 if s==0 else 3
        Z,F,stop=templates(s)
        for j in range(low,20):
            for n in range(at(stop,j)):check_wrap_point(s,j,n);count+=1
        cuts=ordered_endpoints(s)
        for j in range(20,40):
            for l,r in zip(cuts,cuts[1:]):
                # joint period40, all endpoints retain their affine order;
                # different-slope intervals have length>=40 by j20.
                for n in range(at(l,j),min(at(r,j),at(l,j)+40)):
                    check_wrap_point(s,j,n);count+=1
    return count


def exact_q_checks():
    count=0
    # At the alleged last mismatch: s0 has (r,u)=(2,1); others(1,1).
    for s in range(3):
        r=2 if s==0 else 1
        assert fnear(r,1,s,-1)==2
        assert int(B[-9%5])==1
        count+=1
    # For residues1,2 the last2 or3 columns switch earlier in value than
    # the chosen splice. Their finite remaining negative offsets match.
    for s in (1,2):
        for i,(r,width) in enumerate([(2,7),(0,13),(1,19)][:s+1]):
            for delta in range(-width,0):
                # For these columns y-Q_x=delta. At most12 chars before K;
                # all j>=3 provide at least30 chars in the middle M-power.
                off=delta
                got=int(K[r][off]) if off>=-len(K[r]) else int(M[r][(off+len(K[r]))%5])
                want=int(B[(-8+delta)%5])
                assert got==want,(s,r,delta,got,want)
                count+=1
    return count


def front_segments(r,dm=0):
    return segments([(BULK,(2,2*dm)),(H[r],(0,1)),(M[r],(2,2*dm)),(K[r],(0,1)),(R,(20,100))])[0]

def front_checks():
    total=0
    # Exceptional boundary column x=0: known bulk enters at delay6.
    for y in range(100):
        opts=[front_value(0,y-d) for d in (1,4) if y>=d]
        if y>=6:opts.append(int(BULK[(y-6)%8]))
        assert front_value(0,y)==mex(opts)
        total+=1
    # All sequences in this exceptional check are8-periodic after y18.
    for r in range(3):
        Z=front_segments(r);F=front_segments((r-1)%3,-1 if r==0 else 0)
        stop=(26,100);cuts={(0,0),(0,1),(0,4),(0,5),stop}
        for ss,ds in ((Z,(0,1,4)),(F,(5,))):
            for l,h,w in ss:
                assert 40%len(w)==0
                for d in ds:cuts|={shift(l,d),shift(h,d)}
        allcuts=cuts.copy();cuts=sorted((p for p in cuts if 0<=at(p,20)<=at(stop,20)),key=lambda p:at(p,20))
        assert cuts[0]==(0,0) and cuts[-1]==stop
        for l,h in zip(cuts,cuts[1:]):
            da=h[0]-l[0];assert da>=0 and at(h,20)>at(l,20)
            if da:assert at(h,20)-at(l,20)>=40
        for p in allcuts-set(cuts):
            if at(p,20)<0:assert p[0]<=0
            else:assert at(p,20)>at(stop,20) and p[0]>=stop[0]
        assert all(p[0]%2==0 for p in allcuts)
        def one(m,y):
            opts=[lookup(Z,y-d,m) for d in (1,4) if y>=d]
            if y>=5:opts.append(lookup(F,y-5,m))
            assert lookup(Z,y,m)==mex(opts),(r,m,y,lookup(Z,y,m),opts)
        for m in range(1 if r==0 else 0,20):
            for y in range(at(stop,m)):one(m,y);total+=1
        for m in range(20,40):
            for l,h in zip(cuts,cuts[1:]):
                for y in range(at(l,m),min(at(h,m),at(l,m)+40)):one(m,y);total+=1
        # Beyond26m+100 every active value lies in its final R-periodic
        # segment. Its8 phases were already checked immediately before it.
        for ss,ds in ((Z,(0,1,4)),(F,(5,))):
            for d in ds:
                start=shift(ss[-1][0],d)
                assert start[0]==26 and start[1]<=92
    return total

if __name__=='__main__':
    report={'half_strip_checks':front_checks(),
            'nonwrap_interface_checks':interface_checks(),
            'uniform_wrap_checks':wrap_checks(),
            'exact_q_boundary_checks':exact_q_checks(),
            'uniform_threshold':20,'parameter_residue_period':20,
            'coordinate_period':40,'scope':'all upper seams c=5a+1 with a>=10'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
