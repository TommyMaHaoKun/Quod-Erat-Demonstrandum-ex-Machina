"""Exact scalar certificate for the edge bridge 250 <= n <= 1600.

This checks ten endpoint cases, not numerical polynomial roots. All
functions are bounded by rational series with explicit remainders.
"""
from fractions import Fraction as F
from math import factorial


def exp_lower(x, terms=120):
    assert x >= 0
    return sum((x**j/factorial(j) for j in range(terms+1)), F(0))


def log_bounds(x, terms=40):
    assert x >= 1
    power = 0
    while x >= 2:
        x /= 2
        power += 1
    def unit(y):
        z = (y-1)/(y+1)
        low = 2*sum((z**(2*j+1)/(2*j+1) for j in range(terms)), F(0))
        high = low+2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
        return low,high
    low,high = unit(x)
    low2,high2 = unit(F(2))
    return low+power*low2,high+power*high2


eps = F(1,10**6)
eta_k = F(36,1000)/(1-F(36,1000))
eta_h = F(15,1000)/(1-F(15,1000))
assert (1+eta_k)*(1+eta_h)-1 < F(54,1000)
assert F(54,1000)+eps < F(1,15)
p,q = F(11,20),F(1,100)
assert (p+q)/(1-q) < F(57,100)
assert (p+q)/(1-q)**2 < F(58,100)
assert F(58,100) < 2*F(43,100)
assert exp_lower(F(40)) > 1/eps
assert log_bounds(F(4))[0] > 1
assert F(48)*F(22,7)**2/(121*6) < 1

for ell in range(1,11):
    n = max(250,16*(ell-1)**2+1)
    assert n <= 1600
    eleft = 1/exp_lower(F(n,ell*ell))
    eright = 1/exp_lower(F(n,(ell+1)**2))
    assert 4*n*eleft < F(36,1000), ell
    assert 2*(ell+4)*eright < F(15,1000), ell
    assert 16*eleft < F(6,10000), ell
    central_error = 2*(n+1)/exp_lower(F(n-ell,ell+1))
    assert central_error < eps, ell

    rho = F(ell+1,ell)
    log_rho_low,log_rho_high = log_bounds(rho)
    log_D_upper = log_bounds(F(2*(ell+4)))[1]
    u_lower = n*log_rho_low-log_D_upper
    assert u_lower > 40, ell
    assert u_lower > F(11*n,12*(ell+1)), ell
    assert u_lower > F(n-ell+3,ell+1), ell
    # Each inequality is affine increasing in n at fixed ell.
    assert log_rho_low > F(11,12*(ell+1))
    assert log_rho_low > F(1,ell+1)

    # Bonferroni for A(n,m), 1<=m<=ell+2.
    assert (n+1)/exp_lower(F(n,ell+2)) < eps, ell
    assert F(6,11)*(1+eps)/(1-eps) < p
    assert p*eleft < q, ell
    right = F(2*(ell+4))*(F(n,ell)+4)/((n-ell)*(1-eps))*eright
    assert right < q, ell

    # Lower phase endpoint from the trapezoid bound on log rho.
    assert F(n,2*(ell+1)) > 21, ell
    assert F((ell+1)**2,n) < F(1,6), ell
    print("PASS: ell =",ell,"at n_min =",n)

print("PASS: all finite-edge signs, disjointness constants, and phase-index bounds")
