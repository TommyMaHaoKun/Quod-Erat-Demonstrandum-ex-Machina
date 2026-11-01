# Real and simple zeros of the squared Eulerian triangle

**Claude Opus 5.5 and GPT-6 Astra**

**COMPLETE_PROVED**

Let A(0,0)=1, let A(n,k)=0 outside 0 <= k <= n, and define

    A(n,k) = (n-k+1) A(n-1,k-1) + k A(n-1,k),
    B(n,k) = sum_{j=k}^n A(n,j) A(j,k),
    P_n(x) = sum_{k=0}^n B(n,k) x^k.

Here B=A*A is the ordinary matrix square.

**Theorem.** For every integer n >= 1, P_n has a simple zero at 0 and n-1 distinct negative zeros. P_0=1 has no zeros.

This proves the Eulerian part of Mao and Wang's Conjecture 4.1 in the [v1 PDF of The Narayana transformation](https://arxiv.org/pdf/2607.01572v1). The [HTML v1](https://arxiv.org/html/2607.01572v1) renders its number as 4.15.

## Paper and method

The [26-page paper](paper.pdf) contains the complete proof. A strictly increasing phase in an exact pole expansion supplies signs in the central range. Explicit coefficient comparisons handle both extremes. A lattice path of maximizing terms connects the large-root range to the central range; a strict mixed-coefficient inequality separates pairs of close zeros. Exact certificates cover n <= 250. Counting n distinct zeros proves simplicity for all n.

- [Complete TeX source](paper-source/)
- [Proof map](reproducibility/PROOF_MAP.md)
- [Literature and novelty audit](reproducibility/LITERATURE_REVIEW.md)
- [Status](reproducibility/STATUS.md)
- [Build and visual review record](reproducibility/RELEASE_CHECK.md)

## Reproduce

From this folder, with Python 3.9 or later:

```text
python reproducibility/src/verify_all.py
```

Only the standard library is required. Run without `-O`, which disables assertions. All nine mandatory checks must pass. The script resolves its own files and also runs from another working directory. It reconstructs the Eulerian triangle using two exact formulas, verifies every rational sign certificate through n=250, and checks the scalar constants used in the uniform proof. The [recorded clean run](reproducibility/verification.log) passed in 47.7 seconds.

To rebuild the paper, enter `paper-source/` and run:

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The supplied `paper.pdf` was built from these sources and all 26 pages were visually checked. File hashes are listed in [SHA256SUMS](SHA256SUMS).

## License

Verification code is covered by the repository's MIT License. The paper, TeX source, documentation and certificates are covered by CC BY 4.0. Credit Claude Opus 5.5 and GPT-6 Astra.
