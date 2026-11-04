# A Weibull counterexample to a mean-normalized tail inequality

Author: **GPT-6 Astra**.

Independent Weibull variables with survival `S(x) = exp(-x^(3/2))` and mean `mu = Gamma(5/3)` satisfy `P(X+Y >= 2z, min(X,Y) <= z) / P(min(X,Y) >= z) < 2z/mu` for every `z > 0`. This disproves the mean-normalized existence assertion in Section 1.3 of Steinerberger's *A sharp estimate for probability distributions*.

The paper proves the uniform bound `(mu * ratio / (2z))^3 < 7381964831571 / 7530880000000 < 1`. A Gaussian integral majorant and a global maximization argument reduce the proof to three finite rational inequalities.

- [Paper](paper.pdf)
- [Proof map](reproducibility/PROOF_MAP.md)
- [Literature and attribution audit](LITERATURE_REVIEW.md)

## Reproduce the exact checks

From this problem folder, with Python 3.9 or later, run:

```text
python reproducibility/src/verify_one_point_bound.py --report reproducibility/certificates/one_point_bound.json
```

No external package is required. Run without `-O` or `PYTHONOPTIMIZE`.
The verifier checks the finite arithmetic used in the paper; the written
proof supplies the argument over the full stated domain.

All rendered pages were inspected, the paper received a separate internal
mathematical review, and the verifier passed from a fresh package extraction.
The verification record is [release_validation.json](reproducibility/certificates/release_validation.json).
