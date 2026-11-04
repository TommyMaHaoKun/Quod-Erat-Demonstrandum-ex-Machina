# Source and novelty audit

Checked 2026-11-04.

Stefan Steinerberger, *A sharp estimate for probability distributions*,
Statistics & Probability Letters 155 (2019), article 108584,
[DOI](https://doi.org/10.1016/j.spl.2019.108584),
[arXiv:1801.00663](https://arxiv.org/abs/1801.00663).

Section 1.3 asks separately about mean and median normalizations. This is
the mean version. The source's denominator includes `X+Y >= 2z`; that
condition is automatic when `min(X,Y) >= z`. The source notes equality
for exponential distributions.

Its main theorem estimates a different quantity using a density bound and
median. Feldheim and Feldheim's cited result concerns an unweighted ratio.
The present proof supplies the explicit Weibull counterexample and a global
strict bound for every positive threshold. The distribution itself is standard.

Targeted searches for the paper title with “counterexample”, and for
“Steinerberger”, “Weibull”, “mean”, and “tail-ratio”, found no earlier
resolution of this exact assertion. This records the search's scope.
The supplied author-maintained open-problems PDF URL returned HTTP 404;
the original article's Section 1.3 remains directly available.

The analytic argument and exact rational checks received an independent
review, recorded in reproducibility/INDEPENDENT_REVIEW.md.
