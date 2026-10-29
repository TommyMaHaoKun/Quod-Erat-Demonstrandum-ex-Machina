# Complete coverage inventory

Domain: integers a>=2, c>4a, gcd(a,c)=1. Every admissible pair is classified.
The selection below is ordered and disjoint after earlier rows are excluded.

| Case | Full sequence | Least p | Earliest q |
|---|---|---|---|
| a=2, every odd c>8 | Five explicit residue words | Proved, including all reductions | Proved |
| a>=3, c>6a | Five residue constructions | Proved | Proved |
| a>=3, 4a<c<6a, 41abs(c-5a)>=a | 89 affine cones and89 rational seams | Primitive-word certificates | Last-mismatch certificates |
| c=5a+d, 0<41d<a, d>1 | Uniform upper columns and balanced towers | 6a+d | Three quotient formulas below |
| c=5a-d, 0<41d<a, d>1 | Uniform lower columns and balanced towers | 6a-d | Three quotient formulas below |
| c=5a+1, a>=42 | Uniform upper integer-seam word | 6a+1 | Three quadratic formulas below |
| c=5a-1, a>=42 | Uniform lower integer-seam word | 6a-1 | Three quadratic formulas below |

For open near-diagonal cases, write a=kd+b, 0<b<d, k=3m+s. There is
no upper bound on k,d,b or a. The proof covers every k>=41.

| s | Upper q | Lower q |
|---|---|---|
| 0 | (26m+13)a+3md | (26m+3)a+d |
| 1 | (26m-1)a+(3m-1)d | (26m-10)a-(3m-2)d |
| 2 | (26m+40)a | (26m+30)a-(3m+2)d |

For d=1, let s=a mod3. These are separate seam formulas, with separately
proved minimality; they are not obtained by assuming open formulas persist.

| s | Upper q | Lower q |
|---|---|---|
| 0 | (26a^2+42a)/3 | (26a^2+9a)/3+1 |
| 1 | (26a^2-26a)/3-2 | (26a^2-59a)/3+3 |
| 2 | (26a^2-52a)/3-3 | (26a^2-85a)/3+4 |

The seam theorems actually prove all upper a>=10 and lower a>=9; smaller
cases and all junction endpoints are already covered by the atlas or a=2
theorem. In particular, exceptional reductions such as (9,46) and (8,37)
have p=5 in their explicit seam certificates.

Coverage proof: coprimality excludes c=5a and6a. Outside the outer ranges,
d=abs(c-5a) satisfies0<41d<a and gcd(a,d)=1. Division gives k>=41. If the
remainder is positive, an open theorem applies. If it is zero, gcd(a,d)=1
forces d=1 and a>=42. No admissible pair remains. All finite atlas intervals
abut exactly, and all rational endpoints are supplied separately.

Global conclusion: q>0 and p in {5,5a,c+a,c+4a}. The period restriction is
proved; it is not an input to the structural construction. There are no
unresolved parameter families. This is an exact computer-assisted proof,
not a claim of Lean verification or historical novelty.
