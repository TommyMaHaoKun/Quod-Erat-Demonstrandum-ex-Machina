import MathLean.Riesz

namespace MathLean.Riesz
open Real
noncomputable section

def halfChord (φ ψ : ℝ) : ℝ := sin ((φ-ψ)/2)^2

theorem halfChord_identity (φ ψ : ℝ) :
    halfChord φ ψ + halfChord φ (-ψ) - sin φ^2 =
      -2*cos φ*sin ((φ-ψ)/2)*sin ((φ+ψ)/2) := by
  have h1 := sin_sq_eq_half_sub ((φ-ψ)/2)
  have h2 := sin_sq_eq_half_sub ((φ+ψ)/2)
  have h3 := sin_sq_add_cos_sq φ
  have h4 := cos_sub_cos φ ψ
  have h4m := congrArg (fun x : ℝ => cos φ*x) h4
  rw [show 2*((φ-ψ)/2)=φ-ψ by ring, cos_sub] at h1
  rw [show 2*((φ+ψ)/2)=φ+ψ by ring, cos_add] at h2
  unfold halfChord
  rw [show φ- -ψ=φ+ψ by ring]
  nlinarith only [h1,h2,h3,h4m]

/-- Chord ordering, positivity, and the product identity on Fan's arc. -/
theorem halfChord_geometry {φ ψ : ℝ} (hφ : π/2 < φ) (hφ' : φ ≤ 2*π/3)
    (hψ : 0 ≤ ψ) (hψ' : ψ ≤ 2*π-3*φ) :
    let p := halfChord φ ψ
    let q := halfChord φ (-ψ)
    let s := sin φ^2
    let k := p+q-s
    0 < k ∧ k ≤ p ∧ p ≤ q ∧ q ≤ s ∧ k^2=4*cos φ^2*p*q := by
  have hπ := pi_pos
  have hθ1 : 0 < (φ-ψ)/2 := by linarith
  have hθ12 : (φ-ψ)/2 ≤ (φ+ψ)/2 := by linarith
  have hθ2 : (φ+ψ)/2 ≤ π-φ := by linarith
  have hφπ : φ < π := by linarith
  have hθ1π : (φ-ψ)/2 < π := by linarith
  have hθ2π : (φ+ψ)/2 < π := by linarith
  have ha : 0 < sin ((φ-ψ)/2) := sin_pos_of_pos_of_lt_pi hθ1 hθ1π
  have hb : 0 < sin ((φ+ψ)/2) := sin_pos_of_pos_of_lt_pi (by linarith) hθ2π
  have hab : sin ((φ-ψ)/2) ≤ sin ((φ+ψ)/2) :=
    sin_le_sin_of_le_of_le_pi_div_two (by linarith) (by linarith) hθ12
  have hbc : sin ((φ+ψ)/2) ≤ sin φ := by
    have hh := sin_le_sin_of_le_of_le_pi_div_two
      (show -(π/2) ≤ (φ+ψ)/2 by linarith)
      (show π-φ ≤ π/2 by linarith) hθ2
    simpa only [sin_pi_sub] using hh
  have hc : cos φ < 0 := cos_neg_of_pi_div_two_lt_of_lt hφ (by linarith)
  have hid := halfChord_identity φ ψ
  have hk : 0 < halfChord φ ψ+halfChord φ (-ψ)-sin φ^2 := by
    rw [hid]
    exact mul_pos (mul_pos (by linarith : 0 < -2*cos φ) ha) hb
  have hpq : halfChord φ ψ ≤ halfChord φ (-ψ) := by
    unfold halfChord
    rw [show φ- -ψ=φ+ψ by ring]
    nlinarith
  have hqs : halfChord φ (-ψ) ≤ sin φ^2 := by
    unfold halfChord
    rw [show φ- -ψ=φ+ψ by ring]
    nlinarith
  dsimp
  refine ⟨hk, by linarith, hpq, hqs, ?_⟩
  rw [hid]
  unfold halfChord
  rw [show φ- -ψ=φ+ψ by ring]
  ring

def distanceSquared (α β : ℝ) : ℝ := (cos α-cos β)^2+(sin α-sin β)^2

theorem distanceSquared_eq (α β : ℝ) : distanceSquared α β = 4*halfChord α β := by
  have h1 := sin_sq_add_cos_sq α
  have h2 := sin_sq_add_cos_sq β
  have h3 := sin_sq_eq_half_sub ((α-β)/2)
  rw [show 2*((α-β)/2)=α-β by ring, cos_sub] at h3
  unfold distanceSquared halfChord
  nlinarith

theorem halfChord_end (φ : ℝ) :
    halfChord φ (2*π-3*φ) = 4*sin φ^2*cos φ^2 ∧
    halfChord φ (-(2*π-3*φ)) = sin φ^2 := by
  unfold halfChord
  rw [show (φ-(2*π-3*φ))/2=2*φ-π by ring,
    show (φ- -(2*π-3*φ))/2=π-φ by ring,
    sin_sub_pi, sin_two_mul, sin_pi_sub]
  constructor <;> ring

/-- The optimized endpoint bound in half-chord normalization, now with
the full angle domain of Fan's Conjecture 5.9 and all probability masses. -/
theorem fan59_halfChord {φ ψ r u v w : ℝ} (hr : 2 ≤ r)
    (hφ : π/2 < φ) (hφ' : φ ≤ 2*π/3) (hψ : 0 ≤ ψ) (hψ' : ψ ≤ 2*π-3*φ)
    (hu : 0 ≤ u) (hv : 0 ≤ v) (hw : 0 ≤ w) (hm : u+v+w=1) :
    energy ((halfChord φ ψ)^(r/2)) ((halfChord φ (-ψ))^(r/2)) ((sin φ^2)^(r/2)) u v w ≤
      endpointEnergy ((sin φ^2)^(r/2)) ((halfChord φ (2*π-3*φ))^(r/2)) := by
  obtain ⟨hk,hkp,hpq,hqs,hprod⟩ := halfChord_geometry hφ hφ' hψ hψ'
  have hp : 0 < halfChord φ ψ := lt_of_lt_of_le hk hkp
  have hq : 0 < halfChord φ (-ψ) := lt_of_lt_of_le hp hpq
  have he : sin φ^2*(halfChord φ ψ+halfChord φ (-ψ)-sin φ^2)^2 /
      (halfChord φ ψ*halfChord φ (-ψ)) = halfChord φ (2*π-3*φ) := by
    rw [hprod, (halfChord_end φ).1]
    field_simp
    <;> ring
  have h := normalized_endpoint_bound hk hkp hpq hqs (by ring)
    (show 1 ≤ r/2 by linarith) hu hv hw hm
  rwa [he] at h

/-- Riesz energy on A=(cos ψ,sin ψ), B=(cos φ,sin φ), C=(cos φ,-sin φ).
For exponent -r, the kernel is squared Euclidean distance to the power r/2. -/
def circleEnergy (φ ψ r u v w : ℝ) : ℝ :=
  energy ((distanceSquared φ ψ)^(r/2)) ((distanceSquared (-φ) ψ)^(r/2))
    ((distanceSquared φ (-φ))^(r/2)) u v w

theorem circleEnergy_eq (φ ψ r u v w : ℝ) :
    circleEnergy φ ψ r u v w = 4^(r/2)*
      energy ((halfChord φ ψ)^(r/2)) ((halfChord φ (-ψ))^(r/2)) ((sin φ^2)^(r/2)) u v w := by
  have hneg : halfChord (-φ) ψ=halfChord φ (-ψ) := by
    unfold halfChord
    rw [show (-φ-ψ)/2= -((φ- -ψ)/2) by ring, sin_neg]
    ring
  have hbase : halfChord φ (-φ)=sin φ^2 := by
    unfold halfChord
    rw [show (φ- -φ)/2=φ by ring]
  unfold circleEnergy
  rw [distanceSquared_eq, distanceSquared_eq, distanceSquared_eq, hneg, hbase]
  rw [mul_rpow (by norm_num : (0:ℝ) ≤ 4) (show 0 ≤ halfChord φ ψ from sq_nonneg _),
    mul_rpow (by norm_num : (0:ℝ) ≤ 4) (show 0 ≤ halfChord φ (-ψ) from sq_nonneg _),
    mul_rpow (by norm_num : (0:ℝ) ≤ 4) (sq_nonneg (sin φ))]
  unfold energy
  ring

/-- Fan's Conjecture 5.9: an explicit probability measure at the endpoint
dominates every probability measure at every point of the prescribed arc.
This formulation establishes attainment as well as the upper bound. -/
theorem fan59 {φ r : ℝ} (hr : 2 ≤ r) (hφ : π/2 < φ) (hφ' : φ ≤ 2*π/3) :
    ∃ U W : ℝ, 0 < U ∧ 0 < W ∧ U+U+W=1 ∧
      ∀ ψ u v w : ℝ, 0 ≤ ψ → ψ ≤ 2*π-3*φ →
        0 ≤ u → 0 ≤ v → 0 ≤ w → u+v+w=1 →
        circleEnergy φ ψ r u v w ≤ circleEnergy φ (2*π-3*φ) r U U W := by
  have hep : 0 ≤ 2*π-3*φ := by linarith
  obtain ⟨hk,hkp,hpq,hqs,_⟩ := halfChord_geometry hφ hφ' hep (le_refl _)
  have he0 : 0 < halfChord φ (2*π-3*φ) := lt_of_lt_of_le hk hkp
  have hs0 : 0 < sin φ^2 := lt_of_lt_of_le he0 (le_trans hpq hqs)
  let c := (sin φ^2)^(r/2)
  let e := (halfChord φ (2*π-3*φ))^(r/2)
  have hc : 0 < c := rpow_pos_of_pos hs0 _
  have he : 0 < e := rpow_pos_of_pos he0 _
  have hec : e ≤ c := rpow_le_rpow he0.le (le_trans hpq hqs) (by linarith)
  obtain ⟨hu,hw,hs,henergy⟩ := endpoint_attained hc he hec
  refine ⟨c/(4*c-e),(2*c-e)/(4*c-e),hu,hw,hs,?_⟩
  intro ψ u v w hψ hψ' hu' hv' hw' hm
  rw [circleEnergy_eq, circleEnergy_eq, (halfChord_end φ).2]
  change 4^(r/2)*energy _ _ _ _ _ _ ≤ 4^(r/2)*energy e c c _ _ _
  rw [henergy]
  exact mul_le_mul_of_nonneg_left (fan59_halfChord hr hφ hφ' hψ hψ' hu' hv' hw' hm)
    (rpow_nonneg (by norm_num) _)

#print axioms fan59

end
end MathLean.Riesz
