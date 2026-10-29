# Minimum Maximal Domino Packings of the 4 × n Rectangle

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Exact counts A(n) for all n

## Problem

Classify and count the minimum maximal domino packings of a labeled 4 × n rectangle. The minimum size m(n) = ⌈4n/3⌉ (n ≥ 2) is known (Klostermeyer–Yeo; Cibulis–Trump); the structure and the number of optimal packings for every length were not.

## Result

A local grammar describes every minimum packing, and the number A(n) is eventually constant, linear or quadratic by residue: A(3k) = 8 (k ≥ 3), A(3k+2) = 50k + 24 (k ≥ 4), A(3k+1) = 226k² + 106k − 392 (k ≥ 6), with all exceptions listed.

## Method

An elementary proof of the minimum, a boundary potential that bounds the defect of every optimal path, and a finite integer-vector identity that propagates the recurrence to all lengths.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python verify.py --independent
python independent_grammar_audit.py
```

Do not run Python with `-O`; the checks are assertions.

## Status

Computer-assisted proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
