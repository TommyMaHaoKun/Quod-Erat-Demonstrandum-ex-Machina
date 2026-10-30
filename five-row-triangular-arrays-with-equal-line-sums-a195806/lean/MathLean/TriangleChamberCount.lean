import MathLean.TriangleChambers

namespace MathLean.Triangle
open scoped BigOperators

abbrev Lattice (n : ℕ) := {z : Difference n × Difference n //
  normA z.1.val z.2.val ≤ n ∧ normB z.1.val z.2.val ≤ n}

abbrev Chamber (n : ℕ) := {z : Fin (n+1) × Fin (n+1) × Fin 12 //
  3*z.1.val+2*z.2.1.val ≤ n ∧ ChamberValid z.1.val z.2.1.val z.2.2}

instance (h k : ℕ) (t : Fin 12) : Decidable (ChamberValid h k t) :=
  inferInstanceAs (Decidable ((t.val<6 ∨ (0<h ∧ 0<k)) ∧ (h=0 ∧ k=0 → t.val=0)))

noncomputable instance (n : ℕ) : Fintype (Chamber n) := Fintype.ofFinite _

theorem norm_bounds (n : ℕ) (p q : ℤ) (ha : normA p q ≤ n) (hb : normB p q ≤ n) :
    -(n : ℤ) ≤ p ∧ p ≤ n ∧ -(n : ℤ) ≤ q ∧ q ≤ n := by
  simp only [normA, normB, abs_eq_max_neg] at ha hb
  omega

def chamberToLattice (n : ℕ) (z : Chamber n) : Lattice n := by
  let v := orbit z.val.1.val z.val.2.1.val z.val.2.2
  have he := orbit_norms z.val.1.val z.val.2.1.val z.val.2.2
  have ha : normA v.1 (v.2-v.1) ≤ n := by change normA _ _ ≤ _; rw [he.1]; omega
  have hb : normB v.1 (v.2-v.1) ≤ n := by change normB _ _ ≤ _; rw [he.2]; omega
  have hd := norm_bounds n v.1 (v.2-v.1) ha hb
  exact ⟨(⟨v.1, hd.1, hd.2.1⟩, ⟨v.2-v.1, hd.2.2.1, hd.2.2.2⟩), ha, hb⟩

theorem chamberToLattice_injective (n : ℕ) : Function.Injective (chamberToLattice n) := by
  intro z w he
  have hx := congrArg (fun v : Lattice n => v.val.1.val) he
  have hq := congrArg (fun v : Lattice n => v.val.2.val) he
  change (orbit _ _ _).1 = (orbit _ _ _).1 at hx
  change (orbit _ _ _).2-(orbit _ _ _).1 = (orbit _ _ _).2-(orbit _ _ _).1 at hq
  have ho : orbit z.val.1.val z.val.2.1.val z.val.2.2 =
      orbit w.val.1.val w.val.2.1.val w.val.2.2 := Prod.ext hx (by omega)
  obtain ⟨hh, hk, ht⟩ := orbit_injective _ _ _ _ _ _ z.property.2 w.property.2 ho
  apply Subtype.ext
  exact Prod.ext (Fin.ext hh) (Prod.ext (Fin.ext hk) ht)

theorem chamberToLattice_surjective (n : ℕ) : Function.Surjective (chamberToLattice n) := by
  intro z
  obtain ⟨h,k,t,hvalid,hor⟩ := orbit_surjective z.val.1.val (z.val.1.val+z.val.2.val)
  have hn := (orbit_norms h k t).2
  rw [hor] at hn
  simp only [Prod.fst, Prod.snd, add_sub_cancel_left] at hn
  have hc : 3*h+2*k ≤ n := by have hz := z.property.2; omega
  let w : Chamber n := ⟨(⟨h,by omega⟩,⟨k,by omega⟩,t), hc, hvalid⟩
  refine ⟨w, ?_⟩
  apply Subtype.ext
  apply Prod.ext <;> apply Subtype.ext
  · change (orbit h k t).1 = z.val.1.val
    rw [hor]
  · change (orbit h k t).2-(orbit h k t).1 = z.val.2.val
    rw [hor]
    simp

