# Proof map

Author: GPT-6 Astra.

| Claim | Dependencies | Verification |
|---|---|---|
| Explicit coefficients, all nonnegative | Binomial theorem and uniqueness of the Bernstein expansion | Derived in Lemma 2; independently compared with one-step degree elevation |
| Central maximizing indices | Adjacent coefficient ratio; numerator minus denominator is m(r-2j-1) | Algebra checked independently; exact finite checks |
| Equal maxima at elevations 2s-1 and 2s | Two central-binomial identities | Derived in Lemma 2; exact finite checks |
| Maximum divided by h is the stated product | Factorial cancellation and parity identity | Derived in Lemma 2; exact finite checks |
| Strict squared bound (R+n)/R | (a-1)^2=a(a-2)+1 and a telescoping product | Complete finite product proof in Lemma 3; independent mathematical review |
| Requested upper bound and stronger parity bound | R=2 ceil(T/2) >= T; all coefficients nonnegative | Theorem 1, including integer T and h approaching 1 |
| Minimum is odd, with exact product criterion | k>1 at r=0; equal consecutive maxima | Theorem 1 and Corollary 4 |

Two separate internal mathematical reviews found no gap. The verification
program checks finite instances using exact arithmetic; the universal proof
is the algebraic argument in the paper. No formal-proof-assistant claim is made.
