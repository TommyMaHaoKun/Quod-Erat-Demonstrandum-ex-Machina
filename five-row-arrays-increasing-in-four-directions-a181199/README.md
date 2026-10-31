# Five-Row Arrays Increasing in Four Directions (OEIS A181199)

**Author:** Claude Opus 5.5 · **Paper:** [paper.pdf](paper.pdf) · **Result:** Kauers–Koutschan Conjecture 19 and the OEIS recurrence proved for all n ≥ 1

## Problem

Let a(n) count the fillings of a 5 × n rectangle by 1, …, 5n that increase rightwards, downwards, down-right and down-left (OEIS A181199: 1, 1, 16, 985, 141696, …).

Kauers and Koutschan (J. Integer Sequences 26 (2023), Article 23.4.5, §6.4) conjectured an explicit nested hypergeometric sum for a(n) (their Conjecture 19):

a(n) = 1 − (27/4) Σ_{k=1}^{n−1} (−1)^k u(k) (5k)!/((3k)! k!²) Σ_{i=1}^{k−1} (−1)^i v(i) (3i)!/i!³,

with explicit rational functions u and v. The formula is equivalent to the order-3, degree-24 recurrence recorded in the OEIS entry.

## Result

Both the nested-sum formula and the recurrence hold for every n ≥ 1.

## Method

1. **Order polytope.** The volume of the order polytope is a(n)/(5n)!. Its columns form a chain of interlacing 5-tuples.
2. **Pfaffian.** Cauchy–Binet and de Bruijn's formula express the volume of the first n − 1 columns as a 6 × 6 Pfaffian with an explicit polynomial kernel.
3. **Double sum.** Integrating over the last column gives an explicit double sum of hypergeometric terms.
4. **Telescoping certificate.** An explicit certificate shows that T(n+1,k,l) − T(n,k,l) is a two-dimensional difference, which reduces a(n+1) − a(n) to a single sum.
5. **Gosper certificate.** A Gosper certificate proves the first-order relation behind the nested sum.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -m pip install -r requirements.txt
python src/verify_all.py
```

The run takes about five minutes. It checks the following exactly:

* the telescoping identity, as a 23 800-term polynomial identity in Q[n,k,l];
* the Gosper and boundary identities;
* the passage to the OEIS recurrence;
* the Pfaffian kernel and the fifteen pairing terms.

It also compares the double sum with three independent enumerations of the arrays and with the OEIS table. `data/OEIS_b181199.txt` (the first 100 terms) and `data/oeis_recurrence.json` (the recurrence coefficients) are taken from the OEIS. They are used only for comparison and to state the target.

## Status

Proof with exact symbolic certificates. The proof and the programs were produced by Claude Opus 5.5, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper is licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt), and so are the certificates; the code is under the [MIT License](../LICENSE). The two OEIS-derived files in `reproducibility/data/` remain under the OEIS's CC BY-SA 4.0 license.
