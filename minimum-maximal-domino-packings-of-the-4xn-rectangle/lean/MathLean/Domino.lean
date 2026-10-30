import Mathlib.Data.Fin.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Data.List.OfFn

/-! Local certificate for the column model of maximal 4 by n domino packings.
This file does not identify paths with physical packings; that requires the
separate encoding theorem. No external computation is trusted by the proof.
-/
namespace MathLean.Domino
set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev State := Fin 60

def masks : State → ℕ × ℕ
  | ⟨0, _⟩ => (0,0)
  | ⟨1, _⟩ => (0,1)
  | ⟨2, _⟩ => (0,2)
  | ⟨3, _⟩ => (0,4)
  | ⟨4, _⟩ => (0,5)
  | ⟨5, _⟩ => (0,8)
  | ⟨6, _⟩ => (0,9)
  | ⟨7, _⟩ => (0,10)
  | ⟨8, _⟩ => (1,0)
  | ⟨9, _⟩ => (1,2)
  | ⟨10, _⟩ => (1,4)
  | ⟨11, _⟩ => (1,8)
  | ⟨12, _⟩ => (1,10)
  | ⟨13, _⟩ => (2,0)
  | ⟨14, _⟩ => (2,1)
  | ⟨15, _⟩ => (2,4)
  | ⟨16, _⟩ => (2,5)
  | ⟨17, _⟩ => (2,8)
  | ⟨18, _⟩ => (2,9)
  | ⟨19, _⟩ => (3,0)
  | ⟨20, _⟩ => (3,4)
  | ⟨21, _⟩ => (3,8)
  | ⟨22, _⟩ => (4,0)
  | ⟨23, _⟩ => (4,1)
  | ⟨24, _⟩ => (4,2)
  | ⟨25, _⟩ => (4,8)
  | ⟨26, _⟩ => (4,9)
  | ⟨27, _⟩ => (4,10)
  | ⟨28, _⟩ => (5,0)
  | ⟨29, _⟩ => (5,2)
  | ⟨30, _⟩ => (5,8)
  | ⟨31, _⟩ => (5,10)
  | ⟨32, _⟩ => (6,0)
  | ⟨33, _⟩ => (6,1)
  | ⟨34, _⟩ => (6,8)
  | ⟨35, _⟩ => (6,9)
  | ⟨36, _⟩ => (7,0)
  | ⟨37, _⟩ => (7,8)
  | ⟨38, _⟩ => (8,0)
  | ⟨39, _⟩ => (8,1)
  | ⟨40, _⟩ => (8,2)
  | ⟨41, _⟩ => (8,4)
  | ⟨42, _⟩ => (8,5)
  | ⟨43, _⟩ => (9,0)
  | ⟨44, _⟩ => (9,2)
  | ⟨45, _⟩ => (9,4)
  | ⟨46, _⟩ => (10,0)
  | ⟨47, _⟩ => (10,1)
  | ⟨48, _⟩ => (10,4)
  | ⟨49, _⟩ => (10,5)
  | ⟨50, _⟩ => (11,0)
  | ⟨51, _⟩ => (11,4)
  | ⟨52, _⟩ => (12,0)
  | ⟨53, _⟩ => (12,1)
  | ⟨54, _⟩ => (12,2)
  | ⟨55, _⟩ => (13,0)
  | ⟨56, _⟩ => (13,2)
  | ⟨57, _⟩ => (14,0)
  | ⟨58, _⟩ => (14,1)
  | _ => (15,0)

