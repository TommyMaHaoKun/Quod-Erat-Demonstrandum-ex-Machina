# Sun's binomial-harmonic identity for zeta(5) and log 2

Author: **GPT-6 Astra**. Date: 2026-11-01.

The exact identity in Sun's Conjecture 3.11, equation (3.15), is proved:

```text
P(k) = 21k^3 - 22k^2 + 8k - 1

sum(k>=1) 256^k [14 P(k)(H_(2k-1)-H_(k-1)) - 63k^2+44k-8]
                 / [k^7 binom(2k,k)^7]
= (93/2) zeta(5) + pi^4 log(2).
```

The sum is approximately `115.73597742529253867705993088823102571307`.

Read the complete six-page English paper: [research_paper.pdf](paper.pdf).
Its editable source is [main.tex](reproducibility/paper/main.tex).
See [STATUS.md](reproducibility/STATUS.md) for the release status.

## Method and attribution

The proof differentiates Kam Cheong Au's established parameter identity
(arXiv:2312.14051v4, Example XI, equation (4.4)) and uses his auxiliary
evaluation in Example XV. It supplies the parameter normalization,
local uniform convergence and termwise differentiation, and explicit
evaluations of the resulting harmonic Euler sums. Sun's accompanying
Gamma interpolation has a missing exponent; the corrected denominator
is `Gamma(2x)^7`, as derived in the paper.

The exact conjecture is Sun's, and the underlying transformations and
auxiliary evaluation are Au's. [LITERATURE_REVIEW.md](reproducibility/LITERATURE_REVIEW.md)
records the primary sources and later-source/public-repository searches.
[PROOF_MAP.md](reproducibility/PROOF_MAP.md) records every proof dependency.

## Reproduce

Python 3.9 or later and SymPy are sufficient for all arithmetic checks:

```console
cd reproducibility
python -m pip install -r requirements.txt
python src/verify.py
```

The verifier performs six exact symbolic checks and independently encloses
the original series and its stated constant using rational arithmetic.
Both outward-rounded intervals agree to 160 decimal places. The 100-term
series remainder is below `8.175e-171`. The report is written to
`certificates/verification.json`.

Optional additional checks reconstruct a WZ certificate and the
degree-two coefficient calculation in Au's Example XV:

```console
python src/independent_gosper_certificate.py
python src/independent_coefficients.py
```

Their exact scope and formulas appear in [INDEPENDENT_PROOF.md](reproducibility/INDEPENDENT_PROOF.md).
The main paper states and cites Au's two established identities explicitly.
The rational enclosures and symbolic scripts accompany the analytic proof.

With a TeX distribution providing pdfLaTeX on PATH, rebuild the PDF with:

```console
python src/build_pdf.py
```

This runs two compilation passes and writes `output/research_paper.pdf`.
The source is self-contained and has no external bibliography or asset files.

## Checks

The proof and manuscript were reviewed in separate AI review passes, and
the final PDF was rendered and visually inspected page by page.
[RELEASE_CHECK.md](reproducibility/RELEASE_CHECK.md) records the final package checks.

The source is Sun, arXiv:2603.29973v3, Conjecture 3.11 (3.15).
