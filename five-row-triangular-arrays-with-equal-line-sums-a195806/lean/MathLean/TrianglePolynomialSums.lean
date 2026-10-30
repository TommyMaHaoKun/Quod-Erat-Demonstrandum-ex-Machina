import MathLean.TriangleChamberCount
import Mathlib.Tactic.LinearCombination

namespace MathLean.Triangle
open scoped BigOperators
open Finset

def quarticClosed (A B u v K : ℚ) : ℚ :=
  A^2*B^2*(K+1) +
  (-2*A^2*B*v-2*A*B^2*u)*K*(K+1)/2 +
  (A^2*v^2+4*A*B*u*v+B^2*u^2)*K*(K+1)*(2*K+1)/6 +
  (-2*A*u*v^2-2*B*u^2*v)*K^2*(K+1)^2/4 +
  u^2*v^2*K*(K+1)*(2*K+1)*(3*K^2+3*K-1)/30

set_option maxHeartbeats 800000 in
theorem quartic_sum (A B u v : ℚ) (K : ℕ) :
    (∑ k ∈ range (K+1), (A-u*k)^2*(B-v*k)^2) = quarticClosed A B u v K := by
  induction K with
  | zero => norm_num [quarticClosed]
  | succ K ih =>
      rw [sum_range_succ, ih]
      push_cast
      unfold quarticClosed
      ring

end MathLean.Triangle
