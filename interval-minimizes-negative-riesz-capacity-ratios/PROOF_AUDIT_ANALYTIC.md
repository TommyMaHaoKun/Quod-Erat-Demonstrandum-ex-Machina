# Independent analytic audit of the Poisson-mixture proof

Auditor: GPT-6 Astra, independent analytic subagent.

Date: 2026-11-02.

Scope: mathematical audit of the proof, including atomic and singular measures, arbitrary compact sets, interval normalization, and the infinite random partitions. This is an independent AI audit, not human peer review or proof-assistant verification.

## Verdict

The Poisson-mixture argument proves the full inequality for every compact subset of the real line containing at least two points and every `0 < r < s < 1`. No smoothness, finiteness, positive-length, or finite-component restriction on the compact set is needed. The steps below give a self-contained check of the analytic bridges. An optional equality argument also gives equality exactly for nondegenerate compact intervals.

## 1. Interval equilibrium and its normalization

Work first on `[0,1]`. Fix `0 < t < 1`, put `a = (1-t)/2`, and let beta_t have density

    b_t(x) = [x(1-x)]^(a-1) / B(a,a),   0 < x < 1.

Its potential is

    U_t(x) = integral_0^1 |x-y|^t b_t(y) dy.

For `0 < x < 1`, differentiation under the integral gives

    U_t'(x) = t/B(a,a) [L(x)-L(1-x)],

where

    L(x) = integral_0^x (x-y)^(t-1) y^(a-1)(1-y)^(a-1) dy
         = x^(a+t-1) B(a,t) 2F1(1-a,a;a+t;x)
         = B(a,t) [x(1-x)]^(-a).

The last equality uses `a+t = 1-a`, `a+t-1 = -a`, and the binomial identity `2F1(c,a;c;x) = (1-x)^(-a)`. Thus the two derivative terms agree. Differentiation is justified locally because the differentiated singularity has exponent `t-1 > -1`; the fixed endpoint singularities are integrable because `a>0`. Continuity supplies the constant-potential identity at the endpoints as well.

Evaluating at zero yields

    A_t = U_t(0) = B(a+t,a)/B(a,a)
        = Gamma((1+t)/2) Gamma(1-t)/Gamma((1-t)/2)
        = 2^(-t) Gamma((1+t)/2) Gamma(1-t/2)/sqrt(pi).

The last step is the gamma duplication formula.

To check maximality, use the elementary Fourier representation

    |z|^t = c_t integral_0^infinity (1-cos(xi z)) xi^(-1-t) dxi,

with `c_t>0`. For every compactly supported finite signed measure nu of total mass zero,

    integral integral |x-y|^t dnu(x)dnu(y)
      = -c_t integral_0^infinity |nuhat(xi)|^2 xi^(-1-t) dxi <= 0.

Interchanging integrals is valid: applying the nonnegative representation to the total-variation product bounds the absolute integral by a constant times the bounded support diameter raised to `t`. Alternatively, the final Fourier integral is integrable at zero since `nuhat(xi)=O(xi)`, and at infinity since `t>0`.

For any probability mu on `[0,1]`, set `nu=mu-beta_t`. Expanding its energy and using the constant potential gives

    E_t(mu) = A_t + E_t(nu) <= A_t.

Consequently beta_t is an equilibrium measure, and `C_t([0,1])=A_t^(1/t)`. Scaling by two gives exactly the benchmark in the question for `[-1,1]`.

## 2. The interval law attached to a monotone map

Let T be any bounded nondecreasing function on `(0,1)`, and define

    N_t(T)^t = integral integral |T(x)-T(y)|^t d beta_t(x) d beta_t(y).

Let `P_t` be the probability law on ordered pairs `0<x<y<1` whose density is proportional to

    (y-x)^t b_t(x)b_t(y).

Write `D_T(x,y)=(T(y)-T(x))/(y-x)`. Direct cancellation gives the exact identity

    N_t(T)/N_t(id) = [ E_{P_t} D_T^t ]^(1/t).

The exponent on the normalizing factor is essential. There is no missing factor of two: the factor from ordering the symmetric pair appears in both numerator and denominator and cancels.

Set

    x(u) = (1+tanh u)/2,    y=x(u+z),    z>0,
    alpha = 1-t.

Since `x'(u)=(1/2)sech^2 u` and

    x(u+z)-x(u) = sinh(z)/(2 cosh(u)cosh(u+z)),

the law `P_t` has `(u,z)` density

    sinh(z)^(-alpha) [x(u+z)-x(u)] / J_alpha,

where

    J_alpha = integral_0^infinity z sinh(z)^(-alpha) dz.

The normalization follows from the exact identity

    integral_R [x(u+z)-x(u)] du = z.

For example, express the difference as `integral_0^z x'(u+v) dv` and apply Tonelli. The integral defining `J_alpha` is finite and positive for `0<alpha<1`.

## 3. Exact Poisson-mixture representation

