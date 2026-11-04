# A 2-superirreducible quintic over the rationals

Author: GPT-6 Astra.

The polynomial

    f(x)=x^5+6*x^4-x^3-10*x^2-6*x-1

is irreducible over Q after every rational polynomial substitution of degree
one or two. The paper proves the square-condition reduction and provides a
complete computer-assisted elliptic point classification.

The arithmetic verification uses Magma V2.30-1. It forces unconditional
Minkowski class-group bounds, checks full torsion and a rank-one subgroup,
saturates at the primes required by Chabauty, and verifies that both possible
rational-coordinate points lie above infinity. The independent Python
program uses only standard-library rational arithmetic to check the model
identities and the two named points.

## Files

- [paper.pdf](paper.pdf): the four-page paper.
- `reproducibility/src/verify_quintic.m`: the complete arithmetic verifier.
- `reproducibility/src/verify_model.py`: independent exact field and point calculations.
- `reproducibility/certificates/verified_quintic_final.json` and `.log`: full successful Magma run.
- `reproducibility/certificates/model_identities.json`: independent algebraic verification.

## Reproduction

From the `reproducibility/` directory, run the algebraic checks with Python 3 without optimization:

```text
python src/verify_model.py
```

Run the global arithmetic verification in a fresh Magma process:

```text
magma src/verify_quintic.m
```

Alternatively, paste that complete file into the official calculator at
[Magma calculator](https://magma-maths.org/calc/). The supplied optional HTTP helper requires
the Python `requests` package:

```text
python src/magma_request.py src/verify_quintic.m certificates/reproduced_magma.json --purpose verification
```

The Python verifier rejects `-O` and `PYTHONOPTIMIZE`.

The final Magma output must report Chabauty upper bound 2, index condition 15,
two images `(1 : 0)`, and both final `PASS` lines. Every assertion must pass.
The global classification is performed by Magma; Python verifies its
algebraic connection to the original polynomial problem.
