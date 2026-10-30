import Mathlib.Data.Rat.Defs
import Mathlib.Data.Matrix.Notation
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Push
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

namespace MathLean.BinaryGramFormula
set_option maxHeartbeats 0
set_option maxRecDepth 100000

/-- Rational form of the six-term formula, avoiding negative natural exponents. -/
def rawFormula (n : ℕ) : ℚ :=
  4^n*(6*(n:ℚ)^2-219*n+820)/6144 - 2^n*(3*(n:ℚ)+32)/288
  - 113*(-8)^n/49152 + 16^n/512 - (-4)^n*(13*(n:ℚ)-164)/6144
  + 8^n*(288*(n:ℚ)-3473)/147456

def formula (n : ℕ) : ℚ := if n < 4 then 0 else rawFormula n

def Recurrence (a : ℕ → ℚ) : Prop := ∀ n, a (n+16) =
    (-67108864 : ℚ)*a (n+4) +
    (62914560 : ℚ)*a (n+5) +
    (7864320 : ℚ)*a (n+6) +
    (-22609920 : ℚ)*a (n+7) +
    (4349952 : ℚ)*a (n+8) +
    (1812480 : ℚ)*a (n+9) +
    (-624640 : ℚ)*a (n+10) +
    (-15360 : ℚ)*a (n+11) +
    (24288 : ℚ)*a (n+12) +
    (-2040 : ℚ)*a (n+13) +
    (-180 : ℚ)*a (n+14) +
    (30 : ℚ)*a (n+15)

theorem raw_recurrence : Recurrence rawFormula := by
  intro n
  simp only [rawFormula, pow_add]
  push_cast
  ring

theorem formula_recurrence : Recurrence formula := by
  intro n
  unfold formula
  simp only [if_neg (by omega : ¬ n+4<4),
    if_neg (by omega : ¬ n+5<4),
    if_neg (by omega : ¬ n+6<4),
    if_neg (by omega : ¬ n+7<4),
    if_neg (by omega : ¬ n+8<4),
    if_neg (by omega : ¬ n+9<4),
    if_neg (by omega : ¬ n+10<4),
    if_neg (by omega : ¬ n+11<4),
    if_neg (by omega : ¬ n+12<4),
    if_neg (by omega : ¬ n+13<4),
    if_neg (by omega : ¬ n+14<4),
    if_neg (by omega : ¬ n+15<4),
    if_neg (by omega : ¬ n+16<4)]
  exact raw_recurrence n

def initial : Fin 16 → ℚ := ![0,0,0,0,58,1629,28924,507052,8211776,133693904,2140571200,34361115072,549587348992,8798356254976,140744002571264,2252082614856704]

theorem formula_initial : ∀ n : Fin 16, formula n = initial n := by
  intro n
  fin_cases n <;> norm_num [formula, rawFormula, initial]

/-- The recurrence and these sixteen initial values uniquely force the
closed formula. This theorem does not assume that an arbitrary automaton
has that recurrence: the counting-side proof remains a distinct obligation. -/
theorem eq_formula (a : ℕ → ℚ) (hrec : Recurrence a)
    (hinit : ∀ n : Fin 16, a n = initial n) (n : ℕ) : a n = formula n := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    by_cases hn : n < 16
    · exact (hinit ⟨n,hn⟩).trans (formula_initial ⟨n,hn⟩).symm
    · have h := hrec (n-16)
      have hf := formula_recurrence (n-16)
      have hn0 : n-16+16=n := by omega
      rw [hn0] at h hf
      rw [ih (n-16+4) (by omega),
        ih (n-16+5) (by omega),
        ih (n-16+6) (by omega),
        ih (n-16+7) (by omega),
        ih (n-16+8) (by omega),
        ih (n-16+9) (by omega),
        ih (n-16+10) (by omega),
        ih (n-16+11) (by omega),
        ih (n-16+12) (by omega),
        ih (n-16+13) (by omega),
        ih (n-16+14) (by omega),
        ih (n-16+15) (by omega)] at h
      exact h.trans hf.symm

#print axioms eq_formula
end MathLean.BinaryGramFormula
