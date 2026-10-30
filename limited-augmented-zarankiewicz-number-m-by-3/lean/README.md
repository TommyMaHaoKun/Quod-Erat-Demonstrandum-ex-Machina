# Lean proof: Limited augmented Zarankiewicz number for three columns

## Formal statement and coverage

`MathLean.Zarankiewicz.zarankiewicz_exact` proves, for every natural
`m >= 3`, that `floor((3*m+4)/2)` is the greatest attainable value.
The `IsGreatest` statement includes both a universal upper bound and an
admissible limited configuration attaining it. In particular, the value
at `m = 14` is 23.

`Zarankiewicz.lean` defines labeled cells, the base, disjoint 2-edge endpoints,
occupied cells, and admissibility conditions S, C1, C2, C3. Both endpoint
orientations are quantified in C2 and C3, including degenerate 2-edges.
`Limited` means maximum base cardinality among all C4-free bases, not merely
maximality under inclusion. `ZarankiewiczBase.lean` derives the extremal-base
structure and the upper bound from these definitions.
`ZarankiewiczConstruction.lean` checks the explicit attaining family.
No extremal-base structure or construction admissibility is assumed.

## Rebuild

Install Lean's `elan` toolchain manager, then run these commands from this
`lean/` directory (the same commands work in a shell or PowerShell):

```sh
lake exe cache get
lake build
lake env lean MathLean.lean
```

`lean-toolchain` selects **Lean 4.19.0**. `lakefile.toml` selects Mathlib
**v4.19.0**, and `lake-manifest.json` locks Mathlib to
`c44e0c8ee63ca166450922a373c7409c5d26b00b` and pins its transitive dependencies.
The initial setup needs internet access and space for the dependency cache.
Each problem's Lean project is independent; run the commands inside the
chosen project's directory, not at the repository root.

## Proof checking

The final command prints the axioms of the main theorem(s). The expected
set is `[propext, Classical.choice, Quot.sound]`, the standard axioms used
by these Mathlib proofs. There are no `sorry` placeholders, custom axioms,
or `native_decide` proofs. The committed files contain source proofs, not
precompiled `.olean` files or a local dependency cache.

See [VERIFICATION.md](VERIFICATION.md) for the checked source hashes and
the local verification record. Formal checking does not establish novelty
or external peer review of the paper, and its scope is exactly the statement
described above.

Lean code is covered by the repository's [MIT License](../../LICENSE);
this documentation is under [CC BY 4.0](../../LICENSE-CC-BY-4.0.txt).
