# Mathematical and verifier review

Reviewer: GPT-6 Astra, independent internal proof-checking agent.

Date: 2026-11-01.

This record describes an AI-assisted mathematical and code review. It does not
claim external human review or Lean formalization.

## Reviewed claim

For the exact Question 8 assertion, the semigroup `S=<6,7,8,9>` is a
counterexample: its four generators are minimal, it is nearly Gorenstein and
not almost symmetric, and its defining ideal has exactly four minimal
binomial generators.

## Independent proof checks

1. **Cofiniteness and exact gaps.** The represented consecutive block 12--17,
   followed by addition of 6, proves conductor 12. Enumeration below 12 gives
   exactly the gaps `1,2,3,4,5,10,11`.
2. **Exact pseudo-Frobenius set.** Testing every minimal generator suffices by
   additive closure. The small gaps have explicit failing sums. The two large
   gaps pass. Negative integers below -6 fail on addition of 6; all six
   remaining negative candidates have explicit failing sums. Thus
   `PF(S)={10,11}` with the definition taken over all integers.
3. **Nearly Gorenstein.** The vector `(11,10,10,10)` gives a complete 4-by-2
   membership table, whose entries all belong to the generator set.
4. **Not almost symmetric.** For the gap 1, its complementary gap is 10;
   the gap 1 fails the pseudo-Frobenius condition because `1+9=10` is a gap.
5. **Generation of the entire kernel.** The four reductions
   `y^2 -> xz`, `yz -> xw`, `z^2 -> yw`, `w^2 -> x^3` decrease the positive
   auxiliary weight `(1,4,6,7)`. The six terminal bases are
   `1,y,z,w,yw,zw`. Their semigroup degrees have different residues modulo 6.
   Reducing any kernel polynomial therefore gives the zero polynomial, which
   proves that the four relations generate the full defining ideal.
6. **Minimality.** There is no relation below degree 14. Hence no element of
   the ideal multiplied by the homogeneous maximal ideal occurs below degree
   20. The four relations, at distinct degrees 14, 15, 16, 18, yield four
   independent nonzero classes modulo that product ideal. This establishes
   the lower bound four, as well as the upper bound already proved.
7. **Source boundary.** The counterexample concerns the supplied assertion
   `{5,6}`. The 2021 source's Question 4.3 explicitly includes four generators
   in its type-two case, so the example is compatible with that formulation.

## Code review

Reviewed `src/search_verify.py`, which enumerates full factorization fibers
and their connected components, and checks the normal-form certificate.

- Its recursive enumeration is exhaustive because each exponent is tested
  from zero through the largest value allowed by the remaining degree.
- Its component traversal joins factorizations precisely when their supports
  intersect, matching the mathematical factorization graph.
- The finite cutoff `F+8+9=28` is justified: above it every pair of distinct
  generators can occur together in a factorization. The support-incidence
  graph is then connected, so no higher Betti degree is omitted.
- Certificate serialization is recomputed with exact integer arithmetic and
  compared with the saved JSON.
- The six negative pseudo-Frobenius candidates are now checked and recorded.
- The termination weights now match the independent proof: `(1,4,6,7)`.

The standard-library verifier `src/proof_verify.py` was written independently
of the search algorithm. It checks the finite inputs to the algebraic
normal-form and minimality proof. It does not derive its conclusion from the
search program or saved search certificate.

## Executed checks

Both commands completed successfully on 2026-11-01:

```
python src/search_verify.py --write
python src/proof_verify.py
```

The first regenerated the JSON after the review edits and reported exact
Betti degrees `14,15,16,18`, two components each, and `rho=4`. The second
reported `PASS` for the independent normal-form proof data.

## Remaining release checks

This review concerns the mathematics and verifier sources. Final paper prose,
rendered PDF pages, source citations, clean-copy execution, and release-file
selection are to be checked against the completed deliverables by the parent
agent. This record should not be read as reporting checks performed before
those files existed.
