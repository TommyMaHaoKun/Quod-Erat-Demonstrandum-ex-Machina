# Verification record

Checked on 2026-10-30 with Lean 4.19.0 and pinned Mathlib v4.19.0
(`c44e0c8ee63ca166450922a373c7409c5d26b00b`).

The geometric/semantic encoding, cardinality equivalences, linear
recurrence propagation, and closed formula were compiled from Lean
source. All sixteen full-state transition modules completed with exit
code 0. The true initial indicator, all-state vector relation, and
sixteen initial scalar counts also passed kernel checks. Finally the
unconditional theorem module and the published project root both
completed with exit code 0.

The finite certificates were checked in blocks of 128 states, using a
transition implementation proved equal to the original labeled operator.
The build used an SSD copy of the pinned dependency cache. Published
source files were copied byte-for-byte from the checked files; no
precompiled artifacts or local caches are included in the repository.

The axiom reports of `MathLean.GramCount.a181280_formula`,
`a181280_small`, and `matrix_4xn_count_formula` contain only:

```
[propext, Classical.choice, Quot.sound]
```

No proof source contains `sorry`, `admit`, custom `axiom` declarations,
or `native_decide`. The result has no unproved recurrence, initial-count,
or automaton-correspondence hypotheses.

The six-term formula holds for actual `Fin 4 -> Fin n -> Bool` matrices
with the stated ordering and binary Gram conditions, for every n >= 4.
The smaller widths are proved to have count zero. See [README.md](README.md)
for the exact scope and the sequential rebuild command.

## Transition checks

Each row covers all 8192 states. Timings are local observations, not
requirements for other machines.

| Module | Exit code | Seconds |
|---|---:|---:|
| `BinaryGramCertificate00` | 0 | 169.5 |
| `BinaryGramCertificate01` | 0 | 197.5 |
| `BinaryGramCertificate02` | 0 | 210.1 |
| `BinaryGramCertificate03` | 0 | 214.1 |
| `BinaryGramCertificate04` | 0 | 215.5 |
| `BinaryGramCertificate05` | 0 | 224.3 |
| `BinaryGramCertificate06` | 0 | 209.9 |
| `BinaryGramCertificate07` | 0 | 210.7 |
| `BinaryGramCertificate08` | 0 | 212.7 |
| `BinaryGramCertificate09` | 0 | 211.9 |
| `BinaryGramCertificate10` | 0 | 212.2 |
| `BinaryGramCertificate11` | 0 | 213.7 |
| `BinaryGramCertificate12` | 0 | 222.7 |
| `BinaryGramCertificate13` | 0 | 214.7 |
| `BinaryGramCertificate14` | 0 | 207.2 |
| `BinaryGramCertificate15` | 0 | 209.3 |

## SHA-256 of checked files

