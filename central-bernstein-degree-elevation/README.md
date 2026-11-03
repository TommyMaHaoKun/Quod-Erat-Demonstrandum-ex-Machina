# A finite degree-elevation bound for central Bernstein polynomials

Author: **GPT-6 Astra**.

For positive even n, k>1, and h=k binom(n,n/2)/2^n in (0,1), let r_min be
the first elevation at which all Bernstein coefficients of
k binom(n,n/2) x^(n/2)(1-x)^(n/2) lie in [0,1]. With T=nh^2/(1-h^2), we prove

    r_min <= 2 ceil(T/2)-1 <= ceil(T) <= floor(T)+1.

Also, r_min is odd. This proves the requested finite bound and strengthens it.
The argument combines Sawin's explicit coefficients with a strict telescoping
product inequality; it is valid for all stated parameters.

- [Paper](paper.pdf)
- [LaTeX source](paper/main.tex)
- [Literature review](LITERATURE_REVIEW.md)
- [Proof map](PROOF_MAP.md)
- [Status and verification](STATUS.md)

## Reproduction

Python 3.9 or later, standard library only:

```sh
python reproducibility/verify.py
```

Build the paper with a standard LaTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper/main.tex
pdflatex -interaction=nonstopmode -halt-on-error paper/main.tex
```

This produces `main.pdf`; the released copy is named `paper.pdf`. Verification uses exact integers and rational
numbers. The universal proof is in the paper; finite checks test the formulas.

The coefficient formula and central maximum are attributed to Will Sawin.
The original question is due to Peter Occil. The literature search found no
previous complete proof of the exact finite bound in the inspected sources.

Code is MIT licensed; the paper and documentation use CC BY 4.0, as described in the repository root.
