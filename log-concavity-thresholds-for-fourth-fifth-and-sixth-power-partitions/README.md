# Exact Log-Concavity Thresholds for Partitions into Fourth, Fifth and Sixth Powers

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** T₄ = 637855, T₅ = 2507861, T₆ = 35577569

## Problem

For k = 4, 5, 6 let p_k(n) count the partitions of n into positive k-th powers. Determine the exact permanent log-concavity thresholds conjectured by Roy.

## Result

The thresholds are T₄ = 637855, T₅ = 2507861 and T₆ = 35577569. The inequality is strict from each threshold onward, an exact negative value at T_k − 1 proves minimality, and all equality cases are classified.

## Method

Strict analytic tails from 2,000,000, 12,000,000 and 180,000,000 (Wright-function curvature model, Mellin transformation, certified contour bounds), overlapping exact finite reconstructions.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -m pip install -r requirements.txt
python src/verify_all.py --analytic-only
python src/verify_all.py --python-finite
```

`--analytic-only` checks every analytic certificate in minutes. The complete finite reconstruction (`python src/verify_all.py`) recomputes up to 180 million coefficients and uses the C# engines in `src/` (Windows .NET Framework compiler); `--python-finite` is a slower pure-Python alternative. `output/verification_report.json` records the original consolidated verification; `MANIFEST.json` was regenerated for this repository layout.

## Status

Computer-assisted proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.
