# Lean proof of the Arkon recurrence (OEIS A006343)

The fifth-order recurrence proposed by R. J. Mathar holds for every integer
`m >= 5`. The coefficients are defined independently of that recurrence.

Let `C(z)` be the formal Catalan series, characterized by `C=1+z*C^2`,
and let `B` be the compositional inverse at zero of `z/(1+z^2*C(z))`.
The original generating function is `A=B/X`.

The formalization uses the division-free inverse specification

```text
A = 1 + (X*A)^2*T
T = 1 + (X*A)*T^2.
```

Here `T=C(B)` and `B=X*A`. These are precisely the inverse equation and
the Catalan equation at B. The theorem `series_inverseSpec` constructs a
solution; `inverseSpec_unique` proves that every solution has the same A.
Thus no existence or unproved identification is assumed in the final result.
Formal substitution is represented by these defining equations, rather
than by a separate general-purpose power-series composition API.

The exact main theorem, `MathLean.Arkon.a006343_recurrence`, is

```text
-(m+3)*(m-1)*a(m)
+ (11*m^2-2*m-45)*a(m-1)
- (37*m+29)*(m-3)*a(m-2)
+ (29*m^2-125*m+78)*a(m-3)
+ (61*m-106)*(m-3)*a(m-4)
- 155*(m-3)*(m-4)*a(m-5) = 0,    m >= 5.
```

`a(m)` is the rational coefficient of the independently constructed
formal series. Integrality and a combinatorial map-counting interpretation
are not needed for, or asserted by, this recurrence theorem.

## Proof

1. Iterate the coefficient-contracting map
   `V -> 1+X*(3*X*V+(1-X+3*X^3)*V^2+X^5*V^3)` and take its coefficientwise
   limit. Prove the limit exists, is fixed, and is unique.
2. Set `A=1+X^2*V`. Prove the independent known algebraic equation
   `X^3*A^3-(X-1)*A^2+(X-2)*A+1=0`, and the inverse specification above.
3. Differentiate twice. An explicit polynomial identity checked by `ring`
   gives `p2*A''+p1*A'+p0*A=3-36*X+98*X^2`.
4. Rewrite the differential operator using `theta=X*d/dX`. Extract its
   coefficient of `X^(n+5)`, where the forcing term vanishes, and obtain
   exactly the proposed recurrence.

All steps are checked by Lean 4.19.0 with Mathlib v4.19.0. There are no
placeholders, custom axioms, native-decision shortcuts, or assumed recurrence
hypotheses. Main axiom reports contain only `propext`, `Classical.choice`,
and `Quot.sound`. See [VERIFICATION.md](VERIFICATION.md).

## Rebuild

Install Lean via elan and Python 3.9 or later. From this directory:

```sh
lake exe cache get
python check.py
```

The toolchain and exact dependency revisions are pinned in the included
configuration and manifest. The checker builds the import closure in order.
No precompiled proof files are included.

## Attribution and scope

The recurrence and generating-function specification come from
[OEIS A006343](https://oeis.org/A006343) and the local OpenAIMathDiscovery
problem brief. The recurrence is attributed there to R. J. Mathar (2020).
The algebraic generating function is prior input, not a new discovery.
This proof was developed with Codex; no novelty or external peer-review
claim is made. This folder delivers a formal proof, not a separate PDF paper.
