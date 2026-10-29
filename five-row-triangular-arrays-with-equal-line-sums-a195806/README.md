# Exact Enumeration of Five-Row Triangular Arrays with Equal Corresponding Line Sums

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** All six conjectured formulas proved

## Problem

Prove the six quasipolynomial constituents conjectured by Kauers and Koutschan (Conjecture 11) for OEIS A195806, which counts five-row triangular arrays with entries in {0, …, n}, zero corners and equal sums on corresponding lines.

## Result

All six formulas hold for every n ≥ 0; the counting quasipolynomial has degree six and minimal period six. The 2023 source needs an index shift and the coefficient correction 19496 → 19469.

## Method

An integral lattice bijection, exact interval counts and a dihedral chamber sum give a rational generating function; an independent Ehrhart argument proves the period bound.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python src/verify.py
```

Includes two independent enumerations through n = 41 and the source-index audit.

## Status

Analytic proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.
