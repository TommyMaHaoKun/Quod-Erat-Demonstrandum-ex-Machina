# Literature and provenance audit: A172671

Access date: **2026-10-30** (Asia/Shanghai). This is a bounded search, not a claim of worldwide priority.

## Exact target and established prior work

1. Manuel Kauers and Christoph Koutschan, *Some D-Finite and Some Possibly D-Finite Sequences in the OEIS*, Journal of Integer Sequences **26** (2023), Article 23.4.5. The journal records publication on 2023-04-24 and receipt of the revised manuscript on 2023-04-20. Section 4.2, pp. 16–20, treats A172572 and A172671; **Conjecture 7**, p. 20, is the fourth-order recurrence for `b(n)=(n!)^3 a(n)/(3n)!` targeted here. **Theorem 8**, p. 20, proves D-finiteness, not that particular recurrence. The paper gives a walk model and a hypergeometric multisum and reports unsuccessful telescoping attempts. The normalization and recurrence are prior work, not new discoveries of this project.

   - Journal record: <https://cs.uwaterloo.ca/journals/JIS/VOL26/Koutschan/kout4.html>
   - Journal PDF: <https://cs.uwaterloo.ca/journals/JIS/VOL26/Koutschan/kout4.pdf>
   - Journal LaTeX: <https://cs.uwaterloo.ca/journals/JIS/VOL26/Koutschan/kout4.tex>
   - Latest arXiv version observed: **2303.02793v2**, submitted 2023-04-24; v1 was submitted 2023-03-05. No later version was listed: <https://arxiv.org/abs/2303.02793>.

2. **OEIS A172671** identifies the sequence as the number of `3n x 6` arrays with entries in `{0,1,2}`, row sums 2 and column sums `n`. Its offset is 1; the empty-array extension `a(0)=1` is specified by the present problem. The entry still labels its recurrence for the unnormalized sequence as conjectured, attributed to Christoph Koutschan, 2023-02-26. It links 75 terms. This public status is evidence about the entry, not proof that no subsequent solution exists.

   - Entry: <https://oeis.org/A172671>
   - Data: <https://oeis.org/A172671/b172671.txt>

## A relevant later source

Sergey Yurkevich, *Integer sequences, algebraic series and differential operators*, doctoral dissertation, Vienna, **2023**, **Conjecture 10.60**, printed pp. 180–181 (PDF pages 190–191), revisits the same target. His equation **(10.5)** rewrites `8^n a(n)` as the coefficient of `x^(3n)` in

```text
(3n)! (sum_{ell>=0} (2ell)! x^ell/ell!)
      (sum_{k>=0} x^k/[k!(n-2k)!])^6,
```

with the second sum truncated at `floor(n/2)`. This uses `h_2=((sum x_i)^2+sum x_i^2)/2`. Yurkevich reports computing 100 terms quickly and recovering the guessed recurrence, but aborting the creative-telescoping computation after 24 hours. Thus the reduction itself is known; it does not supply a proof of Conjecture 7. The intermediate multinomial display on p. 180 has apparent sign/index typographical errors, so identities used in the present project must be derived and checked independently.

- Author's copy: <https://yurkevi.ch/thesis.pdf>
- University-hosted copy downloaded: <https://homepage.univie.ac.at/herwig.hauser/Publications/yurkevich%20dissertation%202023.pdf>

## Supplementary source and transcription check

The journal provides its original Mathematica notebook and recurrence archive:

- <https://cs.uwaterloo.ca/journals/JIS/VOL26/Koutschan/SequencesOEIS.nb>
- <https://cs.uwaterloo.ca/journals/JIS/VOL26/Koutschan/kout4-recdata.zip>

Both were downloaded. The archive contains `rec172671.m` and a table of the first **33** terms, distinct from the current OEIS table of 75 terms. The A172671 notebook section records enumeration and agreement with input data; it is not a proof certificate for the target. The complete mathematical excerpt in the prepared `literature/target_formula.tex`, from its opening sentence through the end of the conjecture, was found **exactly** in the freshly downloaded JIS LaTeX source. No coefficient mismatch was found. Copies and SHA-256 digests are retained in `literature/`; no Mathematica code from these sources was executed.

## Later-work and public-repository search

Web searches included the exact identifier combined with `proof`, `recurrence`, `Hermite`, `Gaussian`, `Yurkevich`, and the years 2024–2026; the distinctive coefficient pair `3784` / `32164`; the cited authors with `Conjecture 7`; and the array description `row sums 2` / `column sums n`. These searches found the sources above and did not identify a later proof or an independently checkable certificate for the exact recurrence.

The required OpenAI repository check used <https://github.com/openai/math>. At access time, `main` resolved to commit **4eaee87548250b2682affda7d05d947c05554bae**, dated 2026-10-30 00:35:35 UTC. The full current `CONTENTS.md` and `overview.tex` were retrieved through the GitHub connector and searched for `A172671`, `Kauers`, `Koutschan`, and descriptive variants. No exact-target match was found. Repository code search for `A172671` also returned no results. The catalogue includes general contingency-table sampling/approximation work, which is not a proof of this fixed exact recurrence.

- Pinned catalogue: <https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/CONTENTS.md>
- Pinned overview: <https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/overview.tex>

This repository audit covered its catalogue, overview, and indexed identifier search; it was not a line-by-line review of every manuscript. Search indexing, alternate formulations, and unpublished work remain outside the audit. No absence claim stronger than “no prior resolution identified in this search” is warranted.

## Contribution and novelty boundary

The matrix interpretation, normalization, guessed recurrence, D-finiteness, and Yurkevich coefficient reduction are all prior work. This project's completed contribution is the four-moment derivation of the **specified** recurrence, its exact polynomial certificate, and its full nonnegative-index justification. The proof dependencies and verification results are recorded in `PROOF_MAP.md`. The literature search is provenance, not part of the mathematical proof. In particular, the OpenAI repository search above supplies no mathematical result used in the paper and is not included in its bibliography. No external peer review, proof-assistant formalization, or worldwide priority is claimed.

The public package includes the mathematical target excerpt and its recorded canonical hash. Downloaded full articles, notebooks, and search snapshots remain in the local research archive. If a full JIS TeX source is supplied as `literature/kout4.tex`, both verifiers additionally repeat the original-source comparison; it is not needed to check the proof.
