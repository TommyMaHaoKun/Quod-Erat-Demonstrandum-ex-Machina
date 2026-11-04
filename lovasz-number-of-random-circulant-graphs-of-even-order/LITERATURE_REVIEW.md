# Literature review

Access date: 2026-11-04.

## Exact model

Each nonzero inverse orbit in Z/nZ is independently selected with probability 1/2. For even n, the singleton {n/2} is an independent fair orbit. The target is the expectation limit E theta(G_n)/sqrt(n) -> 1 through all integers, for the edge-zero semidefinite-program convention.

## Primary sources

1. Afonso S. Bandeira, Jaroslaw Blasiok, Daniil Dmitriev, Ulysse Faure, Anastasia Kireeva and Dmitriy Kunisky, *The Lovasz number of random circulant graphs*, arXiv:2502.16227v1, 22 February 2025. The current arXiv record lists v1. Its bounds place the expected theta number within a log-log factor of the square-root scale; the abstract and Fourier formulation were checked.
   - https://arxiv.org/abs/2502.16227

2. Afonso S. Bandeira, Daniil Dmitriev, Kevin Lucca, Petar Nizic-Nikolac and Almut Rodder, *Randomstrasse101: Open Problems of 2025*, arXiv:2603.29571v1, Entry 9, Conjecture 18. This records the leading-constant question.
   - https://arxiv.org/html/2603.29571v1

3. Xin Chen, Hongwei Hu, Yanqing Hu, Wei Wang and Luzhen Yang, *Sharp asymptotics for the Lovasz number of random circulant graphs*, arXiv:2610.22971v1, submitted 16 October 2026. The current arXiv record lists only v1. Theorem 1.1 proves the limit along all **odd** orders, including composite orders. The all-integer target therefore requires an even-order extension.
   - https://arxiv.org/abs/2610.22971v1
   - https://arxiv.org/html/2610.22971v1
   - https://arxiv.org/pdf/2610.22971v1

The third paper's PDF, HTML and TeX source were retained locally for theorem-level inspection. Its independent-row sampling proof, abstract Walsh comparison, Gaussian results and Sections 7-11 were checked against the extension's hypotheses.

## Imported results and new argument

The manuscript imports the following results from Chen et al.: the odd-order main theorem; the independent-row Fourier estimate inside Section 5; the abstract Walsh moment comparison in Theorem 7.2; the Gaussian fixed point (Theorem 9.3), Hermite approximation (Proposition 9.4), and tree-degree tail (Theorem 9.5). It also identifies and checks the parity-neutral dependencies in the Fourier duality and smooth scalar-transfer arguments.

The new argument conditions Poisson row sampling on avoiding both self-inverse residues; removes 0 and n/2 from canonical tree flows; proves the same quantitative overlap and covariance bounds with two exceptional output modes; proves an exact degree-d Walsh projection excluding the singleton sign; and includes the resulting leaf residual of squared norm 4/n. It then carries out the expectation integration for even orders. Attribution to the odd-order paper appears in the title-level scope, abstract, introduction, imported lemma and conclusion of the proof.

## Search boundary

Targeted searches included the title, arXiv identifier, "random circulant theta even 2026", and "Lovasz circulant all integers". They located the odd-order paper and no existing even-order extension. A public proof-repository index was also checked directly; its matching circulant entry concerned the Hadamard conjecture, a different problem. The novelty claim is restricted to the even-order extension of the cited theorem.
