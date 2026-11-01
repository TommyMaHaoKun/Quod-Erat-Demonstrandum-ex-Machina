# Claim-by-claim proof map

Author: GPT-6 Astra. Audit date: 2026-11-01.

| Claim | Proof location / dependency | Verification |
|---|---|---|
| Exact target equals Sun Conjecture 3.11 (3.15) | Theorem 1; Sun arXiv:2603.29973v3 | Compared with source PDF and the assigned prompt |
| `S(a)=C(a)B(a)-4aA(a)` | Proposition 2; Au arXiv:2312.14051v4, Example XI (4.4) | Exact duplication and sign normalization written out; independently reviewed |
| Auxiliary inverse-binomial sum equals `93 zeta(5)-7 pi^2 zeta(3)` | Proposition 2; Au Example XV, last sum before Remark 5.3 | Established source result; optional WZ/coefficient audit included |
| All parameter sums holomorphic near zero | Lemma 3 | Uniform summable Gamma-ratio bounds on every disk `|a|<=r<1/8`; poles excluded |
| Analytic extension through `a=0` and differentiated sums | Lemma 3 | Normal convergence plus Cauchy formula; no residual singularity after normalization |
| `U=7 zeta(3)/4-pi^2 log(2)/4` | Lemma 4, beta mixed derivative | Full integral, beta expansion, and half-integer polygamma calculation |
| `W=7 zeta(3)/16` | Lemma 4, generating function and polylogarithm identities | All transformations, endpoint conditions, and integration constants supplied |
| Derivatives of C and B | Section 4, equations (18)-(19) | Exact logarithmic derivatives; six-check verifier includes constant cancellation |
| `A(0)` is one quarter of Au's sum | Section 4, equation (20) | Explicit index shift; exact rational identity in verifier |
| `S'(0)=-93 zeta(5)-2 pi^4 log(2)` | Section 4, equation (21) | Product rule and exact cancellation of `pi^2 zeta(3)` |
| `q_n'(0)/q_n(0)=-28(H_(2n-1)-H_(n-1))` | Section 4 | Differentiation of finite products; symbolic verifier |
| Theorem 1 | Previous two rows and Lemma 3 | `S'(0)` is minus twice the exact target series |
| Corrected Gamma interpolation | Section 5, equation (22) | Factorials and Gamma duplication; separate derivative agrees with finite-product calculation |
| Absolute convergence and explicit remainder | Section 6, equation (23) | Positive harmonic difference bound, binomial lower bound, geometric tail |
| Arithmetic consistency at 160 decimal places | `src/verify.py` | Independent rational enclosures of both sides; all error bounds appear in paper |

## Dependency boundary

The proof relies on two established identities of Au, both stated in full
and attributed in Proposition 2. The subsequent analysis and evaluations
are derived in the paper. The optional symbolic audit reconstructs the
specialized WZ and coefficient calculations behind the second identity;
its underlying analytic transformation remains a cited result of Au.

No unresolved conjecture, numerical recognition, or unverified finite
certificate is used as a mathematical premise. The work is an analytic
proof with exact arithmetic consistency checks; no Lean claim is made.
