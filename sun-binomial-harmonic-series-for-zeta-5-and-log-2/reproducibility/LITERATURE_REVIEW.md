# Literature review for Question 6

Audit date: 2026-11-01 (Asia/Shanghai).

## Exact target and attribution

The target is Zhi-Wei Sun's Conjecture 3.11, equation (3.15), in *Various conjectural series identities*, arXiv:2603.29973v3, dated 13 April 2026. The conjecture itself is dated 12 April 2026. The arXiv abstract page still lists v3 as the latest revision on the audit date.

- Versioned primary text: https://arxiv.org/html/2603.29973v3
- Version and publication history: https://arxiv.org/abs/2603.29973
- PDF: https://arxiv.org/pdf/2603.29973v3

With `P(x)=21x^3-22x^2+8x-1`, the target is

```text
sum(k>=1) 256^k [14 P(k)(H_(2k-1)-H_(k-1))-P'(k)]
                 / [k^7 binom(2k,k)^7]
= (93/2) zeta(5)+pi^4 log(2).
```

The statement is still explicitly conjectural in the current source. Sun's name, conjecture number, equation number, and version must appear in the paper. The series itself is Sun's; this project's contribution is a derivation of its evaluation from Au's earlier parameter identity, with the differentiation and auxiliary evaluations written out.

## The companion evaluation and the parameter identity

Kam Cheong Au, *Wilf-Zeilberger seeds and non-trivial hypergeometric identities*, arXiv:2312.14051v4 (10 October 2024), published in *Journal of Symbolic Computation* **130** (2025), article 102421.

- Version history: https://arxiv.org/abs/2312.14051
- Versioned paper: https://arxiv.org/html/2312.14051v4
- Journal DOI: https://doi.org/10.1016/j.jsc.2025.102421

The current arXiv version is v4. Example XI, equation (4.2), proves

```text
sum(k>=1) 256^k P(k) / [k^7 binom(2k,k)^7] = pi^4/8.
```

The source attributes the conjecture to Jesus Guillera. Sun's Remark 3.11 dates that conjecture to 2003. Au's Example XI supplies its proof by two WZ pairs; equation (4.4) is the one-parameter transformation used in this project. The hypergeometric polynomial on its right is exactly `P(n+2a)`. After duplication of `(4a+1)_(2n)`, its right-hand side is

```text
-(8/a) sum(n>=1) 2^(-6n) P(n+2a)
       (2a+1)_n^7 / [(n+2a)^7 (2a+1/2)_n^7].
```

This gives a legitimate parameter deformation rather than an inference from the single evaluation at `a=0`. Au's proof uses Proposition 2.1 to sum the WZ pairs. Example XI displays the two seed functions and derives (4.4); it omits the large intermediate polynomial `p2`, explicitly explaining that it is obtained by Gosper's algorithm. Any new certificate reconstruction in the present project is verification of this inherited argument, and the transformation remains attributed to Au.

Au's Example XV also evaluates the auxiliary inverse-binomial sum needed after differentiation:

```text
sum(k>=0) (4k+3)(1)_k^4 /
          [(k+1)(2k+1)^5(1/2)_k^4]
= (93 zeta(5)-7 pi^2 zeta(3))/4.
```

This identity and its proof are inherited mathematical ingredients and are explicitly cited in the manuscript. The optional supplement independently reconstructs the specialized WZ certificate and all four coefficient calculations used to obtain this evaluation from Au's equation (5.2). The analytic transformation (5.2) remains an established input attributed to Au.

## Correction to the auxiliary Gamma expression in Sun

Both the HTML and PDF of Remark 3.11 print `Gamma(2x)` to the first power in the denominator of the auxiliary function. The binomial series instead corresponds to

```text
f(x)=2 P(x) 256^(x-1) Gamma(x)^14 / Gamma(2x)^7.
```

Indeed, `Gamma(k+1)=k Gamma(k)` and `Gamma(2k+1)=2k Gamma(2k)` give exactly

```text
f(k)=256^k P(k)/(k^7 binom(2k,k)^7).
```

Logarithmic differentiation of the corrected Gamma factor gives

```text
f'(k)=256^k/[k^7 binom(2k,k)^7]
       * [P'(k)+8 log(2) P(k)-14 P(k)(H_(2k-1)-H_(k-1))].
```