For any `lambda>0`, take a stationary Poisson process of rate lambda on the u-axis, independently of a uniform point `W` in the original interval `(0,1)`. The cell containing `x^(-1)(W)` has endpoints `u,u+z` with density

    Q_lambda(du,dz)
      = lambda^2 exp(-lambda z) [x(u+z)-x(u)] du dz.

One direct verification conditions on `W=x(v)`: the left and right distances from v to the Poisson points are independent rate-lambda exponentials. Integrating v between the proposed endpoints gives the displayed factor `x(u+z)-x(u)`. Its integral is one because

    lambda^2 integral_0^infinity z exp(-lambda z) dz = 1.

Now use the positive binomial series

    sinh(z)^(-alpha)
      = 2^alpha sum_{n>=0} a_n(alpha) exp(-(2n+alpha)z),
    a_n(alpha) = (alpha)_n/n!.

Define

    lambda_n(alpha)=2n+alpha,
    S_alpha = sum_{n>=0} a_n(alpha)/lambda_n(alpha)^2,
    w_n(alpha)=a_n(alpha)/(lambda_n(alpha)^2 S_alpha).

Tonelli gives `J_alpha=2^alpha S_alpha`, and hence the exact mixture identity

    P_t = sum_{n>=0} w_n(1-t) Q_{lambda_n(1-t)}.

All weights are positive and sum to one. Finiteness also follows directly from `a_n(alpha)=O(n^(alpha-1))`; the summands in `S_alpha` are `O(n^(alpha-3))`.

## 4. Ordering the random rates

Suppose `0<r<s<1`, so `alpha_s=1-s < alpha_r=1-r`. The likelihood ratio is

    w_n(alpha_s)/w_n(alpha_r)
      = (S_alpha_r/S_alpha_s)
        [a_n(alpha_s)/a_n(alpha_r)]
        [(2n+alpha_r)/(2n+alpha_s)]^2.

Each n-dependent factor decreases with n. For the Pochhammer quotient, the ratio of successive terms is `(n+alpha_s)/(n+alpha_r)<1`; the second quotient is `1+(alpha_r-alpha_s)/(2n+alpha_s)` and also decreases.

Therefore the integer-valued variable with weights `w_n(alpha_s)` is stochastically smaller than the one with weights `w_n(alpha_r)`. To justify this without invoking a black box, put `q_n=w_n(alpha_s)/w_n(alpha_r)`. It is decreasing and has mean one under `w(alpha_r)`. Its covariance with every increasing upper-tail indicator is nonpositive, giving the claimed tail comparison.

An inverse-CDF coupling gives `N_s <= N_r` almost surely. Consequently

    Lambda_s=2N_s+alpha_s <= 2N_r+alpha_r=Lambda_r.

Conditionally on these rates, construct the rate-Lambda_s process by independent thinning of a rate-Lambda_r stationary Poisson process. The s-partition is then coarser than the r-partition. The uniform original-coordinate point W is independent of the rates and both point processes.

## 5. Singular T, countably infinite partitions, and Jensen

No absolute continuity of T is required. Changing T at its countably many discontinuities changes none of the beta integrals, so take a right-continuous representative. Endpoint values can be set equal to the corresponding one-sided limits. Let nu be its finite positive Lebesgue-Stieltjes measure on `(0,1)`, so that, at continuity endpoints,

    T(b)-T(a) = nu((a,b)).

Every Poisson boundary avoids the countably many atoms of nu almost surely. A countable union of the remaining singletons has nu-measure zero as well. Thus the original-coordinate cells partition `(0,1)` modulo a nu-null set and a Lebesgue-null set, simultaneously for both partitions.

Fix such a realization of the nested partitions. For a cell B define its slope to be `nu(B)/|B|`. Each coarse cell is bounded in logit coordinates and contains finitely many fine cells almost surely, because both rates are finite and strictly positive. If C is a coarse cell and its fine subcells are B_j, then

    nu(C)/|C| = sum_j (|B_j|/|C|) [nu(B_j)/|B_j|].

Concavity of `v -> v^r`, with `0<r<1`, therefore gives

    |C| [nu(C)/|C|]^r
      >= sum_j |B_j| [nu(B_j)/|B_j|]^r.

Sum this nonnegative inequality over the countably many coarse cells and average over the random partitions and rates. The result is

    E_{P_s} D_T^r >= E_{P_r} D_T^r.

There is no hidden integrability problem: for every fixed partition,

    integral_0^1 D_T(cell containing W) dW = nu((0,1)).

Thus the first moment is finite and all moments of orders in `(0,1)` are finite by Jensen. Atomic jumps and singular continuous parts of T are fully included.

Finally, ordinary power-mean monotonicity under the single probability law `P_s` gives

    [E_{P_s} D_T^s]^(1/s)
      >= [E_{P_s} D_T^r]^(1/r)
      >= [E_{P_r} D_T^r]^(1/r).

