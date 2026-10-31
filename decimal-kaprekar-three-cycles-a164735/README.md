# Counting all decimal Kaprekar three-cycles

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Status:** COMPLETE_PROVED

## Problem and result

The ordinary decimal Kaprekar map sorts the input's digits in descending
and ascending order and subtracts, without preserving leading zeros at the
next iteration. Let a(n) count its exact period-three orbits of n-digit
integers, counting cyclic rotations once.

All eighteen formulas in Kauers and Koutschan's Conjecture 23 are proved
for every n >= 3; a(1) = a(2) = 0. Every three-cycle belongs to one of their
two published families X and Y. The contribution is the exhaustive
classification for unbounded digit lengths.

## Proof and verification

The paper derives the exact digit-histogram transition, classifies regular
cycles analytically, and reduces every remaining case to one formula in
unbounded integer arithmetic. A Z3 proof DAG refutes that formula. A
separate checker, with no Z3 import, validates its scoped inferences using
syntactic propositional and equality rules and strict cvc5 local proof checking. It
rejects trusted proof steps and requires a false root with no open
hypotheses. Exact polynomial arithmetic proves all eighteen counting
identities. Finite examples serve only as regression checks.

The [proof map](reproducibility/PROOF_MAP.md),
[literature audit](reproducibility/LITERATURE_REVIEW.md),
and [verification reports](reproducibility/certificates/) are included.

## Reproduce

From `reproducibility/`, with Python 3.9 or later:

```bash
python -m pip install -r requirements.txt
python src/verify_all.py
```

This runs checker regressions, decimal-model checks, the exact comparison
with the source's eighteen polynomials, the generating-function identity,
the full-to-reduced query bridge, and independent verification of the saved
proof DAG. The complete certificate check can take an hour or longer; it
prints progress every 1,000 proof steps.

Optional proof regeneration:

```bash
python src/symbolic_z3proof.py --reduced --arith-solver 2 --timeout 600000
python src/verify_all.py
```

A timeout, unknown solver result, invalid inference, or undischarged root
hypothesis is an explicit failure. Regeneration and verification use exact
integer arithmetic. The stored reports identify the checked files by SHA-256.

The [SHA256SUMS](SHA256SUMS) file identifies the release files, including
the published PDF. The paper's LaTeX sources remain in the local research
folder; the public package includes the attributed formula excerpt needed
for exact verification. The optional `--build-paper` flag requires those
local paper sources.

## Attribution and scope

The families and conjectured formulas are due to Kauers and Koutschan.
Related structural results of Kay and Downes-Ward are cited in the paper.
The bounded literature audit located no prior complete proof of this exact
conjecture; it does not establish worldwide priority.

This computer-assisted proof was prepared by GPT-6 Astra and checked by
independent AI review and the supplied exact verification programs. It has
not undergone external human peer review and is not a Lean formalization.

The paper, documentation, and data use [CC BY 4.0](../LICENSE-CC-BY-4.0.txt);
code uses the [MIT License](../LICENSE). The target formula excerpt is
included with attribution to Kauers and Koutschan.
