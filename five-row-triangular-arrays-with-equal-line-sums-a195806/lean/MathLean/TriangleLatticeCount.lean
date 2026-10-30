import MathLean.TriangleBases

namespace MathLean.Triangle
open scoped BigOperators

abbrev Difference (n : ℕ) := Set.Icc (-(n : ℤ)) (n : ℤ)
abbrev FiberTotal (n : ℕ) := Σ p : Difference n, Σ q : Difference n, Fiber n p.val q.val

def fiberEquiv (n : ℕ) : {v : Parameters // Bounded n (parameterMap v)} ≃ FiberTotal n where
  toFun v := by
    have hd := parameters_difference_bounds n v.val v.property
    have hb := (bounded_parameter_iff n v.val).mp v.property
    exact ⟨⟨v.val.p, hd.1, hd.2.1⟩, ⟨v.val.q, hd.2.2.1, hd.2.2.2⟩,
      ⟨v.val.a, hb.1⟩, ⟨v.val.c, hb.2.1⟩, ⟨v.val.e, hb.2.2.1⟩, ⟨v.val.f, hb.2.2.2⟩⟩
  invFun v :=
    ⟨⟨v.2.2.1.val, v.2.2.2.1.val, v.2.2.2.2.1.val, v.2.2.2.2.2.val, v.1.val, v.2.1.val⟩,
      (bounded_parameter_iff n _).mpr
        ⟨v.2.2.1.property, v.2.2.2.1.property, v.2.2.2.2.1.property, v.2.2.2.2.2.property⟩⟩
  left_inv v := by apply Subtype.ext; rfl
  right_inv v := by
    rcases v with ⟨⟨p, hp⟩, ⟨q, hq⟩, ⟨a, ha⟩, ⟨c, hc⟩, ⟨e, he⟩, ⟨f, hf⟩⟩
    rfl

def latticeWeight (n : ℕ) (p q : ℤ) : ℕ :=
  ((n : ℤ)+1-normA p q).toNat^2 * ((n : ℤ)+1-normB p q).toNat^2

theorem original_lattice_count (n : ℕ) :
    Nat.card (Arrays n) = ∑ p : Difference n, ∑ q : Difference n,
      latticeWeight n p.val q.val := by
  rw [Nat.card_congr ((parameterEquiv n).trans (fiberEquiv n))]
  rw [Nat.card_eq_fintype_card]
  simp only [FiberTotal, Fintype.card_sigma, card_fiber, latticeWeight]

theorem weight_outside (n : ℕ) (p q : ℤ)
    (h : ¬ (normA p q ≤ n ∧ normB p q ≤ n)) : latticeWeight n p q = 0 := by
  unfold latticeWeight
  by_cases ha : normA p q ≤ n
  · have hb : ¬ normB p q ≤ n := fun hb => h ⟨ha, hb⟩
    have hz : ((n : ℤ)+1-normB p q).toNat = 0 := by omega
    simp [hz]
  · have hz : ((n : ℤ)+1-normA p q).toNat = 0 := by omega
    simp [hz]

end MathLean.Triangle
