# Literature review

Accessed 2026-11-04.

## Exact statement and revisions

Michał Jabłonowski, [arXiv:2605.22652v3](https://arxiv.org/html/2605.22652v3), candidate (c7), states the comparison of HOMFLYPT a-span and Kauffman a-span. Appendix entries 32 and 33 explicitly define each as maximum exponent minus minimum exponent, with no division by two.

[Version 4](https://arxiv.org/html/2605.22652v4), August 12, 2026, Proposition 3.14 proves the alternating case. Remark 3.15 retains the nonalternating case as conjectural. [Version 5](https://arxiv.org/html/2605.22652v5), September 15, 2026, omits this inequality from the nine candidates in Section 5 and reuses the label (c7). The inspected text gives no explanation of that omission.

## Existing polynomial data and the counterexample

The [official KnotInfo polynomial workbook](https://knotinfo.org/homelinks/database_download.php) contains full polynomial coefficients for `12n_296` and `12n_550`. Both have HOMFLYPT span 8 and Kauffman span 7. The workbook uses names `12*n_296` and `12*n_550`; the asterisk is a notation marker and was removed when matching the database-package names.

The downloaded official archive is [knot_polys.xlsx.zip](https://raw.githubusercontent.com/knotinfo-org/assets/main/knot_polys.xlsx.zip), SHA256 `bd75a3f183f81c23830fcd9ab3b27c3516401f992b89d8e2d95057c05bb6883a`. The two relevant rows agree coefficient-for-coefficient with database-knotinfo 2026.11.2. Exact source strings and coefficient arrays are retained in `reproducibility/certificates/published_polynomials.json`.

This project attributes the knot and polynomial values to KnotInfo. Its result is the explicit violation of the stated full-span comparison, with a separate exact calculation from the braid. It makes no claim to have discovered new knot types or new polynomial values.

## Related claims and conventions

The [Knot Structures report](https://knot-structures.stainlesssteel4u.de/report/), section C1, mentions a half-a-spread calibration against these same two knots. That calibration is different from the full max-minus-min span explicitly defined in the source. The report also withdraws its earlier claim of complete verification at 14 and 15 crossings after finding unresolved symbolic terms in sample calculations. It does not provide a valid universal solution to the target stated here.

[Ferrand, arXiv:math/0002250v3](https://arxiv.org/pdf/math/0002250), Section 8, gives earlier examples where one-sided HOMFLY and Kauffman degree comparisons fail. The present target compares total widths. Searches for the exact span inequality and the two knot names did not locate an explicit published disproof. Version 5's omission is recorded without assigning a reason or priority.

The source-compatible HOMFLYPT convention is `a P_plus - a^(-1) P_minus = z P_0`, with unknot value 1. KnotInfo uses `v^(-1) H_plus - v H_minus = z H_0`; substituting `v=a^(-1)` preserves span. Kauffman's writhe correction also preserves span.

## Verification provenance

The first discovery engine used [Antonio De Lucreziis's signed-Gauss-code implementation](https://github.com/aziis98/kauffman-polynomial), commit `ded3fd2d56fe4953ec42fffe659bf3e6115033d0`. Its 53 upstream tests passed. Its direct symbolic evaluation from the published PD diagrams reproduced both counterexamples.

The deliverable verifier is a separate standard-library implementation of port-pairing smoothings and exact sparse polynomial arithmetic. It imports no code from that upstream implementation. It computes the polynomial pair for the explicit braid of `12n_296`, reproduces all coefficients, and checks the spans 8 and 7. A separate reviewer reran it and checked twenty additional braid/Markov identities. The final paper includes the complete coefficient tables.
