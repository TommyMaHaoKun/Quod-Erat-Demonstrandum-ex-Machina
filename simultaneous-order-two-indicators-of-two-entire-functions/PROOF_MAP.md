# Proof map

Target: simultaneous realization of every prescribed indicator for a finite set of pairwise independent forms on C^2, at order two and positive finite type.

| Claim | Paper location | Dependencies and checks |
| --- | --- | --- |
| Pairwise maximum condition is necessary | Theorem 1.1, necessity paragraph | Any two forms are a basis; the indicator of a sum is at most the maximum of the two indicators. |
| Finite retained-component approximation preserves all hypotheses | Lemma 2.1 | Local convexity gives uniform Lipschitz bounds; contact derivative signs preserve trigonometrical convexity; discarded heights tend uniformly to zero. |
| Convolution has uniform O(r) error and preserves exact local equality | Equations (3)-(4) | Homogeneous potentials have gradients bounded by C(1+r); unit-radius convolution preserves subharmonicity. |
| Exact normalized shear curvature formula | Lemma 3.1 and equation (7) | Direct matrix differentiation; independently verified by `reproducibility/src/verify_shear_curvature.py` over rational Laurent polynomials. |
| Finite angular metric templates have curvature bounded below by -C/r^2 | Section 4.1 | Fixed endpoint frames cover the entire convolution strip; moving complements occur inside strict deficits; equal-weight gaps use bounded positive matrices. |
| Frame preparation matches both endpoint metrics exactly | Section 4.2, equation (15) | Fixed dominant row, positive scalar factor, linear shear interpolation; common collars cross convolution strips; arbitrary matrix interpolation only where weights are exactly equal. |
| New deficits can be activated uniformly down to t=0 | Section 4.2, equations (16)-(18) | Scalar convex interpolation; radial cross terms controlled by log-radius speed; t exp(-c t r^2) is bounded by 1/(e c r^2). |
| A global positive-curvature metric has the desired exp(o(r^2)) weights | Proposition 4.1, Section 4.3 | Finite stage constants, increasing radii, slow transitions, uniform bounds on unweighted frames, radial subquadratic curvature correction. Covers infinitely many components. |
| Evaluation norms have exact exponential rate | Lemma 5.1 | Upper bound by submean; lower bound by vector-valued L2 d-bar estimate with regularized logarithmic singularity. The correction vanishes at the chosen point. |
| One pair realizes all indicators simultaneously | Section 6 | Countable open dense sets in a Hilbert space, Baire theorem, positive prescribed maxima, and continuity of order-two indicators. |

The analytic construction has been reviewed separately, including same-label contacts, zero-width gaps, whole-circle deficits, fixed-radius convolution strips, infinitely many components, and the small activation-parameter limit. The symbolic program checks the algebraic curvature identity only. No finite computation substitutes for the metric or Baire arguments.
