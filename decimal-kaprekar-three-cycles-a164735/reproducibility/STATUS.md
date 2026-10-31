# Status

COMPLETE_PROVED

Author: GPT-6 Astra. Date: October 31, 2026.

All eighteen branches of Kauers--Koutschan Conjecture 23 are proved for every
n >= 3, for ordinary decimal Kaprekar iteration without retaining leading
zeros. Cyclic rotations count once, and a(1) = a(2) = 0. Every exact
three-cycle belongs to the previously published X or Y family.

The proof combines an analytic regular-cycle classification with an
unbounded integer-arithmetic refutation of every remaining case. The saved
certificate passed independent scoped verification: 637,643 proof nodes,
22,078 strict cvc5 local inference checks, and a false root with no open
hypotheses. Trusted and incomplete cvc5 proof rules are rejected. The checker
does not import Z3; Z3 supplies the candidate certificate.

All prescribed verification programs passed from a clean isolated copy.
The exact query bridge, all eighteen source formulas and generating-function
identities, adversarial checker regressions, and direct decimal-model checks
passed. The saved LaTeX also rebuilt cleanly; all 11 PDF pages were visually
inspected, and the clean rebuild has identical rendered pixels and text.
The presentation audit found no unresolved references, overflow, stray
draft text, local paths, or author-metadata mismatch.

Verification records are in certificates/release_verification.json,
certificates/z3_dag_reduced_verification.json, and
certificates/presentation_verification.json. PROOF_MAP.md distinguishes the
unbounded proof from finite regression checks.

The families and formulas are attributed to Kauers and Koutschan. The new
result is their exhaustive classification for all lengths. The literature
audit is bounded. This is a computer-assisted proof reviewed by AI systems;
it is not a Lean formalization and has not undergone external human peer review.
