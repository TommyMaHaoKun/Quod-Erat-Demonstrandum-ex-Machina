# Independent audit of the Poisson-partition argument

Auditor: GPT-6 Astra (independent research subagent)

Date: 2026-11-02

Status: the argument below proves the transport inequality needed for the full
interval conjecture. This audit is an ordinary mathematical review, not a
proof-assistant verification. The theorem does not depend on numerical tests.

## 1. Exact functional statement

Write `I=[0,1]` and, for `0<t<1`, let `mu_t` be the beta probability measure with
both shape parameters `(1-t)/2`. Its density is

\[
 c_t[x(1-x)]^{-(1+t)/2},\qquad
 c_t=B((1-t)/2,(1-t)/2)^{-1}.
\]

This will be proved below to be the maximum-energy equilibrium measure of the
interval for the kernel `|x-y|^t`; no known equilibrium theorem is needed. Put

\[
 e_t=\iint |x-y|^t\,d\mu_t(x)d\mu_t(y).
\]

For every bounded nondecreasing Borel map `T:(0,1)->R`, define

\[
 F_t(T)=\left(\frac{\iint|T(x)-T(y)|^t\,d\mu_t(x)d\mu_t(y)}{e_t}\right)^{1/t}.
\]

The central statement is `F_r(T) <= F_s(T)` whenever `0<r<s<1`.

Changing `T` at its countably many discontinuities, or at the endpoints, does
not change these integrals. Thus take a right-continuous representative on the
interior, with endpoint values equal to the one-sided limits. It defines a
finite positive Stieltjes measure `nu` on `(0,1)`, with total mass equal to the
difference of its endpoint limits. For Lebesgue-almost every pair `x<y`,

\[
 D_T(x,y)=\frac{T(y)-T(x)}{y-x}=\frac{\nu((x,y))}{y-x}.
\]

Both beta laws have positive densities on the interior, so the same exceptional
sets have zero beta measure. A constant map causes no difficulty: all the
functionals are zero.

## 2. The normalized beta-pair law

Let `P_t` be the probability law on ordered pairs `0<x<y<1` with density

\[
 \frac{2c_t^2}{e_t}(y-x)^t
 [x(1-x)y(1-y)]^{-(1+t)/2}.
\]

Its normalization is exactly the definition of `e_t`; the diagonal has zero
measure. Then `F_t(T)=(E_{P_t} D_T^t)^(1/t)`.

Set

\[
 h(u)=\frac{1+\tanh u}{2},\quad x=h(u),\quad y=h(u+z),\quad z>0,
 \qquad \Delta(u,z)=h(u+z)-h(u).
\]

The identities `h'(u)=1/(2 cosh^2 u)`,
`h(u)(1-h(u))=1/(4 cosh^2 u)`, and

\[
 \Delta(u,z)=\frac{\sinh z}{2\cosh u\cosh(u+z)}
\]

give the exact change of variables

\[
 (y-x)^t[x(1-x)y(1-y)]^{-(1+t)/2}\,dx\,dy
 =2^{t+1}\Delta(u,z)(\sinh z)^{t-1}\,du\,dz.
\]

Also `int_R Delta(u,z) du=z`, by writing the increment as an integral of
`h'` and applying Tonelli. Consequently, with `alpha=1-t`, the transformed
probability law is

\[
 dP_t=\frac{\Delta(u,z)(\sinh z)^{-\alpha}}{Z_\alpha}\,du\,dz,
 \qquad Z_\alpha=\int_0^\infty z(\sinh z)^{-\alpha}\,dz.
\]

This integral is finite and positive: its integrand is asymptotic to
`z^(1-alpha)` at zero and to `2^alpha z exp(-alpha z)` at infinity.

## 3. Positive exponential expansion and the mixing law

For `z>0` and `0<alpha<1`, the binomial series gives

\[
 (\sinh z)^{-\alpha}
 =2^\alpha\sum_{n=0}^\infty a_n(\alpha)e^{-\lambda_n(\alpha)z},
 \qquad
 a_n(\alpha)=\frac{(\alpha)_n}{n!},\quad
 \lambda_n(\alpha)=2n+\alpha.
\]

Every term is nonnegative. Thus Tonelli justifies all integrations and
summations without a uniform-convergence assumption. Define

\[
 S_\alpha=\sum_{n\ge0}\frac{a_n(\alpha)}{\lambda_n(\alpha)^2}
 =2^{-\alpha}Z_\alpha,
 \qquad
 w_n(\alpha)=\frac{a_n(\alpha)}{\lambda_n(\alpha)^2S_\alpha}.
\]

This is a strictly positive probability mass function. In particular, it is
not the binomial coefficient sequence alone: the factor `lambda_n^(-2)` is
essential.

An optional closed form, not needed by the proof, is

