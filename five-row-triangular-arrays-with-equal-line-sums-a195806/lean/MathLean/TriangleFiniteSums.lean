import MathLean.TriangleChamberCount
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic.LinearCombination

namespace MathLean.Triangle
open scoped BigOperators
open Finset

def term (n h k : ℚ) : ℚ := (n+1-2*h-k)^2*(n+1-3*h-2*k)^2

theorem cast_chamberWeight (n h k : ℕ) (hc : 3*h+2*k≤n) :
    (chamberWeight n h k : ℚ) = term n h k := by
  unfold chamberWeight term
  rw [Nat.cast_mul, Nat.cast_pow, Nat.cast_pow,
    Nat.cast_sub (by omega : 2*h+k ≤ n+1), Nat.cast_sub (by omega : 3*h+2*k ≤ n+1)]
  push_cast
  ring

def fullSum (n : ℕ) : ℚ := ∑ h ∈ range (n+1), ∑ k ∈ range (n+1),
  if 3*h+2*k≤n then term n h k else 0
def axisH (n : ℕ) : ℚ := ∑ h ∈ range (n+1), if 3*h≤n then term n h 0 else 0
def axisK (n : ℕ) : ℚ := ∑ k ∈ range (n+1), if 2*k≤n then term n 0 k else 0

theorem weighted_term (n h k : ℕ) :
    (if 3*h+2*k≤n then (multiplicity h k : ℚ)*term n h k else 0) =
    12*(if 3*h+2*k≤n then term n h k else 0) -
    6*(if k=0 then (if 3*h≤n then term n h 0 else 0) else 0) -
    6*(if h=0 then (if 2*k≤n then term n 0 k else 0) else 0) +
    (if h=0 ∧ k=0 then ((n : ℚ)+1)^4 else 0) := by
  by_cases hh : h=0 <;> by_cases hk : k=0 <;>
    simp_all [multiplicity, term] <;> (try split_ifs) <;> ring

theorem weighted_decomposition (n : ℕ) :
    (chamberSum n : ℚ) = 12*fullSum n - 6*axisH n - 6*axisK n + ((n : ℚ)+1)^4 := by
  have hs : (chamberSum n : ℚ) =
      ∑ h ∈ range (n+1), ∑ k ∈ range (n+1),
      if 3*h+2*k≤n then (multiplicity h k : ℚ)*term n h k else 0 := by
    unfold chamberSum
    push_cast
    rw [← Fin.sum_univ_eq_sum_range]
    simp_rw [← Fin.sum_univ_eq_sum_range]
    apply sum_congr rfl
    intro h hh
    apply sum_congr rfl
    intro k hk
    by_cases hc : 3*h.val+2*k.val≤n
    · simp only [hc, ite_true, cast_chamberWeight n h k hc]
    · simp [hc]
  rw [hs]
  simp_rw [weighted_term, sum_add_distrib, sum_sub_distrib, ← mul_sum]
  simp [fullSum, axisH, axisK, sum_ite_irrel, ite_and]

theorem sum_cut (N M : ℕ) (hM : M≤N) (f : ℕ → ℚ) :
    (∑ i ∈ range N, if i<M then f i else 0) = ∑ i ∈ range M, f i := by
  rw [← sum_filter]
  congr 1
  ext i
  simp only [mem_filter, mem_range]
  omega

theorem row_sum (n h : ℕ) (hh : 3*h≤n) :
    (∑ k ∈ range (n+1), if 3*h+2*k≤n then term n h k else 0) =
      ∑ k ∈ range ((n-3*h)/2+1), term n h k := by
  have he : ∀ k, 3*h+2*k≤n ↔ k<(n-3*h)/2+1 := by intro k; omega
  simp_rw [he]
  exact sum_cut _ _ (by omega) _

theorem fullSum_rows (n : ℕ) : fullSum n =
    ∑ h ∈ range (n/3+1), ∑ k ∈ range ((n-3*h)/2+1), term n h k := by
  unfold fullSum
  have he : ∀ h, (∑ k ∈ range (n+1), if 3*h+2*k≤n then term n h k else 0) =
      if h<n/3+1 then ∑ k ∈ range ((n-3*h)/2+1), term n h k else 0 := by
    intro h
    by_cases hh : 3*h≤n
    · rw [if_pos (by omega), row_sum n h hh]
    · rw [if_neg (by omega)]
      apply sum_eq_zero
      intro k hk
      rw [if_neg (by omega)]
  simp_rw [he]
  exact sum_cut _ _ (by omega) _

theorem axisH_range (n : ℕ) : axisH n = ∑ h ∈ range (n/3+1), term n h 0 := by
  unfold axisH
  have he : ∀ h, 3*h≤n ↔ h<n/3+1 := by intro h; omega
  simp_rw [he]
  exact sum_cut _ _ (by omega) _

theorem axisK_range (n : ℕ) : axisK n = ∑ k ∈ range (n/2+1), term n 0 k := by
  unfold axisK
  have he : ∀ k, 2*k≤n ↔ k<n/2+1 := by intro k; omega
  simp_rw [he]
  exact sum_cut _ _ (by omega) _

theorem sum_even_odd (f : ℕ → ℚ) (m : ℕ) :
    (∑ h ∈ range (2*m), f h) =
      (∑ h ∈ range m, f (2*h)) + ∑ h ∈ range m, f (2*h+1) := by
  induction m with
  | zero => simp
  | succ m ih =>
      rw [show 2*(m+1)=2*m+1+1 by omega, sum_range_succ, sum_range_succ, ih]
      simp only [sum_range_succ]
      ring

theorem sum_even_odd_last (f : ℕ → ℚ) (m : ℕ) :
    (∑ h ∈ range (2*m+1), f h) =
      (∑ h ∈ range (m+1), f (2*h)) + ∑ h ∈ range m, f (2*h+1) := by
  rw [sum_range_succ, sum_even_odd, sum_range_succ]
  ring

end MathLean.Triangle
