# Literature and prior-resolution audit

Research assistant: GPT-6 Astra. Access date: 2026-11-02.

## Exact target and notation

For a compact set K in the real line containing at least two points, let

`U_t(K) = max_mu integral integral |x-y|^t dmu(x) dmu(y)`

and `C_t(K) = U_t(K)^(1/t)`, with the maximum over Borel probability measures supported on K. The question is whether, for every `0 < r < s < 1`,

`C_s(K)/C_r(K) >= C_s([-1,1])/C_r([-1,1])`.

The capacity convention is a maximum-energy convention. In the usual negative-exponent notation, `C_t = Cap_{-t}`. Thus the target is equivalent to maximizing `Cap_q(K)/Cap_p(K)` at intervals when `n=1`, `p=-s`, and `q=-r`, so that `-1 < p < q < 0`.

## Primary sources checked

1. Qiuling Fan, *Riesz capacity ratios with negative exponents*, arXiv:2609.11186v1, submitted 2026-09-10.
   - Abstract and revision history: https://arxiv.org/abs/2609.11186
   - Full text: https://arxiv.org/html/2609.11186v1
   - The live revision history lists only v1.
   - Conjecture 4.1 states exactly the target above and attributes it to Clark and Laugesen, Conjecture 12.
   - Theorem 4.3 proves that every point of a finite real set receives positive equilibrium mass for `0 < t < 1`.
   - Sections 4.3-4.5 develop finite-set calculations and numerical evidence. These sections leave Conjecture 4.1 unresolved.
   - The interval benchmark is `C_t([-1,1]) = [Gamma((1+t)/2) Gamma(1-t/2)/sqrt(pi)]^(1/t)`.

2. Carrie Clark and Richard S. Laugesen, *Maximizing Riesz capacity ratios: conjectures and theorems*, arXiv:2410.14809v1, submitted 2024-10-18; published in *SIAM Journal on Mathematical Analysis* 57 (2025), 5683-5717.
   - Abstract and revision history: https://arxiv.org/abs/2410.14809
   - Full arXiv text: https://arxiv.org/html/2410.14809v1
   - Journal DOI: https://doi.org/10.1137/24M171992X
   - The live arXiv revision history lists only v1. The theorem numbers in this paragraph refer to that version.
   - Conjecture 12 includes the exact target after the substitution above and inversion of the positive ratio.
   - Proposition 3 proves interval maximality in the adjacent region `p <= -1 < q < 1`. The target has both exponents above -1, so it remains outside that theorem.
   - Theorem 11 supplies existence of a maximizing compact set when the denominator exponent is negative.
   - Proposition 19 supplies Hausdorff convergence of capacity and finite-set approximation for negative exponents.
   - Theorem 9 treats optimization among two- and three-point planar sets; it does not settle optimization over all compact subsets of the line.
   - Version-number caution: the two-point conjecture is numbered 17 in this arXiv version, whereas Fan refers to it as Conjecture 16. The target's Conjecture 12 attribution agrees.

3. Fan's accompanying code repository, *Riesz capacity ratios with negative exponents*.
   - https://github.com/vhdvhd/Riesz-capacity-ratios-with-negative-exponents
   - Revision inspected: `b7f26ed82e0205c9941d756d3e29a83ba8a57640`.
   - README and paper notes describe numerical evidence for the one-dimensional conjectures. The rigorously certified higher-dimensional examples concern other questions. No full-domain solution of the interval conjecture was located here.

4. OpenAI mathematical manuscript repository.
   - https://github.com/openai/math
   - Revision inspected: `4eaee87548250b2682affda7d05d947c05554bae`.
   - The complete raw `overview.tex`, current `history.md`, and the names of all 751 immediate directories in `preprints/` were searched.
   - Queries included `Riesz`, `capacity`, `capacities`, `interval`, `Fan`, and `Laugesen`. The catalog contains no listed interval Riesz-capacity-ratio result. Hits about Bochner-Riesz multipliers, Riesz transforms, Fourier restriction, quantum-information capacity, and other capacity notions concern different problems.

5. Newer related work listed on Richard Laugesen's research page.
   - Author page: https://publish.illinois.edu/rlaugesen/research/
   - Clark and Laugesen, *Riesz energy deformation through insulated strips*, arXiv:2603.04649v2, revised 2026-07-16: https://arxiv.org/abs/2603.04649 . This paper treats interpolation between exponents differing by one and an approach to a Polya-Szego capacity problem.
   - Clark and Laugesen, *Toward Polya and Szego's conjecture for logarithmic vs Newtonian capacity*, arXiv:2609.35438v1, submitted 2026-09-28: https://arxiv.org/abs/2609.35438 . Its abstract explicitly presents a conditional result toward the logarithmic/Newtonian problem. This is a different parameter regime from Question 9.

## Search scope and outcome

Public searches used the exact paper title and arXiv identifier; `interval conjecture` with `Riesz`, `capacity`, and `proof`; `Fan Conjecture 4.1 capacity`; `Riesz Conjecture 12 interval`; `Clark Laugesen interval capacity ratio proof`; counterexample formulations; and repository-specific searches of `openai/math`.

A public claim concerning Fan's Conjecture 5.9 was also found. It concerns a moving three-point configuration on a circle, not the present interval capacity-ratio conjecture, so it does not resolve Question 9.

No existing proof or counterexample resolving the complete target was located in this audit. The primary sources checked retain the target as a conjecture. This is the outcome of the stated search, not a claim that every unpublished or unindexed source has been examined.

## Additional audit of the proof method

After the project developed its comparison using monotone transport of beta measures and mixtures of Poisson interval partitions, a second targeted search checked combinations of `Riesz capacity`, `Poisson`, `partition`, `beta`, `transport`, `sinh`, and `capacity ratios`, together with `interval conjecture Poisson` and related generalized-Gini formulations. No prior proof of the target or of the particular beta-transport comparison was located. Results on Riesz modulated-energy transport estimates, standard Bessel-Riesz capacities, and random combinatorial partitions address different statements.

The standard ingredients in that route remain standard: the beta/gamma formulas, the generalized binomial expansion, homogeneous Poisson processes and thinning, monotone likelihood-ratio ordering, Jensen's inequality, the power-mean inequality, and one-dimensional quantile transport. The contribution is their particular combination into an interval-normalized energy comparison and its application to the capacity-ratio conjecture. The proof and its independent internal mathematical audits are supplied separately.

## Attribution and project scope

The conjecture belongs to Clark and Laugesen's capacity-ratio program and is explicitly restated by Fan. The interval capacity formula, the finite-set positivity theorem, existence of optimizers, and continuity under Hausdorff approximation must be attributed to the sources above when used.

The final manuscript proves the exact full-domain inequality, with equality only for nondegenerate closed intervals. It also proves the monotone beta-transport comparison and derives the classical interval formula within the same argument. The preliminary Fourier/entropy notes are not used by the final proof. The literature audit and the mathematical verification are distinct records; the numerical examples are optional supporting checks.
