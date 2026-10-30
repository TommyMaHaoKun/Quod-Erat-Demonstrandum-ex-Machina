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
| `MathLean/Cyclic.lean` | `907902123569aec5741ad3ed5cce3910d2dada10a3e0625316f74fe7ee6c39a8` |
| `MathLean.lean` | `940469650b9c1740a29a9517bc275e8fcde6a1816ff4b7a32a3bb9cdbe716049` |
