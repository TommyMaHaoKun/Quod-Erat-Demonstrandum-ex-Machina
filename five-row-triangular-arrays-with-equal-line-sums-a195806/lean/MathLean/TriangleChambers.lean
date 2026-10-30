import MathLean.TriangleLatticeCount

namespace MathLean.Triangle

/-- Twelve images of (h+k,h). Boundary images are retained only once. -/
def orbit (h k : ℕ) : Fin 12 → ℤ × ℤ :=
  ![((h:ℤ)+k,h), (-(h:ℤ),2*(h:ℤ)+k), (-2*(h:ℤ)-k,(h:ℤ)+k),
    (-(h:ℤ)-k,-(h:ℤ)), ((h:ℤ),-2*(h:ℤ)-k), (2*(h:ℤ)+k,-(h:ℤ)-k),
    ((h:ℤ),(h:ℤ)+k), (-(h:ℤ)-k,2*(h:ℤ)+k), (-2*(h:ℤ)-k,(h:ℤ)),
    (-(h:ℤ),-(h:ℤ)-k), ((h:ℤ)+k,-2*(h:ℤ)-k), (2*(h:ℤ)+k,-(h:ℤ))]

def ChamberValid (h k : ℕ) (t : Fin 12) : Prop :=
  (t.val < 6 ∨ (0<h ∧ 0<k)) ∧ (h=0 ∧ k=0 → t.val=0)

def multiplicity (h k : ℕ) : ℕ :=
  if h=0 ∧ k=0 then 1 else if h=0 ∨ k=0 then 6 else 12

theorem chamberValid_iff (h k : ℕ) (t : Fin 12) :
    ChamberValid h k t ↔ t.val < multiplicity h k := by
  unfold ChamberValid multiplicity
  split_ifs <;> omega

set_option maxHeartbeats 2000000 in
theorem orbit_injective (h k h' k' : ℕ) (t t' : Fin 12)
    (ht : ChamberValid h k t) (ht' : ChamberValid h' k' t')
    (he : orbit h k t = orbit h' k' t') : h=h' ∧ k=k' ∧ t=t' := by
  fin_cases t <;> fin_cases t' <;>
    simp [orbit, ChamberValid, Matrix.cons_val, Prod.mk.injEq] at * <;> omega

theorem orbit_surjective (x y : ℤ) : ∃ h k : ℕ, ∃ t : Fin 12,
    ChamberValid h k t ∧ orbit h k t=(x,y) := by
  by_cases hz : x=0 ∧ y=0
  · refine ⟨0,0,0,?_,?_⟩ <;> simp [ChamberValid, orbit, hz.1, hz.2]
  have hc :
      (0≤y ∧ y≤x) ∨ (x≤0 ∧ -2*x≤y) ∨ (x+y≤0 ∧ 0≤x+2*y) ∨
      (y≤0 ∧ x≤y) ∨ (0≤x ∧ y≤-2*x) ∨ (0≤x+y ∧ x+2*y≤0) ∨
      (0<x ∧ x<y) ∨ (0<x+y ∧ 2*x+y<0) ∨ (0<y ∧ x< -2*y) ∨
      (x<0 ∧ y<x) ∨ (x+y<0 ∧ 0<2*x+y) ∨ (y<0 ∧ -2*y<x) := by omega
  rcases hc with h|h|h|h|h|h|h|h|h|h|h|h
  · refine ⟨y.toNat,(x-y).toNat,0,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨(-x).toNat,(y+2*x).toNat,1,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨(-x-y).toNat,(x+2*y).toNat,2,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨(-y).toNat,(y-x).toNat,3,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨x.toNat,(-y-2*x).toNat,4,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨(x+y).toNat,(-x-2*y).toNat,5,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨x.toNat,(y-x).toNat,6,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨(x+y).toNat,(-2*x-y).toNat,7,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨y.toNat,(-x-2*y).toNat,8,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨(-x).toNat,(x-y).toNat,9,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨(-x-y).toNat,(2*x+y).toNat,10,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega
  · refine ⟨(-y).toNat,(x+2*y).toNat,11,?_,?_⟩
    · simp [ChamberValid] <;> omega
    · simp [orbit, Matrix.cons_val] <;> omega

set_option maxHeartbeats 800000 in
theorem orbit_norms (h k : ℕ) (t : Fin 12) :
    normA (orbit h k t).1 ((orbit h k t).2-(orbit h k t).1) = 2*h+k ∧
    normB (orbit h k t).1 ((orbit h k t).2-(orbit h k t).1) = 3*h+2*k := by
  fin_cases t <;> dsimp [orbit] <;>
    simp only [normA, normB, abs_eq_max_neg] <;> omega

end MathLean.Triangle
