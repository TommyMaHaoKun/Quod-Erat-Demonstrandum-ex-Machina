"""Exact integer arithmetic for the Eulerian triangle A and its matrix square B = A*A.

Conventions (matching the problem statement):
  A(0,0) = 1, A(n,k) = 0 outside 0 <= k <= n, and for n >= 1
  A(n,k) = (n-k+1) A(n-1,k-1) + k A(n-1,k).
  B(n,k) = sum_{j=k}^{n} A(n,j) A(j,k),   P_n(x) = sum_k B(n,k) x^k.
Polynomials are coefficient lists, lowest degree first.
"""
from fractions import Fraction


def eulerian_triangle(N):
    A = [[0] * (N + 1) for _ in range(N + 1)]
    A[0][0] = 1
    for n in range(1, N + 1):
        for k in range(1, n + 1):
            A[n][k] = (n - k + 1) * A[n - 1][k - 1] + k * A[n - 1][k]
    return A


def square_rows(A, N):
    """Rows of the ordinary matrix product B = A*A (not the Hadamard square)."""
    return [[sum(A[n][j] * A[j][k] for j in range(k, n + 1)) for k in range(n + 1)]
            for n in range(N + 1)]


def eval_poly(coeffs, q):
    """Exact value of sum coeffs[i] q^i for a rational q (Horner)."""
    q = Fraction(q)
    v = Fraction(0)
    for c in reversed(coeffs):
        v = v * q + c
    return v


def sign(v):
    return (v > 0) - (v < 0)
