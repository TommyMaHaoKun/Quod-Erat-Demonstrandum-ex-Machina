# Simultaneous indicators of two entire functions of order two

**Author: GPT-6 Astra**

The paper proves that the pairwise-maximum condition is necessary and sufficient for a finite family of pairwise independent linear forms on C^2 to have prescribed, individually admissible indicators of order two and positive finite type. The proof allows arbitrary continuous indicators and infinitely many deficit intervals. It does not assume completely regular growth.

Read [the paper](paper.pdf). The [proof map](PROOF_MAP.md) identifies the dependencies of the full argument.

## Auxiliary verification

Run with Python 3.9 or newer; no additional packages are required:

```text
python reproducibility/src/verify_shear_curvature.py
```

The expected result is `PASS_EXACT_SYMBOLIC_IDENTITIES`. This verifies the four entries and trace of the local shear-curvature identity over rational Laurent polynomials. The full realization theorem is proved analytically in the paper and has received separate internal mathematical review.

The [release record](reproducibility/certificates/release_checks.json) identifies the checked PDF and verifier, the clean-package replay, the independent internal review, and the rendered-page and editorial checks. No proof-assistant formalization or external peer review is claimed.
