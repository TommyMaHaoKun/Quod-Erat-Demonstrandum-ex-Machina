# Quod Erat Demonstrandum ex Machina

Complete solutions of open or conjectured problems in mathematics, found and written by AI systems. Each folder holds one problem: the paper as a PDF and the programs and certificates needed to re-check every computational step.

This repository accepts original mathematical results only. Previously published results and expositions of known results are excluded.

| # | Problem | Result | Author | Paper |
|---|---|---|---|---|
| 1 | [Partitions into cubes: sharp log-concavity threshold](log-concavity-threshold-for-cube-partitions/) | T₃ = 15656 | GPT-6 Astra | [PDF](log-concavity-threshold-for-cube-partitions/paper.pdf) |
| 2 | [Partitions into squares: sharp log-concavity threshold](log-concavity-threshold-for-square-partitions/) | T₂ = 1042 | GPT-6 Astra | [PDF](log-concavity-threshold-for-square-partitions/paper.pdf) |
| 3 | [Partitions into 4th, 5th and 6th powers: sharp thresholds](log-concavity-thresholds-for-fourth-fifth-and-sixth-power-partitions/) | T₄ = 637855, T₅ = 2507861, T₆ = 35577569 | GPT-6 Astra | [PDF](log-concavity-thresholds-for-fourth-fifth-and-sixth-power-partitions/paper.pdf) |
| 4 | [Minimum Kirchhoff index of polyomino chains](minimum-kirchhoff-index-of-polyomino-chains/) | Unique minimizer: the zigzag chain | GPT-6 Astra | [PDF](minimum-kirchhoff-index-of-polyomino-chains/paper.pdf) |
| 5 | [Minimum maximal domino packings of 4 × n](minimum-maximal-domino-packings-of-the-4xn-rectangle/) | Exact counts A(n) for all n | GPT-6 Astra | [PDF](minimum-maximal-domino-packings-of-the-4xn-rectangle/paper.pdf) |
| 6 | [Subtraction games with moves {a, 4a, c}](subtraction-games-with-moves-a-4a-c/) | Full classification; p ∈ {5, 5a, c+a, c+4a} | GPT-6 Astra | [PDF](subtraction-games-with-moves-a-4a-c/paper.pdf) |
| 7 | [OEIS A181280: binary matrices with reverse-ordered Gram rows](binary-matrices-with-reverse-ordered-gram-rows-a181280/) | Six-term formula proved | GPT-6 Astra | [PDF](binary-matrices-with-reverse-ordered-gram-rows-a181280/paper.pdf) |
| 8 | [OEIS A181198: four-row arrays increasing in four directions](four-row-arrays-increasing-in-four-directions-a181198/) | Second-order recurrence proved | GPT-6 Astra | [PDF](four-row-arrays-increasing-in-four-directions-a181198/paper.pdf) |
| 9 | [Six-variable cyclic quartic inequality](six-variable-cyclic-quartic-inequality/) | Proved with equality only at x₁ = … = x₆ | GPT-6 Astra | [PDF](six-variable-cyclic-quartic-inequality/paper.pdf) |
| 10 | [Real zeros of the squared Delannoy triangle](real-and-simple-zeros-of-the-squared-delannoy-triangle/) | All zeros real, simple and enclosed | GPT-6 Astra | [PDF](real-and-simple-zeros-of-the-squared-delannoy-triangle/paper.pdf) |
| 11 | [OEIS A195806: five-row triangular arrays](five-row-triangular-arrays-with-equal-line-sums-a195806/) | All six conjectured formulas proved | GPT-6 Astra | [PDF](five-row-triangular-arrays-with-equal-line-sums-a195806/paper.pdf) |
| 12 | [Sun's harmonic-binomial series for ζ(3)](sun-harmonic-binomial-series-for-zeta-3/) | Series equals 3ζ(3) | GPT-6 Astra | [PDF](sun-harmonic-binomial-series-for-zeta-3/paper.pdf) |
| 13 | [Monotonicity of a transformed gamma median](monotonicity-of-a-transformed-gamma-median/) | A′(k) < 0 for all k > 0 | GPT-6 Astra | [PDF](monotonicity-of-a-transformed-gamma-median/paper.pdf) |
| 14 | [Three-point Riesz energy on the circle](three-point-riesz-energy-on-the-circle/) | Fan's Conjecture 5.9 proved | Claude Opus 5.5 | [PDF](three-point-riesz-energy-on-the-circle/paper.pdf) |
| 15 | [OEIS A172572: binary matrices with prescribed margins](binary-matrices-with-prescribed-margins-a172572/) | Third-order recurrence proved | GPT-6 Astra | [PDF](binary-matrices-with-prescribed-margins-a172572/paper.pdf) |
| 16 | [Limited augmented Zarankiewicz number z_L(m, 3)](limited-augmented-zarankiewicz-number-m-by-3/) | z_L(m,3) = ⌊(3m+4)/2⌋; z_L(14,3) = 23 | Claude Opus 5.5 | [PDF](limited-augmented-zarankiewicz-number-m-by-3/paper.pdf) |
| 17 | [OEIS A172671: ternary matrices with prescribed margins](ternary-matrices-with-prescribed-margins-a172671/) | Fourth-order recurrence proved for all n ≥ 0 | GPT-6 Astra | [PDF](ternary-matrices-with-prescribed-margins-a172671/paper.pdf) |
| 18 | [Sun's harmonic-binomial series for L₋₃(4)](sun-harmonic-binomial-series-for-l-minus-3-4/) | Series equals 9 L₋₃(4) | Claude Opus 5.5 | [PDF](sun-harmonic-binomial-series-for-l-minus-3-4/paper.pdf) |
| 19 | [OEIS A181199: five-row arrays increasing in four directions](five-row-arrays-increasing-in-four-directions-a181199/) | Kauers–Koutschan nested sum and order-3 recurrence proved | Claude Opus 5.5 | [PDF](five-row-arrays-increasing-in-four-directions-a181199/paper.pdf) |
| 20 | [Decimal Kaprekar three-cycles: OEIS A164735](decimal-kaprekar-three-cycles-a164735/) | All eighteen formulas proved for every n >= 3 | GPT-6 Astra | [PDF](decimal-kaprekar-three-cycles-a164735/paper.pdf) |
| 21 | [Sun's binomial-harmonic series for ζ(5) and log 2](sun-binomial-harmonic-series-for-zeta-5-and-log-2/) | Series equals (93/2)ζ(5) + π⁴ log 2 | GPT-6 Astra | [PDF](sun-binomial-harmonic-series-for-zeta-5-and-log-2/paper.pdf) |

## Layout

Every problem folder has the same structure:

```
<problem>/
├── README.md          statement, result, method and how to reproduce
├── paper.pdf          the complete paper
├── reproducibility/   verification programs, certificates and requirements.txt
└── lean/              independent Lean project, where available
```

The verification programs in `reproducibility/` are plain Python (3.9 or later). Most use only the standard library; the rest list their dependencies in `requirements.txt`. Run the commands in each problem README from that problem's `reproducibility/` folder.

## Lean formalizations

The following problem folders include independently buildable Lean 4.19.0 / Mathlib v4.19.0 projects:

| Problem | Lean-checked scope | Project |
|---|---|---|
| Six-variable cyclic inequality | Original inequality for all real tuples and equality iff all entries coincide; excludes the stronger variance remainder | [Lean](six-variable-cyclic-quartic-inequality/lean/) |
| Limited augmented Zarankiewicz number | Exact maximum for all m >= 3 from the original definitions, with an attaining construction | [Lean](limited-augmented-zarankiewicz-number-m-by-3/lean/) |
| Three-point Riesz energy | Endpoint maximality and attainment for r >= 2 in Fan's Conjecture 5.9; excludes the paper's additional uniqueness and other-exponent claims | [Lean](three-point-riesz-energy-on-the-circle/lean/) |
| Minimum maximal domino packings of 4 x n | Minimum size and exact count for every positive width, including the physical-packing/path bijection and n = 1 exception | [Lean](minimum-maximal-domino-packings-of-the-4xn-rectangle/lean/) |
| A181280 binary Gram matrices | Original six-term counting formula for every n >= 4 and zero counts below 4, with the matrix/automaton bijection and full-state certificate | [Lean](binary-matrices-with-reverse-ordered-gram-rows-a181280/lean/) |
| A195806 five-row triangular arrays | All six original counting formulas for every n >= 0, including the array/parameter bijection and chamber boundary multiplicities | [Lean](five-row-triangular-arrays-with-equal-line-sums-a195806/lean/) |

Build instructions, exact theorem names, and verification records are in each project.

## Status

These are AI-generated mathematical results. Each proof was checked by internal review and by the exact computations included here, and the scopes listed above have additionally been checked in Lean. None has been externally peer reviewed; claims outside those Lean scopes are not presented as formally verified. The literature searches behind the novelty statements are documented in the papers and are necessarily bounded. Corrections and independent checks are welcome through issues.

## License

- **Code** — all programs in the `reproducibility/` folders and Lean source/configuration files in the `lean/` folders — is released under the [MIT License](LICENSE).
- **Papers, READMEs, certificates and data** are released under [Creative Commons Attribution 4.0 International](LICENSE-CC-BY-4.0.txt) (CC BY 4.0). Please credit the paper's author and link to this repository.
- **Exceptions:** `four-row-arrays-increasing-in-four-directions-a181198/reproducibility/data/OEIS_b181198.txt` is taken from the [OEIS](https://oeis.org/A181198). `five-row-arrays-increasing-in-four-directions-a181199/reproducibility/data/OEIS_b181199.txt` and `oeis_recurrence.json` in the same folder are taken from the [OEIS](https://oeis.org/A181199). All three remain under their original CC BY-SA 4.0 license.
