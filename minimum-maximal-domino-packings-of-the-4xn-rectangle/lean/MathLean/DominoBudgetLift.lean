import MathLean.DominoBudgetPaths

namespace MathLean.DominoBudget
open MathLean.PathLists MathLean.Domino
set_option maxHeartbeats 0

theorem last_eq_finish (s : State) (ts : List State) : lastState s ts=finish s ts := by
  induction ts generalizing s with
  | nil => rfl
  | cons t ts ih => exact ih t

theorem strip_valid (s : Node) (ts : List Node) (hc : Chain Edge s ts)
    (hf : Final (finish s ts)) : ValidSuffix (base s) (ts.map base) := by
  induction ts generalizing s with
  | nil => exact hf.1
  | cons t ts ih => exact ⟨hc.1.1, ih t hc.2 hf⟩

theorem budget_sum (s : Node) (ts : List Node) (hc : Chain Edge s ts) :
    (budget (finish s ts) : ℤ) = (budget s : ℤ)+defectFrom (base s) (ts.map base) := by
  induction ts generalizing s with
  | nil => simp [finish,defectFrom]
  | cons t ts ih =>
    change (budget (finish t ts) : ℤ) =
      (budget s : ℤ)+(defect (base s) (base t)+defectFrom (base t) (ts.map base))
    rw [ih t hc.2,hc.1.2]
    ring

theorem strip_excess (s : Node) (ts : List Node) (hc : Chain Edge s ts)
    (hf : Final (finish s ts)) :
    0 ≤ (budget s : ℤ)+defectFrom (base s) (ts.map base)+potential (lastState (base s) (ts.map base)) ∧
    (budget s : ℤ)+defectFrom (base s) (ts.map base)+potential (lastState (base s) (ts.map base)) ≤ 2 := by
  rw [last_eq_finish,finish_map,← budget_sum s ts hc]
  exact hf.2

theorem strip_injective (s : Node) (ts us : List Node)
    (ht : Chain Edge s ts) (hu : Chain Edge s us) (he : ts.map base=us.map base) : ts=us := by
  induction ts generalizing s us with
  | nil =>
    have hl : us.length=0 := by simpa using (congrArg List.length he).symm
    exact (List.length_eq_zero.mp hl).symm
  | cons t ts ih =>
    cases us with
    | nil => simp at he
    | cons u us =>
      have hh := (List.cons.inj he).1
      have hrest := (List.cons.inj he).2
      clear he
      have htu : t=u := node_ext t u hh (by
        have ht' := ht.1.2
        have hu' := hu.1.2
        rw [hh] at ht'
        omega)
      subst u
      exact congrArg (t :: ·) (ih t us ht.2 hu.2 hrest)

