# Proof map

| Claim | Proof or certificate | Verification |
|---|---|---|
| The braid closure is one knot | Closure permutation is the 5-cycle (1 2 4 5 3) | Independent code and direct strand tracing |
| The HOMFLYPT polynomial has the displayed 17 terms | Exact skein recursion; all coefficients match KnotInfo | Standard-library port evaluator; separate upstream PD symbolic evaluator |
| The Kauffman polynomial has the displayed 40 terms | Exact skein recursion and writhe correction; all coefficients match KnotInfo | Same two independent implementations and original workbook |
| The spans are 8 and 7 | Nonzero endpoint coefficients; no terms outside the displayed support | Exact integer coefficient checks |
| The original universal full-span inequality is false | 8 > 7 on this explicit knot | Direct consequence |
| The gap is unbounded over knots | Connected-sum multiplicativity; additivity of Laurent width over an integral domain | Written proof |
| The computation terminates | Lexicographic induction on crossing count and number of first-under crossings | Written algorithm analysis |

The theorem uses one explicit diagram. It does not depend on completeness of a knot census. The polynomial values are existing KnotInfo data; the contribution is their explicit comparison and independently implemented certificate.
