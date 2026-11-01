# Literature review and source audit

Access date: **1 November 2026**. Authors of the accompanying paper: **Claude Opus 5.5 and GPT-6 Astra**.

## Result and source identification

Let \(A(0,0)=1\), with entries outside the lower triangle equal to zero, and
\[
A(n,k)=(n-k+1)A(n-1,k-1)+kA(n-1,k).
\]
For the ordinary matrix product \(B=A\cdot A\), define
\[
P_n(x)=\sum_{k=0}^n B(n,k)x^k.
\]
The accompanying paper proves that, for every \(n\ge1\), \(P_n\) has a simple zero at zero and \(n-1\) distinct negative zeros; \(P_0=1\). This resolves the Eulerian-square component of Mao and Wang's conjecture. The proof combines analytic estimates valid in all remaining degrees with exact rational sign certificates for the initial rows through \(n=250\).

**Primary source.** Jianxi Mao and Lijie Wang, *The Narayana transformation*, arXiv:2607.01572v1, 2 July 2026. The abstract page lists v1 as the available version on the access date. [Abstract and version history](https://arxiv.org/abs/2607.01572), [versioned HTML](https://arxiv.org/html/2607.01572v1), [PDF](https://arxiv.org/pdf/2607.01572v1), [DOI](https://doi.org/10.48550/arXiv.2607.01572).

The statement appears in Section 4 as **Conjecture 4.1 on printed page 11 of the PDF**, and as **Conjecture 4.15 in the arXiv HTML conversion**. Both refer to the real nonpositive roots of the row generating polynomials of the ordinary matrix squares of the Eulerian and Delannoy triangles. The problem prompt uses the HTML numbering. The source reports numerical real-rootedness of the first 30 Eulerian-square rows.

## Eulerian transformation literature

Write \(A_j(x)=\sum_k A(j,k)x^k\) and \(T(x^j)=A_j(x)\), so that \(P_n=T(A_n)\). Conventions in the literature can differ by a factor of \(x\); the matrix definition above fixes the normalization used here.

1. **Petter Brändén and Katharina Jochemko, *The Eulerian transformation*.** *Transactions of the American Mathematical Society* **375**(3) (2022), 1917–1931; arXiv:2103.00890v2, 11 August 2021. [Versioned text](https://arxiv.org/html/2103.00890v2), [DOI](https://doi.org/10.1090/tran/8539).

   Proposition 2.1 supplies a counterexample to general preservation of real-rootedness by the Eulerian transformation, using \(T((1+t/5)^5)\). Theorem 4.4 proves real-rootedness and interlacing for the transformed families \((t+q)^n\), with \(q\in(0,1]\); \(q=0\) gives the ordinary Eulerian endpoint. Their Conjecture 1 concerns nonnegative combinations of the binomial basis discussed below.

2. **Christos A. Athanasiadis, *On the real-rootedness of the Eulerian transformation*.** *Journal of the London Mathematical Society* **111**(2) (2025), e70083; arXiv:2302.00754v5, 18 February 2025. [Versioned text](https://arxiv.org/html/2302.00754v5), [DOI](https://doi.org/10.1112/jlms.70083).

   Theorem 1.1 settles the Brändén–Jochemko conjecture: it establishes real-rootedness, together with an interlacing structure, for the Eulerian transformation of nonnegative combinations of \(t^{n-k}(1+t)^k\). The theorem concerns this specified input cone. The source does not state the Eulerian matrix-square theorem.

## Classical inputs used in the proof

3. **T. Kyle Petersen, *Eulerian Numbers*.** Birkhäuser Advanced Texts: Basler Lehrbücher, Birkhäuser/Springer, New York, 2015. [Publisher and DOI](https://doi.org/10.1007/978-1-4939-3091-3). This supplies standard Eulerian identities, symmetry, and ordinary Eulerian real-rootedness.

4. **J. N. Darroch, *On the distribution of the number of successes in independent trials*.** *Annals of Mathematical Statistics* **35**(3) (1964), 1317–1321. [DOI](https://doi.org/10.1214/aoms/1177703287). The proof uses the mean–mode theorem for a sum of independent Bernoulli variables.

5. **Richard J. Gardner, *The Brunn–Minkowski inequality*.** *Bulletin of the American Mathematical Society (N.S.)* **39**(3) (2002), 355–405. [DOI](https://doi.org/10.1090/S0273-0979-02-00941-2), [published PDF mirror](https://www.ceremade.dauphine.fr/~carlier/Brunn-Minkowski). The slice-volume consequence of Brunn–Minkowski yields the concavity property of the Eulerian coefficients used in the estimates. The page range follows the published PDF header.

## Later related papers and public repositories

6. **Petter Brändén and Lorenzo Vecchi, *Chow polynomials of totally nonnegative matrices and posets*.** arXiv:2509.17852v3, 10 November 2025. [Version history](https://arxiv.org/abs/2509.17852), [versioned text](https://arxiv.org/html/2509.17852v3).

   Theorem 4.13 gives an interlacing closure result, and Theorem 4.17 concerns the Chow–Eulerian transformation for resolving matrices. Both the transformation and its admissible input cone depend on the selected matrix. The Pascal case recovers Athanasiadis's theorem. These results provide related structural context; the inspected statements do not assert \(T(A_n)\)'s real-rootedness.

7. **Kyle Binder and Lorenzo Vecchi, *Augmented singular cohomology, uniform matroids, and real-rootedness*.** arXiv:2609.15946v1, 14 September 2026. [Versioned text](https://arxiv.org/html/2609.15946v1).

   Section 7.1 and Theorem 7.3 restate Athanasiadis's Theorem 1.1 and apply Eulerian and derangement transformations to refined Hodge–Poincaré polynomials of uniform matroids. No Eulerian matrix-square resolution was located in the inspected source.

8. **Xiaojian Zeng, *Simple negative roots for the rows of the Delannoy matrix square*.** September 2026 repository manuscript in ArtificialZeng/AI-Has-Taste, project BW2-PR20260914-triangular_square_roots; inspected snapshot f3ae144b74f238f22c2b84b5283cb14ce912fd33. [Manuscript source](https://github.com/ArtificialZeng/AI-Has-Taste/blob/f3ae144b74f238f22c2b84b5283cb14ce912fd33/reproducible_source_code/BigWIN2/BW2-PR20260914-triangular_square_roots/source/manuscript/main.tex).

   Theorem 1 treats the **Delannoy-square component** of the same conjecture: the degree-\(n\) row polynomial has \(n\) distinct roots in \((-4-3\sqrt2,-3+2\sqrt2)\). The abstract and final section explicitly leave the Eulerian component unresolved. The current paper proves that Eulerian component. The repository manuscript uses the PDF's conjecture number, 4.1.

9. **PerAlexandersson/RealRooted, issue 1263.** [Issue](https://github.com/PerAlexandersson/RealRooted/issues/1263), titled “[theory][P2] Athanasiadis's Eulerian transformation on the magic cone, and the weighted deco transform”; closed, last updated 25 October 2026. The issue concerns formalization of Athanasiadis's cone theorem, normalization, and weighted decorated-permutation transformations. Its stated target is distinct from the Eulerian matrix-square theorem.

## Search record and contribution

The November 1 search covered arXiv, web search, and public GitHub sources. Queries included:

- "Eulerian" "matrix square" real rooted proof
- "Eulerian" "Conjecture 4.15"
- "iterated Eulerian transformation" real roots
- "2607.01572" proof Eulerian
- Eulerian triangle square real rooted
- Eulerian transformation real-rootedness 2026
- Mao Wang Eulerian square proof 2026
- Eulerian transformation Brändén Vecchi

Targeted repository searches distinguished ordinary matrix squares from entrywise squares, total positivity of the Eulerian triangle, and unrelated uses of “Eulerian.” The search located Zeng's Delannoy-square result above. **No earlier proof of the all-degree Eulerian-square theorem was located in the sources checked.**

The contribution of the accompanying paper is the all-degree Eulerian-square theorem, with simplicity of every root and strict negativity of every nonzero root. The paper includes the analytic estimates, exact finite certificates, and their reproducible verification programs. Its bibliography contains the six mathematical sources used directly: Mao–Wang, Brändén–Jochemko, Athanasiadis, Petersen, Darroch, and Gardner.

## Prompt-required OpenAI repository search

The research prompt additionally requests a search of the public [OpenAI mathematics repository](https://github.com/openai/math). This search record belongs to the audit and is not a mathematical reference in the paper.

The live [manuscript index](https://raw.githubusercontent.com/openai/math/main/CONTENTS.md) inspected on November 1 listed **721 manuscripts in 373 result families**. Case-insensitive searches of that index gave zero occurrences of each of Eulerian, Narayana, Delannoy, and 2607.01572.

Targeted GitHub code searches were also inspected at repository snapshot 4eaee87548250b2682affda7d05d947c05554bae:

| Query | Result relevant to this audit |
| --- | --- |
| Eulerian | Matches used Eulerian-coordinate terminology in unrelated Vlasov–Maxwell or Boltzmann work. |
| Narayana | Matches included unrelated occurrences within the name Narayanan. |
| Eulerian transformation | Returned unrelated PDE text containing both search terms. |
| 2607.01572 | No matching result. |

No matching Eulerian matrix-square theorem was located in the index or these targeted code searches.
