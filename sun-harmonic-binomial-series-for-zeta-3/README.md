# A Telescoping Proof of Sun's Harmonic-Binomial Series for ζ(3)

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Series equals 3ζ(3)

## Problem

Prove Zhi-Wei Sun's Conjecture 3.8, equation (3.12): an inverse-binomial series with harmonic numbers whose sum is 3ζ(3).

## Result

The series converges absolutely and equals 3ζ(3) exactly as stated.

## Method

An explicit harmonic Wilf–Zeilberger pair reduces the series to two classical Euler sums; a beta-integral estimate controls the boundary terms.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -m pip install -r requirements.txt
python src/verify_all.py
```

Checks both certificate identities exactly and encloses both sides to 120 decimal places (the numerical agreement is supplementary).

## Status

Analytic proof (WZ certificate). The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.
