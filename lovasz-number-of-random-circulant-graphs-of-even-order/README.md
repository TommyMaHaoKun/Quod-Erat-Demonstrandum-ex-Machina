# The Lovasz number of random circulant graphs of even order

Author: GPT-6 Astra.

For the random circulant graph on `Z/nZ` in which each nonzero inverse orbit is selected independently with probability one half, the paper proves

`E theta(G_n) / sqrt(n) -> 1`

along all even orders. The singleton orbit `{n/2}` receives its own independent fair bit. Together with Chen, Hu, Hu, Wang and Yang's odd-order theorem, this establishes the limit through all positive integers.

The paper extends the Fourier sampling, canonical tree fields, Walsh projection and expectation argument to even orders. It explicitly imports the Gaussian fixed point and quantitative approximation theorems from [Chen et al., arXiv:2610.22971v1](https://arxiv.org/abs/2610.22971v1).

## Reproduction

Requires Python 3.9 or newer with no third-party packages. From this folder run:

```text
python reproducibility/verify_even_projection.py --output reproducibility/certificates/regenerated_check.json
```

Expected result: `PASS`, 36 exact projection cases, including 20 nonzero canonical fields, and nine singleton leaf-correction checks. The regenerated JSON agrees with `reproducibility/certificates/exact_projection_check.json`. Run without `-O` or `PYTHONOPTIMIZE`; the program rejects optimized execution.

The checks use integer Fourier-Walsh coefficients to compare direct admissible-flow enumeration with polynomial convolution. They verify the projection, orthogonal energy, operator-square and singleton leaf identities. The expectation asymptotic is proved analytically in [paper.pdf](paper.pdf).

The paper passed internal mathematical review and all-page visual inspection. A fresh extraction of its reproduction package regenerated the same exact report. The proof dependencies are recorded in `reproducibility/PROOF_MAP.md`, and the literature scope is documented in `LITERATURE_REVIEW.md`.
