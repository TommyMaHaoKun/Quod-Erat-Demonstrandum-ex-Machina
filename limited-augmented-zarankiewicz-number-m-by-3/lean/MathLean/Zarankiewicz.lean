import Mathlib.Data.Finset.Card
import Mathlib.Data.Set.Card
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Push

/-!
The original (strong) limited augmented Zarankiewicz problem.
`Admissible` transcribes conditions S, C1, C2 and C3, including degenerate
2-edges. Ordered endpoint presentations of 2-edges are harmless: S forces
all endpoints distinct, and the forbidden conditions are symmetric.
-/
namespace MathLean.Zarankiewicz

abbrev Cell (m : ℕ) := Fin m × Fin 3

structure Configuration (m s : ℕ) where
  base : Cell m → Prop
  edge : Fin s → Fin 2 → Cell m

def Configuration.Occupied {m s} (G : Configuration m s) (x : Cell m) : Prop :=
  G.base x ∨ ∃ e t, G.edge e t = x

def Configuration.Full {m s} (G : Configuration m s) (r : Fin m) : Prop :=
  ∀ c, G.Occupied (r,c)

def C4Free {m} (B : Cell m → Prop) : Prop :=
  ∀ r p a b, r ≠ p → a ≠ b →
    B (r,a) → B (r,b) → B (p,a) → ¬ B (p,b)

structure Admissible {m s} (G : Configuration m s) : Prop where
  simple : Function.Injective (fun et : Fin s × Fin 2 => G.edge et.1 et.2)
  free : ∀ e t, ¬ G.base (G.edge e t)
  c1 : C4Free G.base
  c2 : ∀ e (t : Fin 2), (G.edge e t).1 ≠ (G.edge e t.rev).1 →
    (G.edge e t).2 ≠ (G.edge e t.rev).2 →
    G.Occupied ((G.edge e t).1, (G.edge e t.rev).2) →
    ¬ G.Occupied ((G.edge e t.rev).1, (G.edge e t).2)
  c3 : ∀ e (t : Fin 2) k l, k ≠ (G.edge e t).1 → k ≠ (G.edge e t.rev).1 →
    l ≠ (G.edge e t).2 → l ≠ (G.edge e t.rev).2 →
    G.Occupied (k,l) → G.Occupied (k,(G.edge e t).2) →
    G.Occupied (k,(G.edge e t.rev).2) →
    G.Occupied ((G.edge e t).1,l) → ¬ G.Occupied ((G.edge e t.rev).1,l)

noncomputable def Configuration.baseCount {m s} (G : Configuration m s) : ℕ :=
  Set.ncard {x | G.base x}

/-- Maximal cardinality, not merely maximal under inclusion. -/
def Limited {m s} (G : Configuration m s) : Prop :=
  ∀ B : Cell m → Prop, C4Free B → Set.ncard {x | B x} ≤ G.baseCount

/-- The structural facts about an extremal three-column base used by the
unique-full-row lemma. Their derivation from `Limited` is proved in `ZarankiewiczBase`. -/
structure BaseStructure {m s} (G : Configuration m s) : Prop where
  nonempty : ∀ r, ∃ c, G.base (r,c)
  notFull : ∀ r, ∃ c, ¬ G.base (r,c)
  pairs : ∀ a b : Fin 3, a ≠ b → ∃ r, G.base (r,a) ∧ G.base (r,b)

theorem endpoint_occupied {m s} (G : Configuration m s) (e : Fin s) (t : Fin 2) :
    G.Occupied (G.edge e t) := Or.inr ⟨e,t,rfl⟩

theorem third_column (a b : Fin 3) : ∃ l : Fin 3, l ≠ a ∧ l ≠ b := by
  fin_cases a <;> fin_cases b <;> decide

/-- The C3 exclusion applies to same-row and same-column edges as well. -/
theorem full_endpoint_unique {m s} {G : Configuration m s}
    (h : Admissible G) (hb : BaseStructure G) (e : Fin s) (t : Fin 2)
    (hf : G.Full (G.edge e t).1) (k : Fin m) (hk : G.Full k) :
    k = (G.edge e t).1 := by
  classical
  by_contra hkr
  let r := (G.edge e t).1
  let p := (G.edge e t.rev).1
  let a := (G.edge e t).2
  let b := (G.edge e t.rev).2
  have free0 : ¬ G.base (r,a) := h.free e t
  have free1 : ¬ G.base (p,b) := h.free e t.rev
  by_cases hrp : r = p
  · obtain ⟨l,hla,hlb⟩ := third_column a b
    exact h.c3 e t k l hkr (by change k ≠ p; rw [← hrp]; exact hkr)
      hla hlb (hk l) (hk a) (hk b) (hf l)
      (by change G.Occupied (p,l); rw [← hrp]; exact hf l)
  · by_cases hab : a = b
    · obtain ⟨l,hpl⟩ := hb.nonempty p
      have hla : l ≠ a := by
        intro heq
        apply free1
        simpa [heq,hab] using hpl
      obtain ⟨q,hqa,hql⟩ := hb.pairs a l (Ne.symm hla)
      have hqr : q ≠ r := by
        intro heq
        exact free0 (heq ▸ hqa)
      have hqp : q ≠ p := by
        intro heq
        apply free1
        simpa [heq,hab] using hqa
      exact h.c3 e t q l hqr hqp hla (by change l ≠ b; rw [← hab]; exact hla)
        (Or.inl hql) (Or.inl hqa)
        (by change G.Occupied (q,b); rw [← hab]; exact Or.inl hqa)
        (hf l) (Or.inl hpl)
    · have hpa : ¬ G.Occupied (p,a) := h.c2 e t hrp hab (hf b)
      have hkp : k ≠ p := by
        intro heq
        exact hpa (heq ▸ hk a)
      obtain ⟨l,hpl⟩ := hb.nonempty p
      have hla : l ≠ a := by
        intro heq
        exact hpa (Or.inl (heq ▸ hpl))
      have hlb : l ≠ b := by
        intro heq
        exact free1 (heq ▸ hpl)
      exact h.c3 e t k l hkr hkp hla hlb (hk l) (hk a) (hk b) (hf l) (Or.inl hpl)

