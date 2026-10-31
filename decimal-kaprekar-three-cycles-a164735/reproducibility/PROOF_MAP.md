# Proof map

The target is Kauers--Koutschan Conjecture 23, all eighteen branches for every n >= 3, together with a(1) = a(2) = 0. The ordinary decimal map does not retain leading zeros.

| Claim | Argument / dependency | Verification |
|---|---|---|
| Every ordinary cycle has constant digit length | Sorting and subtraction never increase decimal length | Elementary argument in paper Section 1 |
| Exact subtraction word and width-loss condition | Borrow propagation through the positive, central and negative column blocks | Paper Lemma 2; independent decimal checks |
| Exact histogram transition | Half-open interval overlap computes mirrored differences; endpoint corrections count the subtraction word | Paper Lemma 3; src/verify_model.py |
| Histogram cycles correspond bijectively to integer cycles | Sort/subtract is determined by histogram; a deterministic map is injective on a cycle | Paper Lemma 4 |
| Family X exists, is invariant, and has no duplication | Explicit outside-in digit pairing rotates three positive parameters; fixed iff all three equal | Paper Section 3.1; src/families.py |
| Family Y exists and each orbit has one distinguished state | Three explicit vectors and their three histograms; distinct support endpoints | Paper Section 3.2; src/families.py |
| X and Y are disjoint | X has a positive difference-9 count; every Y state has difference-9 count zero | Paper Section 3.2 |
| A missing three-cycle exists iff Phi is satisfiable | All constraints implement the histogram relation, exact period and the complement of X/Y | Paper Lemma 5; three independent AI encoding reviews |
| A zero count above one forces every phase to be regular | The zero count cannot rise above one from below; above one it cannot increase, and equality forces endpoints 9 and 1 | Paper Appendix B, zero-count lemma; independent mathematical review |
| Every all-regular cycle belongs to X | Central width cannot increase; periodicity forces the explicit X inequalities and three-coordinate rotation | Paper Appendix B, regular-cycle classification; median-9 boundary handled separately |
| Every counterexample has a representative satisfying the reduced query Psi | Zero counts at most one, rotation to a nonregular first phase, and the inner-digit imbalance bound | Paper Appendix B, coverage lemma |
| The saved reduced input is the full model plus exactly the proved additions | Match all 199 original assertions and exactly 28 additional scalar constraints | src/verify_query.py; certificates/query_verification.json |
| Psi, and hence Phi, is UNSAT over unbounded integers | A scoped proof DAG ending in false; no maximum n or multiplicity | src/check_z3_dag.py; certificates/z3_dag_reduced_verification.json; release status in STATUS.md |
| The proof checker combines valid local implications without discarding hypotheses | Explicit assumption tracking, checked lemma discharge, syntactic logic/equality rules, strict cvc5 checks without global input assertions | Paper Appendix C; src/test_proof_checker.py; final DAG report |
| Correct orbit count | Remove X fixed points and divide by three; count Y distinguished states once | Paper Section 3 |
| All eighteen specified polynomials agree identically | Compare the program with the source excerpt, then use formal power-series power sums and exact polynomial cross-multiplication | Paper Section 5; src/families.py --symbolic |
| Lengths one and two have no three-cycle | Direct one-digit map and finite two-digit difference map | Paper Section 5 |
| Reproducibility and presentation | Run verifiers in a clean copy; compile saved LaTeX and inspect every page | certificates/release_verification.json and certificates/presentation_verification.json |

The X/Y families and their counts are prior work, attributed to Kauers and Koutschan. The new proof obligation is exhaustive classification. Bounded enumeration and finite regression checks support the model; they do not replace the unbounded refutation. The proof DAG is checked separately from Z3, with strict internal cvc5 proofs for its local arithmetic steps. The mathematical encoding and analytic reduction receive independent AI review. No Lean formalization or external human peer review is claimed.
