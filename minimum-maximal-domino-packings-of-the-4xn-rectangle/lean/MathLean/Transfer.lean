import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring

/-! All-length propagation of a finite transfer certificate. -/
namespace MathLean.Transfer

variable {V : Type*} [AddCommGroup V] [Module ℤ V]

def orbit (T : V →ₗ[ℤ] V) (v : V) : ℕ → V
  | 0 => v
  | n+1 => T (orbit T v n)

/-- A vector relation at lengths 17, 20, 23, 26 propagates to every
later length. Scalar agreement at those lengths would not suffice. -/
theorem propagate_domino_certificate (T : V →ₗ[ℤ] V) (v : V)
    (h : orbit T v 26 - (3:ℤ) • orbit T v 23 + (3:ℤ) • orbit T v 20 -
      orbit T v 17 = 0) (n : ℕ) :
    orbit T v (n+26) - (3:ℤ) • orbit T v (n+23) + (3:ℤ) • orbit T v (n+20) -
      orbit T v (n+17) = 0 := by
  induction n with
  | zero => simpa using h
  | succ n ih =>
    have hm := congrArg T ih
    simpa only [map_sub, map_add, map_zsmul, map_zero, Nat.succ_add, orbit] using hm

/-- Apply an accepting-state linear functional after propagating the
vector certificate. -/
theorem scalar_domino_recurrence (T : V →ₗ[ℤ] V) (v : V) (accept : V →ₗ[ℤ] ℤ)
    (h : orbit T v 26 - (3:ℤ) • orbit T v 23 + (3:ℤ) • orbit T v 20 -
      orbit T v 17 = 0) (n : ℕ) :
    accept (orbit T v (n+26)) =
      3*accept (orbit T v (n+23)) - 3*accept (orbit T v (n+20)) +
      accept (orbit T v (n+17)) := by
  have hh := congrArg accept (propagate_domino_certificate T v h n)
  simp only [map_sub, map_add, map_zsmul, map_zero, zsmul_eq_mul] at hh
  linear_combination hh

end MathLean.Transfer
