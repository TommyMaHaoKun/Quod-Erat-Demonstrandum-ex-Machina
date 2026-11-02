# Proof map

Author: GPT-6 Astra. Reviewed 2026-11-02.

## Exact result

For every compact K in R containing at least two points and every 0 < r < s < 1,

`C_s(K)/C_r(K) >= C_s([-1,1])/C_r([-1,1])`.

Equality holds exactly for nondegenerate closed intervals. The capacity uses the maximum of the probability-measure energy. Theorem numbers below refer to `paper/main.tex` and the compiled paper.

| Claim | Proof dependencies | Verification |
|---|---|---|
| Energy maximum exists and is positive for at least two points | Weak compactness of probability measures, continuity of the kernel, two-point test measure | Checked in introduction |
| Lemma 2.1: Poisson cell density is lambda^2 exp(-lambda z) Delta(u,z) | Independent exponential distances to neighboring Poisson points; logistic Jacobian | Two independent derivations checked; normalization integral included |
| Equation (10): partition slope has mean equal to total variation | Finite Stieltjes measure; Poisson endpoints avoid its countably many atoms | Checked also for singular measures and jump maps |
| Lemma 2.2: coarsening raises each concave slope moment | Poisson superposition; finite subdivision of each coarse cell; Jensen; nonnegative countable sums | Direction and integrability checked independently |
| Lemma 3.1: beta pair law is a mixture of Poisson cells | Logistic identities; positive binomial series; Tonelli; exact normalization | Factors and powers audited; optional quadrature/series checks |
| Lemma 3.2: increasing t lowers the random mixing rate | Decreasing likelihood ratio; cumulative distribution comparison; quantile coupling | Explicit algebra and double-sum proof |
| Proposition 3.3: chord-slope concave moments increase with t | Lemmas 2.2, 3.1, 3.2 | All mixtures normalized; required moments bounded by total variation |
| Theorem 1.2: normalized beta transport energies increase with t | Proposition 3.3 and the power-mean inequality | Equality requires an almost everywhere affine map by strict Jensen and Fubini |
| Lemma 4.1: quantile transfer reaches any compactly supported probability | Inverse distribution function; equivalence of all beta densities to Lebesgue measure | Includes atoms, disconnected supports, and singular measures |
| Proposition 4.2: beta equilibrium and gamma benchmark | Partition Jensen; quantile realization; first variation and full support; beta integral and gamma duplication | Noncircular: equilibrium is derived after the Poisson representation |
| Theorem 1.1: full interval conjecture | Maximizing r-measure; Theorem 1.2; admissibility of transported s-measure; scaling | Entire stated set and parameter domain |
| Equality only for intervals | Affine equality in transport; full interval support; adding an exterior point strictly raises energy | Endpoint comparison and first-variation sign checked |

The theorem uses no numerical computation, finite truncation, or conjectural auxiliary lemma. In particular, the early exploratory idea of monotonicity under arbitrary point insertion is not asserted or used.

## Audit records

- `PROOF_AUDIT_POISSON.md`: independent derivation of the mixture and its consequences.
- `PROOF_AUDIT_ANALYTIC.md`: independent checks of the proof, singular maps, and the interval formula.
- Actual manuscript reviewed by both reviewers after drafting; their wording corrections were incorporated.
- Mathematical review was internal AI review. No Lean formalization or external peer review is claimed.

## Reproducibility

`reproducibility/audit_poisson.py` provides optional 60-digit numerical checks of twelve finite-set quantile transports and three normalization identities. These checks are separate from the proof and are not certified interval-arithmetic bounds. `reproducibility/build_paper.py` builds the standalone LaTeX source without machine-specific paths.
