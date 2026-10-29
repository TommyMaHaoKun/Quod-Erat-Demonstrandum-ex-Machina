# A Hermite-Moment Proof of the Recurrence for Binary Matrices with Prescribed Margins

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Third-order recurrence proved

## Problem

Prove the third-order recurrence conjectured by Kauers and Koutschan (Conjecture 6) for OEIS A172572, the number of 3n × 6 binary matrices with row sums 2 and column sums n.

## Result

The recurrence holds for every n ≥ 0.

## Method

The count is a normalized sixth Gaussian moment of a Hermite polynomial; Gaussian integration by parts gives a three-moment transition, and elimination yields the stated coefficients.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python src/verify_proof.py
python src/independent_count.py --max-n 100 --dp-max-n 15
python src/audit_moments.py
```

All three use only the standard library.

## Status

Analytic proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.
