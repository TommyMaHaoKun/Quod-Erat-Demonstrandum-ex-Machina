# The interval minimizes negative-exponent Riesz capacity ratios

Author: **GPT-6 Astra**.

For every compact set K in R containing at least two points and every
0 < r < s < 1, the paper proves

`C_s(K)/C_r(K) >= C_s([-1,1])/C_r([-1,1])`,

where `C_t(K) = (max_mu integral integral |x-y|^t dmu(x)dmu(y))^(1/t)`.
Equality holds exactly for nondegenerate closed intervals.

This resolves Fan's Conjecture 4.1, the one-dimensional negative-exponent
case of Clark and Laugesen's interval conjecture. The interval formula is
`C_t([-1,1]) = [Gamma((1+t)/2) Gamma(1-t/2)/sqrt(pi)]^(1/t)`.

Read [the paper](paper.pdf), [proof map](PROOF_MAP.md),
[literature review](LITERATURE_REVIEW.md), and [release status](STATUS.md).

The proof compares energies of monotone images of beta measures. A logistic
change of variables represents the weighted pair law as a mixture of Poisson
partition cells. Ordering the mixing rates and applying concavity under
coarsening gives the sharp inequality. Quantile transport covers all compact
sets directly. The proof is analytic and needs no numerical certificate.

## Reproduce

Run the following commands from this problem folder.

Python 3.9 or later and either pdflatex or Tectonic on PATH:

```sh
python reproducibility/build_paper.py --output paper.pdf
```

Optional numerical checks (mpmath 1.3.0):

```sh
python -m pip install -r reproducibility/requirements.txt
python reproducibility/audit_poisson.py
```

The checks use 60-digit arithmetic on twelve finite-set transports and three
mixture normalization identities. They are supporting computations, not steps
of the proof. Results are saved in `reproducibility/numerical_checks.json`.

The saved LaTeX was independently reviewed and the PDF was checked visually
on every page. Mathematical review is internal AI review; no proof-assistant
formalization or external peer review is claimed.
