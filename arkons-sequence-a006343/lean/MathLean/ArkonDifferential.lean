import Mathlib.RingTheory.PowerSeries.Derivative
import Mathlib.RingTheory.PowerSeries.NoZeroDivisors
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-! Algebraic differential certificate for the independently specified
Arkon generating series. This file does not define a sequence by the
recurrence being proved. -/
namespace MathLean.Arkon
open PowerSeries

def equation {R : Type*} [CommRing R] (x y : R) : R :=
  x^3*y^3 - (x-1)*y^2 + (x-2)*y + 1
def fy {R : Type*} [CommRing R] (x y : R) : R :=
  3*x^3*y^2 - 2*(x-1)*y + x-2
def fx {R : Type*} [CommRing R] (x y : R) : R :=
  3*x^2*y^3 - y^2 + y
def fyy {R : Type*} [CommRing R] (x y : R) : R := 6*x^3*y-2*(x-1)
def fxy {R : Type*} [CommRing R] (x y : R) : R := 9*x^2*y^2-2*y+1
def fxx {R : Type*} [CommRing R] (x y : R) : R := 6*x*y^3
def p2 {R : Type*} [CommRing R] (x : R) : R :=
  -x^2*(5*x-1)*(31*x^4-6*x^3-7*x^2+6*x-1)
def p1 {R : Type*} [CommRing R] (x : R) : R :=
  -x*(620*x^5-260*x^4-78*x^3+103*x^2-31*x+3)
def p0 {R : Type*} [CommRing R] (x : R) : R :=
  -310*x^5+138*x^4-36*x^3+103*x^2-36*x+3
def forcing {R : Type*} [CommRing R] (x : R) : R := 3-36*x+98*x^2
def quotient {R : Type*} [CommRing R] (x y : R) : R :=
  -1512*x^9*y^4 + 3564*x^8*y^4 - 1215*x^7*y^4 + 2016*x^7*y^3
  - 1218*x^7*y^2 + 108*x^6*y^4 - 6768*x^6*y^3 + 6534*x^6*y^2
  - 1230*x^6*y + 6372*x^5*y^3 - 8904*x^5*y^2 + 3408*x^5*y
  - 98*x^5 - 1764*x^4*y^3 + 4410*x^4*y^2 - 3288*x^4*y
  + 624*x^4 + 144*x^3*y^3 - 2802*x^3*y^2 + 4014*x^3*y
  - 1395*x^3 + 1554*x^2*y^2 - 2784*x^2*y + 1234*x^2
  - 348*x*y^2 + 672*x*y - 324*x + 24*y^2 - 48*y + 24

set_option maxRecDepth 10000 in
set_option maxHeartbeats 4000000 in
theorem polynomial_certificate {R : Type*} [CommRing R] (x y u v : R) :
    fy x y ^ 3 * (p2 x*v + p1 x*u + p0 x*y - forcing x) =
      p2 x * fy x y ^ 2 *
        (fy x y*v + fyy x y*u^2 + 2*fxy x y*u + fxx x y) +
      (p1 x*fy x y^2 - 2*p2 x*fxy x y*fy x y -
        p2 x*fyy x y*fy x y*u + p2 x*fyy x y*fx x y) *
        (fy x y*u + fx x y) + quotient x y * equation x y := by
  unfold fy fx fyy fxy fxx p2 p1 p0 forcing quotient equation
  ring

noncomputable abbrev D := PowerSeries.derivative ℚ

@[simp] theorem D_two : D (2 : PowerSeries ℚ) = 0 := D.map_natCast 2
@[simp] theorem D_three : D (3 : PowerSeries ℚ) = 0 := D.map_natCast 3

theorem differentiate_equation (A : PowerSeries ℚ) :
    D (equation X A) = fy X A * D A + fx X A := by
  simp [equation, fy, fx, map_sub, map_add, Derivation.leibniz,
    Derivation.leibniz_pow, Derivation.map_natCast, smul_eq_mul]
  ring

theorem differentiate_first (A : PowerSeries ℚ) :
    D (fy X A * D A + fx X A) =
      fy X A * D (D A) + fyy X A * (D A)^2 +
        2*fxy X A * D A + fxx X A := by
  simp [fy, fx, fyy, fxy, fxx, map_sub, map_add, Derivation.leibniz,
    Derivation.leibniz_pow, Derivation.map_natCast, smul_eq_mul]
  ring

theorem differential_equation (A : PowerSeries ℚ)
    (hA : equation X A = 0) (hreg : fy X A ≠ 0) :
    p2 X * D (D A) + p1 X * D A + p0 X * A = forcing X := by
  have h₁ : fy X A * D A + fx X A = 0 := by
    rw [← differentiate_equation, hA, map_zero]
  have h₂ : fy X A * D (D A) + fyy X A * (D A)^2 +
      2*fxy X A * D A + fxx X A = 0 := by
    rw [← differentiate_first, h₁, map_zero]
  have h := polynomial_certificate X A (D A) (D (D A))
  rw [h₁, h₂, hA] at h
  simp only [mul_zero, add_zero] at h
  exact sub_eq_zero.mp ((mul_eq_zero.mp h).resolve_left (pow_ne_zero 3 hreg))

end MathLean.Arkon
