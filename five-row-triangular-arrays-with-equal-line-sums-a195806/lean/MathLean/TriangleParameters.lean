import Mathlib.Data.Fin.VecNotation
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Original labeled triangular arrays for OEIS A195806 and an integral
parameterization. Coordinates are all nonnegative triples of sum four. -/
namespace MathLean.Triangle
open scoped BigOperators

def coords : Fin 15 → Fin 3 → ℕ :=
  ![![0,0,4], ![0,1,3], ![0,2,2], ![0,3,1], ![0,4,0],
    ![1,0,3], ![1,1,2], ![1,2,1], ![1,3,0],
    ![2,0,2], ![2,1,1], ![2,2,0], ![3,0,1], ![3,1,0], ![4,0,0]]

theorem coords_sum : ∀ i, coords i 0 + coords i 1 + coords i 2 = 4 := by decide +kernel
theorem coords_lt : ∀ i j, coords i j < 5 := by decide +kernel

theorem coords_injective : Function.Injective coords := by decide +kernel

theorem coords_cover : ∀ a b c : Fin 5, a.val+b.val+c.val=4 →
    ∃ i : Fin 15, coords i 0=a.val ∧ coords i 1=b.val ∧ coords i 2=c.val := by
  decide +kernel

abbrev Raw := Fin 15 → ℤ

def lineSum (u : Raw) (direction : Fin 3) (level : Fin 5) : ℤ :=
  ∑ i, if coords i direction = level.val then u i else 0

def Lines (u : Raw) : Prop := ∀ level : Fin 5,
  lineSum u 0 level = lineSum u 1 level ∧ lineSum u 1 level = lineSum u 2 level

def Valid (u : Raw) : Prop := u 0=0 ∧ u 4=0 ∧ u 14=0 ∧ Lines u

def Bounded (n : ℕ) (u : Raw) : Prop := ∀ i, 0 ≤ u i ∧ u i ≤ n

/-- All positions retain their labels; rotations are not identified. -/
abbrev Arrays (n : ℕ) := {u : Raw // Valid u ∧ Bounded n u}

@[ext] structure Parameters where
  a : ℤ
  c : ℤ
  e : ℤ
  f : ℤ
  p : ℤ
  q : ℤ
  deriving DecidableEq

def parameterMap (v : Parameters) : Raw :=
  ![0, v.a+2*v.p+v.q, v.c-3*v.p-v.q, v.e+v.p, 0,
    v.e-v.p-v.q, v.f+3*v.p+v.q, v.f+3*v.p+2*v.q, v.a,
    v.c+v.q, v.f, v.c, v.a+v.p, v.e, 0]

def readParameters (u : Raw) : Parameters :=
  ⟨u 8, u 11, u 13, u 10, u 12-u 8, u 9-u 11⟩

theorem read_parameterMap (v : Parameters) : readParameters (parameterMap v) = v := by
  ext <;> simp [readParameters, parameterMap]

set_option maxHeartbeats 800000 in
theorem parameterMap_valid (v : Parameters) : Valid (parameterMap v) := by
  refine ⟨rfl, rfl, rfl, ?_⟩
  intro level
  fin_cases level <;>
    simp [lineSum, coords, parameterMap, Fin.sum_univ_succ, Matrix.cons_val] <;>
    constructor <;> ring

set_option maxHeartbeats 800000 in
theorem parameterMap_read (u : Raw) (hu : Valid u) : parameterMap (readParameters u) = u := by
  rcases hu with ⟨hcorner0, hcorner4, hcorner14, hlines⟩
  have h0 := hlines 0
  have h2 := hlines 2
  have h3 := hlines 3
  simp [lineSum, coords, Fin.sum_univ_succ, Matrix.cons_val] at h0 h2 h3
  funext i
  fin_cases i <;> simp [parameterMap, readParameters, Matrix.cons_val] <;>
    (try dsimp [Fin.ofNat', Fin.succ] at *) <;> omega

def parameterEquiv (n : ℕ) : Arrays n ≃ {v : Parameters // Bounded n (parameterMap v)} where
  toFun u := ⟨readParameters u.val, by rw [parameterMap_read u.val u.property.1]; exact u.property.2⟩
  invFun v := ⟨parameterMap v.val, parameterMap_valid v.val, v.property⟩
  left_inv u := Subtype.ext (parameterMap_read u.val u.property.1)
  right_inv v := Subtype.ext (read_parameterMap v.val)

end MathLean.Triangle
