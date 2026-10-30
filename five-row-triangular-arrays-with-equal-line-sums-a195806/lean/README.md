# Lean proof of all six A195806 counting formulas

The six formulas in the [existing paper](../paper.pdf) hold for every bound
`n >= 0`, including every small and boundary case. The theorem counts the
original labeled arrays; it has no assumed counting identity or recurrence.

## Exact objects and result

`MathLean.Triangle.Arrays n` is the type of integer-valued arrays on the
15 labeled triples `(i,j,k)` of nonnegative integers with `i+j+k=4`.
Every entry lies in `[0,n]`, the three corners are zero, and for each
level `c=0,...,4` the sums on `i=c`, `j=c`, and `k=c` agree. The coordinate
enumeration is checked to be injective and to cover exactly these triples.
No rotations, reflections, or row permutations are identified.

The main theorem `original_six_formulas` states

```text
Nat.card (Arrays (6*m+r)) = formula r m    (m : Nat, r : Fin 6).
```

`original_all_bounds` states the same result for arbitrary `n`, taking
`m=n/6` and `r=n%6`. If `formula r m = sum c[r,j]*m^j`, the coefficients are:

| r | c0 | c1 | c2 | c3 | c4 | c5 | c6 |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 25 | 158 | 650 | 2275 | 4680 | 4680 |
| 1 | 16 | 198 | 1133 | 3900 | 8125 | 9360 | 4680 |
| 2 | 105 | 1087 | 4922 | 12350 | 17875 | 14040 | 4680 |
| 3 | 496 | 4148 | 14783 | 28600 | 31525 | 18720 | 4680 |
| 4 | 1759 | 12121 | 35258 | 55250 | 49075 | 23400 | 4680 |
| 5 | 5052 | 29474 | 72197 | 94900 | 70525 | 28080 | 4680 |

Separate `residue_zero` through `residue_five` theorems display the formulas.
The last also proves the paper's factored form
`(m+1)^2*(5052+19370*m+28405*m^2+18720*m^3+4680*m^4)`.

## Proof

1. Prove an explicit integral bijection between the arrays and six bounded
   parameters, in both directions.
2. Count the four independent interval parameters, leaving an exact sum
   over the two difference parameters.
3. Prove a disjoint chamber parametrization of the supported lattice:
   multiplicity 12 in the interior, 6 on the two boundary rays, and 1 at
   the origin. Prove both coverage and uniqueness.
4. Correct the boundary multiplicities, split the rows by parity, and
   evaluate the resulting finite sums using polynomial antidifferences.
5. Check all six final polynomial identities and connect them back to
   `Nat.card (Arrays n)`.

The Python generator used during development only proposed rational
polynomials. The delivered Lean files contain the complete formulas and
prove their summation identities by induction and polynomial normalization.
Neither Python nor finite sample agreement is trusted by the proof.

## Rebuild and verification

Install elan and Python 3.9 or later, then run from this directory:

```sh
lake exe cache get
python check.py
```

The included toolchain and dependency manifest pin Lean 4.19.0 and Mathlib
v4.19.0. All ten proof modules and the root were freshly compiled from
the publication copies. See [VERIFICATION.md](VERIFICATION.md) for hashes
and axiom reports. No precompiled proof files are distributed.

This formalization covers all six original counting formulas. The paper's
additional generating-function, minimal-period, and independent Ehrhart
arguments are not claimed as formalized here. The proof was developed
with Codex; formal checking is separate from novelty and peer review.
