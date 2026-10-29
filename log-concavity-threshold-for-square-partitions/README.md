# The Exact Log-Concavity Threshold for Partitions into Squares

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** T₂ = 1042

## Problem

Let s(n) count the partitions of n into positive squares. Determine the exact point from which s(n) is permanently log-concave (the square case of Roy's conjecture).

## Result

s(n)² > s(n−1)s(n+1) for every n ≥ 1042, and the inequality fails at n = 1041. There are exactly 421 negative indices and the equality set is {1, 2, 5, 6, 10, 14}.

## Method

Exact arithmetic for every n ≤ 1,200,000 and an explicit analytic estimate (Zagier's generalized eta transformation, a tenth-order steepest-contour approximation and certified minor-arc bounds) for every larger n.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python code/verify_all.py
```

The individual certificate checkers in `code/` can also be run separately.

## Status

Computer-assisted proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
