# A Recurrence for Four-Row Arrays Increasing in Four Directions

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Second-order recurrence proved

## Problem

Prove the second-order polynomial recurrence conjectured by Koutschan for OEIS A181198, the number of fillings of a 4 × n rectangle by 1, …, 4n increasing rightwards, downwards, down-right and down-left.

## Result

The conjectured recurrence holds for every n ≥ 1.

## Method

A cut before the second row fills gives a positive double sum; a polynomial antiderivative turns it into an integral, and two rational integration-by-parts certificates give a first-order inhomogeneous recurrence whose elimination yields the target.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -m pip install -r requirements.txt
python src/reproduce.py
```

The individual checkers in `src/` can also be run separately. `data/OEIS_b181198.txt` holds the first 100 terms of the sequence from the OEIS (CC BY-SA 4.0), used only for comparison.

## Status

Analytic proof with exact symbolic certificates. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
