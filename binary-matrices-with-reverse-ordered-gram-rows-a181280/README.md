# A Finite-State Proof of the A181280 Formula

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Six-term formula proved

## Problem

Prove the six-term formula conjectured by Kauers and Koutschan (Conjecture 20) for OEIS A181280: binary 4 × n matrices with strictly increasing rows whose Gram matrix over F₂ has strictly decreasing rows.

## Result

The formula holds for every n ≥ 4, and a(1) = a(2) = a(3) = 0. The generating function is rational with minimal eventual recurrence of order 11.

## Method

A column automaton, Fourier analysis on the parity group (1,024 blocks of size eight) and quadratic character sums give a universal annihilator of degree 16, so sixteen exact initial values prove the formula for all n.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -B src/reproduce.py
```

Runs all four verification routes and checks that the independent counters agree.

## Status

The six-term counting formula and the exceptional initial values have been formalized in Lean 4.19.0 for the original binary matrices; see the [standalone Lean project](lean/) and its [verification record](lean/VERIFICATION.md). The formalization proves the matrix/automaton correspondence and checks a full-state degree-16 certificate. It does not formalize the paper's Fourier derivation, generating-function claims, or minimality of the eventual recurrence. The paper and programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. The work has not been externally peer reviewed.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
