import MathLean.DominoGeometry

/-! An all-length, cost-preserving bijection between physical column
placements and legal state paths. The finite column certificates only
supply the induction step; they do not replace this bijection. -/
namespace MathLean.Domino

/-- A board described by the dominoes starting in each column. Every cell
has at most one covering domino; adjacent uncovered cells are forbidden.
The final-column test excludes horizontal dominoes leaving the board. -/
def GeometryColumns : (ℕ × ℕ) → List Placement → Prop
  | previous, [] => previous.1=0
  | previous, p::ps => ColumnGeometry previous.1 previous.2 p ∧
      GeometryColumns (physicalNext previous p) ps

def MaximalPacking (ps : List Placement) : Prop := GeometryColumns (0,0) ps

/-- Minimum among all maximal packings of the same labeled rectangle. -/
def MinimumPacking (ps : List Placement) : Prop := MaximalPacking ps ∧
  ∀ qs : List Placement, qs.length=ps.length → MaximalPacking qs →
    packingCost ps ≤ packingCost qs

theorem valid_iff_geometry (s : State) (ps : List Placement) :
    ValidColumns (masks s) ps ↔ GeometryColumns (masks s) ps := by
  induction ps generalizing s with
  | nil => rfl
  | cons p ps ih =>
    constructor
    · intro h
      have he := encode_column_valid s p h.1
      refine ⟨(valid_state_column_iff_geometry s p).mp h.1, ?_⟩
      rw [← he.2.1]
      apply (ih (encodeColumn s p)).mp
      rw [he.2.1]
      exact h.2
    · intro h
      have hp := (valid_state_column_iff_geometry s p).mpr h.1
      have he := encode_column_valid s p hp
      refine ⟨hp, ?_⟩
      rw [← he.2.1]
      apply (ih (encodeColumn s p)).mpr
      rw [he.2.1]
      exact h.2

theorem maximal_packing_iff (ps : List Placement) :
    MaximalPacking ps ↔ ValidColumns (0,0) ps := (valid_iff_geometry 0 ps).symm

def ValidSuffix : State → List State → Prop
  | s, [] => (masks s).1 = 0
  | s, t::ts => Legal s t ∧ ValidSuffix t ts

def costFrom : State → List State → ℕ
  | _, [] => 0
  | s, t::ts => cost s t + costFrom t ts

def encodeColumns : State → List Placement → List State
  | _, [] => []
  | s, p::ps => encodeColumn s p :: encodeColumns (encodeColumn s p) ps

def decodeColumns : State → List State → List Placement
  | _, [] => []
  | s, t::ts => decodeColumn s t :: decodeColumns t ts

theorem encode_length (s : State) (ps : List Placement) :
    (encodeColumns s ps).length = ps.length := by
  induction ps generalizing s with
  | nil => rfl
  | cons p ps ih => simp [encodeColumns, ih]

theorem decode_length (s : State) (ts : List State) :
    (decodeColumns s ts).length = ts.length := by
  induction ts generalizing s with
  | nil => rfl
  | cons t ts ih => simp [decodeColumns, ih]

theorem encode_valid (s : State) (ps : List Placement)
    (h : ValidColumns (masks s) ps) : ValidSuffix s (encodeColumns s ps) := by
  induction ps generalizing s with
  | nil => exact h
  | cons p ps ih =>
    obtain ⟨hp,ht⟩ := h
    obtain ⟨he,hm,_⟩ := encode_column_valid s p hp
    refine ⟨he, ih (encodeColumn s p) ?_⟩
    rw [hm]
    exact ht

theorem decode_valid (s : State) (ts : List State)
    (h : ValidSuffix s ts) : ValidColumns (masks s) (decodeColumns s ts) := by
  induction ts generalizing s with
  | nil => exact h
  | cons t ts ih =>
    obtain ⟨he,ht⟩ := h
    obtain ⟨hp,hi,_⟩ := decode_column_valid s t he
    have hm := (encode_column_valid s (decodeColumn s t) hp).2.1
    rw [hi] at hm
    refine ⟨hp, ?_⟩
    rw [← hm]
    exact ih t ht

theorem decode_encode (s : State) (ps : List Placement)
    (h : ValidColumns (masks s) ps) : decodeColumns s (encodeColumns s ps) = ps := by
  induction ps generalizing s with
  | nil => rfl
  | cons p ps ih =>
    obtain ⟨hp,ht⟩ := h
    obtain ⟨_,hm,hi⟩ := encode_column_valid s p hp
    simp only [encodeColumns, decodeColumns, hi, List.cons.injEq, true_and]
    apply ih
    rw [hm]
    exact ht

theorem encode_decode (s : State) (ts : List State)
    (h : ValidSuffix s ts) : encodeColumns s (decodeColumns s ts) = ts := by
  induction ts generalizing s with
  | nil => rfl
  | cons t ts ih =>
    obtain ⟨he,ht⟩ := h
    have hi := (decode_column_valid s t he).2.1
    simp only [decodeColumns, encodeColumns, hi, List.cons.injEq, true_and]
    exact ih t ht

theorem decode_cost (s : State) (ts : List State) (h : ValidSuffix s ts) :
    packingCost (decodeColumns s ts) = costFrom s ts := by
  induction ts generalizing s with
  | nil => rfl
  | cons t ts ih =>
    obtain ⟨he,ht⟩ := h
    have hc := (decode_column_valid s t he).2.2
    simp only [decodeColumns, packingCost, List.map_cons, List.sum_cons, costFrom]
    rw [hc]
    exact congrArg (cost s t + ·) (ih t ht)

theorem encode_cost (s : State) (ps : List Placement) (h : ValidColumns (masks s) ps) :
    costFrom s (encodeColumns s ps) = packingCost ps := by
  have hc := decode_cost s (encodeColumns s ps) (encode_valid s ps h)
  rw [decode_encode s ps h] at hc
  exact hc.symm

/-- Width and domino count are both preserved, without a symmetry quotient
or a multiplicity factor. Start state 0 has masks `(0,0)`. -/
def physicalPathEquiv (s : State) (n d : ℕ) :
    {ps : List Placement // ps.length=n ∧ ValidColumns (masks s) ps ∧ packingCost ps=d} ≃
    {ts : List State // ts.length=n ∧ ValidSuffix s ts ∧ costFrom s ts=d} where
  toFun p := ⟨encodeColumns s p.val, by
    exact ⟨(encode_length s p.val).trans p.property.1,
      encode_valid s p.val p.property.2.1,
      (encode_cost s p.val p.property.2.1).trans p.property.2.2⟩⟩
  invFun t := ⟨decodeColumns s t.val, by
    exact ⟨(decode_length s t.val).trans t.property.1,
      decode_valid s t.val t.property.2.1,
      (decode_cost s t.val t.property.2.1).trans t.property.2.2⟩⟩
  left_inv p := Subtype.ext (decode_encode s p.val p.property.2.1)
  right_inv t := Subtype.ext (encode_decode s t.val t.property.2.1)

#print axioms physicalPathEquiv
end MathLean.Domino
