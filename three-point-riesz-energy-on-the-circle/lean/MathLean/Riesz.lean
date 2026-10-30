import Mathlib.Analysis.Convex.SpecificFunctions.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

namespace MathLean.Riesz
open Real Set
noncomputable section

/-- Two-term majorization, proved directly from convexity. -/
theorem two_term_majorization {f : ℝ → ℝ} (hf : ConvexOn ℝ (Ici 0) f)
    {k p q s : ℝ} (hk : 0 ≤ k) (hkp : k ≤ p) (hpq : p ≤ q)
    (hqs : q ≤ s) (hsum : p+q=k+s) : f p+f q ≤ f k+f s := by
  by_cases hks : k = s
  · have hp : p = k := by linarith
    have hq : q = k := by linarith
    simp [hp,hq,hks]
  have hd : 0 < s-k := by
    have hle : k ≤ s := le_trans hkp (le_trans hpq hqs)
    have hlt : k < s := lt_of_le_of_ne hle hks
    linarith
  let a := (s-p)/(s-k)
  let b := (p-k)/(s-k)
  have ha : 0 ≤ a := div_nonneg (by linarith) hd.le
  have hb : 0 ≤ b := div_nonneg (by linarith) hd.le
  have hab : a+b=1 := by dsimp [a,b]; field_simp <;> ring
  have hp : a*k+b*s=p := by dsimp [a,b]; field_simp; ring
  have hq : b*k+a*s=q := by
    have heq : b*k+a*s = k+s-p := by dsimp [a,b]; field_simp; ring
    linarith
  have h1 := hf.2 hk (show 0 ≤ s by linarith) ha hb hab
  have h2 := hf.2 hk (show 0 ≤ s by linarith) hb ha (by linarith : b+a=1)
  simp only [smul_eq_mul, hp, hq] at h1 h2
  calc
    f p+f q ≤ (a*f k+b*f s)+(b*f k+a*f s) := add_le_add h1 h2
    _ = (a+b)*f k+(a+b)*f s := by ring
    _ = f k+f s := by rw [hab]; ring

theorem rpow_majorization {k p q s t : ℝ} (ht : 1 ≤ t)
    (hk : 0 ≤ k) (hkp : k ≤ p) (hpq : p ≤ q) (hqs : q ≤ s)
    (hsum : p+q=k+s) : p^t+q^t ≤ k^t+s^t :=
  two_term_majorization (convexOn_rpow ht) hk hkp hpq hqs hsum

def energy (a b c u v w : ℝ) : ℝ := 2*(u*v*a+u*w*b+v*w*c)
def discriminant (a b c : ℝ) : ℝ := 4*a*b-(a+b-c)^2
def endpointEnergy (c e : ℝ) : ℝ := 2*c^2/(4*c-e)

/-- Upper bound on the boundary branch, for every probability vector. -/
theorem two_point_bound {a b c u v w : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 < c) (hab : a+b ≤ c)
    (hu : 0 ≤ u) (hv : 0 ≤ v) (hw : 0 ≤ w) (hs : u+v+w=1) :
    energy a b c u v w ≤ c/2 := by
  have huv : 0 ≤ u*v := mul_nonneg hu hv
  have huw : 0 ≤ u*w := mul_nonneg hu hw
  have hgap : 0 ≤ c-a-b := by linarith
  -- A convex combination of the two star kernels gives a shorter bound.
  have h1 : 4*(u*v+v*w) ≤ 1 := by nlinarith [sq_nonneg (u+w-v)]
  have h2 : 4*(u*w+v*w) ≤ 1 := by nlinarith [sq_nonneg (u+v-w)]
  have h3 : 4*(v*w) ≤ 1 := by nlinarith [sq_nonneg (v-w),sq_nonneg u]
  have hvw : 0 ≤ v*w := mul_nonneg hv hw
  have e1 := mul_nonneg ha (show 0 ≤ 1-4*(u*v+v*w) by linarith)
  have e2 := mul_nonneg hb (show 0 ≤ 1-4*(u*w+v*w) by linarith)
  have e3 := mul_nonneg hgap (show 0 ≤ 1-4*(v*w) by linarith)
  unfold energy
  nlinarith

/-- The identity used to compare the interior optimum with the endpoint. -/
theorem comparison_identity (a b c e : ℝ) :
    c*discriminant a b c-a*b*(4*c-e) = e*a*b-c*(a+b-c)^2 := by
  unfold discriminant
  ring

theorem interior_comparison {a b c e : ℝ}
    (hc : 0 < c) (hd : 0 < discriminant a b c) (he : 0 < 4*c-e)
    (h : c*(a+b-c)^2 ≤ e*a*b) :
    2*a*b*c/discriminant a b c ≤ endpointEnergy c e := by
  unfold endpointEnergy
  apply (div_le_div_iff₀ hd he).2
  have hi := comparison_identity a b c e
  nlinarith [mul_nonneg hc.le (sub_nonneg.mpr h)]

theorem endpoint_above_boundary {c e : ℝ}
    (hc : 0 < c) (he : 0 < e) (hec : e ≤ c) : c/2 < endpointEnergy c e := by
  have hd : 0 < 4*c-e := by linarith
  unfold endpointEnergy
  apply (lt_div_iff₀ hd).2
  nlinarith [mul_pos hc he]

theorem discriminant_pos {a b c : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hac : a ≤ c) (hbc : b ≤ c) (hab : c < a+b) :
    0 < discriminant a b c := by
  have hx : 0 ≤ a+b-c := by linarith
  have hxa : a+b-c ≤ a := by linarith
  have hxb : a+b-c ≤ b := by linarith
  have hh := mul_le_mul hxa hxb hx ha.le
  have hp := mul_pos ha hb
  unfold discriminant
  nlinarith

