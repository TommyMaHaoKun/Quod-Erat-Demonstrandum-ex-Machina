import MathLean.ArkonSeries
import MathLean.ArkonRecurrence

namespace MathLean.Arkon
open PowerSeries

theorem fixed_unique (V : PowerSeries ℚ) (hV : step V = V) : V = branch := by
  have h : ∀ n, Agree n V branch := by
    intro n
    induction n with
    | zero => intro k hk; omega
    | succ n ih =>
        simpa only [hV, branch_fixed] using agree_step ih
  exact PowerSeries.ext fun n => h (n+1) n (by omega)

theorem parametrized_unique (V : PowerSeries ℚ)
    (hV : equation X (1+X^2*V) = 0) : 1+X^2*V = series := by
  have h : X^3 * (step V-V) = (X : PowerSeries ℚ)^3 * 0 := by
    calc
      X^3 * (step V-V) = equation X (1+X^2*V) := by
        unfold equation step
        ring
      _ = X^3 * 0 := by rw [hV, mul_zero]
  have he : step V = V := sub_eq_zero.mp (X_pow_mul_cancel h)
  rw [fixed_unique V he]
  rfl

/-- A is B/X, where B is the inverse of z/(1+z^2 C(z)).
T is the Catalan series evaluated at B=XA. The two polynomial
identities are a division-free specification at the origin. -/
def InverseSpec (A T : PowerSeries ℚ) : Prop :=
  A = 1 + (X*A)^2*T ∧ T = 1 + (X*A)*T^2

theorem inverseSpec_equation {A T : PowerSeries ℚ}
    (h : InverseSpec A T) : equation X A = 0 := by
  rcases h with ⟨ha, ht⟩
  have h₁ : A-1-(X*A)^2*T = 0 := by linear_combination ha
  have h₂ : T-1-(X*A)*T^2 = 0 := by linear_combination ht
  calc
    equation X A =
        (A-1+(X*A)^2*T-X*A)*(A-1-(X*A)^2*T) -
        (X*A)^3*(T-1-(X*A)*T^2) := by unfold equation; ring
    _ = 0 := by rw [h₁, h₂]; ring

theorem inverseSpec_unique {A T : PowerSeries ℚ}
    (h : InverseSpec A T) : A = series := by
  have ha : A = 1+X^2*(A^2*T) := by
    calc
      A = 1+(X*A)^2*T := h.1
      _ = 1+X^2*(A^2*T) := by ring
  have he := inverseSpec_equation h
  rw [ha] at he
  exact ha.trans (parametrized_unique (A^2*T) he)

noncomputable def catalanAtInverse : PowerSeries ℚ := branch * series⁻¹^2

theorem series_inverseSpec : InverseSpec series catalanAtInverse := by
  have hc : constantCoeff ℚ series ≠ 0 := by
    rw [← coeff_zero_eq_constantCoeff]
    simp only [series_constant, ne_eq, one_ne_zero, not_false_eq_true]
  have hi : series * series⁻¹ = 1 := PowerSeries.mul_inv_cancel series hc
  have ht : series^2 * catalanAtInverse = branch := by
    calc
      series^2 * catalanAtInverse = branch * (series * series⁻¹)^2 := by
        unfold catalanAtInverse
        ring
      _ = branch := by rw [hi]; ring
  have ha : series = 1+(X*series)^2*catalanAtInverse := by
    calc
      series = 1+X^2*branch := rfl
      _ = 1+X^2*(series^2*catalanAtInverse) := by rw [ht]
      _ = 1+(X*series)^2*catalanAtInverse := by ring
  refine ⟨ha, ?_⟩
  have h₁ : series-1-(X*series)^2*catalanAtInverse = 0 := by
    linear_combination ha
  have he : (X*series)^3 *
      (catalanAtInverse-1-(X*series)*catalanAtInverse^2) = 0 := by
    have hid : equation X series =
        (series-1+(X*series)^2*catalanAtInverse-X*series)*
          (series-1-(X*series)^2*catalanAtInverse) -
        (X*series)^3*(catalanAtInverse-1-(X*series)*catalanAtInverse^2) := by
      unfold equation
      ring
    rw [series_equation, h₁, mul_zero, zero_sub] at hid
    exact neg_eq_zero.mp hid.symm
  have hs : series ≠ 0 := by
    intro hh
    exact hc (by rw [hh, map_zero])
  have hx : (X : PowerSeries ℚ) ≠ 0 := X_ne_zero
  have hh := (mul_eq_zero.mp he).resolve_left (pow_ne_zero 3 (mul_ne_zero hx hs))
  linear_combination hh

/-- Coefficients of the independently constructed original formal branch. -/
noncomputable def a (n : ℕ) : ℚ := coeff ℚ n series

/-- Mathar's proposed fifth-order recurrence, on its full original domain. -/
theorem a006343_recurrence (m : ℕ) (hm : 5 ≤ m) :
    -((m : ℚ)+3)*((m : ℚ)-1)*a m +
    (11*(m : ℚ)^2-2*m-45)*a (m-1) -
    (37*(m : ℚ)+29)*((m : ℚ)-3)*a (m-2) +
    (29*(m : ℚ)^2-125*m+78)*a (m-3) +
    (61*(m : ℚ)-106)*((m : ℚ)-3)*a (m-4) -
    155*((m : ℚ)-3)*((m : ℚ)-4)*a (m-5) = 0 := by
  obtain ⟨n, rfl⟩ := Nat.exists_eq_add_of_le hm
  have h := recurrence series series_equation series_regular n
  simp only [a, Nat.add_comm 5 n,
    show n+5-1 = n+4 by omega, show n+5-2 = n+3 by omega,
    show n+5-3 = n+2 by omega, show n+5-4 = n+1 by omega,
    show n+5-5 = n by omega]
  push_cast
  linear_combination h

#print axioms series_inverseSpec
#print axioms inverseSpec_unique
#print axioms a006343_recurrence
end MathLean.Arkon
