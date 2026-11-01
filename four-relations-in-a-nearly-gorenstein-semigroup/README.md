# Four minimal relations in a nearly Gorenstein numerical semigroup

**Author:** GPT-6 Astra. **Status:** COMPLETE_KNOWN_RESULT.

The assertion that every four-generated nearly Gorenstein numerical semigroup which is not almost symmetric has five or six minimal relations is **false**. The known example `S=<6,7,8,9>` has `PF(S)={10,11}`, NG vector `(11,10,10,10)`, and exactly four minimal defining relations:

```text
y^2 - xz,   yz - xw,   z^2 - yw,   w^2 - x^3.
```

The paper proves that these generate the whole kernel of `(x,y,z,w) -> (t^6,t^7,t^8,t^9)` and that every generating set needs at least four elements. A separate exact graph certificate verifies the complete Betti set `{14,15,16,18}`.

[Read the paper](paper.pdf) · [Proof map](reproducibility/PROOF_MAP.md) · [Literature review](reproducibility/LITERATURE_REVIEW.md) · [Verification status](reproducibility/STATUS.md)

## Source distinction

This is an exposition and verification of a known example. Its exact minimal presentation appears in Gomes, O'Neill and Torres Davila (2023), [Example 18](https://doi.org/10.37236/10380). The supplied question follows [survey Problem 23, version 3](https://arxiv.org/html/2406.00790v3), which proposes `{5,6}`. Its cited original, [Moscariello-Strazzanti Question 4.3](https://doi.org/10.1007/s00009-021-01761-1), allows four or five relations for type two, and six for type three. This example realizes the original question's four-relation branch.

## Reproduce

With Python 3.9 or later and no third-party Python packages:

```text
cd reproducibility
python src/proof_verify.py
python src/search_verify.py
```

The first checks the elementary normal-form proof; the second independently enumerates every factorization graph through the proved degree bound 28 and verifies the saved certificate. Both passed from a clean temporary copy. Run without Python's `-O` flag.

To rebuild the paper with an installed TeX Live or MiKTeX distribution:

```text
python src/build_paper.py
```

The self-contained source is `reproducibility/paper/main.tex`; the rebuilt PDF is written to `reproducibility/output/research_paper.pdf`. The final four-page PDF was visually reviewed, and its authorship and references were checked.

Code is covered by the repository's MIT license; the paper, notes, and certificates use its CC BY 4.0 license. The package contains original exposition and verification material with references to the published sources.
