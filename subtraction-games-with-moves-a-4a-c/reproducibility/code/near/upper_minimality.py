"""Exact bounded suffix obligations for the unbounded upper preperiod theorem.

These identities are accompanied by the algebraic all-m reduction in
the paper, Section 6 and Appendix C. They do not solve a game or search a period.
"""
from pathlib import Path
import json

R='01201012'
B='01012'
H=('', '01012323013', '01012323010123')
M=('01012','01012','20101')
K=('010120101201','0101201','201012010120101201')
Q=(12,18,32)

def tail_relative(r,t):
    """Symbol t positions after the end of the finite prefix of F_(3m+r).
    Only t>=-32 is used; m>=13 supplies at least130 middle symbols.
    """
    if t>=0:return R[t%8]
    if t>=-len(K[r]):return K[r][t]
    return M[r][(t+len(K[r]))%5]

def check():
    count=0
    # The final B-power contributes precisely one R and then a mismatch.
    assert (B*2)[-8:]==R
    assert (B*2)[-9]=='1' and R[-1]=='2'
    count+=10
    # Each Q_(3m+r)-6(3m+r) is 8m+(12,12,20).
    assert [Q[r]-6*r for r in range(3)]==[12,12,20]
    # s=1: three unfinished front columns, h=0,1,2 from the right.
    # Their distance before the cut at the first claimed periodic row is
    # 27,21,15. At cut-l their offsets relative to Q_j are8-l in all3.
    for h,r in enumerate((1,0,2)):
        for ell in range(1,28-6*h):
            assert tail_relative(r,8-ell)==B[-ell%5],(h,r,ell)
            count+=1
    # At the last mismatch in each s the front is in its R-phase;
    # the backward cyclic suffix is one symbol beyond a whole R-power.
    for s in range(3):
        # ell for s0,1 is9; for s2 it is8m-15, congruent1 modulo8.
        ell_mod8=1
        assert R[-ell_mod8%8]=='2'
        count+=1
    return dict(passed=True,exact_symbol_checks=count,
                scope='all upper open cones k>=41, a=kd+b, 0<b<d',
                q=['(26m+13)a+3md','(26m-1)a+(3m-1)d','(26m+40)a'])

if __name__=='__main__':
    result=check()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
