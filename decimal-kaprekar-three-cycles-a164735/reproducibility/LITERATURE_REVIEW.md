# Literature and novelty audit

Access date: 2026-10-31 (Asia/Shanghai).

## Exact target and primary source

Manuel Kauers and Christoph Koutschan, *Some D-Finite and Some Possibly D-Finite Sequences in the OEIS*, Journal of Integer Sequences **26** (2023), Article 23.4.5, Section 6.8, Conjecture 23, printed pages 37-39:

- [Published paper](https://cs.uwaterloo.ca/journals/JIS/VOL26/Koutschan/kout4.pdf)
- [Published LaTeX](https://cs.uwaterloo.ca/journals/JIS/VOL26/Koutschan/kout4.tex)
- [arXiv record](https://arxiv.org/abs/2303.02793)

The arXiv record lists v1 dated 2023-03-05 and v2 dated 2023-04-24; v2 was the latest revision visible at access. Conjecture 23 concerns ordinary decimal iteration without retaining leading zeroes. It predicts a degree-five quasipolynomial of period 18 for the number of length-three cycles, for n >= 3.

The two displayed word families X and Y and their counts are already in Section 6.8. Their existence and counting pattern are therefore not discoveries of this project. The substantive missing step is exhaustive classification: the source explicitly leaves open whether further families can occur at larger digit lengths. A calculation that regenerates those families or the eighteen polynomial branches does not, by itself, settle the conjecture.

## OEIS and later computation

- [OEIS A164735](https://oeis.org/A164735), created by Joseph Myers, 2009-08-23.
- [Internal entry](https://oeis.org/A164735/internal), entry revision 33 dated 2024-04-13 22:53:15 as displayed at access.
- [Myers's table](https://oeis.org/A164735/b164735.txt), n = 1,...,70.
- [Kauers--Koutschan formula attachment](https://oeis.org/A164735/a164735.txt).

The entry still labels both the closed form and Chai Wah Wu's recurrence/generating function (2024-04-13) as conjectures. The site-wide footer modification date is not the entry revision date.

[Georg Fischer's jOEIS implementation](https://github.com/archmageirvine/joeis/blob/1af2261953e1b9a002735daf90ef8b38e2e968d5/src/irvine/oeis/a164/A164735.java), generated 2024-05-13, instantiates a rational generating function. It contains no completeness proof or independent orbit classification, so its existence must not be cited as a proof of Conjecture 23.

## Related theory with a different proved scope

Anthony Kay and Katrina Downes-Ward, *Fixed Points and Cycles of the Kaprekar Transformation: 2. Even bases*, [arXiv:2408.12257v1](https://arxiv.org/abs/2408.12257), 2024-08-22; [HTML](https://arxiv.org/html/2408.12257v1). Only v1 was listed at access.

Equation (3) expresses image digits through sorted digit differences. Theorem 2 gives digit-count symmetry bounds and a monotonicity property of the zero count; Corollary 3 makes a zero count above one constant along cycles. Theorems 5 and 9 describe symmetric and almost-symmetric cycles, and Example 10 treats decimal 3-cycles explicitly. Their exhaustive classification is proved for base 4, not base 10. The conclusion explicitly acknowledges incomplete classification in higher bases. These results are useful prior structure, but do not close the present target.

Evan Chen, Ken Ono, Richard E. Schwartz and Dinesh Thakur, *Four-Digit Kaprekar Dynamics in Odd Bases*, [JIS **29** (2026), Article 26.4.7](https://cs.uwaterloo.ca/journals/JIS/VOL29/Ono/ono3.html), published 2026-08-12, describes a fixed digit length and varying odd bases. It does not prove an all-length decimal count. No inference from its formalization claim to this project is valid.

## Public repository check

The [openai/math repository](https://github.com/openai/math) was inspected at main commit `4eaee87548250b2682affda7d05d947c05554bae` (2026-10-30). Its complete [CONTENTS.md](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/CONTENTS.md) described 721 manuscripts and 373 result families. A case-insensitive text search of that contents file found no occurrences of `Kaprekar`, `A164735`, `A164736`, `Kauers`, or `Koutschan`; a repository code search for `Kaprekar` returned no results. A recursive-tree request failed, so this was not an exhaustive inspection of every repository file.

Global GitHub search for `A164735` found the jOEIS implementation and its generator records, alongside unrelated substring matches. No proof of the target was found in the relevant results inspected.

## Search scope and conclusion

Web queries included `"A164735" proof`, `"Kaprekar" "Conjecture 23"`, `"Kaprekar" "three" "cycles" proof counting`, `"Kaprekar" "quasipolynomial"`, `"Kaprekar" "quasi-polynomial" proof`, and searches combining the authors' names with Kaprekar. The original journal paper, latest arXiv version records, current OEIS entry, related even-base theory, later fixed-length results, and the specified OpenAI repository were checked.

No complete prior proof of the exact all-length decimal Conjecture 23 was located in this bounded audit. This statement is a report of the search, not a worldwide novelty guarantee. Any final project claim must attribute the X/Y families and target polynomials to Kauers--Koutschan and identify the additional exhaustive-classification argument precisely. The project's mathematical status is recorded separately in STATUS.md; this literature audit alone certifies no solution.
