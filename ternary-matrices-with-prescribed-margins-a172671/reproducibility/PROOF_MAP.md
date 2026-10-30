# Claim-by-claim proof map

Status: **COMPLETE_PROVED**, 2026-10-30.

| Claim | Proof / dependency | Verification | Status |
|---|---|---|---|
| Matrix count is `[t_1^n...t_6^n] h(t)^(3n)` | Each of 21 monomials is exactly one row; multiplication retains labeled row order | Independent last-row DP n=0..8 | Proved |
| Coefficient of `exp(h)` is `a_n/(3n)!` | Target total degree is 6n and h has degree 2 | Paper Lemma 2, normalization review | Proved |
| `b_n=L(P_n^6)/(n!)^3` | Formal Gaussian exponential identity; six factorial denominators | Separate derivation and direct-count agreement | Proved |
| Polynomial differential and shift identities | Differentiate `exp(tx+t^2/2)` coefficientwise | n=0 separately included | Proved |
| Exact integration-by-parts identity | `L(f')=L(xf)` proved on monomials | Derivative and endpoint terms reviewed | Proved |
| Four moments suffice | Reduction decreases x exponent; odd base moments vanish by parity | Divisions only by positive constants | Proved |
| Displayed A(n) is the transfer matrix | Shift `(y,z)->(xy+z,(n+1)y)` and paper formulas (12)--(13) | All 16 entries independently reconstructed by SymPy and Fraction-polynomial arithmetic | Proved |
| Normalized transfer is B(n)=A(n)/(n+1)^3 | Factorial ratio | Independent normalization check | Proved |
| Specified five p_j give zero operator row | Paper identity (14), with all inputs printed | Four exact polynomial residuals, degrees <=20,19,18,17; 78 coefficients zero; independently checked as rational functions | Proved by finite exact algebra |
| Recurrence holds for every n>=0 | Apply identity to U_n; divide by positive `prod_(t=1)^4(n+t)^3` | Boundary and matrix product order reviewed | Proved |
| Initial conditions and forward uniqueness | Moments n=0..3; p_4(n)>0 | DP and explicit moments | Proved |
| Paper reproduces original operator | Original source match and independent polynomial parsing of paper | `verify_certificate.py`, PDF page 2 review | Verified |
| Finite examples agree | DP n=0..8; moments n=0..40; residuals n=0..36 | `independent_checks.py` | Corroboration only |
| Package reproduces from clean directory | Copy essential inputs, run three verifiers, compile twice | `certificates/release_check.json` | Passed |
| PDF readable and agrees with theorem | Saved source compiled, every page rendered and reviewed | `certificates/pdf_review.json` | Passed |

## Verification and novelty boundaries

The finite examples do not infer an all-index recurrence. The proof is
the coefficient-to-moment derivation followed by an exact polynomial
identity whose full inputs and arithmetic are printed in the paper.
Internal implementation checks are not Lean or external human review.

The recurrence and D-finiteness are due to the original authors.
Yurkevich already used the quadratic decomposition for coefficient
computation. This package contributes the four-moment closure and exact
recurrence verification. The bounded audit found no prior proof but does
not certify worldwide priority.
