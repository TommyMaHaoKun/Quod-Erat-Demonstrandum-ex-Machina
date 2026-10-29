# The Minimum Kirchhoff Index of Polyomino Chains

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Unique minimizer: the zigzag chain

## Problem

Among polyomino chains with n square cells (the full class of Sun, Yang and Xu), find the minimum Kirchhoff index and every minimizer. Only a bend-free subclass had been settled.

## Result

For every n ≥ 1 the zigzag chain is the unique minimizer, and the minimum value is given by an exact O(n) formula.

## Method

An electrical recurrence writes the Kirchhoff index as a constant minus a quadratic form in turn variables; a positive-semidefinite comparison maximizes the form for every length, and a strict diagonal estimate gives all equality cases.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python src/minimum.py 10
python src/recurrence_check.py --max-cells 5
python src/verify_theorem.py --max-n 24 --word-n 8 --laplacian-n 5
python src/enumeration_audit.py --max-n 8
```

The first three use only the standard library; the geometric enumeration audit uses the optional packages in `requirements.txt`.

## Status

Analytic proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
