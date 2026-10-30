import MathLean.DominoEncoding

/-! Interpret the bit masks independently in terms of individual cells.
Each bit of a placement specifies an actual horizontal or vertical domino.
The tests below count the dominoes covering a cell and exclude adjacent
uncovered cells, the elementary characterization of a maximal packing. -/
namespace MathLean.Domino
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def bitValue (mask row : ℕ) : ℕ := if mask.testBit row then 1 else 0

/-- A cell may be covered from the left, from a horizontal start here,
from a vertical start here, or from the vertical start one row above. -/
def cellMultiplicity (incoming : ℕ) (p : Placement) (row : ℕ) : ℕ :=
  bitValue incoming row + bitValue p.1.val row + bitValue p.2.val row +
    if row=0 then 0 else bitValue p.2.val (row-1)

def ColumnGeometry (incoming previousHoles : ℕ) (p : Placement) : Prop :=
  (∀ row : Fin 4, cellMultiplicity incoming p row.val ≤ 1) ∧
  (∀ row : Fin 3, ¬(cellMultiplicity incoming p row.val=0 ∧
    cellMultiplicity incoming p (row.val+1)=0)) ∧
  (∀ row : Fin 4, previousHoles.testBit row.val=true →
    cellMultiplicity incoming p row.val ≠ 0)

instance (h u : ℕ) (p : Placement) : Decidable (ColumnGeometry h u p) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

theorem masks_bounds : ∀ s : State, (masks s).1<16 ∧ (masks s).2<16 := by decide +kernel

/-- The algebraic column tests mean exactly nonoverlap and independence
of the uncovered cells, expressed directly for the four rows. -/
theorem column_valid_iff_geometry : ∀ h u : Fin 16, ∀ p : Placement,
    ColumnValid h.val u.val p ↔ ColumnGeometry h.val u.val p := by decide +kernel

/-- The hole bits mark precisely the cells covered by no domino. -/
theorem hole_bit_iff_uncovered : ∀ h : Fin 16, ∀ p : Placement, ∀ row : Fin 4,
    (holes h.val p).testBit row.val=true ↔ cellMultiplicity h.val p row.val=0 := by
  decide +kernel

theorem valid_state_column_iff_geometry (s : State) (p : Placement) :
    ColumnValid (masks s).1 (masks s).2 p ↔ ColumnGeometry (masks s).1 (masks s).2 p :=
  column_valid_iff_geometry ⟨(masks s).1,(masks_bounds s).1⟩
    ⟨(masks s).2,(masks_bounds s).2⟩ p

#print axioms column_valid_iff_geometry
#print axioms hole_bit_iff_uncovered
end MathLean.Domino