Together with the companion evaluation, the exact target is equivalent to
`sum(k>=1) f'(k)=-(93/2) zeta(5)`. The missing seventh power is therefore a source typographical error, separate from the explicit target (3.15). The project follows (3.15) exactly.

## Later and related primary papers checked

1. Kam Cheong Au, *Discovering hypergeometric series with harmonic numbers via Wilf-Zeilberger seeds*, arXiv:2602.08721v3, dated 4 September 2026. Version history: https://arxiv.org/abs/2602.08721 ; text: https://arxiv.org/html/2602.08721v3 . The abstract page and downloaded full text were checked. Example V gives a parameter identity for the reciprocal Gourevich series and first-order harmonic consequences. This is related WZ methodology. The exact target (3.15), the cubic `21n^3-22n^2+8n-1`, and the `256^n/binom(2n,n)^7` evaluation were not found in this paper.
2. Qing-Hu Hou and Zhi-Wei Sun, *Evaluations of some series via the WZ method*, arXiv:2604.15172v1, dated 16 April 2026. Version history: https://arxiv.org/abs/2604.15172 ; text: https://arxiv.org/html/2604.15172v1 . This later paper proves numerous derivative identities and cites arXiv:2603.29973. Its theorem list and full PDF text were inspected for the target. Its Theorem 1.9 concerns the three-power central-binomial series with numerator `21k-8`; it is a different series. No occurrence of the seventh-power target or its cubic polynomial was found.
3. Zhi-Wei Sun, MathOverflow question 486518, *A series for pi^10 with converging rate 1/64*, posted January 2025: https://mathoverflow.net/questions/486518 . This post records the companion identity and attributes its WZ proof to Au. Its higher-order harmonic target differs from the present first-order identity.

These papers were inspected as actual primary sources, with the search engine used only to locate them. Older or unrelated identities in search snippets were not treated as proofs of the target.

## Public repository audit

The current `openai/math` default branch was inspected at commit
`4eaee87548250b2682affda7d05d947c05554bae`:

- https://github.com/openai/math/tree/4eaee87548250b2682affda7d05d947c05554bae
- https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/CONTENTS.md

The initial recursive root-tree request was truncated at 55,173 entries. It was therefore supplemented by a separate complete recursive request for the `preprints` subtree, which returned 13,578 entries with `truncated=false`. The full `CONTENTS.md`, all preprint paths, and title/path matches for Sun, harmonic, binomial, hypergeometric, WZ/Wilf, series, and zeta were examined. No listed preprint on this target or an equivalent hypergeometric evaluation was found. This inspection covers the published preprint catalog and its complete path inventory; it is not a claim that every Lean source file was read.

Two further repositories found through exact-source searches were checked:

- https://github.com/chokmah-me/fragile-proof-audit/blob/main/docs/WORKPLAN.md lists the Sun batch `2603.29973` as work awaiting a `HypergeometricEval` component; this entry supplies no proof of the present conjecture.
- https://github.com/demonstrandum-research/artifacts/blob/main/RESULTS.md concerns other problems. Its Sun entry is a determinant/permanent conjecture, not the present series.

Saved tree responses and catalog snapshots in `literature/` document the scope of this audit. These audit-only files and third-party PDFs need not be republished in the final proof package.

## Search record and conclusion

Searches made on 2026-11-01 included the source identifier `2603.29973`, the exact phrase `Conjecture 3.11`, the coefficient patterns `21k^3-22k^2+8k-1` and `21n^3-22n^2+8n-1`, combinations with `93/2`, `zeta(5)`, `log 2`, `harmonic`, and Guillera/Au/Sun, and a targeted `site:github.com/openai/math` search. Equivalent Gamma-derivative wording and recent papers by Sun and Au were also checked.

No separate published proof of this exact first-order identity was located in the sources and repositories inspected. The appropriate positioning is: **an explicit proof of Sun's Conjecture 3.11 obtained by differentiating Au's established transformation, with the required analytic and Euler-sum steps supplied.** The existing transformation, WZ method, and auxiliary special-value identities receive full attribution. The project makes no claim to invent those tools or to have exhaustively searched all mathematical literature.
