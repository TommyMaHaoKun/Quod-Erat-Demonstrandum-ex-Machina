# Mathematical encoding, version 1.1.1

All indices start at zero; intervals are half-open in the position coordinate. All arithmetic is exact. JSON arrays are ordered, so word runs are concatenated in the stored order. Digits are values 0,1,2,3, not decimal integers representing a whole word.

## Open affine cones

`certificates/atlas.json` contains 89 records. Write c = base*a + r and t = r/a. Each identifier is the triple `(base, lo, hi)`, with rational endpoints encoded as strings. The record applies only when lo < t < hi. `base` is 4 or 5. Every admissible point strictly inside a cone has a >= 2, 0 < r < a, gcd(a,r)=1.

`[v,[u,w]]` means the run consisting of digit v repeated u*a+w*r times. `prefix` is the ordered list defining H; `period` defines W. The pairs `p=[p0,p1]`, `q=[q0,q1]` give p=p0*a+p1*r and q=q0*a+q1*r. Then

    G(n) = H[n]                 for 0 <= n < q
    G(n) = W[(n-q) mod p]       for n >= q.

The verifier checks positive run lengths throughout the open cone, total lengths, recurrence, primitive W, and H[q-1] != W[p-1]. The fields `seed` and `runs` are retained discovery metadata, ignored by the evaluator and proof. `singleton` is false for these open records. No formula at lo or hi is inferred by continuity.

The full record `(4,0,1/2)` decodes to

    H = 0^a 1^a 0^a 1^a 2^a 3^r 0^(a-r) 2^r 1^(a-r) 3^r 0^a 1^a 2^(a-r) 3^r
    W = 0^a 1^a 2^r 0^a 1^a 2^a
    p = 5a+r, q = 10a+r.

For (a,c)=(3,13), (p,q)=(16,31). Paper Section 5.1 prints both complete specialized strings, also asserted in `code/check_examples.py`.

## Rational seams

`certificates/seams.json` contains 89 records. Its identifier is `(base,t)`. Reduce the exact rational t=u/v: the unique primitive pair is **a=v, c=base*v+u**. `a,c,p,q` are integers; `prefix` and `block` are literal digit strings of lengths q,p. Use the same formula above with W=`block`.

The required identifiers are exactly the rational endpoints strictly between 0 and 1 of the two atlas partitions: base 4 covers (0,40/41] and base 5 covers [1/41,1). The association validator separately checks the contiguous atlas intervals and their outer limits, then uniqueness and equality of both identifier and parameter-pair inventories. Different spellings such as `1/2` and `2/4` count as the same identifier and cannot hide a duplicate.

`state_first`, `state_repeat`, `terms`, `status`, `ratio`, `c_mod_5a` and `c_div_5a`, when present, are auxiliary provenance. In particular `ratio` is not an alternative authoritative identifier: `t` is. The verifier checks the reported q,q+p state equality as a consistency check but does not rely on discovery of the first repeated state. Recurrence through q+c+p, primitive W, and the q-1 mismatch prove the result directly.

## Direct formulas and generated reports

For the central strip, all defining formulas are printed in Sections 6–7. `code/near/uniform_classification.py:formula(a,c)` returns `(p,q,symbol)`; `symbol(n)` returns a one-character digit without constructing the whole prefix. `code/classify.py` materializes H,W for all families.

Other JSON files are generated check results: bounds, counts, cases and pass information. They do not replace the two defining tables or the printed mathematical reductions. The manifest names the defining inputs explicitly.
