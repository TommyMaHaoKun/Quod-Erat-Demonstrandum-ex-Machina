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
| `MathLean/Zarankiewicz.lean` | `914886d81b39def1bfa17849b4d06268d06ebbd17c2a409ee490f7c739cd5a9f` |
| `MathLean/ZarankiewiczBase.lean` | `2871928e86f102280c988dabe9c5639a4b4d2c4db120b34aa39dcc0269d4e175` |
| `MathLean/ZarankiewiczConstruction.lean` | `8af91aa5aacb5d868197983c34d5c0840d0dc739b9f97128b72866d6f9ff9bc1` |
| `MathLean.lean` | `3cf4a7c5e52ec870708c4b3349ff5f281cc7adbbd7cf593ceaef5932d404a3a9` |
