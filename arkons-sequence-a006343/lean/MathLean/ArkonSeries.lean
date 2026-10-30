import MathLean.ArkonDifferential

/-! A coefficientwise fixed point constructs the formal algebraic branch
independently of Mathar's fifth-order recurrence. -/
namespace MathLean.Arkon
open PowerSeries
open scoped BigOperators

def Agree (n : ℕ) (f g : PowerSeries ℚ) : Prop :=
  ∀ k < n, coeff ℚ k f = coeff ℚ k g

theorem agree_refl (n : ℕ) (f : PowerSeries ℚ) : Agree n f f := fun _ _ => rfl

theorem agree_mono {n m : ℕ} {f g : PowerSeries ℚ}
    (h : Agree m f g) (hn : n ≤ m) : Agree n f g :=
  fun k hk => h k (lt_of_lt_of_le hk hn)

theorem agree_trans {n : ℕ} {f g h : PowerSeries ℚ}
    (h₁ : Agree n f g) (h₂ : Agree n g h) : Agree n f h :=
  fun k hk => (h₁ k hk).trans (h₂ k hk)

theorem agree_add {n : ℕ} {f g f' g' : PowerSeries ℚ}
    (hf : Agree n f f') (hg : Agree n g g') : Agree n (f+g) (f'+g') := by
  intro k hk
  simp only [map_add, hf k hk, hg k hk]

theorem agree_mul {n : ℕ} {f g f' g' : PowerSeries ℚ}
    (hf : Agree n f f') (hg : Agree n g g') : Agree n (f*g) (f'*g') := by
  intro k hk
  simp only [coeff_mul]
  apply Finset.sum_congr rfl
  intro ij hij
  have he := Finset.mem_antidiagonal.mp hij
  rw [hf ij.1 (by omega), hg ij.2 (by omega)]

theorem agree_pow {n : ℕ} {f g : PowerSeries ℚ}
    (h : Agree n f g) (k : ℕ) : Agree n (f^k) (g^k) := by
  induction k with
  | zero => exact agree_refl _ _
  | succ k ih => simpa only [pow_succ] using agree_mul ih h

noncomputable def step (V : PowerSeries ℚ) : PowerSeries ℚ :=
  1 + X * (3*X*V + (1-X+3*X^3)*V^2 + X^5*V^3)

theorem agree_step {n : ℕ} {f g : PowerSeries ℚ}
    (h : Agree n f g) : Agree (n+1) (step f) (step g) := by
  have hp : Agree n
      (3*X*f + (1-X+3*X^3)*f^2 + X^5*f^3)
      (3*X*g + (1-X+3*X^3)*g^2 + X^5*g^3) :=
    agree_add (agree_add (agree_mul (agree_refl _ _) h)
      (agree_mul (agree_refl _ _) (agree_pow h 2)))
      (agree_mul (agree_refl _ _) (agree_pow h 3))
  intro k hk
  cases k with
  | zero => simp [step]
  | succ k =>
      simpa only [step, map_add, coeff_succ_X_mul] using
        (congrArg (fun z => coeff ℚ (k+1) (1 : PowerSeries ℚ) + z) (hp k (by omega)))

noncomputable def approx : ℕ → PowerSeries ℚ
  | 0 => 0
  | n+1 => step (approx n)

theorem approx_adjacent (n : ℕ) : Agree n (approx n) (approx (n+1)) := by
  induction n with
  | zero => intro k hk; omega
  | succ n ih => exact agree_step ih

theorem approx_stable {n m : ℕ} (h : n ≤ m) : Agree n (approx n) (approx m) := by
  induction m, h using Nat.le_induction with
  | base => exact agree_refl _ _
  | succ m hm ih => exact agree_trans ih (agree_mono (approx_adjacent m) hm)

noncomputable def branch : PowerSeries ℚ :=
  mk fun n => coeff ℚ n (approx (n+1))

theorem branch_agrees (n : ℕ) : Agree n branch (approx n) := by
  intro k hk
  simp only [branch, coeff_mk]
  exact approx_stable (by omega : k+1 ≤ n) k (by omega)

theorem branch_fixed : step branch = branch := by
  apply PowerSeries.ext
  intro n
  have h := agree_step (branch_agrees (n+1)) n (by omega)
  have hs := approx_stable (Nat.le_succ (n+1)) n (by omega)
  simpa only [approx, branch, coeff_mk] using h.trans hs.symm

/-- The formal branch A(0)=1, A'(0)=0 of the known Arkon algebraic equation. -/
noncomputable def series : PowerSeries ℚ := 1 + X^2 * branch

theorem series_equation : equation X series = 0 := by
  calc
    equation X series = X^3 * (step branch - branch) := by
      unfold equation series step
      ring
    _ = 0 := by rw [branch_fixed, sub_self, mul_zero]

theorem series_constant : coeff ℚ 0 series = 1 := by simp [series]

theorem series_linear : coeff ℚ 1 series = 0 := by
  simp [series, coeff_X_pow_mul']

theorem series_regular : fy X series ≠ 0 := by
  intro h
  have hc := congrArg (coeff ℚ 1) h
  have he : fy X series =
      X^3 * (C ℚ 3*series^2) - X * (C ℚ 2*series) + C ℚ 2*series + X - C ℚ 2 := by
    simp only [map_ofNat]
    unfold fy
    ring
  rw [he] at hc
  simp [coeff_X_pow_mul', coeff_C_mul, ← coeff_zero_eq_constantCoeff,
    series_constant, series_linear] at hc
  norm_num at hc

end MathLean.Arkon
