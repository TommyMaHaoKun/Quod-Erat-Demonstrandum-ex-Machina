# Proof map

| Claim | Manuscript location | Dependency and check |
|---|---|---|
| All-integer expectation limit | Theorem 1.1 | Even-order proof in this paper plus Chen et al. Theorem 1.1 for odd orders |
| Exact Fourier operator, K squared = I-J | Section 2, equation (1) | Full multiplier includes singleton; character orthogonality; exact auxiliary checks |
| Fourier LP and complementary product | Section 2, equations (2)-(4) | Cyclic averaging; the parity-neutral duality argument in Chen et al. Propositions 3.1-3.3 |
| Interior barrier and deterministic residual certificate | Lemma 2.1 | Direct convexity, stationarity and norm identities; proof included |
| Uniform tail and exceptional-event integration | Section 3, equations (7)-(8) | Independent signs, sum of squared coefficients below 2n, exponential-moment bound |
| Paired Fourier kernel bound for even n | Lemma 3.1 | Condition N_0=N_h=0 with probability 1/2; adjoin singleton independently; independent-row theorem is valid for every modulus |
| Uniform tree influence, covariance and Gaussian comparison | Proposition 4.1 | Laminar identity minors, bounded-gcd congruence counts, h exclusion, two exceptional modes; abstract sign comparison |
| Exact singleton-free Walsh projection | Lemma 5.1 | Fourier convolution, degree count, exclusion of epsilon_h; 36 exact checks |
| Quantitative Wick-grafting estimate | Proposition 5.2 | Exact projection/Pythagoras, full K squared identity, one- and two-mode moment estimates, at most 6n exceptional pairs |
| Gaussian fixed point and quantitative tails | Lemma 6.1 | Explicitly imported from Chen et al. Theorem 9.3, Proposition 9.4, Theorem 9.5 |
| Smooth scalar transfer | Section 6, equation (21) | Chen et al. Proposition 10.3's compact-test proof uses the established characteristic-function and moment bounds; extra mode costs at most exp(C_tau D M log(DM+2))/n |
| Full residual, including singleton leaf | Proposition 6.2, equations (25)-(26) | Five displayed residual pieces; singleton piece has squared norm exactly 4/n |
| Growing-cutoff estimates | Proposition 6.2 | D=O((log log n)^3), M=O((log log n)^2); all finite-size exponential factors are n^o(1) |
| Expectation upper bound | Section 7 | Kernel event, discrepancy, bad-event probability p_n sqrt(log n)->0, explicit tail integration, then tau->0 |
| Verification scope | Section 8 | Finite algebraic identities checked with integer arithmetic; asymptotic estimates proved analytically |

## Review record

An independent internal mathematical cross-check reviewed the extension note, the corresponding source arguments, and the complete manuscript. It reported PASS on 2026-11-04, specifically covering the deterministic certificate, Poisson law, overlap/covariance estimates, exact projection, polynomial and Gaussian transfer, all five residual terms, cutoff rates and expectation integration.

The exact verifier uses independent constructions: direct admissible-flow enumeration versus Fourier-Walsh convolution and Hermite expansion. It refuses optimized Python execution so assertion checks remain active.
