# Verification record

Fresh publication-copy build completed on 2026-10-30 with Lean 4.19.0
(compiler commit `6caaee842e94`) and Mathlib v4.19.0
(`c44e0c8ee63ca166450922a373c7409c5d26b00b`).

All ten proof modules and the publication root passed in a separate output
directory. Only dependency outputs were reused; every project proof output
was freshly built. Source hashes were checked before and after compilation.
The source audit found no placeholders, custom axioms, or native-decision
shortcuts. The reports for `original_six_formulas`, `original_all_bounds`,
and `residue_five` contain only `[propext, Classical.choice, Quot.sound]`.

The original-object definition, exact theorem scope, and rebuild instructions
are in [README.md](README.md). This record does not claim formal verification
of the paper's additional generating-function or minimal-period arguments.

| Source | Result | SHA-256 |
|---|---|---|
| `MathLean/TriangleParameters.lean` | Passed | `eb6c0aa246dcf66a26daea348fbefb308e42c680fc6164d6831c3662f0ec7493` |
| `MathLean/TriangleBases.lean` | Passed | `de685602490a39782d87f50e6d893747bcd3d722e2d61f7d678e54a7dd300abf` |
| `MathLean/TriangleLatticeCount.lean` | Passed | `268c80a264016aef4bb296ad42909f9608c0164f6a6f22aecb95a987a2e5a14c` |
| `MathLean/TriangleChambers.lean` | Passed | `6a43f24b2e450b8d38fa9e7d571824796e1416e4f3f62750dc98d2c4b17a42d7` |
| `MathLean/TriangleChamberCount.lean` | Passed | `304dcd1472264fbec883216ee8eef6afa5b9f5bea044ebb660f043adabf9520e` |
| `MathLean/TriangleFiniteSums.lean` | Passed | `98a911cb33bab03ef0d1d2bb3d27b29d7aa02389551d997e6570f2470daad9fc` |
| `MathLean/TrianglePolynomialSums.lean` | Passed | `f79e1a1ce2672ecbea2bfeff82f70f5527f0899eeae40e46756b037836e30b17` |
| `MathLean/TriangleRowPolynomials.lean` | Passed | `4327cc049b9f43949ec5ca85eaea1ee4fb665548dea27017ac90c61ec539d4ba` |
| `MathLean/TriangleEvaluation.lean` | Passed | `13ce49ab12dd9ee4250cd565aed20f716b4b1e30389c210b76363d5b4be6d48a` |
| `MathLean/Triangle.lean` | Passed | `fecbc155019548507c67bc12747a8baa404d6d11ee7138d9a235f01551ea6e6b` |
| `MathLean.lean` | Passed | `caac2b75cf136d78a417b38d762580dcb52c712124dd5c8b549884bb98c569ab` |
