# Proof/program map, version 1.1.1

Read paper Appendix C for the full hypotheses and derived thresholds, and Sections 6–7 for the identities themselves. This index names actual functions; generated reports are not assumptions. All program paths below are relative to the supplement root.

| Mathematical obligation | Exact program and functions | Reduction and domain | Bounds/horizon and conclusion |
|---|---|---|---|
| Open affine recurrence and least p,q | `code/verify_atlas.py:check` | Lemmas 2.1, 2.5, 2.6; all 89 open cones | Every shifted homogeneous endpoint, order checked at both rational ends; F=HW^2 or HW^3 covers q+c+p. Rotations and isolated roots excluded; last mismatch. 350750 cells. |
| Seam association and finite inventory | `code/seam_inventory.py:validate_record,validate_inventory,load_tables` | Reduced rational t=u/v; a=v,c=base*v+u | Exact identifiers and pairs, no duplicates, prescribed interval endpoints/adjacency. 89 records. |
| Seam recurrence and least p,q | `code/verify_seams.py:verify` | Finite word Lemma 2.1 | All q+c+p positions; all proper divisors; last mismatch. 419798 positions. |
| Complete finite parameter partition | `code/verify_coverage.py:main` | Finite set/order checks plus Section 9 algebra | Base 4 endpoints 0,40/41; base 5 endpoints 1/41,1; infinite remainder classified by the printed near theorems. |
| Large repetition families | `code/uniform_certificate.py:template,bound,check,main` | Lemma 2.4; the nine domains of the uniform-bound table | Complete 0,1,4,c shifts; normalized period 5; K=ceil((U-L+5)/5), at least k_min. K list 4,4,5,5,6,8,9,7,5. 14829 cells. |
| Large j=4 transition identities | `code/band4_tables.py:table,less,main` | Exact affine homogeneous-cell order, 0<r<a | Printed transient/early/late intervals; all target/option endpoints; no phase parameter. Counts 11,6,11. |
| All a=2 words | `code/a2_certificate.py:boundaries,certify` | Affine reduction with period 10 | Shifts 0,2,8,c; intercepts [-10,50], slopes divisible by 10; K=7; exact q+c+p. 4199 positions. |
| Upper half-strip | `code/near/upper_splice_certificate.py:front_checks,front_segments` | Lemma 2.7; every column index | Complete shifts 0,1,4,5, horizon 26m+100; stable-order and clipping assertions at K=20; L=40,M=20; all tails active by 26m+92. Special column zero delay 6 checked through 99. 30520 positions. |
| Upper integer seam wrap | Same file: `templates,ordered_endpoints,wrap_checks,check_wrap_point` | Lemma 2.7, a>=10 | K=20,L=40,M=20; horizon 26m+(20,18,24); all omitted cuts remain outside by slope test. 23082 positions. |
| Upper integer seam join/last mismatch | Same file: `interface_checks,exact_q_checks` | Fixed offsets and printed suffix reduction | Join offsets -1..3; u>=3 reduced by period 8; 150 joins and 62 exact-q symbols. |
| Upper open boundary | `code/near/upper_boundary_uniform.py:templates,macro_ends,bounds,check,main` | Lemma 2.7; six (s,delta), m>=13 | Shifts S+(0,1,4), F+6; horizon |S|-1; F extended by rho^(2m+10); gap 8; K=18,18,18,18,18,20. L=40,M=20. 114528 positions. Fully derived in C.1. |
| Upper open last mismatch | `code/near/upper_minimality.py:tail_relative,check` | Fixed suffix identities after cancelling common powers; m>=13 | 76 symbols (including 63 residue-one comparisons). Printed proof bounds every column and exhibits q-1. |
| Lower half-strip | `code/near/halfstrip_certificate.py:templates,boundaries,check,main` | Lemma 2.7; every column | Intercepts [-3,10],[0,24],[0,30], gap 10, K=6,7,7; L=40,M=20; ordinary horizon Q_j+8; token identity after Q_j+4. Column zero checks y=0..13, all final eight phases. 28424 positions. |
| Lower open boundary | `code/near/lower_open_boundary_uniform.py:templates,macro_ends,bounds,check,main` | Lemma 2.7; six (s,delta), m>=13 | S+(0,1,4), F+4; horizon |S|-1; gap 8; K=16,16,16,18,18,19; L=40,M=20; affine input coverage checked. 105970 positions. Fully derived in C.2. |
| Lower open last mismatch | `code/near/lower_open_minimality.py:main` | Fixed suffix identities and printed all-column comparison | 44 symbols, including widths 20,14. Primitivity is separately proved from token parsing/cluster counts. |
| Lower integer seam wrap/join/last mismatch | `code/near/lower_seam_uniform_certificate.py:wbound,symbolic_bounds,check_boundary,main` | Lemma 2.7, h>=3 | Cyclic copies -2..5 with coverage inequalities; horizon D+P+10; shifted endpoints and mismatch successor. Intercepts [-8,25],[-10,39],[-28,75], gap 2; K=37,45,72, L=40,M=20. |
| Lower integer seam interior mismatch | Same file: `check_column_difference,main` | Lemma 2.7 plus agreeing final tails | max(Q_j,Q_next)+8; mismatch successor; gap 10, K=7,8,9. Combined lower seam count 304624. |
| Token identity (redundant) | `code/near/tail_stationarity_check.py` (module loop) | Locality in four tokens; also analytic Lemma 2.8 | 16 contexts, 64 third-token positions cover delays 1,4 and advance 1. |
| Extra pure-extension obstruction (optional) | `code/pure_obstruction_certificate.py:main,prove,refine` | Independent exact affine obstruction | 11 cases; final universal q>0 instead follows from Section 9 and the proved period restriction. |

## Independent corroboration and safeguards

- `code/test_seam_inventory.py:main`: accepts all 89 original records and rejects seven corrupt inventories; does not alter data.
- `code/crosscheck_atlas.py` (module loop): 178 rational specializations near both ends of all 89 cones; 15164928 independently generated mex terms.
- `code/near/crosscheck_uniform.py:one`: 38 inputs; 5694978 independent mex terms, primitive-block and last-mismatch checks.
- `code/near/lower_open_crosscheck.py:main`: separate formula implementation; 54 inputs, 11229686 positions checked against initialized mex and q.
- `code/near/lower_seam_crosscheck.py` (module loop): separate seam formula; 71 inputs, 2002430 positions checked against initialized mex and q.
- `code/check_examples.py:main,compare`: printed strings, towers, inverse, splice and example table; 413 fresh recurrence comparisons, 165031 positions, including the outer bands.

The full driver runs essential checks and these corroborations, distinguishing their roles in the paper and instructions. It invokes no discovery/state-search routine. A state-search utility is included only as an optional reference.
