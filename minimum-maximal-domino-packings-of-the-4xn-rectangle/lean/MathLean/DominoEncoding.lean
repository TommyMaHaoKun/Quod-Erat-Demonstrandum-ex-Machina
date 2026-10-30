import MathLean.Domino
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Prod
import Mathlib.Tactic.FinCases

/-! Independent physical-column description of maximal domino packings.
A placement records which horizontal dominoes start in this column and
which of its three vertical edges carry dominoes. Bits record placements,
not placement order, and coordinates retain their labels. -/
namespace MathLean.Domino
set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev Placement := Fin 16 × Fin 8

def verticalCells (p : Placement) : ℕ := p.2.val ||| (p.2.val <<< 1)

def holes (incoming : ℕ) (p : Placement) : ℕ :=
  15 ^^^ (incoming ||| p.1.val ||| verticalCells p)

/-- Nonoverlap of the chosen horizontal and vertical dominoes, followed
by independence of uncovered cells within and between columns. -/
def ColumnValid (incoming previousHoles : ℕ) (p : Placement) : Prop :=
  p.2.val &&& (p.2.val <<< 1) = 0 ∧
  incoming &&& p.1.val = 0 ∧
  (incoming ||| p.1.val) &&& verticalCells p = 0 ∧
  holes incoming p &&& (holes incoming p <<< 1) = 0 ∧
  previousHoles &&& holes incoming p = 0

instance (h u : ℕ) (p : Placement) : Decidable (ColumnValid h u p) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _))

def physicalNext (previous : ℕ × ℕ) (p : Placement) : ℕ × ℕ :=
  (p.1.val, holes previous.1 p)

/-- End boundary excludes outgoing overhangs. Starting at `(0,0)` excludes
left overhangs. All possible uncovered-cell adjacencies are tested. -/
def ValidColumns : (ℕ × ℕ) → List Placement → Prop
  | previous, [] => previous.1 = 0
  | previous, p::ps => ColumnValid previous.1 previous.2 p ∧
      ValidColumns (physicalNext previous p) ps

def placementCost (p : Placement) : ℕ := pop p.1.val + pop p.2.val

def packingCost (ps : List Placement) : ℕ := (ps.map placementCost).sum

def stateOfMasks (h u : ℕ) : State :=
  ([0,1,2,0,3,4,0,0,5,6,7,0,0,0,0,0,8,0,9,0,10,0,0,0,11,0,12,0,0,0,0,0,13,14,0,0,15,16,0,0,17,18,0,0,0,0,0,0,19,0,0,0,20,0,0,0,21,0,0,0,0,0,0,0,22,23,24,0,0,0,0,0,25,26,27,0,0,0,0,0,28,0,29,0,0,0,0,0,30,0,31,0,0,0,0,0,32,33,0,0,0,0,0,0,34,35,0,0,0,0,0,0,36,0,0,0,0,0,0,0,37,0,0,0,0,0,0,0,38,39,40,0,41,42,0,0,0,0,0,0,0,0,0,0,43,0,44,0,45,0,0,0,0,0,0,0,0,0,0,0,46,47,0,0,48,49,0,0,0,0,0,0,0,0,0,0,50,0,0,0,51,0,0,0,0,0,0,0,0,0,0,0,52,53,54,0,0,0,0,0,0,0,0,0,0,0,0,0,55,0,56,0,0,0,0,0,0,0,0,0,0,0,0,0,57,58,0,0,0,0,0,0,0,0,0,0,0,0,0,0,59,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] : List State).getD (16*h+u) 0

def encodeColumn (s : State) (p : Placement) : State :=
  stateOfMasks p.1.val (holes (masks s).1 p)

def verticalStarts (mask : ℕ) : Fin 8 :=
  match mask with
  | 3 => 1
  | 6 => 2
  | 12 => 4
  | 15 => 5
  | _ => 0

def decodeColumn (s t : State) : Placement :=
  (⟨(masks t).1 % 16, Nat.mod_lt _ (by decide)⟩,
    verticalStarts (15 ^^^ ((masks s).1 ||| (masks t).1 ||| (masks t).2)))

theorem encode_column_valid : ∀ s : State, ∀ p : Placement,
    ColumnValid (masks s).1 (masks s).2 p →
      Legal s (encodeColumn s p) ∧
      masks (encodeColumn s p) = physicalNext (masks s) p ∧
      decodeColumn s (encodeColumn s p) = p := by decide +kernel

theorem decode_column_valid : ∀ s t : State, Legal s t →
    ColumnValid (masks s).1 (masks s).2 (decodeColumn s t) ∧
      encodeColumn s (decodeColumn s t) = t ∧
      placementCost (decodeColumn s t) = cost s t := by decide +kernel

#print axioms encode_column_valid
#print axioms decode_column_valid
end MathLean.Domino
