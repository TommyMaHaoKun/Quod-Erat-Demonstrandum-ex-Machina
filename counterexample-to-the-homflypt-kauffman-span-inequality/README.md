# A counterexample to the HOMFLYPT–Kauffman span inequality

Author: GPT-6 Astra.

The closure of the five-strand braid `[-1,2,3,-4,-1,3,-4,2,2,2,3,2]`, tabulated as `12n_296`, has HOMFLYPT a-span **8** and Kauffman a-span **7**. This disproves the universal full-span inequality. Connected sums give every positive integer as a span difference.

The full polynomial values are attributed to KnotInfo. A separate exact implementation reconstructs them from the braid using port-pairing skein recursion. Its implementation is independent of the upstream signed-Gauss-code engine used for a secondary check.

## Reproduction

Requires Python 3.9 or newer and no third-party packages. From this folder run:

```text
python reproducibility/src/verify_all.py
```

The verifier checks the full polynomial coefficients, the single-component closure, the spans, known small-knot formulas and braid/Markov identities. It writes `reproducibility/output/verification_report.json`. No network access is required.

[paper.pdf](paper.pdf) contains the argument and the complete coefficient tables. The clean supplement contains the two standard-library Python scripts and the source coefficient data; exploratory tools and third-party software are excluded.

The source data came from KnotInfo's official polynomial workbook, accessed November 4, 2026. Its URL and archive hash are recorded in `reproducibility/certificates/published_polynomials.json`.
