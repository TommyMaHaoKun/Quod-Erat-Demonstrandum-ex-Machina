# A four-moment proof of the recurrence for A172671

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Fourth-order recurrence proved

## Problem and result

Let a(n) count labeled 3n × 6 matrices with entries in {0,1,2}, row sums 2,
and column sums n. For b(n) = (n!)³ a(n)/(3n)!, the exact fourth-order
recurrence in Kauers and Koutschan's Conjecture 7 holds for every n ≥ 0.
The initial values are 1, 15, 2249, 444975. The leading coefficient is
positive on this domain, so these values determine the sequence uniquely.

## Method

The coefficient count is a sixth formal Gaussian moment of a modified
Hermite polynomial. Integration by parts reduces it to four moments.
An explicit 4 × 4 transfer matrix and an exact polynomial identity then
establish the specified recurrence. All 78 residual coefficients vanish.

## Reproduce

Run from [`reproducibility/`](reproducibility/) with Python 3.9 or later:

```bash
python src/verify_certificate.py
python src/independent_checks.py
```

Both use only the standard library. The first derives all 16 transfer
entries, parses the target coefficients from the supplied mathematical
excerpt, checks the paper's coefficients, and verifies the identity exactly.
The second counts matrices directly through n = 8 and checks explicit
sixth moments through n = 40. Finite checks corroborate the all-index proof.

For the separate symbolic derivation, install the dependency in
`requirements.txt` and run:

```bash
python -m pip install -r requirements.txt
python src/route_alt_transfer.py
```

The [LaTeX source](reproducibility/paper/main.tex),
[proof map](reproducibility/PROOF_MAP.md),
[literature audit](reproducibility/LITERATURE_REVIEW.md), and
[verification reports](reproducibility/certificates/) are included.
The target excerpt was compared with the original JIS source before
publication. Verification is offline; the full third-party article is
not redistributed. If supplied as `literature/kout4.tex`, it is also
compared directly by the verifiers.

With pdfLaTeX installed, `python src/release_check.py` reruns all three
verifiers and rebuilds the paper twice in a clean temporary folder.
On Windows, `src/build_paper.ps1` builds the paper into
`reproducibility/output/research_paper.pdf`.

## Status and attribution

Complete computer-assisted proof for every n ≥ 0. The proof and programs
were produced by GPT-6 Astra, an AI system, and checked by internal review
and exact computations. They have not been externally peer reviewed or
formalized in a proof assistant.

The recurrence and D-finiteness result are due to Kauers and Koutschan;
Yurkevich previously used the quadratic coefficient decomposition.
The contribution here is the four-moment closure and exact elimination
certificate. The bounded literature audit does not establish worldwide priority.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt);
the code is under the [MIT License](../LICENSE). The mathematical target
formula is reproduced with attribution to Kauers and Koutschan.