This proves the monotone-transport inequality

    N_s(T)/N_s(id) >= N_r(T)/N_r(id).

## 6. Transfer to an arbitrary compact K

For compact K, the probability measures on K form a weakly compact set, and the energy is continuous because `|x-y|^t` is continuous and bounded on `K x K`. Hence an r-equilibrium measure mu_r exists. Its energy is positive when K has two distinct points, as seen by assigning half the mass to each.

The beta_r distribution has a continuous strictly increasing distribution function F_beta_r. Let Q_mu_r be the generalized quantile function of mu_r, and take

    T = Q_mu_r composed with F_beta_r.

This bounded nondecreasing function pushes beta_r to mu_r. Its values lie in K for interior quantiles, because K is compact and supports mu_r. In particular its beta_s pushforward is a probability on K. Equivalently, beta_r and beta_s are mutually absolutely continuous with positive densities on `(0,1)`, so beta_r-null exceptions are harmless for beta_s too.

Therefore

    C_s(K) >= N_s(T)
           >= N_r(T) N_s(id)/N_r(id)
           = C_r(K) C_s([0,1])/C_r([0,1]).

Translation and scaling replace `[0,1]` by `[-1,1]` in the ratio. This covers every compact K in the question, including finite sets, Cantor sets, and compact sets with infinitely many components.

## 7. Optional equality statement

The final power-mean step is strict unless `D_T` is constant `P_s`-almost surely. The law `P_s` has strictly positive density on every ordered pair `0<x<y<1`. Thus equality forces `T(y)-T(x)=b(y-x)` for almost every pair, which by Fubini implies `T(x)=a+bx` almost everywhere. The nonzero energy forces `b>0`.

The r-equilibrium measure mu_r then has support exactly `J=[a,a+b]`, so `J` is contained in K. If K had a point outside J, its potential under mu_r would be strictly larger than the constant equilibrium potential on J: moving beyond an endpoint increases every distance to J. Assigning a small positive mass to that point would increase the r-energy, contradicting optimality. Hence K equals J. Conversely every nondegenerate compact interval has equality by scaling.

## 8. Shorter interval-equilibrium proof available for the manuscript

The manuscript can omit the Fourier and hypergeometric arguments in Section 1. Those arguments remain here as an independent cross-check. There is a shorter proof from the Poisson representation itself, and its dependency order is noncircular.

In Sections 2 and 3, define beta_t solely by its normalized beta density, and define `P_t` by normalizing `(y-x)^t b_t(x)b_t(y)`. Neither step assumes that beta_t is an equilibrium measure. The chord-slope identity and exact Poisson-mixture representation therefore hold before maximality is known.

For any bounded nondecreasing T with values in `[0,1]`, the fixed-partition identity from Section 5 and Jensen yield

    integral_0^1 D_T(cell containing W)^t dW
       <= [nu((0,1))]^t <= 1.

Averaging over the mixture gives `N_t(T)^t <= N_t(id)^t`. Every probability mu on `[0,1]` is the pushforward of beta_t by a monotone quantile transport. Hence beta_t maximizes the energy among all these probabilities.

Write `A_t=E_t(beta_t)` and `U_t(x)=integral |x-y|^t d beta_t(y)`. First variation against a point mass gives `U_t(x)<=A_t` for every x in `[0,1]`: indeed

    E_t((1-epsilon) beta_t + epsilon delta_x)
      = A_t + 2 epsilon [U_t(x)-A_t] + O(epsilon^2).

The potential is continuous, beta_t has full support `[0,1]`, and `integral U_t d beta_t=A_t`. These facts force `U_t` to be identically `A_t`. Evaluating at zero gives the same ordinary beta integral and gamma-duplication calculation in Section 1. This proof uses no negative-type theorem, uniqueness theorem, or differentiation of a singular integral.

The shorter argument also supplies exactly the constant-potential fact needed for the equality discussion in Section 7.

## Adversarial checks completed

- Recomputed both coordinate Jacobians and the ordered-pair normalization.
- Verified the Poisson cell law by independent exponential left/right distances.
- Verified the mixture weights include the essential `lambda_n^(-2)` factor.
- Checked the likelihood-ratio direction and the resulting thinning direction.
- Checked that Jensen has the required direction because `r<1`.
- Separated Jensen across two coupled laws from the power-mean step under one fixed law.
- Checked finite first moments despite potentially unbounded chord slopes.
- Included atomic, singular continuous, and discontinuous monotone transports.
- Checked compactness, positive capacity, quantile support, and both interval scalings.
- Verified the interval equilibrium density and the beta/gamma benchmark directly.
- Checked the shorter Poisson/Jensen proof of interval equilibrium and its noncircular dependency order.

No remaining mathematical gap was found in this argument. The coordinating agent subsequently completed manuscript editing, clean-source rebuilding, and visual checks of all seven PDF pages; see reproducibility/release_checks.json.
