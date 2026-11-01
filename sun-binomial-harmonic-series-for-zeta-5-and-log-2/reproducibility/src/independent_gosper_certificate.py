"""Verify a compact rational WZ certificate for Au, Example XV, c=0.

The reconstruction by a degree-two Gosper ansatz is not needed to run this
verification. The asserted identity is v(n,k) R(n,k+1)-R(n,k)=u(n,k)-1,
where u and v are the n- and k-shift ratios of Au's displayed F(n,k).
"""
import sympy as s

a,b,d,n,k,e=s.symbols('a b d n k e')
h=s.S.Half
P=(4*a*a*d+4*a*a*n-2*a*a-4*a*b*d-4*a*b*n+2*a*b
   +8*a*d*e+12*a*d*n-2*a*d+8*a*e*n-4*a*e+12*a*n*n-8*a*n+a
   -4*b*d*e-4*b*d*n+2*b*e+4*d*e*e+16*d*e*n-2*d*e+12*d*n*n-4*d*n
   +8*e*e*n-2*e*e+24*e*n*n-12*e*n+e+16*n**3-12*n*n+2*n)
Q=s.expand(P.subs({n:n+1,e:k-h},simultaneous=True)/4)
W=a+2*k+2*n+h

# R=(a-d+k) Q/[W(a-b-d-n-1/2)(d+n+1/2)(a+k+2n+3/2)].
# Clearing denominators turns the WZ equation into this polynomial identity.
A=k*(a+k+n+h)*(b+k+n+h)*(d+k+2*n+h)
B=(a-d+k)*(k+n+1)*(a-b+k+n+1)*(a+k+2*n+h+2)
den=W*(a-b-d-n-h)*(d+n+h)*(k+n+1)*(a-b+k+n+1)*(a+k+2*n+h+1)*(a+k+2*n+h+2)
un=(W+2)*(a+k+n+h)*(b+k+n+h)*(d+k+2*n+h)*(d+k+2*n+h+1)*(a-b+n+1)*(-n-1)
assert s.expand(A*Q.subs(k,k+1)-B*Q-un+den)==0
print('Exact polynomial WZ certificate: PASS')

# After setting the boundary k=e+1/2 and n -> n-1, the numerator is P/4.
assert s.expand(4*Q.subs({n:n-1,k:e+h},simultaneous=True)-P)==0
assert s.expand(P.subs({a:0,b:0,d:0,e:0})-2*n*(2*n-1)*(4*n-1))==0
print('Boundary numerator and constant specialization: PASS')