/-- Completing squares bounds the quadratic energy on the entire affine
plane u+v+w=1 when the discriminant is positive. -/
theorem interior_bound {a b c u v w : ℝ} (hb : 0 < b)
    (hd : 0 < discriminant a b c) (hs : u+v+w=1) :
    energy a b c u v w ≤ 2*a*b*c/discriminant a b c := by
  have hid : 4*a*b^2*c-2*b*discriminant a b c*energy a b c u v w =
      discriminant a b c*(2*b*u+(b+c-a)*v-b)^2 +
      (discriminant a b c*v-b*(a+c-b))^2 := by
    rw [show w=1-u-v by linarith]
    unfold discriminant energy
    ring
  have hnn : 0 ≤ discriminant a b c*(2*b*u+(b+c-a)*v-b)^2 +
      (discriminant a b c*v-b*(a+c-b))^2 := by positivity
  apply (le_div_iff₀ hd).2
  nlinarith [mul_pos hb hd]

/-- An endpoint comparison valid for every probability measure on the
three points. The nonlinear majorization input is stated explicitly. -/
theorem energy_le_endpoint {a b c e z u v w : ℝ}
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c)
    (hac : a ≤ c) (hbc : b ≤ c) (he : 0 < e) (hec : e ≤ c)
    (hz : 0 ≤ z) (hmajor : a+b-c ≤ z) (hprod : e*a*b=c*z^2)
    (hu : 0 ≤ u) (hv : 0 ≤ v) (hw : 0 ≤ w) (hs : u+v+w=1) :
    energy a b c u v w ≤ endpointEnergy c e := by
  by_cases hab : a+b ≤ c
  · exact (two_point_bound ha.le hb.le hc hab hu hv hw hs).trans
      (endpoint_above_boundary hc he hec).le
  · have hx : 0 ≤ a+b-c := by linarith
    have hsq : (a+b-c)^2 ≤ z^2 := by nlinarith
    have hcomp : c*(a+b-c)^2 ≤ e*a*b := by
      rw [hprod]
      exact mul_le_mul_of_nonneg_left hsq hc.le
    have hd := discriminant_pos ha hb hac hbc (by linarith : c < a+b)
    exact (interior_bound hb hd hs).trans
      (interior_comparison hc hd (by linarith) hcomp)

theorem endpoint_attained {c e : ℝ} (hc : 0 < c) (he : 0 < e) (hec : e ≤ c) :
    let u := c/(4*c-e)
    let w := (2*c-e)/(4*c-e)
    0 < u ∧ 0 < w ∧ u+u+w=1 ∧ energy e c c u u w=endpointEnergy c e := by
  have hd : 0 < 4*c-e := by linarith
  dsimp
  refine ⟨div_pos hc hd, div_pos (by linarith) hd, ?_, ?_⟩
  · field_simp
    ring
  · unfold energy endpointEnergy
    field_simp
    <;> ring

/-- Fan's majorization argument in squared-half-chord coordinates.
The endpoint short squared half-chord is s*k^2/(p*q).
This theorem optimizes over arbitrary masses, not a prescribed formula. -/
theorem normalized_endpoint_bound {k p q s t u v w : ℝ}
    (hk : 0 < k) (hkp : k ≤ p) (hpq : p ≤ q) (hqs : q ≤ s)
    (hsum : p+q=k+s) (ht : 1 ≤ t)
    (hu : 0 ≤ u) (hv : 0 ≤ v) (hw : 0 ≤ w) (hm : u+v+w=1) :
    energy (p^t) (q^t) (s^t) u v w ≤ endpointEnergy (s^t) ((s*k^2/(p*q))^t) := by
  have hp : 0 < p := lt_of_lt_of_le hk hkp
  have hq : 0 < q := lt_of_lt_of_le hp hpq
  have hs : 0 < s := lt_of_lt_of_le hq hqs
  have ht0 : 0 ≤ t := by linarith
  have hkt : 0 < k^t := rpow_pos_of_pos hk t
  have hpt : 0 < p^t := rpow_pos_of_pos hp t
  have hqt : 0 < q^t := rpow_pos_of_pos hq t
  have hst : 0 < s^t := rpow_pos_of_pos hs t
  have he0 : 0 < s*k^2/(p*q) := by positivity
  have hksq : k^2 ≤ p*q := by
    have h := mul_le_mul hkp (le_trans hkp hpq) hk.le hp.le
    nlinarith
  have hes : s*k^2/(p*q) ≤ s := by
    apply (div_le_iff₀ (mul_pos hp hq)).2
    nlinarith [mul_nonneg hs.le (sub_nonneg.mpr hksq)]
  have hprod : (s*k^2/(p*q))^t * p^t * q^t = s^t*(k^t)^2 := by
    rw [div_rpow (by positivity) (by positivity), mul_rpow hs.le (sq_nonneg k),
      mul_rpow hp.le hq.le]
    rw [sq, mul_rpow hk.le hk.le]
    field_simp
    <;> ring
  apply energy_le_endpoint hpt hqt hst
    (rpow_le_rpow hp.le (le_trans hpq hqs) ht0)
    (rpow_le_rpow hq.le hqs ht0)
    (rpow_pos_of_pos he0 t) (rpow_le_rpow he0.le hes ht0) hkt.le
    (by linarith [rpow_majorization ht hk.le hkp hpq hqs hsum]) hprod hu hv hw hm

end
end MathLean.Riesz
