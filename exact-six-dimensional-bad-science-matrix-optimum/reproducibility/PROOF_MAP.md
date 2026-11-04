# Proof map

Exact target: `beta_6 = 1 + sqrt(3)/2` for real 6 by 6 matrices with unit Euclidean row norms.

| Claim | Argument and dependency | Verification |
| --- | --- | --- |
| Matrix objective equals a maximum over oriented cell families | One representative per antipodal pair; winning row with deterministic ties; orient its sign. Converse chooses each row parallel to its cell sum. | Proposition 2; both directions and zero sums handled in prose. |
| Antipodal-free set of size m has squared sum norm at most 32m | Cube orthogonality and Cauchy-Schwarz on disjoint S and -S. | Lemma 3; algebraic proof for all m, with empty/zero cases explicit. |
| Compression reduces arbitrary subsets to order ideals without decreasing squared sum norm | Reflect the initial sum into the nonnegative orthant; replace a negative coordinate by a missing positive partner. | Lemma 4; potential decreases, termination and ideal property explicit. Antipodal-freeness is not assumed after compression. |
| Small-set maxima for m=0,...,11 are 0,6,20,38,64,86,116,150,192,214,244,278 | Enumerate all ideals of size at most eleven by increasing code insertion, checking all immediate predecessors. | Lemma 5 gives complete executable code and completeness/uniqueness proof. Independent verifier checks 7,867 ideals and attaining initial segments. |
| Universal affine majorant for antipodal-free sets | For m<=11 use exact table and rational bounds 5/3 < sqrt(3) < 7/4. For m>=12 use 32m and positive increasing quadratic gap. | Lemma 6; ranges cover all 0<=m<=32 with no gap; verifier checks finite arithmetic. |
| Universal matrix upper bound | Sum six affine bounds with total cell cardinality 32. | Theorem 1 gives 32 beta <= 32+16 sqrt(3). |
| Lower bound attained | Steinerberger's matrix has unit rows; max norm is 2 when x1=x4 and sqrt(3) otherwise. | Algebraic proof plus exact rational evaluation of all 64 squared output norms. |
| Equality cell sizes | Strict affine gaps outside m=4,8; six cells total 32. | Corollary 7: four size-4 cells and two size-8 cells. |

## Computational independence

`src/cube_ideal_bounds.py` is the discovery program. It uses nested pairs of five-dimensional ideals and NumPy integer arithmetic to enumerate all 7,828,354 six-dimensional ideals. `src/verify_theorem.py` imports neither that program nor NumPy; it recursively inserts vertices and uses Python integers and fractions. Its main proof range consists of 7,867 ideals.

The finite enumeration is part of the computer-assisted proof. The universal passage from those finite values to arbitrary real matrices is proved in the manuscript. Release checks are recorded separately in `certificates/release_validation.json`.
