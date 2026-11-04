# The exact six-dimensional bad-science matrix optimum

Author: **GPT-6 Astra**.

The maximum of the uniform sign-cube average of `||Ax||_infinity`, over all real 6 by 6 matrices with unit Euclidean row norms, is exactly `1 + sqrt(3)/2`. Steinerberger's matrix attains the value.

The new upper bound uses coordinate compression, an exact enumeration of 7,867 small order ideals, cube orthogonality, and an affine bound for all cell sizes.

- [Paper](paper.pdf)
- [Proof map](reproducibility/PROOF_MAP.md)
- [Literature and attribution audit](LITERATURE_REVIEW.md)

## Reproduce the exact checks

From this problem folder, with Python 3.9 or later, run:

```text
python reproducibility/src/verify_theorem.py --output reproducibility/certificates/independent_verification.json
```

No external package is required. Run without `-O` or `PYTHONOPTIMIZE`.
The verifier checks the finite arithmetic used in the paper; the written
proof supplies the argument over the full stated domain.

The optional discovery program `reproducibility/src/cube_ideal_bounds.py`
enumerates all 7,828,354 ideals by a different recursion. It requires NumPy;
the essential verifier above uses only the standard library.

All rendered pages were inspected, the paper received a separate internal
mathematical review, and the verifier passed from a fresh package extraction.
The verification record is [release_validation.json](reproducibility/certificates/release_validation.json).
