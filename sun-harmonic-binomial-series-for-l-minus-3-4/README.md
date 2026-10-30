# A Markov–WZ Proof of Sun's Harmonic-Binomial Series for L₋₃(4)

**Author:** Claude Opus 5.5 · **Paper:** [paper.pdf](paper.pdf) · **Result:** Series equals 9 L₋₃(4)

## Problem

Prove Zhi-Wei Sun's Conjecture 3.9, equation (3.13) (arXiv:2603.29973v3):

∑_{k≥1} (−27)^{k−1} [(15k−4)(9H⁽²⁾_{3k−1} − 5H⁽²⁾_{k−1}) − 18/(3k−1)] / (k³ C(2k,k)² C(3k,k)) = 9 L₋₃(4),

where H⁽²⁾_m = ∑_{j≤m} 1/j² and L₋₃(s) = ∑_{j≥0} ((3j+1)^{−s} − (3j+2)^{−s}).

## Result

The series converges absolutely and equals 9 L₋₃(4) exactly as stated.

## Method

Sun's series is 1/27 of the a² Taylor coefficient of a one-parameter Markov–WZ identity. That identity is the case β = 1/3, γ = 2/3 of Theorem 1 of Kh. and T. Hessami Pilehrood (Electron. J. Combin. 18(2), 2012), and its constant term is Sun's earlier series for L₋₃(2). The paper reproves the identity with explicit estimates and computes the a² coefficient in closed form. The key identity is due to Hessami Pilehrood and Hessami Pilehrood. The contribution here is recognising the conjecture as its a² coefficient and giving a complete proof.

## Reproducibility

Run from the [`reproducibility/`](reproducibility) folder with Python 3.9 or later (dependencies are listed in `requirements.txt`):

```bash
python -m pip install -r requirements.txt
python src/verify_all.py
```

The run takes a few seconds. It checks the WZ relation symbolically. It checks it again independently in exact rational arithmetic, including a 343-point grid proof of the underlying polynomial identity. It confirms the Taylor-coefficient computation exactly for the first 80 terms. Finally, it compares both sides of Sun's identity to about 130 digits; this numerical agreement is supplementary.

## Status

Analytic proof (Markov–WZ pair). The proof and the programs were produced by Claude Opus 5.5, an AI system, and checked by internal review and the exact computations listed here. It has not been externally peer reviewed or formalized in a proof assistant.

## License

The paper and data are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt); the code is under the [MIT License](../LICENSE).