| File | SHA-256 |
|---|---|
| `check.py` | `f52e96a241fa692e34e799e41b20e324bd0294666ee4c9f00a735f7e6f56fee3` |
| `lake-manifest.json` | `a4aac9be5ecfc50a0ac4dd3000078db9c83f7523c2f25f428f7e5f5e6dbb4a72` |
| `lakefile.toml` | `487db1bc682b63a7092aa12dbc601a5cf3af3ece21f8d0756c76bb41384c1ad2` |
| `lean-toolchain` | `55e97be96000b5e9e290c9e74482e5e317861499a5540353ce845471bded8cea` |
| `MathLean/BinaryGram.lean` | `995e72691c14d5a6df966072818aa92f4b3a32551b4fa6b6ebba424071465f9b` |
| `MathLean/BinaryGramAutomaton.lean` | `c35596efcada510202ca6727c5d26952d6f2be648592d8839e2a91a4d79fc5dc` |
| `MathLean/BinaryGramCertificate00.lean` | `ed21598f03a5755d517b0b4d3134bbdb52b7cc901f2d2aea9262f3ceb8fe7beb` |
| `MathLean/BinaryGramCertificate01.lean` | `924bea9f1b62cf2a7e0984980ad1d535a655b94cb6cb27447107b90e7ff74987` |
| `MathLean/BinaryGramCertificate02.lean` | `30edf2f45dffa7511cf78408f53e8b656eda410a6d54d2e844ad14f6ac44f4fa` |
| `MathLean/BinaryGramCertificate03.lean` | `453bbaf79044f9903004f701df9bdbe848b7a8bfb2c76fa9ef698fef3af4d5ce` |
| `MathLean/BinaryGramCertificate04.lean` | `d566df81e925ad48263166958b9e808769dfc44b1eb6ed0f4c9273d6064dac97` |
| `MathLean/BinaryGramCertificate05.lean` | `b39fa35b66558b15ab676d7696261cb3b23c826b44d97468fb09312dd55f21d3` |
| `MathLean/BinaryGramCertificate06.lean` | `7e3f0aa64d4dd20535974a7d86e4047ac33987fcff0505f609ae14472efc3440` |
| `MathLean/BinaryGramCertificate07.lean` | `ff1722d1c50ebcb22b171dcc6048d426bc91ffcb5a4337ff0dd5a87aa2b056b2` |
| `MathLean/BinaryGramCertificate08.lean` | `ed33a03185c08260c6daf783c443e72d404baed9fa3a004f52afc41d88d4496a` |
| `MathLean/BinaryGramCertificate09.lean` | `070ba9d213c6518567a5b7abfe639f21a667da0c28703de246ce4fdfd01dc8d1` |
| `MathLean/BinaryGramCertificate10.lean` | `13f808992135814e712d4f4afe566cbb0a04bc60f4f8c4298f0f32501a48a851` |
| `MathLean/BinaryGramCertificate11.lean` | `60f4b7fdb1bef7a53c3caa9cd09860f93b1a53c9fb6544bb6c060d472d4fe4df` |
| `MathLean/BinaryGramCertificate12.lean` | `708dfbc94aee9d2be096d61d2f2914b02a17417d248c3cd749da8d28d4cf7010` |
| `MathLean/BinaryGramCertificate13.lean` | `b1587c3e09abb28b3a796355a11028f62931eb95e09c494701e698e3ce0b0332` |
| `MathLean/BinaryGramCertificate14.lean` | `735576e4012fe73bcdb70bfa48dc2311e2f91d9142e036afc6074944d241db78` |
| `MathLean/BinaryGramCertificate15.lean` | `1bad3e5390b472810b936ccb41128e5b20eae8f643db4464fe56cb1195891f40` |
| `MathLean/BinaryGramCertificateBase.lean` | `bc382a4a79bd442de61014ef67f68bbd24d1f6aea24154041f10862de5df1e2b` |
| `MathLean/BinaryGramCertificateTable.lean` | `41d6ea557b78bf4a1d9b37543ba93e92079a95b738c84fdee4d3158d5b9b8da6` |
| `MathLean/BinaryGramConclusion.lean` | `f0e04eefbf402ce8d5de7cdd119679f8b9781c6791d09e55123eff518f884373` |
| `MathLean/BinaryGramCount.lean` | `c03dae55bff77de3facb291c3bc0a371e425ed01f9cf50a2e70c362fa6cb2f92` |
| `MathLean/BinaryGramData.lean` | `92a5296ee0cfb136f3cecbb1272da0ccc11c4b0f75d168e599939dc9a031d310` |
| `MathLean/BinaryGramEncoding.lean` | `324b7c5097c8342ea88b91504db42a0d8f64ac3a3f16c7aea210fa6fc41387e6` |
| `MathLean/BinaryGramFast.lean` | `ac7e213d207b3bf81f5335f9f73246406167dc6010ca1be0f3528fc0b87c7d18` |
| `MathLean/BinaryGramFormula.lean` | `8dacc858492f57b0f2818666ab82fa1ec4dccd8bebe6ea29a12e2f40fee691c8` |
| `MathLean/BinaryGramInitialCertificate.lean` | `bee03598cc24bac01f866290b7bf839c39179aa4042e6053b39d97f84dee7eba` |
| `MathLean/BinaryGramMatrix.lean` | `655da581d4bdc9cca29e525becd0ba295a5106f0b1f16b1a728519c1febd4775` |
| `MathLean/BinaryGramRelationCertificate.lean` | `f6a7dc814893504694d139cbb3f684ba5987cff1ee8b99538a296951439840aa` |
| `MathLean/BinaryGramWords.lean` | `085e92db59f2c67fc7c2b14f47c8f8e7368665e3e29f5df4dbc9904dc5b1e6d9` |
| `MathLean/Transfer.lean` | `5e896db512df7bedd6dc9a81b113086e6d532b5f8d219c48d0bc21ac8663ef5a` |
| `MathLean.lean` | `c822f2f987421f01f5555d4d4f66d3083455c16a3ec15e764a78d482a771d510` |
