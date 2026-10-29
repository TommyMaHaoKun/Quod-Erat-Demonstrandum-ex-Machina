"""Independent checker for minor_far_sharp certificates.

No generator import. It uses 24-bit factor bounds (generator: 20 bits), checks
saved square-root bounds by multiplication, and audits dyadic coverage.
"""
if not __debug__:
    raise RuntimeError("Run this proof checker without Python -O.")
from fractions import Fraction as Q
from math import factorial
import argparse, gzip, hashlib, json, time
from pathlib import Path


def require(value,message):
    if not value:raise ArithmeticError(message)


def independent_constants(k,X):
    low=Q(3141592653589793,10**15)
    high=Q(3141592653589794,10**15)
    def enclosure(q,N):
        positive=Q(0);negative=Q(0)
        for r in range(N):
            term=Q(1,(2*r+1)*q**(2*r+1))
            if r%2:negative+=term
            else:positive+=term
        endpoint=positive-negative
        other=endpoint+(-1)**N*Q(1,(2*N+1)*q**(2*N+1))
        return sorted((endpoint,other))
    e5=enclosure(5,32);e239=enclosure(239,12)
    require(low<16*e5[0]-4*e239[1],"pi lower endpoint")
    require(16*e5[1]-4*e239[0]<high,"pi upper endpoint")
    grid=[]
    for i in range(1025):
        if i==0:value=Q(0)
        elif i==1024:value=Q(1)
        else:
            y=Q(i,2048)
            positive=sum(((low*y)**p/factorial(p) for p in (1,5,9)),Q(0))
            negative=sum(((high*y)**p/factorial(p) for p in (3,7,11)),Q(0))
            value=positive-negative
            require(value>=0,"negative sine lower endpoint")
        grid.append(value.numerator*2**40//value.denominator)
    hyp=[]
    for j in range(1,3*X//2+1):
        u=Q(j**k,2*X**k)
        initial=sum((u**p/factorial(p) for p in range(1,42,2)),Q(0))
        ratio=u*u/(44*45)
        require(ratio<1,"hyperbolic sine geometric ratio")
        upper=initial+(u**43/factorial(43))/(1-ratio)
        hyp.append((upper.numerator*2**60+upper.denominator-1)//upper.denominator)
    return grid,hyp


def verify(path):
    start=time.monotonic()
    with gzip.open(path,"rt",encoding="utf-8") as f:data=json.load(f)
    require(data["method_version"]==3,"certificate version")
    k=data["k"];X=data["X"]
    require(k in (4,5,6) and isinstance(X,int) and X>=15,"parameter domain")
    require(data["delta"]==str(Q(1,6**k)),"delta")
    require(data["scaling_exponent"]=="7/2","scaling exponent")
    rows=data["partition"]
    require(len(rows)==data["leaves"],"leaf count")
    require(bool(rows),"empty partition")
    depth=max(row[0] for row in rows)
    require(depth<200,"unreasonable dyadic depth")
    for row in rows:
        require(len(row)==5 and all(isinstance(v,int) for v in row),"row encoding")
        level,index,z,exponent,stored_strong=row
        require(0<=level<=depth and 0<=index<2**level,"dyadic index")
        require(z>0 and exponent>=level,"positive reciprocal upper bound")
    intervals=sorted(((index<<(depth-level),(index+1)<<(depth-level))
                      for level,index,_,_,_ in rows))
    last=0
    for a,b in intervals:
        require(a==last and b>a,"coverage gap or overlap")
        last=b
    require(last==2**depth,"incomplete terminal coverage")
    grid,hyp=independent_constants(k,X)
    B=44*6**k;W=B//2-7
    totals=[Q(0),Q(0),Q(0)]
    min_strong=len(hyp)
    for number,(level,index,z,exponent,_) in enumerate(rows,1):
        D=B*2**level
        L=7*2**level+index*W
        U=L+W
        P=1;strong=0
        for j,sh in enumerate(hyp,1):
            aa=L*j**k;bb=U*j**k
            # Independent closed-interval integer containment test.
            if (aa+D-1)//D<=bb//D:
                distance=0
            else:
                distance=min(aa%D,D-bb%D)
            pos=2048*distance//D
            if pos==1024:
                sine_num=D*2**40
            else:
                rem=2048*distance-pos*D
                sine_num=(D-rem)*grid[pos]+rem*grid[pos+1]
            numer=sine_num*2**20
            denom=D*sh
            factor=2**24*numer*numer//(denom*denom)
            P*=2**24+factor
            if factor>=7*2**24:strong+=1
        require(strong>=4,"insufficient scaling exponent")
        min_strong=min(min_strong,strong)
        require(z*z*P>=2**(24*len(hyp)+2*(exponent-level)),"invalid reciprocal square-root upper bound")
        for m in range(3):
            totals[m]+=Q(z*U**m,2**(exponent+m*level))
        if number%100000==0:
            print(json.dumps({"file":path.name,"verified_leaves":number}),flush=True)
    scales=[Q(44*W,7*B)*Q(44,7*B)**m for m in range(3)]
    moments=[scales[m]*totals[m] for m in range(3)]
    require([str(v) for v in moments]==data["moments"],"saved moment mismatch")
    require(data["success"] and data["bad_scaling_cells"]==0,"unfinished certificate")
    require(moments[2]<=Q(data["target_moment2"]),"target moment not reached")
    return {"certificate":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "k":k,"X":X,"leaves":len(rows),"maximum_depth":depth,
            "minimum_strong_factors":min_strong,"moments":[str(v) for v in moments],
            "moments_display":[float(v) for v in moments],"verified":True,
            "seconds":round(time.monotonic()-start,3)}


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("paths",nargs="*")
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args()
    base=Path(__file__).resolve().parents[1]
    paths=[Path(p) for p in args.paths] if args.paths else [base/"certificates"/f"minor_far_sharp_k{k}_x{x}.json.gz" for k,x in ((4,18),(5,15),(6,15))]
    outcomes=[verify(p) for p in paths]
    if args.write:
        dest=base/"certificates"/"minor_far_verification.json"
        dest.write_text(json.dumps(outcomes,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(outcomes,indent=2),flush=True)
