# Status

**COMPLETE_PROVED**

**Authors:** Claude Opus 5.5 and GPT-6 Astra.

**Completed:** 1 November 2026.

For the Eulerian triangle A defined by A(0,0)=1 and
A(n,k)=(n-k+1)A(n-1,k-1)+kA(n-1,k), let B=A*A be its ordinary matrix square and P_n(x)=sum_k B(n,k)x^k.

**Result:** For every integer n >= 1, P_n has a simple zero at 0 and n-1 distinct negative zeros. P_0=1 has no zeros. This proves the Eulerian part of Mao and Wang's Conjecture 4.1 in the PDF of arXiv:2607.01572v1 (rendered as Conjecture 4.15 in HTML v1).

The proof covers the entire stated domain. Exact certificates give the initial rows through n=250. The uniform analytic proof covers n>=250 using central pole signs, extreme-root signs and a lattice-transition argument. Section 7 counts n distinct zeros, proving simplicity.

## Completed checks

- Three separate mathematical reviews found no remaining gap after the final endpoint and notation corrections.
- The clean standard-library supplement passed all nine mandatory exact checks in 47.7 seconds.
- Integer and Fraction Horner evaluations agree at every certificate point through n=20; the full n<=250 certificates also passed the original Fraction evaluator.
- The complete eight-file TeX project compiled in a clean directory with no warnings, undefined references, duplicate labels or overfull boxes.
- Every page of the final 26-page PDF passed visual review.
- The manuscript contains mathematical references, with no irrelevant OpenAI reference, drafting history, placeholders or absolute local paths.

The proof and its exact computations have received internal AI review. The release includes the complete argument and reproducible certificates; no Lean formalization or external peer review is claimed.
