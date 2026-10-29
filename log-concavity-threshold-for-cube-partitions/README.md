# The Exact Log-Concavity Threshold for Partitions into Cubes

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** T₃ = 15656

## Problem

Let c(n) count the partitions of n into positive cubes (repetitions allowed, order ignored). Roy conjectured explicit sharp thresholds after which the power-partition functions are log-concave; this is the cubic case.

## Result

c(n)² > c(n−1)c(n+1) for every n ≥ 15656, while the inequality fails at n = 15655. The exceptional set is determined completely: 5505 negative indices and 41 equality indices.

## Method

Exact integer computation through n = 10,000,000, joined to an explicit analytic estimate for the infinite tail (cubic Mellin transformation, a 24th-order saddle expansion with proved remainder, and a rational covering of the minor arcs).

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python code/verify_all.py
```

About two minutes on a laptop. `code/finite_generate.py` regenerates the finite certificate from scratch.

## Status

Computer-assisted proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
