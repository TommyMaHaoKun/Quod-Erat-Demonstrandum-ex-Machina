import MathLean.DominoCount
import MathLean.FiniteTransfer
import Mathlib.Algebra.BigOperators.Group.Finset.Piecewise

namespace MathLean.DominoCount
open scoped BigOperators

/-- An edge of the explicit graph, as a type with either zero or one element. -/
def Edge (s t : Fin 114) := {u : Unit // s ∈ pred t}

instance (s t : Fin 114) : Fintype (Edge s t) :=
  inferInstanceAs (Fintype {u : Unit // s ∈ pred t})

theorem edge_card (s t : Fin 114) :
    (Fintype.card (Edge s t) : ℤ) = if s ∈ pred t then 1 else 0 := by
  by_cases h : s ∈ pred t <;> simp [Edge,h]

theorem graph_transfer_eq : FiniteTransfer.transfer Edge = T := by
  apply LinearMap.ext
  intro v
  funext t
  change (∑ s, (Fintype.card (Edge s t) : ℤ)*v s) = ∑ s ∈ pred t, v s
  simp_rw [edge_card,ite_mul,one_mul,zero_mul]
  exact Fintype.sum_ite_mem (pred t) v

theorem graph_initial_eq : FiniteTransfer.initial (0 : Fin 114) = initial := by
  funext i
  simp only [FiniteTransfer.initial,initial,eq_comm]

theorem graph_accept_eq : FiniteTransfer.accepted (fun t => t ∈ finals) = accept := by
  apply LinearMap.ext
  intro v
  change (∑ t : {s // s ∈ finals}, v t.val) = ∑ t ∈ finals, v t
  exact (Finset.sum_subtype finals (fun _ => Iff.rfl) v).symm

abbrev AcceptedPaths (n : ℕ) :=
  Σ t : {s // s ∈ finals}, FiniteTransfer.Paths Edge (0 : Fin 114) n t.val

/-- The closed form is the cardinality of the graph's actual path type,
not merely a sequence defined by a recurrence. -/
theorem card_graph_paths (n : ℕ) : (Fintype.card (AcceptedPaths n) : ℤ) = formula n := by
  have h := FiniteTransfer.card_accepted_paths Edge (0 : Fin 114) (fun t => t ∈ finals) n
  rw [graph_transfer_eq,graph_initial_eq,graph_accept_eq] at h
  exact h.trans (count_eq_formula n)

#print axioms card_graph_paths

theorem formula_positive (n : ℕ) : 0 < formula n := by
  by_cases hn : n < 17
  · have hi : ∀ i : Fin 17, 0 < initialCounts i := by decide +kernel
    simpa only [formula,dif_pos hn] using hi ⟨n,hn⟩
  · simp only [formula,dif_neg hn]
    by_cases h0 : n%3=0
    · simp [h0]
    · simp only [if_neg h0]
      by_cases h1 : n%3=1
      · simp only [if_pos h1]
        have hq : 6 ≤ n/3 := by omega
        have hk : (6 : ℤ) ≤ ((n/3 : ℕ) : ℤ) := by exact_mod_cast hq
        nlinarith [sq_nonneg (((n/3 : ℕ) : ℤ)-6)]
      · simp only [if_neg h1]
        omega

theorem exists_accepted_path (n : ℕ) : Nonempty (AcceptedPaths n) := by
  apply Fintype.card_pos_iff.mp
  have h := formula_positive n
  rw [← card_graph_paths n] at h
  exact_mod_cast h

#print axioms exists_accepted_path
end MathLean.DominoCount