/-- Every valid suffix whose final excess is 0, 1, or 2 lifts uniquely to
the four-budget graph. Prefix budgets cannot exceed the final budget. -/
theorem exists_lift (s : Node) (ts : List State) (hv : ValidSuffix (base s) ts)
    (he : 0 ≤ (budget s : ℤ)+defectFrom (base s) ts+potential (lastState (base s) ts) ∧
      (budget s : ℤ)+defectFrom (base s) ts+potential (lastState (base s) ts) ≤ 2) :
    ∃ us : List Node, Chain Edge s us ∧ Final (finish s us) ∧ us.map base=ts := by
  induction ts generalizing s with
  | nil => exact ⟨[],trivial,⟨hv,by simpa [defectFrom,lastState] using he⟩,rfl⟩
  | cons t ts ih =>
    have hd := defect_nonneg (base s) t hv.1
    have htail := defect_from_nonneg t ts hv.2
    have hp := (terminal_bound (lastState t ts) (last_terminal t ts hv.2)).1
    let d : ℤ := (budget s : ℤ)+defect (base s) t
    have hdn : 0 ≤ d := by dsimp [d]; omega
    have hdu : d ≤ 3 := by
      change 0 ≤ (budget s : ℤ)+(defect (base s) t+defectFrom t ts)+potential (lastState t ts) ∧
        (budget s : ℤ)+(defect (base s) t+defectFrom t ts)+potential (lastState t ts) ≤ 2 at he
      dsimp [d]
      omega
    let b : Fin 4 := ⟨d.toNat,by omega⟩
    let y : Node := mk t b
    have hy : base y=t := base_mk t b
    have hb : (budget y : ℤ)=d := by
      rw [show budget y=b.val from budget_mk t b]
      exact Int.toNat_of_nonneg hdn
    have hyvalid : ValidSuffix (base y) ts := hy.symm ▸ hv.2
    have hyex : 0 ≤ (budget y : ℤ)+defectFrom (base y) ts+potential (lastState (base y) ts) ∧
        (budget y : ℤ)+defectFrom (base y) ts+potential (lastState (base y) ts) ≤ 2 := by
      rw [hy,hb]
      change 0 ≤ (budget s : ℤ)+(defect (base s) t+defectFrom t ts)+potential (lastState t ts) ∧
        (budget s : ℤ)+(defect (base s) t+defectFrom t ts)+potential (lastState t ts) ≤ 2 at he
      dsimp [d]
      omega
    obtain ⟨us,hc,hf,hm⟩ := ih y hyvalid hyex
    refine ⟨y::us,⟨⟨?_,?_⟩,hc⟩,hf,?_⟩
    · rw [hy]; exact hv.1
    · rw [hy,hb]
    · simp only [List.map_cons,hy,hm]

abbrev CeilingPaths (n : ℕ) :=
  {ts : List State // ts.length=n ∧ ValidSuffix 0 ts ∧ costFrom 0 ts=(4*n+2)/3}

def toCeiling (n : ℕ) (p : BudgetLists n) : CeilingPaths n :=
  ⟨p.val.map base,by
    have hv := strip_valid 0 p.val p.property.2.1 p.property.2.2
    have he := strip_excess 0 p.val p.property.2.1 p.property.2.2
    have ht := telescope 0 (p.val.map base)
    have hl : (p.val.map base).length=n := by simpa using p.property.1
    have b0 : base 0=0 := rfl
    have q0 : budget 0=0 := rfl
    have p0 : potential 0=0 := rfl
    rw [b0,q0] at he
    rw [p0,hl] at ht
    exact ⟨hl,hv,by omega⟩⟩

theorem toCeiling_bijective (n : ℕ) : Function.Bijective (toCeiling n) := by
  constructor
  · intro p q he
    apply Subtype.ext
    exact strip_injective 0 p.val q.val p.property.2.1 q.property.2.1 (congrArg Subtype.val he)
  · intro p
    have ht := telescope 0 p.val
    have p0 : potential 0=0 := rfl
    rw [p0,p.property.1,p.property.2.2] at ht
    have he : 0 ≤ (budget (0 : Node) : ℤ)+defectFrom (base 0) p.val+potential (lastState (base 0) p.val) ∧
        (budget (0 : Node) : ℤ)+defectFrom (base 0) p.val+potential (lastState (base 0) p.val) ≤ 2 := by
      change 0 ≤ (0 : ℤ)+defectFrom 0 p.val+potential (lastState 0 p.val) ∧
        (0 : ℤ)+defectFrom 0 p.val+potential (lastState 0 p.val) ≤ 2
      omega
    obtain ⟨us,hc,hf,hm⟩ := exists_lift 0 p.val p.property.2.1 he
    refine ⟨⟨us,?_,hc,hf⟩,Subtype.ext hm⟩
    have hl := congrArg List.length hm
    simpa only [List.length_map,p.property.1] using hl

noncomputable def ceilingBudgetEquiv (n : ℕ) : CeilingPaths n ≃ BudgetLists n :=
  (Equiv.ofBijective (toCeiling n) (toCeiling_bijective n)).symm

#print axioms ceilingBudgetEquiv
end MathLean.DominoBudget
