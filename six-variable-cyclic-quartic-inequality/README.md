# A Six-Variable Cyclic Quartic Inequality with a Variance Remainder

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Proved with equality only at x₁ = … = x₆

## Problem

Prove (Σxᵢ²)² ≥ (Σxᵢ)(Σxᵢxᵢ₊₁²) for six variables in cyclic order, the (a, b) = (1, 2) case that Javaheri supported only numerically.

## Result

For every real six-tuple the left side exceeds the right by at least ¼(Σ(xᵢ − x̄)²)². Hence the inequality holds on all of ℝ⁶, with equality exactly when all entries are equal.

## Method

Centering, an opposite-pair decomposition, Cauchy–Schwarz and an eigenvalue bound for a trace-zero symmetric 3 × 3 matrix. A rational sum-of-squares certificate is included as an independent check.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python src/verify_identities.py
python src/verify_opposite_pair.py
python src/verify_certificate.py
```

The proof itself needs no computer; these scripts check its identities and the supplementary certificate exactly.

## Status

Analytic proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.
