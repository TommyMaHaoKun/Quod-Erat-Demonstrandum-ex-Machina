import MathLean.ZarankiewiczBase
import Mathlib.Tactic.NormNum

namespace MathLean.Zarankiewicz
noncomputable section
attribute [local instance] Classical.propDecidable
set_option maxHeartbeats 0
set_option maxRecDepth 10000

def constructionBase (h : ℕ) (ε : Fin 2) (x : Cell (2*h+ε.val+3)) : Prop :=
  if x.1.val<3 then x.1.val ≠ x.2.val else
    if x.1.val<3+2*h ∧ x.1.val%2=1 then x.2=2 else x.2=0

def constructionEdge (h : ℕ) (ε : Fin 2) (e : Fin (h+ε.val)) (t : Fin 2) :
    Cell (2*h+ε.val+3) :=
  if hi : e.val<h then
    if t=0 then (⟨3+2*e.val,by omega⟩,1) else (⟨4+2*e.val,by omega⟩,2)
  else
    if t=0 then (⟨2,by omega⟩,2) else (⟨3+2*h,by have := e.isLt; have := ε.isLt; omega⟩,1)

def construction (h : ℕ) (ε : Fin 2) : Configuration (2*h+ε.val+3) (h+ε.val) :=
  ⟨constructionBase h ε,constructionEdge h ε⟩

theorem construction_simple (h : ℕ) (ε : Fin 2) :
    Function.Injective (fun et : Fin (h+ε.val) × Fin 2 => constructionEdge h ε et.1 et.2) := by
  intro x y heq
  rcases x with ⟨i,t⟩
  rcases y with ⟨j,u⟩
  have hr := congrArg (fun x => x.1.val) heq
  have hc := congrArg (fun x => x.2.val) heq
  have hi := i.isLt
  have hj := j.isLt
  have he := ε.isLt
  apply Prod.ext <;> apply Fin.ext
  all_goals fin_cases t <;> fin_cases u <;>
    dsimp [constructionEdge] at hr hc <;> split_ifs at hr hc <;> norm_num at hr hc ⊢ <;> omega

theorem construction_free (h : ℕ) (ε : Fin 2) (e : Fin (h+ε.val)) (t : Fin 2) :
    ¬ constructionBase h ε (constructionEdge h ε e t) := by
  have hi := e.isLt
  have he := ε.isLt
  fin_cases t <;> unfold constructionEdge <;> split_ifs <;>
    simp_all [constructionBase] <;> omega

theorem construction_c4free (h : ℕ) (ε : Fin 2) : C4Free (constructionBase h ε) := by
  intro r p a b hrp hab hra hrb hpa hpb
  have hrp' : r.val ≠ p.val := fun hh => hrp (Fin.ext hh)
  by_cases hr : r.val<3
  · by_cases hp : p.val<3
    · simp only [constructionBase,if_pos hr,if_pos hp] at hra hrb hpa hpb
      have hab' : a.val ≠ b.val := fun hh => hab (Fin.ext hh)
      have ha := a.isLt
      have hb := b.isLt
      omega
    · simp only [constructionBase,if_neg hp] at hpa hpb
      split_ifs at hpa hpb <;> exact hab (hpa.trans hpb.symm)
  · simp only [constructionBase,if_neg hr] at hra hrb
    split_ifs at hra hrb <;> exact hab (hra.trans hrb.symm)

def constructionPattern (h : ℕ) (ε : Fin 2) (x : Cell (2*h+ε.val+3)) : Prop :=
  (x.1.val=0 ∧ x.2.val≠0) ∨ (x.1.val=1 ∧ x.2.val≠1) ∨
  (x.1.val=2 ∧ (x.2.val≠2 ∨ ε.val=1)) ∨
  (3≤x.1.val ∧ x.1.val<3+2*h ∧
    ((x.1.val%2=1 ∧ x.2.val≠0) ∨ (x.1.val%2=0 ∧ x.2.val≠1))) ∨
  (x.1.val=3+2*h ∧ ε.val=1 ∧ x.2.val≠2)

theorem construction_occupied_pattern (h : ℕ) (ε : Fin 2)
    (x : Cell (2*h+ε.val+3)) (hx : (construction h ε).Occupied x) :
    constructionPattern h ε x := by
  have he := ε.isLt
  rcases hx with hb | ⟨i,t,hit⟩
  · change constructionBase h ε x at hb
    have hr := x.1.isLt
    have hc := x.2.isLt
    unfold constructionBase at hb
    unfold constructionPattern
    split_ifs at hb <;> omega
  · rw [← hit]
    have hi := i.isLt
    change constructionPattern h ε (constructionEdge h ε i t)
    fin_cases t <;> unfold constructionEdge <;> split_ifs <;>
      simp_all [constructionPattern] <;> omega

