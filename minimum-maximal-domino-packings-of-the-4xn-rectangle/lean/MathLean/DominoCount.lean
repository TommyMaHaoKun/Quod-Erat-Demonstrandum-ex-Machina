import MathLean.DominoCountCertificate

namespace MathLean.DominoCount
open MathLean.Transfer
open scoped BigOperators
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem orbit_table (n : Fin 27) : orbit T initial n.val = table n := by
  induction n using Fin.induction with
  | zero => exact initial_checked.symm
  | succ n ih =>
    change orbit T initial n.val = table n.castSucc at ih
    change T (orbit T initial n.val) = table n.succ
    rw [ih]
    exact steps_checked n

theorem vector_certificate :
    orbit T initial 26 - (3:ℤ) • orbit T initial 23 + (3:ℤ) • orbit T initial 20 -
      orbit T initial 17 = 0 := by
  have h26 : orbit T initial 26 = table 26 := orbit_table (26 : Fin 27)
  have h23 : orbit T initial 23 = table 23 := orbit_table (23 : Fin 27)
  have h20 : orbit T initial 20 = table 20 := orbit_table (20 : Fin 27)
  have h17 : orbit T initial 17 = table 17 := orbit_table (17 : Fin 27)
  rw [h26,h23,h20,h17]
  funext i
  exact vector_checked i

def finals : Finset (Fin 114) := {0,1,2,3,5,50,51,52,53,54,55,56,57,86,87,88,89,90,91,92,93,110}

def accept : Vec →ₗ[ℤ] ℤ where
  toFun := fun v => ∑ i ∈ finals, v i
  map_add' := by intro x y; simp [Finset.sum_add_distrib]
  map_smul' := by intro c x; simp [Finset.mul_sum]

def count (n : ℕ) : ℤ := accept (orbit T initial n)

theorem recurrence (n : ℕ) :
    count (n+26) = 3*count (n+23)-3*count (n+20)+count (n+17) :=
  scalar_domino_recurrence T initial accept vector_certificate n

def initialCounts : Fin 17 → ℤ := ![1,1,6,7,100,51,10,663,124,8,1892,178,8,3652,224,8,5796]

def formula (n : ℕ) : ℤ :=
  if h : n < 17 then initialCounts ⟨n,h⟩ else
    if n%3=0 then 8 else
      if n%3=1 then 226*((n/3 : ℕ) : ℤ)^2+106*((n/3 : ℕ) : ℤ)-392 else 50*((n/3 : ℕ) : ℤ)+24

theorem initial_counts_checked : ∀ n : Fin 26, accept (table n.castSucc) = formula n := by decide +kernel

theorem formula_recurrence (n : ℕ) :
    formula (n+26) = 3*formula (n+23)-3*formula (n+20)+formula (n+17) := by
  have h26 : ¬ n+26 < 17 := by omega
  have h23 : ¬ n+23 < 17 := by omega
  have h20 : ¬ n+20 < 17 := by omega
  have h17 : ¬ n+17 < 17 := by omega
  have d26 : (n+26)/3 = (n+17)/3+3 := by omega
  have d23 : (n+23)/3 = (n+17)/3+2 := by omega
  have d20 : (n+20)/3 = (n+17)/3+1 := by omega
  have m26 : (n+26)%3 = (n+17)%3 := by omega
  have m23 : (n+23)%3 = (n+17)%3 := by omega
  have m20 : (n+20)%3 = (n+17)%3 := by omega
  simp only [formula, dif_neg h26, dif_neg h23, dif_neg h20, dif_neg h17,
    d26, d23, d20, m26, m23, m20]
  split_ifs <;> push_cast <;> ring

/-- Closed formula for every length of the explicit transfer graph. -/
theorem count_eq_formula (n : ℕ) : count n = formula n := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    by_cases hn : n < 26
    · unfold count
      rw [orbit_table (⟨n,by omega⟩ : Fin 27)]
      exact initial_counts_checked ⟨n,hn⟩
    · have h := recurrence (n-26)
      have hf := formula_recurrence (n-26)
      have hn0 : n-26+26=n := by omega
      rw [hn0] at h hf
      rw [ih (n-26+23) (by omega), ih (n-26+20) (by omega), ih (n-26+17) (by omega)] at h
      exact h.trans hf.symm

#print axioms count_eq_formula
end MathLean.DominoCount
