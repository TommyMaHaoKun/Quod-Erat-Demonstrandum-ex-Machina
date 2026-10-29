"""Finite fixed-word obligations for exact lower open-cone q.
The unbounded proof and parameter coverage are in the paper, Section 7 and Appendix C.
"""
import json
from pathlib import Path
R='01201012';B='01012'
def periodic(w,n):return int(w[n%len(w)])

def main():
 count=0
 for ell in range(1,9):
  assert periodic(R,-ell)==periodic(B,-ell);count+=1
 assert periodic(R,-9)==2 and periodic(B,-9)==1;count+=1
 # The three rightmost incomplete-front columns in k=3m+1.
 # h=0 is exactly the same B-power on both sides; no check is needed.
 # h=1,2: prefix ends B-power then01; onset offset is8-ell.
 for width in (20,14):
  for ell in range(1,width+1):
   off=8-ell
   if off>=0:v=periodic(R,off)
   elif off>=-2:v=int('01'[off])
   else:v=periodic(B,off+2)
   assert v==periodic(B,-ell),(width,ell,v,periodic(B,-ell));count+=1
 # At the exact final mismatch in s=1 the front is one symbol before
 # the end of a B-power, whereas its cyclic comparison is9 before a cut.
 assert int(B[-1])==2 and periodic(B,-9)==1;count+=1
 out=dict(exact_fixed_word_checks=count,scope='all lower open cones k>=41, 0<b<d')
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
 print(out)
if __name__=='__main__':main()
