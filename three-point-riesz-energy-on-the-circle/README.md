# Endpoint Maximality of a Three-Point Riesz Energy on the Circle: A Proof of Fan's Conjecture 5.9

**Author:** Claude Opus 5.5 · **Paper:** [paper.pdf](paper.pdf) · **Result:** Fan's Conjecture 5.9 proved

## Problem

Q. Fan conjectured that a three-point Riesz energy (equivalently, the Riesz (−r)-capacity) on the unit circle is maximized at the endpoint where the triangle is isosceles (Conjecture 5.9, arXiv:2609.11186).

## Result

For r = 2 the energy is constant; for r > 2 the endpoint is the unique maximizer, with maximum 2^{r−1} sin^r φ / (1 − 2^{r−2}|cos φ|^r). For 0 < r < 2 the endpoint is the unique minimizer. With Björck's support theorem this also gives Fan's Conjecture 5.6.

## Method

An exact solution of the three-weight problem and a single algebraic identity reduce the comparison to a two-term majorization inequality.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -m pip install -r requirements.txt
python src/verify_symbolic.py
python src/verify_numeric.py
```

The proof is analytic; the symbolic script checks its identities and the numeric script is a regression check.

## Status

Analytic proof. The proof and the programs were produced by Claude Opus 5.5, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.
