# Literature and attribution audit

Audit date: 2026-11-04. Target: the maximum of the uniform sign-cube average of the infinity norm for arbitrary real 6 by 6 matrices with unit Euclidean row norms.

## Primary sources read

1. Stefan Steinerberger, *Bad Science Matrices*, arXiv:2402.03205v2, 7 February 2024. [Paper](https://arxiv.org/html/2402.03205). Section 2.6 supplies exactly the attaining matrix used here and the lower bound `(2 + sqrt(3))/2`. The paper presents it as a candidate, with no six-dimensional matching upper bound. **The construction and its value are attributed to Steinerberger.**
2. Alex Albors, Hisham Bhatti, Lukshya Ganjoo, Raymond Guo, Dmitriy Kunisky, Rohan Mukherjee, Alicia Stepin and Tony Zeng, *On the Structure of Bad Science Matrices*, arXiv:2408.00933v2, 20 January 2025; Involve 19 (2026), 443-460, [DOI](https://doi.org/10.2140/involve.2026.19.443). [ArXiv text](https://arxiv.org/html/2408.00933v2). The abstract and Sections 1.4-1.5 give exact optimality through dimension four; the structural results do not supply a six-dimensional optimum.
3. Shridhar Sinha, *The Structure of Extremal Bad Science Matrices*, arXiv:2509.10580v1, 11 September 2025. [Paper](https://arxiv.org/html/2509.10580). This contains structural and asymptotic results, with no exact six-dimensional optimality theorem. The arXiv submission history currently contains v1.
4. trureturing, *The exact five-dimensional bad science optimum*, [public dossier](https://www.trureturing.org/research/albors-et-al-2024-bad-science-matrix-five/), accessed 4 November 2026. The dossier links `D5/S3/Combinatorics/Hamming/BadScienceFiveOptimality.lean` and states the exact five-dimensional optimum `(2+3 sqrt(3))/4`. Its Route section uses an affine majorant for antipodal-free cube sums and sums that bound over oriented cells. Its Scope assessment explicitly lists dimensions at least six as open. **The affine-majorant strategy in the present paper was inspired by this source and is cited.** The six-dimensional finite enumeration and affine bound are developed in this project.

## Additional status searches

Targeted web searches for six-dimensional bad-science matrices, the exact expression `1 + sqrt(3)/2`, later work citing the source papers, and six-dimensional optimality did not locate an earlier matching upper bound in the searched material.

## Exact contribution and boundary

The result proved here is `beta_6 = 1 + sqrt(3)/2` on the full original domain. The contribution is the universal matching upper bound. It combines coordinate compression, a complete exact enumeration of the 7,867 Boolean-lattice ideals of cardinality at most eleven, an orthogonality bound for larger antipodal-free sets, and the affine function `(2 sqrt(3)-2)m + 16-8 sqrt(3)`.

The finite computation has two independently structured implementations: nested-slice enumeration of all 7,828,354 ideals, and increasing-vertex enumeration of only the 7,867 ideals used in the proof. No floating-point computation is needed in the essential verifier. The manuscript does not claim a classification of all maximizing matrices or a formal proof-assistant verification. Its cell-cardinality restriction is an additional consequence of the strict affine gaps.

The searches above did not locate an earlier six-dimensional upper bound.
