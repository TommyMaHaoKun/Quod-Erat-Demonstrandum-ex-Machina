"""Exact adaptive certificate for weighted far-arc integrals.

Floats select refinement order and display progress only. All enclosures,
termination decisions and certificate values use integers and fractions.
"""
if not __debug__:
    raise RuntimeError("Run this proof calculation without Python -O.")
from fractions import Fraction as F
from math import factorial, isqrt
import argparse, gzip, heapq, json, time
from pathlib import Path

PI_LO=F(3141592653589793,10**15)
PI_HI=F(3141592653589794,10**15)
GRID=2048
SIN_BITS=40
SINH_BITS=60
A_BITS=20
RHO_BITS=16


def atan_bounds(q, terms):
    z=F(1,q)
    s=sum(((-1)**r*z**(2*r+1)/(2*r+1) for r in range(terms)),F(0))
    nxt=(-1)**terms*z**(2*terms+1)/(2*terms+1)
    return min(s,s+nxt),max(s,s+nxt)


def constants(k,X):
    a,b=atan_bounds(5,30)
    c,d=atan_bounds(239,10)
    assert PI_LO < 16*a-4*d <= 16*b-4*c < PI_HI
    sine=[]
    for i in range(GRID//2+1):
        if i==0: value=F(0)
        elif i==GRID//2:value=F(1)
        else:
            dl=PI_LO*F(i,GRID)
            du=PI_HI*F(i,GRID)
            value=sum((dl**(2*r+1)/factorial(2*r+1) if r%2==0 else
                       -du**(2*r+1)/factorial(2*r+1) for r in range(6)),F(0))
        sine.append((value.numerator<<SIN_BITS)//value.denominator)
    maxj=(3*X)//2
    sinh=[]
    for j in range(1,maxj+1):
        v=F(j**k,2*X**k)
        term=v
        value=term
        for r in range(1,21):
            term*=v*v/((2*r)*(2*r+1))
            value+=term
        next_term=term*v*v/(42*43)
        ratio=v*v/(44*45)
        assert ratio<1
        value+=next_term/(1-ratio)
        sinh.append(((value.numerator<<SINH_BITS)+value.denominator-1)//value.denominator)
    return sine,sinh


def cell(k,X,level,index,sine,sinh):
    base=44*6**k
    width=base//2-7
    den=base<<level
    lo=(7<<level)+index*width
    hi=lo+width
    product=1
    strong=0
    for j,sh in enumerate(sinh,1):
        a=lo*j**k; b=hi*j**k
        if a//den!=b//den:
            dist=0
        else:
            dist=min(a%den,den-b%den)
        grid_i=GRID*dist//den
        if grid_i==GRID//2:
            sin_num=(1<<SIN_BITS)*den
        else:
            sin_num=sine[grid_i]*den+(sine[grid_i+1]-sine[grid_i])*(GRID*dist-grid_i*den)
        # sin >= sin_num/(den*2^SIN_BITS); sinh <= sh/2^SINH_BITS.
        aa=(((sin_num<<(SINH_BITS-SIN_BITS))**2)<<A_BITS)//(den*sh)**2
        product*=(1<<A_BITS)+aa
        strong+=aa>=7*(1<<A_BITS)
    scale_bits=A_BITS*len(sinh)
    h=(product.bit_length()-1-scale_bits)//2
    numerator=1<<(scale_bits+2*h+2*RHO_BITS)
    z=isqrt(numerator//product)
    if z*z*product<numerator:z+=1
    assert z*z*product>=numerator
    return z,level+h+RHO_BITS,strong,hi


def generate(k,X,target,max_splits,write=False):
    sine,sinh=constants(k,X)
    base=44*6**k; width=base//2-7
    scale0=F(44*width,7*base)
    scale1=scale0*F(44,7*base)
    scale2=scale1*F(44,7*base)
    scales=(scale0,scale1,scale2)
    cells={};heap=[];total=[F(0),F(0),F(0)];bad=0;serial=0
    def add(level,index):
        nonlocal bad,serial
        z,exponent,strong,hi=cell(k,X,level,index,sine,sinh)
        masses=[F(z*hi**m,1<<(exponent+m*level)) for m in range(3)]
        for m in range(3):total[m]+=masses[m]
        bad+=strong<4
        cells[(level,index)]=(z,exponent,strong)
        serial+=1
        priority=-1.0 if strong<4 else -float(masses[2])
        heapq.heappush(heap,(priority,serial,level,index))
    add(0,0);start=time.monotonic();done=0
    while (bad or scale2*total[2]>target) and done<max_splits:
        _,_,level,index=heapq.heappop(heap)
        z,exponent,strong=cells.pop((level,index))
        hi=(7<<level)+(index+1)*width
        for m in range(3):total[m]-=F(z*hi**m,1<<(exponent+m*level))
        bad-=strong<4
        add(level+1,2*index);add(level+1,2*index+1);done+=1
        if done%10000==0:
            print(json.dumps({"k":k,"X":X,"splits":done,"bad":bad,"moment2":float(scale2*total[2]),"seconds":round(time.monotonic()-start,2)}),flush=True)
    obj={"method_version":3,"k":k,"X":X,"delta":str(F(1,6**k)),
         "target_moment2":str(target),"scaling_exponent":"7/2",
         "moments":[str(scales[m]*total[m]) for m in range(3)],
         "moments_display":[float(scales[m]*total[m]) for m in range(3)],
         "leaves":len(cells),"bad_scaling_cells":bad,
         "success":not bad and scale2*total[2]<=target,"splits":done,
         "seconds":time.monotonic()-start,
         "partition":[[level,index,z,exponent,strong] for (level,index),(z,exponent,strong) in sorted(cells.items())]}
    if write:
        dest=Path(__file__).resolve().parents[1]/"certificates"/f"minor_far_sharp_k{k}_x{X}.json.gz"
        dest.parent.mkdir(parents=True,exist_ok=True)
        with gzip.open(dest,"wt",encoding="utf-8") as f:json.dump(obj,f,separators=(",",":"))
        print("Wrote",dest,flush=True)
    print(json.dumps({a:b for a,b in obj.items() if a!="partition"},indent=2),flush=True)
    return obj


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--k",type=int,required=True,choices=[4,5,6])
    p.add_argument("--x",type=int,default=15)
    p.add_argument("--target",type=F,required=True)
    p.add_argument("--max-splits",type=int,default=1000000)
    p.add_argument("--write",action="store_true")
    a=p.parse_args()
    generate(a.k,a.x,a.target,a.max_splits,a.write)