\[
 S_\alpha=\frac14 B(\alpha/2,1-\alpha)
 [\psi(1-\alpha/2)-\psi(\alpha/2)].
\]

## 4. Interpretation by cells of a stationary Poisson process

Take a homogeneous Poisson point process of intensity `lambda>0` on the real
`u`-axis. Its consecutive points partition the line into bounded intervals
almost surely. Map these cells through `h`; they partition `(0,1)` into
intervals. Independently choose `X` uniformly on `(0,1)` and let `(L,R)` be
the transformed cell containing `X`.

The density of a cell with logit endpoints `(u,u+z)`, selected in this way, is

\[
 \lambda^2 e^{-\lambda z}\Delta(u,z)\,du\,dz.
\]

A direct derivation avoids any point-process integration theorem: conditional
on `h^{-1}(X)=v`, the distances from `v` to the nearest Poisson points on its
left and right are independent exponentials of rate `lambda`. Their joint
density is `lambda^2 exp(-lambda z)`. Integrating the density `h'(v)` of the
base point over `u<v<u+z` supplies precisely the factor `Delta(u,z)`.

Therefore `P_t` is exactly the mixture of these cell laws obtained by sampling
`n` from `w_n(alpha)` and then taking `lambda=2n+alpha`.

The chord slope is the cell average

\[
 A=\frac{\nu((L,R))}{R-L}.
\]

It has finite mean equal to `nu((0,1))`. Indeed, conditional on a partition,
uniform sampling selects a cell with probability its length, so the expected
slope is the sum of the masses of all cells. Random endpoints avoid every
fixed atom of `nu` almost surely. Since a finite measure has only countably
many atoms, all partition boundaries are `nu`-null almost surely. This also
handles singular continuous measures and jump maps; absolute continuity of
`T` is not required.

## 5. Ordering the random rates

Suppose `0<alpha_s<alpha_r<1`, as occurs for `r<s`. Apart from a constant
independent of `n`,

\[
 \frac{w_n(\alpha_s)}{w_n(\alpha_r)}
 =\frac{S_{\alpha_r}}{S_{\alpha_s}}
 \frac{(\alpha_s)_n}{(\alpha_r)_n}
 \left(\frac{2n+\alpha_r}{2n+\alpha_s}\right)^2.
\]

The Pochhammer ratio decreases with `n`, since its next factor is
`(n+alpha_s)/(n+alpha_r)<1`. The final ratio also decreases with `n`. Hence
the displayed likelihood ratio decreases with `n`.

For completeness, decreasing likelihood ratio implies the needed stochastic
order as follows. For the initial segment `{0,...,k}`, the average likelihood
ratio under the `alpha_r` law is at least its unconditional average, namely
one; the average over the initial segment is at least the average over its
complement. Thus its probability under `alpha_s` is at least its probability
under `alpha_r`. The cumulative-distribution inequalities allow the inverse-CDF
coupling `N_s<=N_r` using one uniform variable. It follows pathwise that

\[
 \Lambda_s=2N_s+\alpha_s\le 2N_r+\alpha_r=\Lambda_r.
\]

The discreteness and shift of the two rate supports are harmless: we couple
the indices first, then the rates.

## 6. Nested partitions and the two inequalities

Conditional on the coupled rates, generate the rate-`Lambda_r` Poisson process.
Independently retain each point with probability `Lambda_s/Lambda_r`. The
retained points form a homogeneous process of rate `Lambda_s`; its partition
coarsens the first one. This construction has the exact required marginal
laws after averaging over the rates.

For any coarse cell `J` with fine subcells `J_i`, additivity of `nu` and
Lebesgue length gives

\[
 A_J=\sum_i\frac{|J_i|}{|J|}A_{J_i}.
\]

There are finitely many fine subcells in each bounded logit cell almost surely.
For `0<r<1`, concavity of `a^r` implies

\[
 |J|A_J^r\ge\sum_i|J_i|A_{J_i}^r.
\]

Sum over the countably many coarse cells and then average over both random
partitions and the rates. All terms are nonnegative. This proves

\[
 \mathbb E A_s^r\ge\mathbb E A_r^r.
\]

Both random variables have finite first moment, so their `r` and `s` moments
are finite. The usual monotonicity of probability-space power means gives

\[
 (\mathbb E A_s^s)^{1/s}
 \ge (\mathbb E A_s^r)^{1/r}
 \ge (\mathbb E A_r^r)^{1/r}.
\]

By the exact marginal identifications above, these are `F_s(T)>=F_r(T)`.

## 7. Interval equilibrium and its value from the same argument

For any bounded nondecreasing `T`, the cell slope has mean equal to the total
variation `V` of `T`. Concavity gives

\[
 F_t(T)^t=\mathbb E A_t^t\le(\mathbb E A_t)^t=V^t.
\]

