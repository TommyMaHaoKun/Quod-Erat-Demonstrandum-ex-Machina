# Verification record

Verified on **2026-10-30** with Lean **4.19.0** and the Mathlib revision
locked in this project's `lake-manifest.json`.

Every source module below was compiled from this directory into a fresh
project-local output directory, in dependency order. The project root was
then compiled and its main-theorem axiom reports inspected. All compiler
exit codes were 0; there were no `sorryAx` dependencies. Each main theorem
reported exactly `[propext, Classical.choice, Quot.sound]`.

This local check used the Lean compiler directly with `LEAN_PATH` pointing
to cached libraries for the pinned Mathlib and this project's newly compiled
modules. It did not import modules from the original development project.
It is a source-compilation and axiom audit, not a claim of a fresh network
installation or a hosted CI run. See the README for the portable Lake commands.

Source SHA-256 hashes:

| File | SHA-256 |
|---|---|
| `MathLean/Riesz.lean` | `4a2a81686fdefc379d6a847cf1a44c39db5182c235e06311cd24eff1016a9b23` |
| `MathLean/RieszCircle.lean` | `96c06bb8b3c46965276acbb024d42893c4e3135da1cd76bd0c2b19ca3682e1c4` |
| `MathLean.lean` | `599f411309c4fb77a8b3d2fbd0d6121d969a7f78e6ebf1de1e81902f4162a441` |
