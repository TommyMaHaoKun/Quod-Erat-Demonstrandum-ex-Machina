import MathLean.ArkonDifferential
import Mathlib.Tactic.LinearCombination

namespace MathLean.Arkon
open PowerSeries

noncomputable def theta (A : PowerSeries ℚ) : PowerSeries ℚ := X * D A

theorem coeff_theta (A : PowerSeries ℚ) (n : ℕ) :
    coeff ℚ n (theta A) = n * coeff ℚ n A := by
  cases n with
  | zero => simp [theta]
  | succ n => simp [theta, coeff_derivative, Nat.succ_eq_add_one, mul_comm]

noncomputable def weighted (A : PowerSeries ℚ) (a b c : ℚ) : PowerSeries ℚ :=
  C ℚ a * theta (theta A) + C ℚ b * theta A + C ℚ c * A

theorem coeff_weighted (A : PowerSeries ℚ) (a b c : ℚ) (n : ℕ) :
    coeff ℚ n (weighted A a b c) =
      (a * (n : ℚ)^2 + b*n + c) * coeff ℚ n A := by
  simp only [weighted, map_add, coeff_C_mul, coeff_theta]
  ring

noncomputable def recurrenceOperator (A : PowerSeries ℚ) : PowerSeries ℚ :=
  weighted A (-1) (-2) 3 +
  X^1 * weighted A 11 20 (-36) +
  X^2 * weighted A (-37) (-66) 103 +
  X^3 * weighted A 29 49 (-36) +
  X^4 * weighted A 61 199 138 +
  X^5 * weighted A (-155) (-465) (-310)

theorem operator_identity (A : PowerSeries ℚ) :
    recurrenceOperator A = p2 X * D (D A) + p1 X * D A + p0 X * A := by
  norm_num [recurrenceOperator, weighted, theta, p2, p1, p0,
    Derivation.leibniz, smul_eq_mul, map_ofNat]
  ring

theorem recurrence (A : PowerSeries ℚ)
    (hA : equation X A = 0) (hreg : fy X A ≠ 0) (n : ℕ) :
    -((n : ℚ)+8)*((n : ℚ)+4)*coeff ℚ (n+5) A +
    (11*((n : ℚ)+5)^2-2*((n : ℚ)+5)-45)*coeff ℚ (n+4) A -
    (37*((n : ℚ)+5)+29)*((n : ℚ)+2)*coeff ℚ (n+3) A +
    (29*((n : ℚ)+5)^2-125*((n : ℚ)+5)+78)*coeff ℚ (n+2) A +
    (61*((n : ℚ)+5)-106)*((n : ℚ)+2)*coeff ℚ (n+1) A -
    155*((n : ℚ)+2)*((n : ℚ)+1)*coeff ℚ n A = 0 := by
  have h := congrArg (coeff ℚ (n+5)) (differential_equation A hA hreg)
  rw [← operator_identity] at h
  have h1 : n+5 = (n+4)+1 := by omega
  have h2 : n+5 = (n+3)+2 := by omega
  have h3 : n+5 = (n+2)+3 := by omega
  have h4 : n+5 = (n+1)+4 := by omega
  simp only [recurrenceOperator, map_add] at h
  rw [show coeff ℚ (n+5) (X^1 * weighted A 11 20 (-36)) =
      coeff ℚ (n+4) (weighted A 11 20 (-36)) by rw [h1, coeff_X_pow_mul],
    show coeff ℚ (n+5) (X^2 * weighted A (-37) (-66) 103) =
      coeff ℚ (n+3) (weighted A (-37) (-66) 103) by rw [h2, coeff_X_pow_mul],
    show coeff ℚ (n+5) (X^3 * weighted A 29 49 (-36)) =
      coeff ℚ (n+2) (weighted A 29 49 (-36)) by rw [h3, coeff_X_pow_mul],
    show coeff ℚ (n+5) (X^4 * weighted A 61 199 138) =
      coeff ℚ (n+1) (weighted A 61 199 138) by rw [h4, coeff_X_pow_mul],
    coeff_X_pow_mul] at h
  simp only [coeff_weighted, Nat.cast_add, Nat.cast_ofNat] at h
  have hz : coeff ℚ (n+5) (forcing X : PowerSeries ℚ) = 0 := by
    have he : (forcing X : PowerSeries ℚ) =
        C ℚ 3 - C ℚ 36 * X + C ℚ 98 * X^2 := by norm_num [forcing, map_ofNat]
    rw [he]
    simp [coeff_C_mul, coeff_X, coeff_X_pow, show n+5 ≠ 0 by omega,
      show n+5 ≠ 1 by omega, show n+5 ≠ 2 by omega]
  rw [hz] at h
  linear_combination h

end MathLean.Arkon
