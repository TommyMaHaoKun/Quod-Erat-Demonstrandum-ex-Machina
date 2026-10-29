# Strict Monotonicity of a Transformed Gamma Median

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** A′(k) < 0 for all k > 0

## Problem

Let m(k) be the median of the gamma distribution with shape k and scale one. Lyon (2023) left open whether A(k) = 2^{1/k} m(k) − k is decreasing.

## Result

A′(k) < 0 for every real k > 0.

## Method

Analytic estimates on (0, 1/10] and [7, ∞), and 1,052 certified secant inequalities on [1/10, 7] built on the strict convexity of the gamma median.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python src/rational_verify.py
```

Verifies all 1,483 rational median brackets and 1,052 intervals with integer arithmetic. `src/generate_certificate.py` regenerates the candidate data.

## Status

Computer-assisted proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
