"""Uniform proof obligations for the lower integer-ratio seam splice.

See the paper, Section 7 and Appendix C. All candidate words are explicit; no state search is used.
"""
from pathlib import Path
import json
from halfstrip_certificate import B,A,T,prefix,value,templates,boundaries

STEP=20;PERIOD=40
add=lambda x,y:(x[0]+y[0],x[1]+y[1])
ev=lambda x,h:x[0]*h+x[1]

def params(h,s):
    a=3*h+s;P=6*a-1;D=16*h+(4,12,15)[s];shift=10*h+(-19,-5,1)[s]
    W=T*(h-2)+A*(2*h+3) if s==0 else T*h+A*(2*h+1) if s==1 else T*h+'012012'+A*(2*h+1)
    assert len(W)==P
    return a,P,D,shift,W

def wbound(s):
    cur=(0,0);out=[cur]
    chunks=[(T,(1,-2)),(A,(2,3))] if s==0 else [(T,(1,0)),(A,(2,1))] if s==1 else [(T,(1,0))]+[(v,(0,1)) for v in '012012']+[(A,(2,1))]
    for pat,(u,v) in chunks:
        assert PERIOD%len(pat)==0
        cur=add(cur,(len(pat)*u,len(pat)*v));out.append(cur)
    assert cur==(18,6*s-1)
    return out

def symbolic_bounds(s):
    P=(18,6*s-1);D=(16,(4,12,15)[s]);shift=(10,(-19,-5,1)[s]);cross=(18,6*s-6)
    wb=[]
    for j in range(-2,6):
        for x in wbound(s):wb.append((x[0]+j*P[0]-shift[0],x[1]+j*P[1]-shift[1]))
    g0=[(0,0),(0,1),(0,2),D]+wb
    left=boundaries(2,-1,0) if s==0 else boundaries(s-1,0,0)
    left+=[add(D,cross)]+[add(x,cross) for x in wb]
    lines=[(0,0),add(add(D,P),(0,10)),((26,16,16)[s],(4,0,11)[s])]
    for shift_y in (0,1,4,-5):lines += [add(x,(0,shift_y)) for x in g0]
    for shift_y in (0,4):lines += [add(x,(0,shift_y)) for x in left]
    assert all((a*STEP)%PERIOD==0 for a,b in lines)
    # The finite cycle list covers every tail argument in the checked horizon,
    # including negative coordinates of the left column's periodic extension.
    def nonnegative_for_h_ge_3(x,strict=False):
        assert x[0]>=0 and ev(x,3)>=(1 if strict else 0)
    # -5-cross+shift >= -2P and D+P+15+shift < 5P.
    nonnegative_for_h_ge_3((2*P[0]-cross[0]+shift[0],2*P[1]-5-cross[1]+shift[1]))
    nonnegative_for_h_ge_3((4*P[0]-D[0]-shift[0],4*P[1]-D[1]-15-shift[1]),True)
    return lines

def check_boundary(h,s):
    a,P,D,shift,W=params(h,s);V=prefix(*divmod(a-1,3));V0=prefix(0,0)
    w=lambda z:int(W[(z+shift)%P])
    g0=lambda y:value(V0,y) if y<D else w(y)
    left=lambda y:value(V,y) if y-6*(a-1)<D else w(y-6*(a-1))
    M=D+P+10
    for y in range(M):
        opts={g0(y-d) for d in (1,4) if y>=d}
        if y>=4:opts.add(left(y-4))
        v=g0(y)
        assert v not in opts and all(j in opts for j in range(v)),('boundary',h,s,y,v,opts)
    last=max(y for y in range(M) if left(y)!=g0(y+5))
    assert last==(26*h+3,16*h-1,16*h+10)[s],('last',h,s,last)
    # All columns are in their T phase for the splice's narrow join zone.
    assert D-4>=8*h+10
    f=lambda z:int(T[(z-2)%8]) if z<D else w(z)
    for z in range(D-1,D+4):
        opts={f(z-1),f(z-4),f(z+1)};v=f(z)
        assert v not in opts and all(j in opts for j in range(v)),('join',h,s,z)
    return M

def check_column_difference(m,s):
    H=prefix(m,s);J=prefix(m+1,0) if s==2 else prefix(m,s+1)
    M=max(len(H),len(J))+8
    last=max(y for y in range(M) if value(H,y)!=value(J,y+6))
    assert last==(16*m+4,26*m+15,16*m+13)[s],(m,s,last)
    return M

def main():
    report=[]
    for s in range(3):
        lines=symbolic_bounds(s);L=min(b for a,b in lines);U=max(b for a,b in lines)
        slopes=sorted({a for a,b in lines});gap=min(y-x for x,y in zip(slopes,slopes[1:]))
        K=max(3,(U-L+PERIOD+gap-1)//gap)
        assert gap*K-(U-L)>=PERIOD
        count=sum(check_boundary(h,s) for h in range(3,K+STEP))
        report.append(dict(kind='wrap_and_splice',residue=s,L=L,U=U,slope_gap=gap,K=K,h_checked=[3,K+STEP-1],positions=count))
    for s in range(3):
        lines=boundaries(s,0,0)+boundaries((s+1)%3,1 if s==2 else 0,-6)
        lines += [(26,(2,16,22)[s]+8),(26, (2,16,22)[(s+1)%3]+(26 if s==2 else 0)+8),((16,26,16)[s],(5,16,14)[s])]
        L=min(b for a,b in lines);U=max(b for a,b in lines);slopes=sorted({a for a,b in lines});gap=min(y-x for x,y in zip(slopes,slopes[1:]))
        K=max(1,(U-L+PERIOD+gap-1)//gap)
        count=sum(check_column_difference(m,s) for m in range(K+STEP))
        report.append(dict(kind='interior_last_mismatch',residue=s,L=L,U=U,slope_gap=gap,K=K,m_checked=[0,K+STEP-1],positions=count))
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Uniform lower seam obligations passed:',sum(r['positions'] for r in report),'positions;',report)

if __name__=='__main__':main()
