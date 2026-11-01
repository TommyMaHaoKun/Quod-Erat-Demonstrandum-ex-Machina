# Status

**COMPLETE_KNOWN_RESULT**

Completed: 2026-11-01. Author: **GPT-6 Astra**.

The exact Question 8 assertion is **false**. The known semigroup `S=<6,7,8,9>` is nearly Gorenstein, is not almost symmetric, and has exactly four minimal relations. Its full pseudo-Frobenius set is `{10,11}`, and an NG vector is `(11,10,10,10)`.

The paper proves every hypothesis and proves both generation and minimality of the defining ideal. The result is attributed as a known example: its exact four-relation presentation appears in Gomes, O'Neill and Torres Davila (2023), Example 18. The supplied `{5,6}` formulation differs from Moscariello and Strazzanti (2021), Question 4.3, which expressly allows four relations in type two.

## Completed checks

- Independent elementary proof and separate factorization-graph verification agree on `rho=4`.
- Every factorization degree through the proved cutoff 28 was checked exactly.
- Primary-source, mathematical, and editorial reviews passed.
- `paper/main.tex` compiles twice with no unresolved references or overfull/underfull boxes.
- All four pages of `output/research_paper.pdf` were visually inspected; tables, formulas, references, and author metadata are correct.
- Both verifiers and the PDF build passed from a clean temporary copy, invoked from another working directory. The rebuilt PDF has identical extracted text.
- The release certificate records hashes of the final LaTeX and PDF, plus the clean-copy checks.

The exact requested formulation has been resolved. No checkpoint or unfinished proof obligation remains for that formulation. The distinct original type-dependent classification is outside this result's scope.
