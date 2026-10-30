# Lean proof: minimum maximal domino packings of the 4 x n rectangle

## Formal statement

`MathLean.Domino.minimum_count` proves, for every positive width `n`,

```lean
(Nat.card (MinimumPackings n) : Int) = MathLean.DominoCount.formula n
```

The objects counted are domino placements on the labeled rectangle, with
no quotient by reflections or rotations. A column records the horizontal
and vertical dominoes starting there. `MaximalPacking` requires at most
one domino per cell and no pair of adjacent uncovered cells, with no
horizontal overhang at either boundary. `MinimumPacking` minimizes the
number of dominoes among all such maximal packings of the same width.

`minimum_iff_ceiling` proves that, for `n >= 2`, these are exactly the
maximal packings of size `ceil(4*n/3)`. Attainment is proved for every
width. For `n = 1`, the unique minimum is the middle vertical domino;
that case is proved separately.

The count is `1, 6, 7, 100, 51, 10, 663, 124, 8, 1892, 178, 8, 3652,
224, 8, 5796` at widths 1 through 16. For `n >= 17`, writing `k = n/3`
with integer division, it is:

- `8` if `n % 3 = 0`;
- `226*k^2 + 106*k - 392` if `n % 3 = 1`;
- `50*k + 24` if `n % 3 = 2`.

The proof checks the local geometric encoding, its inverse and cost
preservation, a minimum-size lower bound, the budget increments and
trimming of the finite graph, and the all-length bijection between the
accepted paths and the physical packings. A checked vector certificate
then gives the recurrence and closed count. The theorem is about the
original packing type, not only a sequence or an abstract graph.

## Rebuild

Install Lean's `elan` toolchain manager and run from this directory:

```sh
lake exe cache get
lake build
lake env lean MathLean.lean
```

The project pins Lean 4.19.0 and Mathlib v4.19.0, with Mathlib commit
`c44e0c8ee63ca166450922a373c7409c5d26b00b` locked in the manifest.
The first build checks substantial finite certificates and can take
several minutes. No Python program or external certificate loader is
needed to check the Lean sources.

## Verification and scope

The main theorems depend only on `propext`, `Classical.choice`, and
`Quot.sound`. There are no proof placeholders, custom axioms, or
`native_decide` calls. Finite computations are checked by Lean's kernel.
See [VERIFICATION.md](VERIFICATION.md) for the source hashes and local
build record. The project contains sources, not compiled files or caches.

The formalized result covers the minimum size and the exact count for
positive widths. It does not certify the paper's novelty claims, its
literature survey, or every additional structural classification in the
paper. Formal checking does not constitute external peer review.

Lean code is covered by the repository's [MIT License](../../LICENSE);
this documentation is under [CC BY 4.0](../../LICENSE-CC-BY-4.0.txt).
