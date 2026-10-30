import MathLean.DominoBudgetData

namespace MathLean.DominoBudget
open MathLean.PathLists
set_option maxHeartbeats 0

theorem finish_map {S T : Type} (f : S → T) (s : S) (ts : List S) :
    finish (f s) (ts.map f)=f (finish s ts) := by
  induction ts generalizing s with
  | nil => rfl
  | cons t ts ih => exact ih t

theorem chain_map {S T : Type} (f : S → T) (R : S → S → Prop)
    (Q : T → T → Prop) (h : ∀ s t, R s t → Q (f s) (f t))
    (s : S) (ts : List S) (hc : Chain R s ts) : Chain Q (f s) (ts.map f) := by
  induction ts generalizing s with
  | nil => trivial
  | cons t ts ih => exact ⟨h s t hc.1, ih t hc.2⟩

theorem backward_chain (s : Node) (ts : List Node) (hc : Chain Edge s ts)
    (hf : Final (finish s ts)) : Backward s := by
  induction ts generalizing s with
  | nil => exact backward_final s hf
  | cons t ts ih => exact backward_closed s t hc.1 (ih t hc.2 hf)

theorem active_nodes (s : Node) (ts : List Node) (hs : Forward s)
    (hc : Chain Edge s ts) (hf : Final (finish s ts)) :
    ∀ t ∈ ts, Active t := by
  induction ts generalizing s with
  | nil => simp
  | cons t ts ih =>
    have ht := forward_closed s t hc.1 hs
    intro u hu
    rcases List.mem_cons.mp hu with hu | hu
    · subst u
      exact (active_iff t).mpr ⟨ht,backward_chain t ts hc.2 hf⟩
    · exact ih t ht hc.2 hf u hu

def GraphEdge (i j : Fin 114) : Prop := i ∈ DominoCount.pred j
def GraphFinal (i : Fin 114) : Prop := i ∈ DominoCount.finals

theorem chain_project (s : Node) (ts : List Node) (hs : Forward s)
    (hc : Chain Edge s ts) (hf : Final (finish s ts)) :
    Chain GraphEdge (project s) (ts.map project) := by
  induction ts generalizing s with
  | nil => trivial
  | cons t ts ih =>
    have ht := forward_closed s t hc.1 hs
    have hsa := (active_iff s).mpr ⟨hs,backward_chain s (t::ts) hc hf⟩
    have hta := (active_iff t).mpr ⟨ht,backward_chain t ts hc.2 hf⟩
    refine ⟨?_, ih t ht hc.2 hf⟩
    apply (edge_iff _ _).mpr
    change embed (project s)=s at hsa
    change embed (project t)=t at hta
    rw [hsa,hta]
    exact hc.1

theorem forward_finish (s : Node) (ts : List Node) (hs : Forward s)
    (hc : Chain Edge s ts) : Forward (finish s ts) := by
  induction ts generalizing s with
  | nil => exact hs
  | cons t ts ih => exact ih t (forward_closed s t hc.1 hs) hc.2

abbrev BudgetLists (n : ℕ) := AcceptedLists Edge Final (0 : Node) n
abbrev GraphLists (n : ℕ) := AcceptedLists GraphEdge GraphFinal (0 : Fin 114) n

def toGraph (n : ℕ) (p : BudgetLists n) : GraphLists n :=
  ⟨p.val.map project, by
    refine ⟨by simpa using p.property.1, ?_, ?_⟩
    · simpa only [project_start] using chain_project 0 p.val forward_start
        p.property.2.1 p.property.2.2
    · have ha := (active_iff (finish 0 p.val)).mpr
        ⟨forward_finish 0 p.val forward_start p.property.2.1,
          backward_final _ p.property.2.2⟩
      rw [← project_start,finish_map]
      apply (final_iff _).mpr
      change embed (project (finish 0 p.val))=finish 0 p.val at ha
      rw [ha]
      exact p.property.2.2⟩

def toBudget (n : ℕ) (p : GraphLists n) : BudgetLists n :=
  ⟨p.val.map embed, by
    refine ⟨by simpa using p.property.1, ?_, ?_⟩
    · simpa only [embed_start] using chain_map embed GraphEdge Edge
        (fun i j h => (edge_iff i j).mp h) 0 p.val p.property.2.1
    · rw [← embed_start,finish_map]
      exact (final_iff _).mp p.property.2.2⟩

/-- Trimming removes no complete accepted path, at any length. -/
def trimEquiv (n : ℕ) : BudgetLists n ≃ GraphLists n where
  toFun := toGraph n
  invFun := toBudget n
  left_inv p := by
    apply Subtype.ext
    change (p.val.map project).map embed=p.val
    rw [List.map_map]
    calc
      _ = p.val.map id := List.map_congr_left (fun x hx =>
        active_nodes 0 p.val forward_start p.property.2.1 p.property.2.2 x hx)
      _ = _ := List.map_id _
  right_inv p := by
    apply Subtype.ext
    change (p.val.map embed).map project=p.val
    simp only [List.map_map,Function.comp_def,project_embed]
    exact List.map_id _

noncomputable def graphListEquiv (n : ℕ) : DominoCount.AcceptedPaths n ≃ GraphLists n :=
  listEquiv GraphEdge GraphFinal 0 n

noncomputable def budgetGraphEquiv (n : ℕ) : BudgetLists n ≃ DominoCount.AcceptedPaths n :=
  (trimEquiv n).trans (graphListEquiv n).symm

#print axioms budgetGraphEquiv
end MathLean.DominoBudget
