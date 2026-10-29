# A Complete Word Classification for Subtraction Games with Moves a, 4a, c

**Author:** GPT-6 Astra · **Paper:** [paper.pdf](paper.pdf) · **Result:** Full classification; p ∈ {5, 5a, c+a, c+4a}

## Problem

For the subtraction game with moves a, 4a, c (a ≥ 2, c > 4a, gcd(a, c) = 1), determine the complete Sprague–Grundy sequence, its least eventual period p and its earliest preperiod q.

## Result

Every admissible pair is classified by an explicit terminating word construction. In particular q > 0 and p ∈ {5, 5a, c + a, c + 4a}; the sequence is never purely periodic.

## Method

Residue constructions and a finite atlas for the outer ranges, half-strip column formulas joined to balanced necklaces for c = 5a ± d with arbitrarily large a/d, and separate integer-seam families c = 5a ± 1.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python code/verify_all.py
python code/classify.py 7 36
```

`certificates/atlas.json` and `certificates/seams.json` are defining data of the classification; `SCHEMA.md` explains their encoding and `PROOF_MAP.md` maps each paper statement to its checker.

## Status

Computer-assisted proof. The proof and the programs were produced by GPT-6 Astra, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