def potential : State → ℤ
  | ⟨0, _⟩ => 0
  | ⟨1, _⟩ => 0
  | ⟨2, _⟩ => 0
  | ⟨3, _⟩ => 0
  | ⟨4, _⟩ => 0
  | ⟨5, _⟩ => 0
  | ⟨6, _⟩ => -1
  | ⟨7, _⟩ => 0
  | ⟨8, _⟩ => 3
  | ⟨9, _⟩ => 1
  | ⟨10, _⟩ => 3
  | ⟨11, _⟩ => 2
  | ⟨12, _⟩ => 1
  | ⟨13, _⟩ => 3
  | ⟨14, _⟩ => 2
  | ⟨15, _⟩ => 3
  | ⟨16, _⟩ => 2
  | ⟨17, _⟩ => 2
  | ⟨18, _⟩ => 2
  | ⟨19, _⟩ => 4
  | ⟨20, _⟩ => 4
  | ⟨21, _⟩ => 4
  | ⟨22, _⟩ => 3
  | ⟨23, _⟩ => 2
  | ⟨24, _⟩ => 3
  | ⟨25, _⟩ => 2
  | ⟨26, _⟩ => 2
  | ⟨27, _⟩ => 2
  | ⟨28, _⟩ => 4
  | ⟨29, _⟩ => 3
  | ⟨30, _⟩ => 4
  | ⟨31, _⟩ => 2
  | ⟨32, _⟩ => 4
  | ⟨33, _⟩ => 3
  | ⟨34, _⟩ => 3
  | ⟨35, _⟩ => 2
  | ⟨36, _⟩ => 4
  | ⟨37, _⟩ => 4
  | ⟨38, _⟩ => 3
  | ⟨39, _⟩ => 2
  | ⟨40, _⟩ => 3
  | ⟨41, _⟩ => 1
  | ⟨42, _⟩ => 1
  | ⟨43, _⟩ => 4
  | ⟨44, _⟩ => 4
  | ⟨45, _⟩ => 4
  | ⟨46, _⟩ => 4
  | ⟨47, _⟩ => 4
  | ⟨48, _⟩ => 3
  | ⟨49, _⟩ => 2
  | ⟨50, _⟩ => 4
  | ⟨51, _⟩ => 4
  | ⟨52, _⟩ => 4
  | ⟨53, _⟩ => 4
  | ⟨54, _⟩ => 4
  | ⟨55, _⟩ => 4
  | ⟨56, _⟩ => 4
  | ⟨57, _⟩ => 4
  | ⟨58, _⟩ => 4
  | _ => 4

def pop (n : ℕ) : ℕ := n%2 + (n/2)%2 + (n/4)%2 + (n/8)%2

def Legal (s t : State) : Prop :=
  let (h,u) := masks s
  let (k,v) := masks t
  h &&& (k ||| v) = 0 ∧ u &&& v = 0 ∧
    (15 ^^^ (h ||| k ||| v)) ∈ ([0,3,6,12,15] : List ℕ)

instance (s t : State) : Decidable (Legal s t) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))

def cost (s t : State) : ℕ :=
  pop (masks t).1 + pop (15 ^^^ ((masks s).1 ||| (masks t).1 ||| (masks t).2)) / 2

def defect (s t : State) : ℤ := 3*(cost s t : ℤ)-4+potential s-potential t

/-- All 304 legal transitions satisfy the displayed potential inequality. -/
theorem defect_nonneg : ∀ s t : State, Legal s t → 0 ≤ defect s t := by decide

/-- The terminal potential is zero, except at hole mask 9 where it is -1. -/
theorem terminal_potential : ∀ s : State, (masks s).1 = 0 →
    potential s = if (masks s).2 = 9 then -1 else 0 := by decide

def pathCost : List State → ℤ
  | [] => 0
  | [_] => 0
  | s::t::rest => (cost s t : ℤ) + pathCost (t::rest)

def pathDefect : List State → ℤ
  | [] => 0
  | [_] => 0
  | s::t::rest => defect s t + pathDefect (t::rest)

def LegalPath : List State → Prop
  | [] => True
  | [_] => True
  | s::t::rest => Legal s t ∧ LegalPath (t::rest)

theorem pathDefect_nonneg : ∀ p : List State, LegalPath p → 0 ≤ pathDefect p
  | [], _ => le_refl 0
  | [_], _ => le_refl 0
  | s::t::rest, h => Int.add_nonneg (defect_nonneg s t h.1) (pathDefect_nonneg (t::rest) h.2)

#print axioms defect_nonneg
end MathLean.Domino
