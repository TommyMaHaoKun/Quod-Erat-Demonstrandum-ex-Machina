# Independent review of the Weibull counterexample

Author: GPT-6 Astra. Review date: 2026-11-04.

The proposed Weibull distribution gives a complete negative answer to the
mean-normalized assertion in Question 4. The proof below treats every positive
threshold, with no numerical optimization step. The source statement was
checked independently against Steinerberger, *A sharp estimate for probability
distributions*, arXiv:1801.00663v3, Section 1.3:
https://arxiv.org/html/1801.00663v3 . Its denominator includes the condition
X+Y >= 2z, which is automatic when min(X,Y) >= z.

## 1. Distribution and exact normalization

Take independent X,Y with survival function S(x)=exp(-x^(3/2)) for x>=0.
This is an absolutely continuous probability distribution with unbounded
support, density f(x)=(3/2)sqrt(x) exp(-x^(3/2)) for x>0, and finite positive
mean mu=Gamma(5/3). The mean follows by integrating S and substituting
t=x^(3/2).

Put

    I(z) = integral_0^z f(x) S(2z-x) dx,
    Q(z) = mu I(z)/(z S(z)^2).

The event in the numerator is the union of the two symmetric events in which
X<=z or Y<=z. Their overlap, under the additional sum condition, is a null
boundary point. Consequently its probability is 2I(z). Independence gives
P(min(X,Y)>=z)=S(z)^2. The questioned inequality is exactly Q(z)>=1.

Substituting x=z(1-u) gives

    Q(z) = (3/2) mu sqrt(z) integral_0^1 sqrt(1-u)
           * exp(-z^(3/2) phi(u)) du,
    phi(u)=(1-u)^(3/2)+(1+u)^(3/2)-2.

For 0<=u<1,

    phi''(u)=(3/4)[(1-u)^(-1/2)+(1+u)^(-1/2)] >= 3/2.

Since phi(0)=phi'(0)=0, integration gives phi(u)>=3u^2/4, including u=1 by
continuity. Also sqrt(1-u)<=1-u/2. Therefore, with t=(3/4)z^(3/2) and

    F(t)=integral_0^1 (1-u/2) exp(-tu^2) du,
    H(t)=t^(1/3)F(t),

we obtain

    Q(z) <= (3/2) mu (4/3)^(1/3) H(t).

Log-convexity of Gamma, at 5/3=(2/3)(3/2)+(1/3)2, gives mu^3<=pi/4.
Using pi<22/7, we have the uniform reduction

    Q(z)^3 < (99/28) H(t)^3.                         (1)

All factors are positive; the strict sign in (1) is justified by pi<22/7.

## 2. Location of the maximum of H

Let w(u)=1-u/2 and let E_t be expectation with density proportional to
w(u) exp(-tu^2) on [0,1]. Differentiating under the integral gives

    sign H'(t) = sign(1-3t E_t[u^2]).

After s=sqrt(t)u, the quantity t E_t[u^2] is the expectation of s^2 with
density proportional to

    k_t(s)=exp(-s^2)(1-s/(2sqrt(t))) 1_[0,sqrt(t)](s).

This expectation is strictly increasing in t. Indeed, for t2>t1, the ratio

    k_t2(s)/k_t1(s)
      = (1-s/(2sqrt(t2)))/(1-s/(2sqrt(t1)))

is strictly increasing on the common support, and the second density has a
positive extension beyond sqrt(t1). To verify the expectation comparison
directly, multiply its difference by both normalizing integrals. On the
common support, symmetrize the double integral over x<y: its integrand is

    (y^2-x^2)[k_t2(y)k_t1(x)-k_t2(x)k_t1(y)] > 0.

The extra region y>sqrt(t1), x<=sqrt(t1) also has positive integrand. Thus
no additional probability comparison theorem is required.

Set t0=41/20 and M2(t)=integral_0^1 u^2 w(u)exp(-tu^2)du. The exact checks
in Section 4 give

    F(t0)>482/1000,    M2(t0)<78/1000.

Hence

    F(t0)-3t0 M2(t0) > 23/10000 > 0.

The increasing-expectation result implies H'(t)>0 for every 0<t<=t0.
Moreover H tends to zero at both endpoints: use F<=3/4 at zero and
F<=sqrt(pi)/(2sqrt(t)) at infinity. Thus a global maximum is attained at an
interior stationary point t*>t0. The same expectation argument also shows
that this point is unique, although uniqueness is not needed below.

## 3. An upper bound at every stationary point

Write K(t)=integral_0^1 u exp(-tu^2)du=(1-exp(-t))/(2t). Integrating the
derivative of u w(u)exp(-tu^2) gives

    (1/2)exp(-t) = F(t)-(1/2)K(t)-2tM2(t).

At a stationary point, F(t)=3tM2(t), so

    F(t)=(3/4)[(2-1/t)exp(-t)+1/t].

Define

    G(t)=(3/4)t^(1/3)[(2-1/t)exp(-t)+1/t].

Then H(t*)=G(t*). Direct differentiation yields

    G'(t)=(3/4)t^(-5/3)
           *[-2/3+exp(-t)(-2t^2+5t/3+2/3)].

For t>=2, the quadratic in parentheses is at most -4 and decreases, so
G'(t)<0. Since t*>t0>2 and exp(-t0)<13/100,

    max H < (3/4)(41/20)^(1/3)
               *[(2-20/41)(13/100)+20/41].

Combining this with (1) proves, for every z>0,

    Q(z)^3 < 7381964831571/7530880000000 < 1.

Thus Q(z)<1 at every positive threshold. This is the strict opposite of the
proposed existential inequality for the stated admissible distribution.

## 4. Three short rational checks

Define

    c_k = 1/(2k+1)-1/(4k+4),
    L5 = sum_(k=0)^5 (-t0)^k c_k/k!,
    U6 = sum_(k=0)^6 (-t0)^k c_(k+1)/k!,
    E6 = sum_(k=0)^6 t0^k/k!.

The signed Taylor remainder for exp(-x), valid for every x>=0, gives
F(t0)>=L5 and M2(t0)<=U6. The positive Taylor series gives exp(t0)>E6.
The required finite arithmetic is

    L5 > 482/1000,   U6 < 78/1000,   E6 > 100/13.

The standard-library checker `src/verify_one_point_bound.py` verifies these
using exact fractions, checks a second pair of degree-15/16 truncations, and
recomputes the final displayed rational number. Its report is
`certificates/one_point_bound.json`. The computations certify these explicit
finite rational comparisons; Sections 1-3 supply the proof covering all z.

## Review outcome

The factor of two in the probability, the change of variables, the exponent
bound, the Gamma bound, the likelihood-ratio comparison, the stationary
identity, the monotonicity of G, and the rational arithmetic have each been
checked independently. No assumption of compact support, monotone density,
or a restricted threshold range was introduced. The counterexample resolves
the exact mean version asked in Question 4.
