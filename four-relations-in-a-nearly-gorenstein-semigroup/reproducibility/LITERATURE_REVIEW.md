# Literature review and statement audit

Access date: 2026-11-01 (Asia/Shanghai).

## Resolution and attribution

The exact assertion in the supplied Question 8, and in Problem 23 of the cited survey v3, is false. The classical semigroup

\[
S=\langle6,7,8,9\rangle
\]

is nearly Gorenstein, is not almost symmetric, and has four minimal relations. Its four-relation minimal presentation is explicitly published in Gomes, O'Neill and Torres Davila (2023), Example 18. The nearly Gorenstein property also follows from the established arithmetic-sequence results recalled by Moscariello and Strazzanti (2021), Proposition 3.4.

Accordingly, the project verifies and explains a known example, with a self-contained proof and exact certificate. The appropriate attribution is **a known counterexample to the precise formulation in the prompt**. The project does not claim a new numerical semigroup, a new minimal presentation, or a solution to the distinct, broader Question 4.3 of Moscariello and Strazzanti.

## 1. The question in the survey

Alessio Moscariello and Alessio Sammartano, *Open problems on relations of numerical semigroups*.

- Checked version: arXiv:2406.00790v3, 28 September 2026.
- [Versioned text](https://arxiv.org/html/2406.00790v3).
- [Version history](https://arxiv.org/abs/2406.00790).
- Location: Section 5, Problem 23, attributed there to MS21, Question 4.3.

The hypotheses are: a numerical semigroup of embedding dimension four that is nearly Gorenstein and is not almost symmetric. The proposed conclusion is `rho(S) in {5,6}`. The version-history page lists v3 as the latest revision on the access date. This is exactly the assertion reproduced in the supplied Question 8.

The survey also gives the type bound `t(S) <= 3` as Theorem 15, citing MS21, Theorem 2.4. Type and the number of minimal relations are separate invariants.

## 2. The original question permits four relations

Alessio Moscariello and Francesco Strazzanti, *Nearly Gorenstein vs Almost Gorenstein Affine Monomial Curves*, Mediterranean Journal of Mathematics **18** (2021), article 127.

- [Published open-access article](https://link.springer.com/article/10.1007/s00009-021-01761-1).
- DOI: [10.1007/s00009-021-01761-1](https://doi.org/10.1007/s00009-021-01761-1).
- [Published PDF mirror](https://d-nb.info/1244016322/34).
- Publication date: 13 May 2021.

Question 4.3 has the same nearly Gorenstein, non-almost-symmetric, four-generator hypotheses, but asks for these type-dependent possibilities:

| Type | Proposed number of defining-ideal generators |
|---|---|
| 2 | 4 or 5 |
| 3 | 6 |

It also states the corresponding proposed Betti sequences `(1,4,5,2)`, `(1,5,6,2)`, and `(1,6,8,3)`. Thus the four-relation example agrees with the possibility explicitly retained in the original source. The survey's set `{5,6}` omits that possibility. This discrepancy is material and must appear in the paper and project summary.

Other relevant established statements in this article are Proposition 1.1 (the numerical nearly Gorenstein criterion used in the prompt), Theorem 2.4 (`t(S) <= 3` in embedding dimension four), and Proposition 3.4 (the criterion for generalized arithmetic sequences). In particular, an ordinary arithmetic sequence yields a nearly Gorenstein numerical semigroup. The paragraph preceding Proposition 3.4 gives the almost-symmetric classification for generalized arithmetic sequences.

## 3. A published minimal presentation for the exact example

Tara Gomes, Christopher O'Neill and Eduardo Torres Davila, *Numerical Semigroups, Polyhedra, and Posets III: Minimal Presentations and Face Dimension*, Electronic Journal of Combinatorics **30**(2) (2023), Paper P2.57.

- DOI: [10.37236/10380](https://doi.org/10.37236/10380).
- [Publisher PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p57/pdf/).
- Published: 30 June 2023.
- Example 8, printed page 5: `Ap(S;6) = {0,7,8,9,16,17}` for `S=<6,7,8,9>`.
- Example 18, printed page 10: an explicit minimal presentation for this exact semigroup has the following four pairs of factorizations, with coordinates ordered as `(6,7,8,9)`:

\[
\begin{aligned}
((0,1,0,1),(0,0,2,0)),\\
((1,0,0,1),(0,1,1,0)),\\
((1,0,1,0),(0,2,0,0)),\\
((3,0,0,0),(0,0,0,2)).
\end{aligned}
\]

These are precisely the degree-16, degree-15, degree-14 and degree-18 relations used in this project, up to order and sign. The exact presentation therefore has a direct published source, beyond its derivation from a general arithmetic-sequence theorem. Example 18 and the surrounding page were checked in the publisher PDF.

## 4. Classical arithmetic-sequence formulas

Philippe Gimenez, Indranath Sengupta and Hema Srinivasan, *Minimal graded free resolutions for monomial curves defined by arithmetic sequences*, Journal of Algebra **388** (2013), 294-310.

- DOI: [10.1016/j.jalgebra.2013.04.026](https://doi.org/10.1016/j.jalgebra.2013.04.026).
- Checked preprint: [arXiv:1108.3203v1](https://arxiv.org/abs/1108.3203v1), 16 August 2011.
- [Full HTML](https://arxiv.org/html/1108.3203).
- Relevant locations: Section 1.1; Theorem 3.10; Theorem 4.1 and equation (4.1).

For an arithmetic sequence `(m_0,...,m_n)`, write `m_0=an+b` with `1<=b<=n`. Equation (4.1) gives

\[
\beta_j=j\binom{n}{j+1}+
\begin{cases}
(n-b+2-j)\binom{n}{j-1},&1\le j\le n-b+1,\\
(j-n+b-1)\binom{n}{j},&n-b+1<j\le n.
\end{cases}
\]

The example has `n=3`, `m_0=6=1*3+3`, so `b=3`. Substitution gives `(beta_0,beta_1,beta_2,beta_3)=(1,4,5,2)`. This provides a second published route to the exact relation count. The project's elementary proof verifies the example directly and does not require the reader to reconstruct the general resolution.

## 5. Subsequent papers checked

1. Dumitru I. Stamate and Francesco Strazzanti, *Nearly Gorenstein and almost symmetric properties in shifted numerical semigroups*, Journal of Pure and Applied Algebra **230** (2026), no. 9, 108330. Checked [arXiv:2601.19629v2](https://arxiv.org/html/2601.19629v2), 4 July 2026; DOI [10.1016/j.jpaa.2026.108330](https://doi.org/10.1016/j.jpaa.2026.108330). Theorem 3.4 establishes eventual preservation of nearly Gorensteinness under the specified shift, and Corollary 4.1 treats almost symmetry. Its subject is shifted families, rather than a universal `{5,6}` classification.
2. Kazufumi Eto, Naoyuki Matsuoka, Alessio Moscariello, Takahiro Numata, Alessio Sammartano and Kei-ichi Watanabe, *The structure of almost symmetric almost complete intersection numerical semigroups*. Checked [arXiv:2609.24880v2](https://arxiv.org/html/2609.24880v2), 13 October 2026, and its [version history](https://arxiv.org/abs/2609.24880). Theorem 1 concerns almost symmetric almost complete intersections; in particular these have odd embedding dimension. Example A.4 gives a different four-generated almost complete intersection, `<26,46,67,91>`. The paper's central hypotheses differ from Question 8, which expressly excludes almost symmetry.

These checks did not identify a correction to the survey's displayed Problem 23. The original 2021 question and the published 2023 example already determine the appropriate interpretation of this project.

## 6. Public proof-repository and search audit

The public [OpenAI mathematics repository](https://github.com/openai/math) and its [current manuscript catalogue](https://raw.githubusercontent.com/openai/math/main/CONTENTS.md) were inspected on the access date. The catalogue reported 721 manuscripts in 373 result families. Searches of that catalogue for `nearly Gorenstein`, `four-generated`, `numerical semigroups`, and `semigroup rings`, together with repository-targeted web searches, did not return an entry resolving this exact question. This records a catalogue audit, not a claim to have read every manuscript or proof artifact.

Additional searches used the exact question, `nearly Gorenstein minimal relations`, `nearly Gorenstein four-generated`, `nearly Gorenstein 5 or 6`, the exact semigroup `<6,7,8,9>`, the survey title with `correction`, and the arithmetic-sequence resolution title. The decisive positive matches are the primary sources above.

## 7. Scope of the contribution

The deliverable supplies a complete direct verification of all hypotheses and of `rho(<6,7,8,9>)=4`, plus a source comparison explaining the omitted value in the survey formulation. Its mathematical ingredients and exact four-relation presentation are established literature. The original type-dependent classification in MS21 Question 4.3 is outside the claim resolved here.
