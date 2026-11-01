# Final release check

Date: 2026-11-01. Author: GPT-6 Astra. Result: **PASS**.

## Mathematics and source checks

- Exact target checked against pages 17-19 of the assigned research-prompt PDF and Sun's original Conjecture 3.11 (3.15).
- Two separate AI review passes checked every displayed proof step, normal convergence, differentiation, source normalization, Euler sums, and the Gamma correction. The review records are `MATHEMATICAL_REVIEW.md` and `FINAL_REVIEW.md`.
- The reviewed manuscript then received only a balanced title line break, removal of repetitive attribution prose, and a shorter reproduction paragraph. The mathematical content is unchanged. Final source hash is recorded below.
- Final author name: GPT-6 Astra. No invented affiliation, human review, or formal-verification claim appears in the manuscript.
- Literature attribution distinguishes Sun's conjecture from Au's established transformations and auxiliary evaluation.
- No prompt residue, temporary research narrative, unresolved placeholder, or absolute local path appears in the manuscript.

## PDF checks

- `output/research_paper.pdf`: 6 pages, 358065 bytes.
- Two pdfLaTeX passes succeeded. Final log has no undefined references/citations, overfull boxes, or underfull boxes.
- All six final pages were rendered and visually inspected at readable resolution. Equations, title, references, page breaks, glyphs, and margins pass.
- A text-bounding-box check found no spans outside the safe page area.
- The references fit on the sixth page; there is no nearly empty trailing page.

## Clean-package verification

A new temporary directory received only the explicitly selected source,
dependency, and documentation files. From that directory:

```console
python src/verify.py
python src/independent_gosper_certificate.py
python src/independent_coefficients.py
python src/build_pdf.py
```

All four commands returned exit code 0. The first script passed six exact
symbolic checks and independent rational enclosures at 160 decimal places.
The WZ script passed its polynomial and boundary-numerator identities.
The coefficient script passed all four coefficient identities.
The PDF builder compiled the saved source twice.

The arithmetic certificate generated in the clean directory was byte-identical
to `certificates/verification.json`. Text extracted from the clean rebuilt
PDF matched the delivered PDF on all six pages. PDF byte hashes can differ
between builds because TeX embeds build metadata.

## Final hashes

| File | SHA-256 |
|---|---|
| `paper/main.tex` | `15f4c6689f5f2d2eb58033122ae61d7922b331d507f2977a9683d8811f871552` |
| `output/research_paper.pdf` | `8df55a790099322dde81502aebee2f4f249dca67f0066afc62a0257f1cf50640` |
| `src/verify.py` | `da2012c3de036b49d850e93ce180d522b065b0183142de1c9718d76a1798c3c0` |

## Public-package scope

The release contains the PDF, its complete LaTeX source, four standalone
Python scripts, dependency list, arithmetic certificate, proof map,
literature audit, optional coefficient-audit explanation, and status/review
records. Third-party papers, large source snapshots, discovery scratch
programs, downloaded repository inventories, and temporary builds remain
local. Existing repository projects are outside this change.
