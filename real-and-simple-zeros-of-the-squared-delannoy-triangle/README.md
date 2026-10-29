# Real and Simple Zeros of the Squared Delannoy Triangle

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** All zeros real, simple and enclosed

## Problem

Prove the Delannoy component of the Mao–Wang conjecture: the row polynomials Gₙ of the squared Delannoy matrix D² have only real zeros.

## Result

For every n ≥ 1, Gₙ has exactly n distinct real zeros, all in (−4 − 3√2, −3 + 2√2).

## Method

A divided-difference formula reduces Gₙ to ordinary Delannoy polynomials; a continuity argument and the explicit sine formula supply n sign changes.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -m pip install -r requirements.txt
python -B src/verify.py --independent
```

The proof is analytic; the script checks the identities and the zero count exactly through degree 50.

## Status

Analytic proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.
