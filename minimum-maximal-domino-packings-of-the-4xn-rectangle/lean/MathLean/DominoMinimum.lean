import MathLean.DominoBudgetLift

namespace MathLean.Domino
open MathLean.DominoBudget
set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev CeilingPackings (n : ℕ) :=
  {ps : List Placement // ps.length=n ∧ MaximalPacking ps ∧ packingCost ps=(4*n+2)/3}

abbrev MinimumPackings (n : ℕ) :=
  {ps : List Placement // ps.length=n ∧ MinimumPacking ps}

def ceilingPhysicalEquiv (n : ℕ) : CeilingPackings n ≃ CeilingPaths n :=
  (Equiv.subtypeEquivRight (fun ps => by
    change (ps.length=n ∧ MaximalPacking ps ∧ packingCost ps=(4*n+2)/3) ↔
      (ps.length=n ∧ ValidColumns (masks 0) ps ∧ packingCost ps=(4*n+2)/3)
    rw [maximal_packing_iff]
    rfl)).trans (physicalPathEquiv 0 n ((4*n+2)/3))

noncomputable def ceilingGraphEquiv (n : ℕ) : CeilingPackings n ≃ DominoCount.AcceptedPaths n :=
  (ceilingPhysicalEquiv n).trans ((ceilingBudgetEquiv n).trans (budgetGraphEquiv n))

theorem ceiling_attained (n : ℕ) : Nonempty (CeilingPackings n) := by
  obtain ⟨p⟩ := DominoCount.exists_accepted_path n
  exact ⟨(ceilingGraphEquiv n).symm p⟩

theorem minimum_iff_ceiling (ps : List Placement) (hn : 2 ≤ ps.length) :
    MinimumPacking ps ↔ MaximalPacking ps ∧ packingCost ps=(4*ps.length+2)/3 := by
  constructor
  · intro hp
    obtain ⟨q⟩ := ceiling_attained ps.length
    have hlo := maximal_packing_lower_bound ps hp.1 hn
    have hhi := hp.2 q.val q.property.1 q.property.2.1
    exact ⟨hp.1,by rw [q.property.2.2] at hhi; omega⟩
  · intro hp
    refine ⟨hp.1,?_⟩
    intro qs hl hq
    have hqlo := maximal_packing_lower_bound qs hq (by omega)
    rw [hl,← hp.2] at hqlo
    exact hqlo

def minimumCeilingEquiv (n : ℕ) (hn : 2 ≤ n) : MinimumPackings n ≃ CeilingPackings n :=
  Equiv.subtypeEquivRight (fun ps => by
    change (ps.length=n ∧ MinimumPacking ps) ↔
      (ps.length=n ∧ MaximalPacking ps ∧ packingCost ps=(4*n+2)/3)
    constructor
    · rintro ⟨hl,hp⟩
      have h := (minimum_iff_ceiling ps (by omega)).mp hp
      exact ⟨hl,h.1,by simpa only [hl] using h.2⟩
    · rintro ⟨hl,hp,hc⟩
      refine ⟨hl,(minimum_iff_ceiling ps (by omega)).mpr ⟨hp,?_⟩⟩
      simpa only [hl] using hc)

theorem minimum_count_ge_two (n : ℕ) (hn : 2 ≤ n) :
    (Nat.card (MinimumPackings n) : ℤ)=DominoCount.formula n := by
  have h := Nat.card_congr ((minimumCeilingEquiv n hn).trans (ceilingGraphEquiv n))
  rw [h,Nat.card_eq_fintype_card]
  exact DominoCount.card_graph_paths n

instance geometryDecidable (previous : ℕ × ℕ) (ps : List Placement) :
    Decidable (GeometryColumns previous ps) := by
  induction ps generalizing previous with
  | nil => exact inferInstanceAs (Decidable (previous.1=0))
  | cons p ps ih =>
    letI := ih (physicalNext previous p)
    exact inferInstanceAs (Decidable (_ ∧ _))

instance (ps : List Placement) : Decidable (MaximalPacking ps) :=
  inferInstanceAs (Decidable (GeometryColumns (0,0) ps))

def middleDomino : Placement := (0,2)

theorem middle_maximal : MaximalPacking [middleDomino] := by decide +kernel
theorem middle_cost : packingCost [middleDomino]=1 := by decide

theorem one_column_bound : ∀ p : Placement, MaximalPacking [p] → 1 ≤ packingCost [p] := by
  decide +kernel

theorem one_column_unique : ∀ p : Placement,
    MaximalPacking [p] → packingCost [p] ≤ 1 → p=middleDomino := by decide +kernel

theorem minimum_one_iff (ps : List Placement) (hn : ps.length=1) :
    MinimumPacking ps ↔ ps=[middleDomino] := by
  constructor
  · intro hp
    obtain ⟨p,rfl⟩ := List.length_eq_one.mp hn
    have h := hp.2 [middleDomino] rfl middle_maximal
    rw [middle_cost] at h
    rw [one_column_unique p hp.1 h]
  · intro hp
    subst ps
    refine ⟨middle_maximal,?_⟩
    intro qs hl hq
    obtain ⟨q,rfl⟩ := List.length_eq_one.mp hl
    rw [middle_cost]
    exact one_column_bound q hq

def minimumOneEquiv : MinimumPackings 1 ≃ Unit where
  toFun _ := ()
  invFun _ := ⟨[middleDomino],rfl,(minimum_one_iff _ rfl).mpr rfl⟩
  left_inv p := Subtype.ext ((minimum_one_iff p.val p.property.1).mp p.property.2).symm
  right_inv _ := rfl

/-- The original count for every positive width, with the actual minimum
packing definition. Width one is proved separately from the ceiling graph. -/
theorem minimum_count (n : ℕ) (hn : 0 < n) :
    (Nat.card (MinimumPackings n) : ℤ)=DominoCount.formula n := by
  by_cases h1 : n=1
  · subst n
    rw [Nat.card_congr minimumOneEquiv,Nat.card_unique]
    rfl
  · exact minimum_count_ge_two n (by omega)

#print axioms minimum_count
end MathLean.Domino
