import MathLean.Zarankiewicz
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.NormNum

namespace MathLean.Zarankiewicz
open scoped BigOperators
noncomputable section
attribute [local instance] Classical.propDecidable
set_option maxRecDepth 10000
set_option maxHeartbeats 0

def degree {m} (B : Cell m → Prop) (r : Fin m) : ℕ := by
  classical
  exact (if B (r,0) then 1 else 0)+(if B (r,1) then 1 else 0)+(if B (r,2) then 1 else 0)

def pairDegree {m} (B : Cell m → Prop) (r : Fin m) : ℕ := by
  classical
  exact (if B (r,0) ∧ B (r,1) then 1 else 0)+
    (if B (r,0) ∧ B (r,2) then 1 else 0)+(if B (r,1) ∧ B (r,2) then 1 else 0)

theorem degree_le {m} (B : Cell m → Prop) (r : Fin m) : degree B r ≤ 1+pairDegree B r := by
  classical
  by_cases h0 : B (r,0) <;> by_cases h1 : B (r,1) <;> by_cases h2 : B (r,2) <;>
    simp [degree,pairDegree,h0,h1,h2]

theorem cardinal_eq_sum_degree {m} (B : Cell m → Prop) :
    Nat.card {x : Cell m // B x} = ∑ r, degree B r := by
  classical
  rw [Nat.card_eq_fintype_card, Fintype.card_subtype, Finset.card_filter,
    Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro r _
  simp only [degree, Fin.sum_univ_succ, Fin.sum_univ_zero, add_zero, add_assoc]
  rfl

theorem pair_count_le_one {m} {B : Cell m → Prop} (h : C4Free B)
    (a b : Fin 3) (hab : a ≠ b) :
    ∑ r : Fin m, (if B (r,a) ∧ B (r,b) then 1 else 0 : ℕ) ≤ 1 := by
  classical
  rw [← Finset.card_filter]
  apply Finset.card_le_one.mpr
  intro r hr p hp
  have hr' := (Finset.mem_filter.mp hr).2
  have hp' := (Finset.mem_filter.mp hp).2
  by_contra hrp
  exact h r p a b hrp hab hr'.1 hr'.2 hp'.1 hp'.2

theorem pair_degree_sum_le {m} {B : Cell m → Prop} (h : C4Free B) :
    ∑ r, pairDegree B r ≤ 3 := by
  classical
  have h01 := pair_count_le_one h 0 1 (by decide)
  have h02 := pair_count_le_one h 0 2 (by decide)
  have h12 := pair_count_le_one h 1 2 (by decide)
  simp only [pairDegree, Finset.sum_add_distrib]
  omega

/-- The classical three-column Zarankiewicz upper bound. -/
theorem classical_upper_bound {m} {B : Cell m → Prop} (h : C4Free B) :
    Nat.card {x : Cell m // B x} ≤ m+3 := by
  rw [cardinal_eq_sum_degree]
  have h1 := Finset.sum_le_sum (s := Finset.univ) (fun r _ => degree_le B r)
  have h2 := pair_degree_sum_le h
  simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, smul_eq_mul, mul_one] at h1
  omega

theorem degree_eq_of_extremal {m} {B : Cell m → Prop} (h : C4Free B)
    (hsize : Nat.card {x : Cell m // B x} = m+3) (r : Fin m) :
    degree B r = 1+pairDegree B r := by
  have hle := degree_le B r
  apply Nat.le_antisymm hle
  by_contra hn
  have hlt : degree B r < 1+pairDegree B r := by omega
  have hs := Finset.sum_lt_sum (s := Finset.univ) (fun t _ => degree_le B t)
    ⟨r,Finset.mem_univ _,hlt⟩
  have hp := pair_degree_sum_le h
  rw [← cardinal_eq_sum_degree,hsize] at hs
  simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, smul_eq_mul, mul_one] at hs
  omega

theorem pair_sum_eq_of_extremal {m} {B : Cell m → Prop} (h : C4Free B)
    (hsize : Nat.card {x : Cell m // B x} = m+3) : ∑ r, pairDegree B r = 3 := by
  have hd := cardinal_eq_sum_degree B
  simp_rw [degree_eq_of_extremal h hsize] at hd
  simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, smul_eq_mul, mul_one, hsize] at hd
  omega

/-- At m+3 edges, the ordinary C4-free base has all the structural facts
needed by the unique-full-row argument. -/
theorem base_structure_of_size {m s} {G : Configuration m s} (h : C4Free G.base)
    (hsize : Nat.card {x : Cell m // G.base x} = m+3) : BaseStructure G := by
  classical
  have hlocal := degree_eq_of_extremal h hsize
  have hsum := pair_sum_eq_of_extremal h hsize
  have h01 := pair_count_le_one h 0 1 (by decide)
  have h02 := pair_count_le_one h 0 2 (by decide)
  have h12 := pair_count_le_one h 1 2 (by decide)
  simp only [pairDegree, Finset.sum_add_distrib] at hsum
  have e01 : ∑ r : Fin m, (if G.base (r,0) ∧ G.base (r,1) then 1 else 0 : ℕ) = 1 := by omega
  have e02 : ∑ r : Fin m, (if G.base (r,0) ∧ G.base (r,2) then 1 else 0 : ℕ) = 1 := by omega
  have e12 : ∑ r : Fin m, (if G.base (r,1) ∧ G.base (r,2) then 1 else 0 : ℕ) = 1 := by omega
  have existsPair (a b : Fin 3)
      (he : ∑ r : Fin m, (if G.base (r,a) ∧ G.base (r,b) then 1 else 0 : ℕ) = 1) :
      ∃ r, G.base (r,a) ∧ G.base (r,b) := by
    by_contra hn
    push_neg at hn
    have hz : ∑ r : Fin m, (if G.base (r,a) ∧ G.base (r,b) then 1 else 0 : ℕ) = 0 := by
      apply Finset.sum_eq_zero
      intro r _
      exact if_neg (fun hh => hn r hh.1 hh.2)
    omega
  refine ⟨?_,?_,?_⟩
  · intro r
    by_contra hn
    push_neg at hn
    have hh := hlocal r
    simp [degree,pairDegree,hn] at hh
  · intro r
    by_contra hn
    push_neg at hn
    have hh := hlocal r
    simp [degree,pairDegree,hn] at hh
  · intro a b hab
    have p01 := existsPair 0 1 e01
    have p02 := existsPair 0 2 e02
    have p12 := existsPair 1 2 e12
    fin_cases a <;> fin_cases b
    all_goals first | exact False.elim (hab rfl) | exact p01 | exact p02 | exact p12 |
      (obtain ⟨r,hr,hq⟩ := p01; exact ⟨r,hq,hr⟩) |
      (obtain ⟨r,hr,hq⟩ := p02; exact ⟨r,hq,hr⟩) |
      (obtain ⟨r,hr,hq⟩ := p12; exact ⟨r,hq,hr⟩)

theorem upper_bound_of_base_size {m s} {G : Configuration m s}
    (h : Admissible G) (hsize : Nat.card {x : Cell m // G.base x} = m+3) :
    m+3+s ≤ (3*m+4)/2 :=
  upper_bound_of_base_structure h (base_structure_of_size h.c1 hsize) hsize

/-- A C4-free base attaining m+3 cells, for every m at least three. -/
theorem exists_classical_base {m : ℕ} (hm : 3 ≤ m) :
    ∃ B : Cell m → Prop, C4Free B ∧ Nat.card {x : Cell m // B x} = m+3 := by
  classical
  let f : Fin m ⊕ Fin 3 → Cell m := fun z => match z with
    | .inl r => (r,if r.val=0 then 1 else 0)
    | .inr i => (⟨i.val,lt_of_lt_of_le i.isLt hm⟩,if i.val=2 then 1 else 2)
  have hf : Function.Injective f := by
    intro a b heq
    have hr := congrArg (fun x => x.1.val) heq
    have hc := congrArg (fun x => x.2.val) heq
    cases a with
    | inl a =>
      cases b with
      | inl b => exact congrArg Sum.inl (Fin.ext hr)
      | inr b =>
        exfalso
        fin_cases b <;> dsimp [f] at hr hc <;> split_ifs at hc <;> norm_num at hc <;> omega
    | inr a =>
      cases b with
      | inr b => exact congrArg Sum.inr (Fin.ext hr)
      | inl b =>
        exfalso
        fin_cases a <;> dsimp [f] at hr hc <;> split_ifs at hc <;> norm_num at hc <;> omega
  let shape (x : Cell m) := (x.1.val<3 ∧ x.1.val≠x.2.val) ∨ (3≤x.1.val ∧ x.2=0)
  have hshape : ∀ z, shape (f z) := by
    intro z
    cases z with
    | inl r =>
      dsimp [shape,f]
      split_ifs <;> simp_all <;> omega
    | inr i => fin_cases i <;> simp [shape,f]
  refine ⟨Set.range f,?_,?_⟩
  · intro r p a b hrp hab hra hrb hpa hpb
    have ra : shape (r,a) := by obtain ⟨z,hz⟩ := hra; exact hz ▸ hshape z
    have rb : shape (r,b) := by obtain ⟨z,hz⟩ := hrb; exact hz ▸ hshape z
    have pa : shape (p,a) := by obtain ⟨z,hz⟩ := hpa; exact hz ▸ hshape z
    have pb : shape (p,b) := by obtain ⟨z,hz⟩ := hpb; exact hz ▸ hshape z
    have hrp' : r.val ≠ p.val := fun hh => hrp (Fin.ext hh)
    have hab' : a.val ≠ b.val := fun hh => hab (Fin.ext hh)
    fin_cases a <;> fin_cases b <;> dsimp [shape] at ra rb pa pb hab' <;> omega
  · change Nat.card (Set.range f) = m+3
    rw [← Nat.card_congr (Equiv.ofInjective f hf)]
    simp only [Nat.card_eq_fintype_card,Fintype.card_sum,Fintype.card_fin]

theorem limited_base_size {m s} {G : Configuration m s} (hm : 3 ≤ m)
    (h : C4Free G.base) (hl : Limited G) : Nat.card {x : Cell m // G.base x} = m+3 := by
  obtain ⟨B,hB,hsize⟩ := exists_classical_base hm
  have hlo := hl B hB
  have hhi := classical_upper_bound h
  have hn (P : Cell m → Prop) : Set.ncard {x | P x} = Nat.card {x : Cell m // P x} := by
    rw [← Set.Nat.card_coe_set_eq]
    rfl
  unfold Configuration.baseCount at hlo
  rw [hn,hn,hsize] at hlo
  exact Nat.le_antisymm hhi hlo

/-- The upper half of z_L(m,3)=floor((3m+4)/2), directly from Definition 1. -/
theorem limited_upper_bound {m s} {G : Configuration m s} (hm : 3 ≤ m)
    (h : Admissible G) (hl : Limited G) :
    G.baseCount+s ≤ (3*m+4)/2 := by
  have hs := limited_base_size hm h.c1 hl
  have hb := upper_bound_of_base_size h hs
  have hn : G.baseCount = Nat.card {x : Cell m // G.base x} := by
    unfold Configuration.baseCount
    rw [← Set.Nat.card_coe_set_eq]
    rfl
  simpa only [hn,hs] using hb

#print axioms limited_upper_bound

end
end MathLean.Zarankiewicz
