# Verification record

Fresh publication-copy build completed on 2026-10-30, using Lean 4.19.0
(compiler commit `6caaee842e94`) and pinned Mathlib v4.19.0
(`c44e0c8ee63ca166450922a373c7409c5d26b00b`).

All four proof modules and the publication root passed in a separate output
directory. Source hashes were checked before and after compilation. Only
dependency outputs were reused; project proof outputs were freshly built.
The axiom reports for `a006343_recurrence`, `series_inverseSpec`, and
`inverseSpec_unique` contain only `[propext, Classical.choice, Quot.sound]`.
The source audit found no placeholders, custom axioms, or `native_decide`.

The exact checked scope and the original inverse specification are in
[README.md](README.md). Formal verification does not imply a novelty claim
or external peer review.

| Source | Result | SHA-256 |
|---|---|---|
| `MathLean/ArkonDifferential.lean` | Passed | `70ac9b3475de4862d9aecd8f9ecab6fcfd590a515094222e8105f1403bf9cef0` |
| `MathLean/ArkonSeries.lean` | Passed | `94203293f21ce02b8324d7358a90f3d65c70e345d37ce51658262e131a369d0f` |
| `MathLean/ArkonRecurrence.lean` | Passed | `129c29e4802121f7f0750c740a9fa23063f5f4eafe0068107e2c05c4f6e2025c` |
| `MathLean/Arkon.lean` | Passed | `ce3373a322363f86c3d7a348cd04f5ec1095dd18f5d167421d70396f3819e1d9` |
| `MathLean.lean` | Passed | `1fdff2fe9d3f6d4a838c3419490c4ad7a68c1fc3661e5be5d6d92747fcc4290f` |
