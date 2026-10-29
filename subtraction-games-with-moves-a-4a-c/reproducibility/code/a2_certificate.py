# Exact finite certificate for the uniform a=2 proof.
# This is NOT a state-repeat search. The affine-boundary lemma in
# the accompanying paper proves that these finite word checks cover every k.
from collections import defaultdict

B = '0011001122'
D = '0011021021'

# Each triple (w,A,C) means the word w repeated A*k+C times.
# Total word length is exactly T = q + c + p.
TEMPLATES = {
  1: [(B,1,0),('031203102103',0,1),('1',0,1),(D,1,0),('021',0,1),(D,1,0)],
  3: [(B,1,-1),('001100112',0,1),('20011',2,1),('200',0,1)],
  5: [(B,1,0),('00110210213',0,1),('0210210011',1,1),('02102',0,1)],
  7: [(B,1,1),('03',0,1),('12001',2,2),('12',0,1)],
  9: [(B,1,1),('30213001123',0,1),(B,1,0),('00112001122',0,1),(B,1,0),('001120011',0,1)],
}

def word(t,k):
    return ''.join(w*(A*k+C) for w,A,C in TEMPLATES[t])

def boundaries(t):
    """Return every shifted boundary as the affine pair (A,B): A*k+B."""
    starts=[]
    a=b=0
    for w,A,C in TEMPLATES[t]:
        if A:
            assert 10 % len(w) == 0
            starts.append((a,b))
            a += len(w)*A
            b += len(w)*C
        else:
            # Each fixed literal letter is a period-one segment.
            for ch in w*C:
                starts.append((a,b))
                b += 1
    starts.append((a,b))
    out={(0,0),(a,b)}
    for aa,bb in starts:
        for sa,sb in ((0,0),(0,2),(0,8),(10,t)):
            out.add((aa+sa,bb+sb))
    return out

def certify():
    total=0
    for t in (1,3,5,7,9):
        bounds=boundaries(t)
        assert all(A % 10 == 0 and -10 <= C <= 50 for A,C in bounds)
        signatures=defaultdict(set)
        terms=0
        for k in range(0 if t==9 else 1,8):
            f=word(t,k)
            c=10*k+t
            p={1:c+2,3:5,5:10,7:5,9:c+2}[t]
            q={1:c+11,3:c-4,5:c+6,7:c+5,9:c+12}[t]
            assert len(f)==q+c+p
            for n,ch in enumerate(f):
                opts=frozenset(int(f[n-s]) for s in (2,8,c) if n>=s)
                g=int(ch)
                assert g not in opts and all(x in opts for x in range(g)), (t,k,n)
                signatures[g].add(tuple(sorted(opts)))
            terms+=len(f)
        total+=terms
        print(t, 'intercepts', min(C for A,C in bounds),max(C for A,C in bounds),
              'terms',terms,'option sets',dict(signatures))
    print('Verified',total,'recurrence positions; the affine-boundary lemma extends this to all k.')

if __name__=='__main__':
    certify()
