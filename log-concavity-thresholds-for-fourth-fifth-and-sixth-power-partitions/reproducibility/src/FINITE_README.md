# Exact finite computation

The final finite ranges used by the analytic proof are:

| k | all determinants checked | last negative | equality count | last equality |
|---|---:|---:|---:|---:|
| 4 | 1 through 2,000,000 | 637,854 | 525 | 1,118 |
| 5 | 1 through 12,000,000 | 2,507,860 | 2,223 | 4,098 |
| 6 | 1 through 180,000,000 | 35,577,568 | 11,411 | 25,767 |

Every subsequent determinant through the corresponding endpoint is strictly
positive. Each JSON certificate lists every equality and stores exact boundary
coefficients and determinants. The compressed signed-byte stream records every
sign. The separate analytic proof handles all larger indices.

## Arithmetic and independent verification

For each permitted part w=j^k, the ascending update a(n)+=a(n-w), starting
from a(0)=1 and a(n)=0 otherwise, adds arbitrary multiplicities of w.
Induction over the finite part set proves the coefficient recurrence.
The generator uses ascending part order and two 64-bit limbs. The checker
independently regenerates coefficients with descending part order and four
32-bit limbs, then computes every determinant with BigInteger and compares
every sign byte. Digests check reproducibility; they do not replace arithmetic.
The additional identity

    n p_k(n) = sum(A_k(m) p_k(n-m), m=1,...,n),
    A_k(m) = sum(j^k : j^k divides m),

checks the prefix through 8192 independently by logarithmic differentiation.
The disk generator and final disk verifier share the BigInteger determinant
scan; their coefficient reconstruction routines and part order are different.

`finite_bounds.py` gives exact rational a priori coefficient bounds requiring
126, 111, and 122 bits at the three final endpoints. Every coefficient addition
also checks overflow. For k=5,6, disjoint unit boxes around multiplicity vectors
for parts 2^k,...,m^k give the simplex bound

    (L+sum(j^k, j=2,...,m))^(m-1) / ((m-1)! product(j^k,j=2,...,m))
      * product(1+floor(L/j^k), j=m+1,...,floor(L^(1/k))).

The multiplicity of 1 is uniquely determined. The k=4 entropy bound is below.

## Reproduction and recovery

From the project root, run the cases sequentially:

```powershell
python src/finite_fast_verify.py certificates/finite_k4_2000000.json
python src/finite_fast_verify.py certificates/finite_k5_12000000.json
python src/finite_fast_verify.py certificates/finite_k6_180000000.json
```

The helper uses Python's standard library and the installed Windows .NET
Framework C# compiler. It recompiles the checker, expands the compact signs,
and regenerates all coefficients. For k=6 it selects `finite_inplace.cs`,
followed by the exact sign and witness scan in `finite_disk.cs`.
The one-file route uses about 12 MB of coefficient buffers and a 2,880,000,032
byte disk array, plus small journals and a single undo block. The CLR has
additional runtime overhead. Allow roughly 3.1 GB extra disk space.

Each in-place block saves and flushes its original bytes before any overwrite.
An intent records old and new hashes; the state commits only after the updated
coefficient bytes and journal are flushed. Resume restores an uncommitted
block or validates a committed one, then checks the complete mixed-stage file
before continuing. Atomic metadata uses unique temporary names and bounded
retry for transient Windows file-sharing conflicts. The authoritative state
is `disk_verify_inplace/state.txt` inside the case directory. Repeating the
same command resumes this state. A finished coefficient reconstruction writes
the compatibility state used by the final BigInteger sign scan.

The reproducible minimal test is `python src/finite_inplace_smoketest.py`.
`certificates/finite_inplace_validation.json` records successful uncommitted
undo, committed-intent recovery, corruption rejection, and comparison with
Python arbitrary-precision coefficients through 10001. Earlier two-file tests
and original smaller finite ranges are historical validation evidence.

`finite_verify.py` is a portable all-Python alternative. It was executed on the
original 700,000 fourth-power range; a full sixth-power Python run is not
claimed and can require about 10 GB RAM. The executed C# route is preferred.

The compact certificates and compressed signs suffice for fresh regeneration.
Completed raw coefficient arrays are regenerable caches; removal records retain
their verified size and SHA-256. Never remove an active checkpoint array.

### Elementary entropy bound for the enlarged fourth-power range

Let f(u)=-log(1-exp(-t*u^k)), v=t*u^k. Direct differentiation gives

    f''(u) = k*t*u^(k-2)/(exp(v)-1)
             * [k*v/(1-exp(-v))-(k-1)] > 0.

Convexity on the unit intervals centered at the positive integers gives
log F_k(exp(-t)) <= integral_(1/2)^infinity f(u) du. The integral over all
positive u is A*t^(-1/k), where A=Gamma(1+1/k)*zeta(1+1/k), by expanding the
logarithm into its nonnegative exponential series and integrating. Also
f(u)>=-log(t*u^k), so

    log F_k(exp(-t))
       <= A*t^(-1/k) + (1/2)*log(t) - (k/2)*(1+log(2))
       <= A*t^(-1/k) + (1/2)*log(t).

Adding ones injects the partitions of N into those of every larger integer.
Thus F_k(exp(-t)) >= p_k(N)*exp(-Nt)/(1-exp(-t)), and therefore

    p_k(N) <= t^(3/2) * exp(Nt+A*t^(-1/k)).

For k=4, no numerical special-function dependency is needed. Gamma log-convexity
between 1 and 2 gives Gamma(5/4)<=1. The integral test and the exact rational
fourth-root bounds (17/20)^4>1/2 and (19/25)^4>1/3 give

    zeta(5/4) < 1 + 2^(-5/4) + (13/3)*3^(-1/4)
              < 1 + 17/40 + (13/3)*(19/25) = 2831/600 < 19/4.

Set N=2000001 and t=18^(-4). It follows that

    p_4(N) < exp(3658483/34992)/18^6 < 2^128.

`finite_bounds.py` proves the final strict inequality by summing the positive
exponential Taylor series and bounding the remaining terms by a geometric
series. The resulting rational upper bound's ceiling has 126 bits. The bound
holds for all earlier indices by monotonicity and all partial coin passes by
inclusion of their partition sets. The exact numerator and denominator are
stored in `finite_k4_2000000.json`.