theorem construction_admissible (h : ℕ) (ε : Fin 2) : Admissible (construction h ε) := by
  refine ⟨construction_simple h ε,construction_free h ε,construction_c4free h ε,?_,?_⟩
  · intro e t hr hc ho hp
    have hO := construction_occupied_pattern h ε _ ho
    have hP := construction_occupied_pattern h ε _ hp
    have hi := e.isLt
    have he := ε.isLt
    clear hr hc ho hp
    fin_cases t <;> dsimp [construction,constructionEdge] at hO hP <;>
      split_ifs at hO hP <;> norm_num [constructionPattern] at hO hP <;> omega
  · intro e t k l hk0 hk1 hl0 hl1 hkl hka hkb hal hbl
    have o0 := construction_occupied_pattern h ε _ hkl
    have o1 := construction_occupied_pattern h ε _ hka
    have o2 := construction_occupied_pattern h ε _ hkb
    have o3 := construction_occupied_pattern h ε _ hal
    have o4 := construction_occupied_pattern h ε _ hbl
    have hi := e.isLt
    have he := ε.isLt
    have hk := k.isLt
    have hl := l.isLt
    have kr0 : k.val ≠ ((construction h ε).edge e t).1.val := fun hh => hk0 (Fin.ext hh)
    have kr1 : k.val ≠ ((construction h ε).edge e t.rev).1.val := fun hh => hk1 (Fin.ext hh)
    have lc0 : l.val ≠ ((construction h ε).edge e t).2.val := fun hh => hl0 (Fin.ext hh)
    have lc1 : l.val ≠ ((construction h ε).edge e t.rev).2.val := fun hh => hl1 (Fin.ext hh)
    clear hk0 hk1 hl0 hl1 hkl hka hkb hal hbl
    fin_cases t <;> dsimp [construction,constructionEdge] at o1 o2 o3 o4 kr0 kr1 lc0 lc1 <;>
      split_ifs at o1 o2 o3 o4 kr0 kr1 lc0 lc1 <;>
      norm_num [constructionPattern, -Fin.val_eq_zero_iff] at o0 o1 o2 o3 o4 kr0 kr1 lc0 lc1 <;> omega

theorem construction_base_size (h : ℕ) (ε : Fin 2) :
    Nat.card {x : Cell (2*h+ε.val+3) // constructionBase h ε x} = (2*h+ε.val+3)+3 := by
  rw [cardinal_eq_sum_degree]
  have hd (r : Fin (2*h+ε.val+3)) :
      degree (constructionBase h ε) r = if r.val<3 then 2 else 1 := by
    by_cases hr : r.val<3
    · have cases3 : r.val=0 ∨ r.val=1 ∨ r.val=2 := by omega
      rcases cases3 with hh|hh|hh <;> simp [degree,constructionBase,hr,hh]
    · by_cases ht : r.val<3+2*h ∧ r.val%2=1 <;>
        simp [degree,constructionBase,hr,ht]
  have tail (x : ℕ) : (if x+1+1+1<3 then 2 else 1 : ℕ) = 1 := by split_ifs <;> omega
  simp_rw [hd]
  simp (disch := omega) [Fin.sum_univ_succ,Fin.val_zero,Fin.val_succ]
  simp only [tail,Finset.sum_const,Finset.card_univ,Fintype.card_fin,smul_eq_mul,mul_one]
  omega

theorem construction_limited (h : ℕ) (ε : Fin 2) : Limited (construction h ε) := by
  intro B hB
  have hb := classical_upper_bound hB
  have hs := construction_base_size h ε
  unfold Configuration.baseCount
  rw [← Set.Nat.card_coe_set_eq,← Set.Nat.card_coe_set_eq]
  change Nat.card {x // B x} ≤ Nat.card {x // constructionBase h ε x}
  rw [hs]
  exact hb

theorem construction_value (h : ℕ) (ε : Fin 2) :
    (construction h ε).baseCount + (h+ε.val) = (3*(2*h+ε.val+3)+4)/2 := by
  unfold Configuration.baseCount
  rw [← Set.Nat.card_coe_set_eq]
  change Nat.card {x // constructionBase h ε x} + (h+ε.val) = _
  rw [construction_base_size]
  have he := ε.isLt
  omega

def attainableValues (m : ℕ) : Set ℕ :=
  {v | ∃ s, ∃ G : Configuration m s, Admissible G ∧ Limited G ∧ G.baseCount+s=v}

/-- Exact strong limited augmented Zarankiewicz number for three columns.
`IsGreatest` states both attainability and the universal upper bound, so
this is precisely the assertion that the maximum is floor((3m+4)/2). -/
theorem zarankiewicz_exact (m : ℕ) (hm : 3 ≤ m) :
    IsGreatest (attainableValues m) ((3*m+4)/2) := by
  constructor
  · have repr : ∃ h : ℕ, ∃ ε : Fin 2, m=2*h+ε.val+3 := by
      refine ⟨(m-3)/2,⟨(m-3)%2,by omega⟩,?_⟩
      dsimp
      omega
    obtain ⟨h,ε,rfl⟩ := repr
    exact ⟨h+ε.val,construction h ε,construction_admissible h ε,
      construction_limited h ε,construction_value h ε⟩
  · intro v hv
    obtain ⟨s,G,ha,hl,rfl⟩ := hv
    exact limited_upper_bound hm ha hl

#print axioms zarankiewicz_exact
end
end MathLean.Zarankiewicz



