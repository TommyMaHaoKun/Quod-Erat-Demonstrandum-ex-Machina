# Verification record

Checked on 2026-10-30 with Lean 4.19.0 and pinned Mathlib v4.19.0
(`c44e0c8ee63ca166450922a373c7409c5d26b00b`).

All 16 modules below were compiled from the published project directory
into a fresh standalone output directory, in dependency order. Every
compiler exit code was 0. The published root module was also checked.
This pass used an existing copy of the pinned dependency libraries; it
did not rely on the original workspace's compiled project modules.
The standard fresh-install commands are in [README.md](README.md).

The final axiom reports for `MathLean.Domino.minimum_count` and
`MathLean.Domino.minimum_iff_ceiling` contain only:

```
[propext, Classical.choice, Quot.sound]
```

These reports include the dependencies of the geometric, bijection,
finite-state and recurrence proofs. Source inspection found no `sorry`,
`admit`, custom `axiom`, or `native_decide` in the proof sources.

## SHA-256 of checked files

| File | SHA-256 |
|---|---|
| `lake-manifest.json` | `a4aac9be5ecfc50a0ac4dd3000078db9c83f7523c2f25f428f7e5f5e6dbb4a72` |
| `lakefile.toml` | `487db1bc682b63a7092aa12dbc601a5cf3af3ece21f8d0756c76bb41384c1ad2` |
| `lean-toolchain` | `55e97be96000b5e9e290c9e74482e5e317861499a5540353ce845471bded8cea` |
| `MathLean/Domino.lean` | `479e2fe0c35232e1831fc19553628c55323dc8f23434614ddf81821bad713695` |
| `MathLean/DominoBounds.lean` | `be053bd9cc13d2f07369052c4267f97f5be2beddbab9643e5a4032be7cbe861c` |
| `MathLean/DominoBudgetData.lean` | `de12994ee22071bc1b0ab32e979dbfc758dae47bc65efbaab4bdb5239442a18d` |
| `MathLean/DominoBudgetLift.lean` | `acb93b7e3f890c17f99ada59be4b1e39ff7f347a44dc42bc84dbbccbf3e78e7f` |
| `MathLean/DominoBudgetPaths.lean` | `dc1be211b29a1cd37d91c33209450979a0c117b55f3659601721549b48eec3dd` |
| `MathLean/DominoCount.lean` | `df6dc72ca8fe2a3bb378f3718c463bd56811ec2116ff10ea5d0da5b3b028abc3` |
| `MathLean/DominoCountCertificate.lean` | `52bb6a1f4bb65992eaccecced92caa79ff11a0f5a3d88583178ffab9fd2e87db` |
| `MathLean/DominoCountData.lean` | `aa14e391c88af5a4cf399014edd24990d407c275dec99c7d310a201cddd456d7` |
| `MathLean/DominoEncoding.lean` | `035edccc2b23df5897d06d6a1d151a6318aab9f586fa8a450360d9f7c6d5ab0a` |
| `MathLean/DominoGeometry.lean` | `9edf3860ad88a23fccfa272507b97abd84df26197f4883e2d0809c5fe05b5c51` |
| `MathLean/DominoGraphPaths.lean` | `61450dbdebb8da1f88136de41d2ef5e34190c332527bc5a7ec8dd6b70680c897` |
| `MathLean/DominoMinimum.lean` | `b2463cb8ec948e495dc6c3e5a49271ff9b403cd397305acc6dbbf8cbf2770f98` |
| `MathLean/DominoPaths.lean` | `f50c5502ca8cadcd7a806b3b55a1206655779a2853de51af1686593989950352` |
| `MathLean/FiniteTransfer.lean` | `6848d2abb0839e7ec56f496944758dde97cb5657ec5a0889485c5a60059314b3` |
| `MathLean/PathLists.lean` | `794dc389df66f46a5e77b4b7d01a6b37fec54fcac37e01d3f6af6acfbe2f7fa2` |
| `MathLean/Transfer.lean` | `5e896db512df7bedd6dc9a81b113086e6d532b5f8d219c48d0bc21ac8663ef5a` |
| `MathLean.lean` | `3221a8c66015705e73c0ccadfc416863251eb57d556e5cc64d6c7b886e9459fc` |
