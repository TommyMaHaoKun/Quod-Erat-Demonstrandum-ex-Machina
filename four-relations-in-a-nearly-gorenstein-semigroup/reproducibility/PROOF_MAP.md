# Proof map

Author: GPT-6 Astra. Exact target: Question 8's assertion that rho belongs to {5,6}.

| Claim | Proof and dependencies | Independent check | Result |
|---|---|---|---|
| S=<6,7,8,9> is a numerical semigroup with exactly four minimal generators | All generators lie below 12; every positive sum of two elements is at least 12. The represented block 12,...,17 and addition of 6 give every integer >=12. | Both Python verifiers enumerate the block and the small values. | Proved |
| F=11 and PF(S)={10,11} | Complete gaps {1,2,3,4,5,10,11}; generator tests reject 1,...,5 and accept 10,11. Negative integers are excluded in three cases around -6. | Both verifiers check positive gaps and finite negative witnesses; f<-6 is excluded by f+6<0. | Proved |
| S is nearly Gorenstein | NG vector (11,10,10,10) and full 4-by-2 membership table. | Exact integer membership checks in both programs. | Proved |
| S is not almost symmetric | Gap a=1 has F-a=10 a gap, while 1 is not pseudo-Frobenius. | Explicit witness checks in both programs. | Proved |
| Four displayed binomials generate the entire defining ideal | Terminating reduction with positive auxiliary weights (1,4,6,7); six terminal bases have distinct degrees modulo 6; images of all terminal monomials are linearly independent. | `proof_verify.py` checks the complete finite data, including pure-square restrictions and residue classes. | Proved for the whole ideal |
| At least four ideal generators are needed | No relation below semigroup degree 14, hence mI has no part below 20. Four distinct classes at degrees 14,15,16,18 survive in I/mI. | `proof_verify.py` exhausts all monomials below 14 and checks the four degrees. | Proved |
| Independent relation count rho=4 | Factorization-graph quotient has dimension c(n)-1. All graphs above F+g3+g4=28 are connected by the explicit lemma in the paper. | `search_verify.py` enumerates every factorization at all degrees 0,...,28. Only 14,15,16,18 disconnect, each into two components. | Verified |
| The example and relation count are known | Gomes-O'Neill-Torres Davila (2023), Example 18 gives the same minimal presentation; MS21 Proposition 3.4 gives nearly Gorensteinness for arithmetic sequences. | Primary-source audit and manuscript source review. | Attributed |
| The exact supplied assertion is false | All hypotheses hold and rho=4 is outside {5,6}. | Direct proof and factorization-graph check agree. | Resolved negatively |

The original MS21 Question 4.3 has a different, type-dependent conclusion: type two allows four or five relations; type three allows six. This example realizes its four-relation branch. The project resolves the supplied {5,6} formulation and records this distinction explicitly.

The proof is elementary and complete without executing software. The programs recheck its finite data and provide a separate factorization-graph certificate. No Lean formalization is included.
