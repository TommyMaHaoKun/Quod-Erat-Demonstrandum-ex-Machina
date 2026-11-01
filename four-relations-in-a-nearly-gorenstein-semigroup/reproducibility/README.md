# Four minimal relations in a nearly Gorenstein numerical semigroup

Author: **GPT-6 Astra**.

**Question 8 is false as written.** The semigroup `S=<6,7,8,9>` has exactly four minimal generators, is nearly Gorenstein, is not almost symmetric, and has `rho(S)=4`.

Its complete nonnegative gap set is `{1,2,3,4,5,10,11}`, its Frobenius number is 11, and its pseudo-Frobenius set is `{10,11}`. The NG vector is `(11,10,10,10)`. Almost symmetry fails at the gap 1, since `11-1=10` is a gap and 1 is not pseudo-Frobenius.

Under `(x,y,z,w) -> (t^6,t^7,t^8,t^9)`, a minimal generating set for the entire defining ideal is

```text
y^2 - xz,   yz - xw,   z^2 - yw,   w^2 - x^3.
```

The paper proves generation by terminating monomial reduction, and proves that every ideal-generating set needs at least four elements. A separate exact factorization-graph check gives the four Betti degrees `14,15,16,18`.

## Attribution and exact scope

This is a verified **known result**, with final checks recorded in [STATUS.md](STATUS.md). Gomes, O'Neill and Torres Davila (2023), Example 18, already give this exact four-relation minimal presentation. Moscariello and Strazzanti (2021), Proposition 3.4, includes this arithmetic-sequence example in the nearly Gorenstein class.

The supplied prompt follows Problem 23 of the survey `arXiv:2406.00790v3`, whose proposed set is `{5,6}`. The cited original **Question 4.3** instead allows **four or five relations in type two**, and six in type three. Our example gives the negative answer to the supplied formulation and realizes the four-relation branch of the original question. The original type-dependent classification is outside the resolved claim.

See [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md) for exact source locations and the search audit, and [PROOF_MAP.md](PROOF_MAP.md) for the proof dependencies.

## Paper and verification

- [English paper](../paper.pdf)
- [Self-contained LaTeX source](paper/main.tex)
- [Complete exact certificate](certificates/search_counterexample_6_7_8_9.json)

From this directory, with Python 3.9 or later:

```text
python src/proof_verify.py
python src/search_verify.py
```

Both use the Python standard library. The first checks the elementary proof data. The second independently enumerates full factorization graphs through the proved bound 28, checks the hypotheses, and compares every recorded value with the saved certificate. It supports `--write` to regenerate the certificate. The programs locate their data relative to their own files and also work when invoked from another working directory. Run without Python's `-O` flag, because the graph verifier uses assertions.

To rebuild the PDF with an installed TeX Live or MiKTeX distribution:

```text
python src/build_paper.py
```

The build script compiles twice and rejects unresolved references and overfull or underfull boxes. The source uses standard LaTeX packages and an inline bibliography; no downloaded assets are needed.

## Supplementary records

`src/search_semigroups.cs` and the discovery logs preserve the exact initial search, which stopped after 15 tuples when the counterexample was found at maximum generator 9. They are optional discovery records; the two Python verifiers reproduce all results used in the paper. The locally compiled executable and downloaded third-party source cache are excluded from publication.

The note and verification programs were prepared by GPT-6 Astra. Mathematical and source reviews are recorded in `certificates/`.
