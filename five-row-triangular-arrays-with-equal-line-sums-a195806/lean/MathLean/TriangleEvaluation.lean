import MathLean.TriangleFiniteSums
import MathLean.TriangleRowPolynomials

namespace MathLean.Triangle
open scoped BigOperators
open Finset

theorem row_closed (n h K : ℕ) :
    (∑ k ∈ range (K+1), term n h k) =
      quarticClosed ((n : ℚ)+1-2*h) ((n : ℚ)+1-3*h) 1 2 K := by
  simpa only [term, one_mul] using
    quartic_sum ((n : ℚ)+1-2*h) ((n : ℚ)+1-3*h) 1 2 K

theorem even_row (m v : ℕ) (r : Fin 6) (hv : v≤m) :
    (∑ k ∈ range ((6*m+r.val-3*(2*(m-v)))/2+1), term (6*m+r.val : ℕ) (2*(m-v) : ℕ) k) =
      quarticClosed (2*(m : ℚ)+4*v+evenA r) (6*(v : ℚ)+evenB r) 1 2 (3*(v : ℚ)+evenD r) := by
  have hh : (6*m+r.val-3*(2*(m-v)))/2 = 3*v+evenD r := by
    fin_cases r <;> dsimp [evenD] <;> omega
  rw [hh, row_closed]
  simp only [Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat, Nat.cast_sub hv]
  congr 1 <;> fin_cases r <;> norm_num [evenA, evenB, evenD] <;> ring

theorem odd_small_row (m v : ℕ) (r : Fin 6) (hr : r.val<3) (hv : v<m) :
    (∑ k ∈ range ((6*m+r.val-3*(2*(m-1-v)+1))/2+1), term (6*m+r.val : ℕ) (2*(m-1-v)+1 : ℕ) k) =
      quarticClosed (2*(m : ℚ)+4*v+oddA r) (6*(v : ℚ)+oddB r) 1 2 (3*(v : ℚ)+oddD r) := by
  have hh : (6*m+r.val-3*(2*(m-1-v)+1))/2 = 3*v+oddD r := by
    fin_cases r <;> dsimp [oddD] at * <;> omega
  rw [hh, row_closed]
  have hv' : v+1≤m := by omega
  rw [show m-1-v=m-(v+1) by omega]
  simp only [Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat, Nat.cast_sub hv']
  fin_cases r <;> norm_num [oddA, oddB, oddD] at hr ⊢ <;> congr 1 <;> ring

theorem odd_large_row (m v : ℕ) (r : Fin 6) (hr : 3≤r.val) (hv : v≤m) :
    (∑ k ∈ range ((6*m+r.val-3*(2*(m-v)+1))/2+1), term (6*m+r.val : ℕ) (2*(m-v)+1 : ℕ) k) =
      quarticClosed (2*(m : ℚ)+4*v+oddA r) (6*(v : ℚ)+oddB r) 1 2 (3*(v : ℚ)+oddD r) := by
  have hh : (6*m+r.val-3*(2*(m-v)+1))/2 = 3*v+oddD r := by
    fin_cases r <;> dsimp [oddD] at * <;> omega
  rw [hh, row_closed]
  simp only [Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat, Nat.cast_sub hv]
  fin_cases r <;> norm_num [oddA, oddB, oddD] at hr ⊢ <;> congr 1 <;> ring

theorem even_rows (m : ℕ) (r : Fin 6) :
    (∑ h ∈ range (m+1), ∑ k ∈ range ((6*m+r.val-3*(2*h))/2+1), term (6*m+r.val : ℕ) (2*h : ℕ) k) =
      evenPolynomial r m ((m : ℚ)+1) := by
  rw [← sum_range_reflect (fun h => ∑ k ∈ range ((6*m+r.val-3*(2*h))/2+1),
    term (6*m+r.val : ℕ) (2*h : ℕ) k) (m+1)]
  simp only [Nat.add_sub_cancel]
  have hs := even_row_sum r (m : ℚ) (m+1)
  push_cast at hs
  rw [← hs]
  apply sum_congr rfl
  intro v hv
  exact even_row m v r (by have := mem_range.mp hv; omega)

theorem odd_rows_small (m : ℕ) (r : Fin 6) (hr : r.val<3) :
    (∑ h ∈ range m, ∑ k ∈ range ((6*m+r.val-3*(2*h+1))/2+1), term (6*m+r.val : ℕ) (2*h+1 : ℕ) k) =
      oddPolynomial r m m := by
  rw [← sum_range_reflect (fun h => ∑ k ∈ range ((6*m+r.val-3*(2*h+1))/2+1),
    term (6*m+r.val : ℕ) (2*h+1 : ℕ) k) m, ← odd_row_sum r (m : ℚ) m]
  apply sum_congr rfl
  intro v hv
  exact odd_small_row m v r hr (mem_range.mp hv)

theorem odd_rows_large (m : ℕ) (r : Fin 6) (hr : 3≤r.val) :
    (∑ h ∈ range (m+1), ∑ k ∈ range ((6*m+r.val-3*(2*h+1))/2+1), term (6*m+r.val : ℕ) (2*h+1 : ℕ) k) =
      oddPolynomial r m ((m : ℚ)+1) := by
  rw [← sum_range_reflect (fun h => ∑ k ∈ range ((6*m+r.val-3*(2*h+1))/2+1),
    term (6*m+r.val : ℕ) (2*h+1 : ℕ) k) (m+1)]
  simp only [Nat.add_sub_cancel]
  have hs := odd_row_sum r (m : ℚ) (m+1)
  push_cast at hs
  rw [← hs]
  apply sum_congr rfl
  intro v hv
  exact odd_large_row m v r hr (by have := mem_range.mp hv; omega)

theorem fullSum_six (m : ℕ) (r : Fin 6) : fullSum (6*m+r.val) =
    evenPolynomial r m ((m : ℚ)+1) + oddPolynomial r m (if r.val<3 then (m : ℚ) else (m : ℚ)+1) := by
  rw [fullSum_rows]
  by_cases hr : r.val<3
  · rw [if_pos hr, show (6*m+r.val)/3+1=2*m+1 by omega,
      sum_even_odd_last, even_rows, odd_rows_small m r hr]
  · rw [if_neg hr, show (6*m+r.val)/3+1=2*(m+1) by have := r.isLt; omega,
      sum_even_odd, even_rows, odd_rows_large m r (by omega)]

end MathLean.Triangle
