# Proof map

The numbering follows the final paper, *Real and simple zeros of the squared Eulerian triangle*, by Claude Opus 5.5 and GPT-6 Astra.

| Claim | Statement | Dependencies | Verification |
|---|---|---|---|
| Theorem 1.1 | For every n >= 1, P_n has a simple zero at 0 and n-1 distinct negative zeros; P_0=1 | Section 7 and Appendix A | Complete |
| Lemmas 2.1-2.2 | Eulerian real-rootedness, reciprocity, Frobenius identity, Bonferroni bounds and concavity of section volumes | Eulerian recurrence; elementary sign induction; Brunn's theorem | Complete analytic proofs |
| Lemma 2.3 | F_n(t)=sum_j j! A(n,j)t^j has simple nonpositive zeros | Second-order recurrence; signs at critical points | Complete induction for all n |
| Lemmas 2.4-2.5 | Exact absolutely convergent pole expansion and strictly increasing phase from -(n+1)pi to 0 | Lemma 2.3; partial fractions | Complete, including n=1 |
| Lemma 3.2 | Weighted mean at least (n+1)/2 for t >= e/n | Eulerian symmetry; paired factorial weights | Complete analytic proof |
| Lemma 3.3 | Tilted Poisson-binomial variance < 8n/Y^2 through u=4 sqrt(n) | Lemmas 2.2-2.3; Darroch's mode theorem; exact tail bounds | Complete; rational constants verified |
| Lemma 3.1 | Nearest conjugate poles determine signs for abs(s) <= 4 sqrt(n), n >= 250 | Lemmas 3.2-3.3; factor and kernel comparisons | Complete; positive-tail bounds .85 and .33, negative-tail bound .88 |
| Lemma 4.1 | K=floor(sqrt(n)/3) small negative zeros after phase node -(K+1)pi | Logarithmic-mean curvature; coefficient estimates; Eulerian phase comparison | Complete analytic proof |
| Lemma 5.1 | Two outer zeros per explicit four-term comparison, through L=floor(sqrt(n)/(2 sqrt(log n))) | Double-sum identity; quadratic sign margins; Bonferroni and tail bounds | Complete analytic proof |
| Lemma 5.2 | For 250 <= n <= 1600, L=ceil(sqrt(n)/4) outer pairs reach a correctly indexed bulk endpoint | Same four-term comparison; monotonicity in n | Ten exact endpoint checks cover the interval |
| Section 6.1 | Fixed-total maximizers form an ordered lattice path; same-coordinate events are separated | Strict concavity and coordinate ratios | Complete analytic proof |
| Lemma 6.1 | Global positive-quadrant envelope and weighted tail < .04AB | Four descent losses; geometric sums | Exact rational verifier passes |
| Lemma 6.2 | Single-mode dominance and exact exterior zero count | Global descent; Bonferroni bound; Rouche's theorem | Exact rational verifier passes |
| Section 6.3 | A paired transition gives two real sign changes | Exact residual factor; independent-zero locations; joint and independent tails; Eulerian replacement error | Midpoint sign < -.79AB/H; exact rational verifier passes |
| Lemma 6.3 | Separator phase differs from (r-n)pi by < 3pi/4 | Tilted log-concavity and canonical phase | Complete; exact constants verified |
| Lemma 6.4 | For n > 1600, the outer roots join a separator in [4 sqrt(n)-8,4 sqrt(n)] | Lemmas 5.1, 6.1-6.3; event geometry | Complete; gap < 4 forms a cluster, gap >= 4 gives a separator |
| Section 7 | Disjoint intervals yield r+1+(n-r-K-2)+K=n-1 negative zeros | Lemmas 3.1, 4.1, 5.2, 6.4; degree n; B(n,1)=n! | Complete for all n >= 250 |
| Appendix A.1 | Every row 0 <= n <= 250 has the stated zeros | Exact rational sign certificates and intermediate value theorem | All rows pass; Eulerian recurrence equals closed formula |
| Appendix A.2-A.3 | Scalar reductions are checked by rational arithmetic | Taylor bounds, geometric remainders, polynomial coefficients | All nine mandatory checks pass |

## Independent checks

- The Eulerian recurrence and alternating-sum formula agree for all certificate rows.
- Denominator-cleared integer Horner evaluation agrees exactly with Fraction Horner at every certificate point through n=20.
- The complete n<=250 certificate also passed the original Fraction evaluator.
- Three separate mathematical reviews checked the proof assembly, transition geometry, tail errors, phase matching and final count.
- The minimal supplement was run from an unrelated working directory with all nine checks passing.
- Every page of the compiled 26-page paper was visually inspected; every page affected by the final text and citation corrections was inspected again.

The computer checks certify the finite initial rows and explicit scalar bounds. The paper proves the uniform analytic estimates and assembles the all-n result.
