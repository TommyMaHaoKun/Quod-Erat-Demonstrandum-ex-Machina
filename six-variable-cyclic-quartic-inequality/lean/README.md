# Lean proof: Six-variable cyclic quartic inequality

## Formal statement and coverage

For every real six-tuple, `MathLean.Cyclic.cyclic_inequality` proves
`(sum x_i^2)^2 >= (sum x_i) * (sum x_i*x_(i+1)^2)`, with cyclic indices.
`MathLean.Cyclic.equality_iff` proves that the polynomial gap is zero
if and only if all six variables are equal. `sos_identity` checks the
explicit rational sum-of-squares identity with `ring`.

The coefficients are embedded in `MathLean/Cyclic.lean`; rebuilding does
not require Python, an external SOS solver, or loading a certificate file.
The paper's stronger variance-remainder bound is **not formalized here**.

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

The SOS proof contains large rational coefficients; its first compilation
can take several minutes.

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
