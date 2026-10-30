import MathLean.DominoPaths
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace MathLean.Domino
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def defectFrom : State → List State → ℤ
  | _, [] => 0
  | s, t::ts => defect s t + defectFrom t ts

def lastState : State → List State → State
  | s, [] => s
  | _, t::ts => lastState t ts

theorem last_terminal (s : State) (ts : List State) (h : ValidSuffix s ts) :
    (masks (lastState s ts)).1=0 := by
  induction ts generalizing s with
  | nil => exact h
  | cons t ts ih => exact ih t h.2

theorem defect_from_nonneg (s : State) (ts : List State) (h : ValidSuffix s ts) :
    0 ≤ defectFrom s ts := by
  induction ts generalizing s with
  | nil => exact le_refl 0
  | cons t ts ih => exact add_nonneg (defect_nonneg s t h.1) (ih t h.2)

theorem telescope (s : State) (ts : List State) :
    defectFrom s ts = 3*(costFrom s ts : ℤ)-4*(ts.length : ℤ)+
      potential s-potential (lastState s ts) := by
  induction ts generalizing s with
  | nil => simp [defectFrom,costFrom,lastState]
  | cons t ts ih =>
    simp only [defectFrom,costFrom,lastState,List.length_cons,Nat.cast_add,Nat.cast_one]
    rw [ih]
    unfold defect
    ring

/-- A checked backward-closed set in the zero-defect graph containing
the exceptional terminal state `(0,9)`. -/
def leadsToBad (s : State) : Prop := s ∈ ([0,2,3,6,50,55,59] : List State)

instance (s : State) : Decidable (leadsToBad s) := inferInstanceAs (Decidable (_ ∈ _))

theorem bad_in_set : leadsToBad 6 := by decide

theorem bad_backward : ∀ s t : State,
    Legal s t → defect s t=0 → leadsToBad t → leadsToBad s := by decide +kernel

theorem start_to_bad : ∀ t : State,
    Legal 0 t → defect 0 t=0 → leadsToBad t → t=6 := by decide +kernel

theorem bad_no_return : ∀ t : State,
    Legal 6 t → defect 6 t=0 → leadsToBad t → False := by decide +kernel

theorem terminal_bound : ∀ s : State, (masks s).1=0 →
    -1 ≤ potential s ∧ (potential s=-1 ↔ s=6) := by decide +kernel

theorem zero_suffix_leads (s : State) (ts : List State) (h : ValidSuffix s ts)
    (hz : defectFrom s ts=0) (he : lastState s ts=6) : leadsToBad s := by
  induction ts generalizing s with
  | nil => change s=6 at he; rw [he]; exact bad_in_set
  | cons t ts ih =>
    have hd := defect_nonneg s t h.1
    have ht := defect_from_nonneg t ts h.2
    change defect s t+defectFrom t ts=0 at hz
    exact bad_backward s t h.1 (by omega) (ih t h.2 (by omega) he)

/-- The only zero-defect path from the start to the exceptional terminal
has one column. This proves the boundary exception for all path lengths. -/
theorem zero_bad_length (ts : List State) (h : ValidSuffix 0 ts)
    (hz : defectFrom 0 ts=0) (he : lastState 0 ts=6) : ts.length=1 := by
  cases ts with
  | nil => exact False.elim ((by decide : (0 : State) ≠ 6) he)
  | cons t ts =>
    have hd := defect_nonneg 0 t h.1
    have ht := defect_from_nonneg t ts h.2
    change defect 0 t+defectFrom t ts=0 at hz
    have hzt : defectFrom t ts=0 := by omega
    have hb := zero_suffix_leads t ts h.2 hzt he
    have ht6 := start_to_bad t h.1 (by omega) hb
    subst t
    cases ts with
    | nil => rfl
    | cons u us =>
      have hu := defect_nonneg 6 u h.2.1
      have hus := defect_from_nonneg u us h.2.2
      change defect 6 u+defectFrom u us=0 at hzt
      have hbu := zero_suffix_leads u us h.2.2 (by omega) he
      exact False.elim (bad_no_return u h.2.1 (by omega) hbu)

/-- Every maximal packing of width at least two needs ceil(4n/3)
dominoes. Attainment is a separate theorem. -/
theorem path_lower_bound (ts : List State) (h : ValidSuffix 0 ts)
    (hn : 2 ≤ ts.length) : (4*ts.length+2)/3 ≤ costFrom 0 ts := by
  have ht := telescope 0 ts
  have hd := defect_from_nonneg 0 ts h
  have hp := terminal_bound (lastState 0 ts) (last_terminal 0 ts h)
  have p0 : potential 0=0 := rfl
  rw [p0] at ht
  by_contra hbad
  have hz : defectFrom 0 ts=0 := by omega
  have he : lastState 0 ts=6 := hp.2.mp (by omega)
  have hlen := zero_bad_length ts h hz he
  omega

theorem packing_lower_bound (ps : List Placement) (h : ValidColumns (0,0) ps)
    (hn : 2 ≤ ps.length) : (4*ps.length+2)/3 ≤ packingCost ps := by
  have hv : ValidColumns (masks 0) ps := h
  have hh := path_lower_bound (encodeColumns 0 ps) (encode_valid 0 ps hv)
    (by rwa [encode_length])
  rwa [encode_length,encode_cost 0 ps hv] at hh

#print axioms packing_lower_bound

theorem maximal_packing_lower_bound (ps : List Placement) (h : MaximalPacking ps)
    (hn : 2 ≤ ps.length) : (4*ps.length+2)/3 ≤ packingCost ps :=
  packing_lower_bound ps ((maximal_packing_iff ps).mp h) hn

#print axioms maximal_packing_lower_bound
end MathLean.Domino
