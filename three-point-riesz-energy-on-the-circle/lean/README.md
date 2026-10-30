# Lean proof: Three-point Riesz energy: Fan's Conjecture 5.9

## Formal statement and coverage

`MathLean.Riesz.fan59` proves endpoint maximality for `r >= 2`,
`pi/2 < phi <= 2*pi/3`, and `0 <= psi <= 2*pi - 3*phi`.
It constructs positive endpoint masses `(U,U,W)` with total mass one
whose energy dominates every probability measure `(u,v,w)` at every
admissible `psi`. Thus the formal statement includes attainment as well
as the upper bound.

`circleEnergy` uses squared Euclidean distances between the circle points
`(cos psi, sin psi)`, `(cos phi, sin phi)`, and `(cos phi, -sin phi)`, raised
to `r/2`. `RieszCircle.lean` proves the geometric identities and ordering;
`Riesz.lean` proves the convexity comparison and the algebraic energy bounds.

The paper's additional strict uniqueness claim for `r > 2`, constancy of
the optimized energy for `r = 2`, the `0 < r < 2` minimization result,
the stated simplified trigonometric maximum, and the consequence for
Conjecture 5.6 are **not formalized here**.

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