theorem full_row_unique {m s} {G : Configuration m s}
    (h : Admissible G) (hb : BaseStructure G) (r k : Fin m)
    (hr : G.Full r) (hk : G.Full k) : k = r := by
  obtain ⟨a,ha⟩ := hb.notFull r
  obtain ⟨e,t,het⟩ := (hr a).resolve_left ha
  have her : (G.edge e t).1 = r := congrArg Prod.fst het
  have hf : G.Full (G.edge e t).1 := by simpa only [her] using hr
  simpa only [her] using full_endpoint_unique h hb e t hf k hk

/-- Counting holes after the unique-full-row lemma. -/
theorem occupied_card_le {m s} {G : Configuration m s}
    (h : Admissible G) (hb : BaseStructure G) :
    Nat.card {x : Cell m // G.Occupied x} ≤ 2*m+1 := by
  classical
  have hfull : Fintype.card {r : Fin m // G.Full r} ≤ 1 := by
    apply Fintype.card_le_one_iff_subsingleton.mpr
    exact ⟨fun a b => Subtype.ext (full_row_unique h hb b.val a.val b.property a.property)⟩
  have hex : ∀ r : {r : Fin m // ¬ G.Full r}, ∃ c, ¬ G.Occupied (r.val,c) := by
    intro r
    simpa only [Configuration.Full, not_forall] using r.property
  let f : {r : Fin m // ¬ G.Full r} → {x : Cell m // ¬ G.Occupied x} :=
    fun r => ⟨(r.val,Classical.choose (hex r)),Classical.choose_spec (hex r)⟩
  have hinj : Function.Injective f := by
    intro a b hab
    exact Subtype.ext (congrArg (fun x => x.val.1) hab)
  have hcards := Fintype.card_le_of_injective f hinj
  rw [Fintype.card_subtype_compl, Fintype.card_subtype_compl] at hcards
  have htotal := Fintype.card_subtype_le G.Occupied
  simp only [Fintype.card_fin, Fintype.card_prod] at hcards htotal
  rw [Nat.card_eq_fintype_card]
  omega

/-- Simplicity counts every ordinary edge and both halves of every 2-edge. -/
theorem base_add_halves_le {m s} {G : Configuration m s} (h : Admissible G) :
    Nat.card {x : Cell m // G.base x} + 2*s ≤ Nat.card {x : Cell m // G.Occupied x} := by
  classical
  let f : {x : Cell m // G.base x} ⊕ (Fin s × Fin 2) → {x : Cell m // G.Occupied x} :=
    fun x => match x with
    | .inl b => ⟨b.val,Or.inl b.property⟩
    | .inr et => ⟨G.edge et.1 et.2,endpoint_occupied G et.1 et.2⟩
  have hinj : Function.Injective f := by
    intro a b hab
    have heq := congrArg Subtype.val hab
    cases a with
    | inl a =>
      cases b with
      | inl b => exact congrArg Sum.inl (Subtype.ext heq)
      | inr b =>
        change a.val = G.edge b.1 b.2 at heq
        exact False.elim (h.free b.1 b.2 (heq ▸ a.property))
    | inr a =>
      cases b with
      | inl b =>
        change G.edge a.1 a.2 = b.val at heq
        exact False.elim (h.free a.1 a.2 (heq.symm ▸ b.property))
      | inr b => exact congrArg Sum.inr (h.simple heq)
  have hh := Fintype.card_le_of_injective f hinj
  simpa only [Nat.card_eq_fintype_card, Fintype.card_sum, Fintype.card_prod,
    Fintype.card_fin, Nat.mul_comm s 2] using hh

/-- The numerical upper bound, with the extremal-base facts exposed.
The remaining equivalence with `Limited` must establish these base facts. -/
theorem upper_bound_of_base_structure {m s} {G : Configuration m s}
    (h : Admissible G) (hb : BaseStructure G)
    (hsize : Nat.card {x : Cell m // G.base x} = m+3) :
    m+3+s ≤ (3*m+4)/2 := by
  have h1 := base_add_halves_le h
  have h2 := occupied_card_le h hb
  rw [hsize] at h1
  omega

#print axioms full_row_unique
end MathLean.Zarankiewicz
