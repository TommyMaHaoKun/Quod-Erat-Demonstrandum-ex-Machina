# Independent check of Au's auxiliary evaluation

The established auxiliary sum in Kam Cheong Au, *Wilf-Zeilberger seeds and non-trivial hypergeometric identities*, arXiv:2312.14051v4, Example XV (p. 26), is

\[
T=\sum_{n\ge1}\frac{(1)_n^4}{(1/2)_n^4}
 \frac{4n-1}{4n^5(2n-1)}=93\zeta(5)-7\pi^2\zeta(3).
\]

The sum used in the Question 6 proof is exactly one quarter of this sum, by the substitution n=k+1:

\[
\frac{(1)_{k+1}^4}{(1/2)_{k+1}^4}
\frac{4k+3}{4(k+1)^5(2k+1)}
=4\frac{(1)_k^4}{(1/2)_k^4}
\frac{4k+3}{(k+1)(2k+1)^5}.
\]

## Exact coefficient audit

Au derives T from equation (5.2) using the coefficient operator in his footnote 21,

\[
\mathcal L=-[a^2]+\tfrac12[ab]+[b^2]-\tfrac12[ad]+\tfrac12[ae].
\]

The variable c can be set to zero throughout this calculation. The script `src/independent_coefficients.py` independently differentiates Au's explicit A(k), B and D, using exact rational arithmetic in formal symbols for the Euler constant, log 2, zeta(2), zeta(3), and harmonic sums. It verifies these three identities:

\[
\mathcal L A(k)=\frac{96}{(2k+1)^5},\qquad
\mathcal L\{B-D\Gamma(a-d)\}=7\pi^2\zeta(3),\qquad
\mathcal L\left\{D\frac{\Gamma(n+a-d)}{n!}\right\}=0.
\]

For the first check, put q=2k+1 and let g_i be the logarithmic derivative of A(k) at the origin. The script obtains

\[
g_a=4(-H_{2k}+H_k+\log2)-8/q,\quad g_b=3/q,
\]
\[
g_d=-2H_k-4\log2+6/q,\quad
g_e=-4H_{2k}+2H_k-5/q.
\]

Thus -g_a+g_b-g_d+g_e=0, the quadratic-gradient contribution is 9/q^2, and the corresponding logarithmic-Hessian contribution is 3/q^2. Since A(k) at the origin equals 16/q^3, the result is 96/q^5.

For the second check let t=a-d. Au's gamma factors simplify to

\[
B-D\Gamma(t)=D_0\{Q\Gamma(-t)+2^{-t}\Gamma(t)\},\quad D=-2^{-t}D_0,
\]
\[
Q=\frac{\Gamma(t+e+1/2)\Gamma(t-b+1/2)}
 {\Gamma(e+1/2)\Gamma(1/2-b)}.
\]

The pole terms cancel. A third-order Taylor expansion of Q suffices to extract the second-order finite coefficient. The script retains all Euler-constant and log terms and checks that the stated operator leaves exactly 7 zeta(3), after dividing by D_0(0)=pi^2.

The regulating summand is D Gamma(n+t)/n!, because Gamma(1+t)(1+t)_n/[(n+t)n!] simplifies to that expression. This also confirms two typographical corrections to the regularization paragraph of the source: the convergent remainder is analytic for Re(t)<1 (locally), and the factor D must be retained in the displayed regularized summand.

The sum of 96/(2k+1)^5 is 93 zeta(5).

## Reconstruction of the omitted polynomial

The polynomial in Au's C(n), at c=0, has now been reconstructed independently. With the ordering P=P(a,b,d,e,n), it is

```
4*a^2*d + 4*a^2*n - 2*a^2 - 4*a*b*d - 4*a*b*n + 2*a*b
+ 8*a*d*e + 12*a*d*n - 2*a*d + 8*a*e*n - 4*a*e
+ 12*a*n^2 - 8*a*n + a - 4*b*d*e - 4*b*d*n + 2*b*e
+ 4*d*e^2 + 16*d*e*n - 2*d*e + 12*d*n^2 - 4*d*n
+ 8*e^2*n - 2*e^2 + 24*e*n^2 - 12*e*n + e
+ 16*n^3 - 12*n^2 + 2*n.
```

For Au's displayed F(n,k), specialized at c=0 at the level of shift ratios, define

\[
Q(n,k)=\tfrac14P(a,b,d,k-1/2,n+1),\quad W=a+2k+2n+1/2,
\]
\[
R(n,k)=\frac{(a-d+k)Q(n,k)}
 {W(a-b-d-n-1/2)(d+n+1/2)(a+k+2n+3/2)}.
\]

The exact WZ relation G(n,k)=F(n,k)R(n,k) follows by multiplying by common denominators and expanding a polynomial identity. The short script `src/independent_gosper_certificate.py` verifies this identity exactly; it requires neither a Gosper implementation nor any downloaded source file. Substituting the boundary n -> n-1, k=e+1/2 yields P above. The normalizing factor, after dividing F by c and taking c -> 0, is

\[
N_1=\frac{\Gamma(a-d+1)\Gamma(b+e+1)\Gamma(d+e+1)\Gamma(a-b+1)}
 {\Gamma(b+1/2)\Gamma(a-d+e+1/2)\Gamma(d+1/2)\Gamma(a-b+e+1/2)}.
\]

After division by N_1, the boundary value has exactly Au's C(n), with the displayed P. The factor N_1 follows from the standard second transformation of the very-well-poised 7F6 in equation (3.5), using initial parameters

\[
A=a+2e+3/2,\quad(C,D,E,F,G)=(e+1/2,a+e+1,b+e+1,1,d+e+1).
\]

For clarity, C(n) can be specified without Pochhammer symbols as -P/4 times the following gamma product:

\[
\frac{\Gamma(n)\Gamma(n+a+e)\Gamma(n+b+e)
 \Gamma(2n-1+d+e)\Gamma(n+a-b)}
 {\Gamma(n+d+1/2)\Gamma(n+e+1/2)
 \Gamma(n-a+b+d+1/2)\Gamma(n+a-b+e+1/2)\Gamma(2n+1+a+e)}
\]
\[
\times\frac{\Gamma(d+1/2)\Gamma(e+1/2)
 \Gamma(-a+b+d+1/2)\Gamma(a-b+e+1/2)}
 {\Gamma(b+e+1)\Gamma(d+e+1)\Gamma(a-b+1)}.
\]

Its constant term is

\[
C(n)|_0=-\frac{(1)_n^4}{(1/2)_n^4}\frac{4n-1}{4n^4}.
\]

The fourth assertion in `src/independent_coefficients.py` verifies

\[
\frac{\mathcal L C(n)}{C(n)|_0}=-\frac1{n(2n-1)},
\]

with all harmonic/polygamma symbols canceled exactly. Thus the coefficient calculation in Au's proof has been independently reproduced on both sides, with the omitted polynomial supplied. Summing gives T=93 zeta(5)-7 pi^2 zeta(3).

The analytic five-parameter transformation (5.2), including its limiting boundary term B, remains the cited established result. These checks independently verify its precise coefficient specialization; they are not a separate proof of that general transformation.

## Reproduction

Run `python src/independent_gosper_certificate.py` and `python src/independent_coefficients.py` with SymPy installed. Their scope is the exact WZ polynomial certificate and the four displayed coefficient identities.
