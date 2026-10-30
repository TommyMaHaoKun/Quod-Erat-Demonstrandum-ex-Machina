# Lean proof: OEIS A181280

## Formal statement

`MathLean.GramCount.a181280_formula` proves the six-term formula for every
`n >= 4`. `a181280_small` proves the count is zero for `n < 4`.
`matrix_4xn_count_formula` combines both statements for every natural `n`.

The objects counted by `GoodMatrices4n n` are literal binary matrices
`Fin 4 -> Fin n -> Bool`. Their rows are strictly increasing in ordinary
left-to-right lexicographic order. Their Gram matrix is computed over F2,
including diagonal parities, and its rows are strictly decreasing in the
same original row-index order. Rows and columns keep their labels; neither
permutations nor symmetry classes are counted instead of matrices.

For `n >= 4`, the count, viewed as a rational number, equals

```text
  4^n * (6*n^2 - 219*n + 820) / 6144
- 2^n * (3*n + 32) / 288
- 113 * (-8)^n / 49152
+ 16^n / 512
- (-4)^n * (13*n - 164) / 6144
+ 8^n * (288*n - 3473) / 147456.
```

The rational formulation avoids negative natural exponents. The left side
is the cardinality of the finite matrix type, not a sequence postulated to
satisfy a recurrence.

## Proof structure

The formal proof establishes a bijection between the original matrices
and accepted column words, and identifies their count with the iteration
of a linear transfer operator on all 8192 states. It checks 17 exact count
vectors, all 16 successive transitions, the full degree-16 vector
relation, and the initial accepting indicator. Linearity propagates the
vector identity to every length. The independently checked formula has
the same recurrence and sixteen initial values, so uniqueness proves the
result for every n.

The certificate uses the full state space. It does not assume a smaller
quotient or infer a recurrence from scalar samples. A faster list of legal
transitions is proved equal to the original labeled transition operator.
Large finite checks are split into blocks and verified by Lean's kernel.

This formalization proves the original counting formula. It does not
formalize the paper's Fourier derivation, minimality of its eventual
recurrence, rational-generating-function claims, or novelty claims.

## Rebuild

Install Lean's `elan` toolchain manager and Python 3.9 or later. Run from
this `lean/` directory:

```sh
lake exe cache get
python check.py
```

`check.py` invokes Lean sequentially in import order and prints the main
theorem's axiom reports. Python performs no arithmetic certification;
every proof is in the Lean sources. Sequential compilation limits memory
use. A fresh build of the finite certificates can take tens of minutes.
The report is saved to `.lake/check-results.json`.

Lean 4.19.0 and Mathlib v4.19.0 are pinned. The manifest locks Mathlib to
`c44e0c8ee63ca166450922a373c7409c5d26b00b` and fixes its dependencies.
The first dependency-cache setup needs internet access.

## Verification

The final theorems depend only on `propext`, `Classical.choice`, and
`Quot.sound`. There are no proof placeholders, custom axioms, or
`native_decide` calls. No generated numerical data is trusted: Lean
checks every transition and the all-state vector relation.

See [VERIFICATION.md](VERIFICATION.md) for the build record and checked
source hashes. This is formal verification of the stated mathematical
result, not external peer review of the paper.

Lean code and the build helper are covered by the repository's
[MIT License](../../LICENSE); documentation is under
[CC BY 4.0](../../LICENSE-CC-BY-4.0.txt).
