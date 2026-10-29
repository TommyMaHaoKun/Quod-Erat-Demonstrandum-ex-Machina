"""Uniform lower half-strip column formula: finite proof obligations.

No finite-game solver or discovered SG word is used. See the paper, Section 7 and Appendix C
for the reduction from unbounded column index to the checked finite set.
"""
import json
from pathlib import Path

B='01012323';A='01012';T='01201012'
PERIOD=40
STEP=20

def prefix(m,s):
    if s==0:return B*(2*m)+A*(2*m)+'01'
    if s==1:return B*(2*m+1)+'013'+A*(2*m+1)
    if s==2:return B*(2*m+1)+'0101232'+A*(2*m+1)+'01'
    raise ValueError(s)

def templates(s):
    """(pattern, repetition-count affine coefficients in m)."""
    if s==0:return [(B,(2,0)),(A,(2,0)),('0',(0,1)),('1',(0,1))]
    if s==1:return [(B,(2,1))]+[(v,(0,1)) for v in '013']+[(A,(2,1))]
    if s==2:return [(B,(2,1))]+[(v,(0,1)) for v in '0101232']+[(A,(2,1)),('0',(0,1)),('1',(0,1))]
    raise ValueError(s)

def boundaries(s,delta=0,shift=0):
    cur=(0,shift);out=[cur]
    for pattern,(u,v) in templates(s):
        assert PERIOD%len(pattern)==0
        cur=(cur[0]+len(pattern)*u,cur[1]+len(pattern)*(v+u*delta))
        out.append(cur)
    assert all((a*STEP)%PERIOD==0 for a,b in out)
    return out

def value(H,y):
    assert y>=0
    return int(H[y]) if y<len(H) else int(T[(y-len(H))%8])

def check(m,s):
    H=prefix(m,s)
    assert len(H)==26*m+(2,16,22)[s]
    if s==0 and m==0:old=None
    elif s==0:old=prefix(m-1,2)
    else:old=prefix(m,s-1)
    count=0
    # The special x=0 option is the bulk omega stream, rather than the
    # preceding column's rho tail. Its first fully periodic target row is
    # Q_0+4=6, so check all eight phases y=6,...,13 explicitly.
    horizon=len(H)+12 if old is None else len(H)+8
    for y in range(horizon):
        opts={value(H,y-d) for d in (1,4) if y>=d}
        if old is None:
            if y>=4:opts.add(int(B[(y-4)%8]))
        elif y>=5:opts.add(value(old,y-5))
        v=value(H,y)
        assert v not in opts and all(j in opts for j in range(v)),(m,s,y,v,opts)
        count+=1
    # At y>=Q_j+4 all operands are in period-eight segments. For j>0,
    # their common rho phases satisfy the token identity identically.
    # For j=0 the complete eight-phase block was checked explicitly.
    assert old is None or len(old)+5<=len(H)
    return count

def main():
    report=[]
    for s in range(3):
        lines=[]
        for shift in (0,1,4):lines+=boundaries(s,0,shift)
        lines+=boundaries((s-1)%3,-1 if s==0 else 0,5)
        lines.append((26,(2,16,22)[s]+8))
        constants=[b for a,b in lines]
        slopes=sorted({a for a,b in lines})
        gap=min(b-a for a,b in zip(slopes,slopes[1:]))
        L,U=min(constants),max(constants)
        K=max(1,(U-L+PERIOD+gap-1)//gap)
        assert gap*K-(U-L)>=PERIOD
        assert all((a*STEP)%PERIOD==0 for a,b in lines)
        cells=sum(check(m,s) for m in range(K+STEP))
        report.append(dict(residue=s,minimum_intercept=L,maximum_intercept=U,
                           slope_gap=gap,K=K,modulus=STEP,
                           m_checked=[0,K+STEP-1],positions=cells))
    path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(report,indent=2)+'\n')
    print('Uniform lower half-strip proved:',sum(r['positions'] for r in report),'positions;',report)

if __name__=='__main__':main()