Every probability measure `eta` on `[0,1]` is `T#mu_t` for its quantile map
composed with the CDF of `mu_t`; that `T` takes values in `[0,1]`, hence has
`V<=1`. Consequently its energy is at most `e_t`. Thus `mu_t` maximizes energy
on the interval. This proof uses `e_t` solely as its defining double integral,
so it does not presuppose the equilibrium formula.

Let `U(x)=int |x-y|^t dmu_t(y)`. Varying `mu_t` toward `delta_x` gives a
right derivative `2(U(x)-e_t)<=0`, hence `U(x)<=e_t` for all `x` in the
interval. Since `int U dmu_t=e_t`, continuity of `U` and full support of
`mu_t` imply `U=e_t` everywhere on `[0,1]`. In particular,

\[
 e_t=U(0)
 =\frac{B((1+t)/2,(1-t)/2)}{B((1-t)/2,(1-t)/2)}
 =\frac{\Gamma((1+t)/2)\Gamma(1-t)}{\Gamma((1-t)/2)}
 =2^{-t}\frac{\Gamma((1+t)/2)\Gamma(1-t/2)}{\sqrt\pi}.
\]

The final identity is the gamma duplication formula. This recovers the
classical interval equilibrium and benchmark within the proof itself.

## 8. Transfer to arbitrary compact sets

Let `K` be compact with at least two points. A maximum-energy probability
measure `eta` for exponent `r` exists because the space of probabilities on
`K` is weakly compact and the kernel is bounded and continuous. The maximum
is positive by testing equal masses on two distinct points.

Let `H_r` be the continuous strictly increasing CDF of `mu_r`, and let `Q_eta`
be a nondecreasing quantile function of `eta`. Set `T=Q_eta o H_r`. Then
`T#mu_r=eta`. Values at exceptional quantiles can be chosen in the closed
support of `eta`, so `T#mu_s` is also supported on `K`. Alternatively, beta
measures are mutually absolutely continuous on `(0,1)`, so the full-measure
support statement for one beta measure holds for all the others.

Writing `E_t(K)` for the maximum energy,

\[
 \frac{C_s(K)}{C_s(I)}
 \ge F_s(T)\ge F_r(T)
 =\frac{C_r(K)}{C_r(I)}.
\]

All factors are positive. Rearrangement is exactly the requested inequality.
Scaling changes `[0,1]` to `[-1,1]` without changing the ratio. This argument
works directly for every compact `K`; no finite-set limiting argument is
needed.

## 9. Equality classification

Equality in the power-mean step with `r<s` forces `A_s` to be constant almost
surely. (Apply strict Jensen to `A_s^r` and the power `s/r>1`.) The `P_s`
density is strictly positive on the open triangle `0<x<y<1`. Therefore
`D_T(x,y)` is the same constant for almost every ordered pair, which by Fubini
implies `T(x)=a+cx` for almost every `x`. Its monotone representative agrees
with this affine function throughout the interior. Conversely, affine maps
give equality in the transport inequality.

If equality holds in the compact-set inequality, the chain in Section 8 has
equality throughout. Thus its chosen `r`-equilibrium measure is the affine
image of `mu_r`, with support a nondegenerate interval `J=[a,a+c]` contained
in `K`. Its potential is constant, equal to its energy, on `J` by Section 7
and affine covariance. If `K` contained `z` outside `J`, then its potential
at `z` would be strictly larger than at the closest endpoint of `J`, since
every distance to points of `J` is strictly larger. Varying the equilibrium
measure toward `delta_z` would increase its energy, a contradiction. Hence
`K=J`. Every nondegenerate closed interval gives equality by scaling.

This proves the equality classification included in the final manuscript.

## 10. Adversarial checks and scope

- A tempting monotonicity claim for the unnormalized energy gain is false;
  this proof uses normalized power means throughout.
- Fixed logit length was not shown to give ordered slope laws. The positive
  exponential mixture, ordered random rates, and Poisson thinning replace
  that unproved assertion.
- The proof does not establish monotonicity of the capacity ratio under
  arbitrary set inclusion, even when the convex hull is fixed. That stronger
  claim is unnecessary here and should not be included as a theorem.
- Boundary atoms, infinitely many partition cells, singular quantile maps,
  and exchange of sums/integrals have been addressed explicitly above.
- The interval equilibrium is derived in Section 7 rather than used as an
  unproved input; the normalization argument needs only its defining integral.
- Equality is addressed in Section 9. The positive density of the entire pair
  law, not just its mean, is essential for the affine conclusion.

## 11. Independent numerical checks

The saved `reproducibility/audit_poisson.py` performs deterministic, high-precision checks
on finite sets and their quantile transports, plus checks of the mixing
normalization. Its results are supporting numerical evidence only.