noncomputable def chamberEquiv (n : ℕ) : Chamber n ≃ Lattice n :=
  Equiv.ofBijective (chamberToLattice n)
    ⟨chamberToLattice_injective n, chamberToLattice_surjective n⟩

theorem sum_restrict {α : Type*} [Fintype α] (p : α → Prop) [DecidablePred p]
    (f : α → ℕ) (hf : ∀ a, ¬p a → f a=0) :
    (∑ a, f a) = ∑ a : {a // p a}, f a.val := by
  rw [← Fintype.sum_subtype_add_sum_subtype p f]
  have hz : (∑ a : {a // ¬p a}, f a.val) = 0 :=
    Finset.sum_eq_zero fun a _ => hf a.val a.property
  rw [hz, add_zero]

theorem original_supported_count (n : ℕ) : Nat.card (Arrays n) =
    ∑ z : Lattice n, latticeWeight n z.val.1.val z.val.2.val := by
  rw [original_lattice_count]
  rw [← Fintype.sum_prod_type (fun z : Difference n × Difference n => latticeWeight n z.1.val z.2.val)]
  exact sum_restrict _ _ (fun z hz => weight_outside n z.1.val z.2.val hz)

def chamberWeight (n h k : ℕ) : ℕ :=
  (n+1-(2*h+k))^2 * (n+1-(3*h+2*k))^2

theorem orbit_weight (n h k : ℕ) (t : Fin 12) :
    latticeWeight n (orbit h k t).1 ((orbit h k t).2-(orbit h k t).1) =
      chamberWeight n h k := by
  rw [latticeWeight, (orbit_norms h k t).1, (orbit_norms h k t).2]
  have ha : ((n : ℤ)+1-(2*h+k)).toNat = n+1-(2*h+k) := by omega
  have hb : ((n : ℤ)+1-(3*h+2*k)).toNat = n+1-(3*h+2*k) := by omega
  rw [ha,hb]
  rfl

theorem original_chamber_type_count (n : ℕ) : Nat.card (Arrays n) =
    ∑ z : Chamber n, chamberWeight n z.val.1.val z.val.2.1.val := by
  rw [original_supported_count, ← (chamberEquiv n).sum_comp]
  apply Finset.sum_congr rfl
  intro z hz
  exact orbit_weight n z.val.1.val z.val.2.1.val z.val.2.2

theorem sum_tags (h k w : ℕ) :
    (∑ t : Fin 12, if ChamberValid h k t then w else 0) = multiplicity h k*w := by
  classical
  by_cases hh : h=0 <;> by_cases hk : k=0 <;>
    simp [ChamberValid, multiplicity, hh, hk, Nat.pos_iff_ne_zero, Fin.sum_univ_succ] <;> omega

def chamberSum (n : ℕ) : ℕ := ∑ h : Fin (n+1), ∑ k : Fin (n+1),
  if 3*h.val+2*k.val ≤ n then multiplicity h.val k.val * chamberWeight n h.val k.val else 0

theorem original_chamber_count (n : ℕ) : Nat.card (Arrays n) = chamberSum n := by
  classical
  rw [original_chamber_type_count]
  have hs : (∑ z ∈ Finset.univ.filter
      (fun z : Fin (n+1) × Fin (n+1) × Fin 12 =>
        3*z.1.val+2*z.2.1.val ≤ n ∧ ChamberValid z.1.val z.2.1.val z.2.2),
      chamberWeight n z.1.val z.2.1.val) =
      ∑ z : Chamber n, chamberWeight n z.val.1.val z.val.2.1.val := Finset.sum_subtype
    (Finset.univ.filter (fun z : Fin (n+1) × Fin (n+1) × Fin 12 =>
      3*z.1.val+2*z.2.1.val ≤ n ∧ ChamberValid z.1.val z.2.1.val z.2.2))
    (by intro z; simp)
    (fun z => chamberWeight n z.1.val z.2.1.val)
  rw [← hs, Finset.sum_filter]
  simp only [Fintype.sum_prod_type, chamberSum]
  apply Finset.sum_congr rfl
  intro h hh
  apply Finset.sum_congr rfl
  intro k hk
  by_cases hc : 3*h.val+2*k.val ≤ n
  · simp only [hc, true_and, ite_true]
    exact sum_tags h.val k.val _
  · simp [hc]

end MathLean.Triangle
