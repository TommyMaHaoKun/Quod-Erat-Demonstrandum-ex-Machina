# The Original Limited Augmented Zarankiewicz Number in the m × 3 Case, and z_L(14, 3) = 23

**Author:** Claude Opus 5.5 · **Paper:** [paper.pdf](paper.pdf) · **Result:** z_L(m,3) = ⌊(3m+4)/2⌋; z_L(14,3) = 23

## Problem

Determine the limited augmented Zarankiewicz number z_L(m, 3) of Qi, Cui and Xu, known only for m ≤ 13; in particular z_L(14, 3).

## Result

z_L(m, 3) = ⌊(3m + 4)/2⌋ for every m ≥ 3; in particular z_L(14, 3) = 23.

## Method

A lemma showing that at most one row is fully occupied gives the upper bound; an explicit family of configurations attains it. Exhaustive branch-and-bound and an independent SAT encoding confirm m = 14.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -m pip install -r requirements.txt
python src/check_package.py
```

A few minutes. The SAT step is skipped if `z3-solver` is not installed.

## Status

Analytic proof. The proof and the programs were produced by Claude Opus 5.5, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.
