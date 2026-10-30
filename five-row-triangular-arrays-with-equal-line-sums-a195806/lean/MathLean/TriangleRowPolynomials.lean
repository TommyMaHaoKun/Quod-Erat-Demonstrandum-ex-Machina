import MathLean.TrianglePolynomialSums

namespace MathLean.Triangle
open scoped BigOperators
open Finset

def evenA : Fin 6 → ℕ := ![1, 2, 3, 4, 5, 6]
def evenB : Fin 6 → ℕ := ![1, 2, 3, 4, 5, 6]
def evenD : Fin 6 → ℕ := ![0, 0, 1, 1, 2, 2]

def evenPolynomial (r : Fin 6) (m t : ℚ) : ℚ :=
  match r.val with
  | 0 => 36*m^2*t^4 - 24*m^2*t^3 - 14*m^2*t^2 + 6*m^2*t + 468*m*t^5/5 - 72*m*t^4 - 190*m*t^3/3 + 36*m*t^2 + 146*m*t/15 + 327*t^6/5 - 288*t^5/5 - 271*t^4/4 + 48*t^3 + 427*t^2/20 - 42*t/5
  | 1 => 36*m^2*t^4 - 20*m^2*t^2 + 468*m*t^5/5 + 18*m*t^4 - 256*m*t^3/3 - 10*m*t^2 + 236*m*t/15 + 327*t^6/5 + 117*t^5/5 - 173*t^4/2 - 64*t^3/3 + 311*t^2/10 + 59*t/15
  | 2 => 36*m^2*t^4 + 24*m^2*t^3 - 14*m^2*t^2 - 6*m^2*t + 468*m*t^5/5 + 108*m*t^4 - 118*m*t^3/3 - 50*m*t^2 + 56*m*t/15 + 327*t^6/5 + 522*t^5/5 - 91*t^4/4 - 221*t^3/3 - 3*t^2/20 + 353*t/30
  | 3 => 36*m^2*t^4 + 48*m^2*t^3 + 4*m^2*t^2 - 8*m^2*t + 468*m*t^5/5 + 198*m*t^4 + 224*m*t^3/3 - 46*m*t^2 - 244*m*t/15 + 327*t^6/5 + 927*t^5/5 + 247*t^4/2 - 128*t^3/3 - 429*t^2/10 + 49*t/15
  | 4 => 36*m^2*t^4 + 72*m^2*t^3 + 34*m^2*t^2 - 2*m^2*t + 468*m*t^5/5 + 288*m*t^4 + 770*m*t^3/3 + 40*m*t^2 - 334*m*t/15 + 327*t^6/5 + 1332*t^5/5 + 1409*t^4/4 + 138*t^3 - 573*t^2/20 - 77*t/5
  | 5 => 36*m^2*t^4 + 96*m^2*t^3 + 76*m^2*t^2 + 16*m^2*t + 468*m*t^5/5 + 378*m*t^4 + 1520*m*t^3/3 + 246*m*t^2 + 356*m*t/15 + 327*t^6/5 + 1737*t^5/5 + 1327*t^4/2 + 1604*t^3/3 + 1511*t^2/10 - 31*t/15
  | _ => 0

theorem evenPolynomial_zero (r : Fin 6) (m : ℚ) : evenPolynomial r m 0 = 0 := by
  fin_cases r <;> norm_num [evenPolynomial]

set_option maxHeartbeats 800000 in
theorem evenPolynomial_step (r : Fin 6) (m t : ℚ) :
    evenPolynomial r m (t+1) = evenPolynomial r m t +
      quarticClosed (2*m+4*t+evenA r) (6*t+evenB r) 1 2 (3*t+evenD r) := by
  fin_cases r <;> norm_num [evenPolynomial, evenA, evenB, evenD, quarticClosed] <;> ring

theorem even_row_sum (r : Fin 6) (m : ℚ) (t : ℕ) :
    (∑ v ∈ range t, quarticClosed (2*m+4*v+evenA r) (6*v+evenB r) 1 2 (3*v+evenD r)) =
      evenPolynomial r m t := by
  induction t with
  | zero => simp [evenPolynomial_zero]
  | succ t ih =>
      rw [sum_range_succ, ih]
      push_cast
      exact (evenPolynomial_step r m t).symm

def oddA : Fin 6 → ℕ := ![3, 4, 5, 2, 3, 4]
def oddB : Fin 6 → ℕ := ![4, 5, 6, 1, 2, 3]
def oddD : Fin 6 → ℕ := ![1, 2, 2, 0, 0, 1]

def oddPolynomial (r : Fin 6) (m t : ℚ) : ℚ :=
  match r.val with
  | 0 => 36*m^2*t^4 + 48*m^2*t^3 + 4*m^2*t^2 - 8*m^2*t + 468*m*t^5/5 + 162*m*t^4 + 80*m*t^3/3 - 50*m*t^2 - 124*m*t/15 + 327*t^6/5 + 693*t^5/5 + 67*t^4/2 - 68*t^3 - 189*t^2/10 + 47*t/5
  | 1 => 36*m^2*t^4 + 72*m^2*t^3 + 34*m^2*t^2 - 2*m^2*t + 468*m*t^5/5 + 252*m*t^4 + 554*m*t^3/3 + 6*m*t^2 - 304*m*t/15 + 327*t^6/5 + 1098*t^5/5 + 869*t^4/4 + 83*t^3/3 - 803*t^2/20 - 143*t/30
  | 2 => 36*m^2*t^4 + 96*m^2*t^3 + 76*m^2*t^2 + 16*m^2*t + 468*m*t^5/5 + 342*m*t^4 + 1232*m*t^3/3 + 170*m*t^2 + 116*m*t/15 + 327*t^6/5 + 1503*t^5/5 + 967*t^4/2 + 916*t^3/3 + 471*t^2/10 - 149*t/15
  | 3 => 36*m^2*t^4 - 24*m^2*t^3 - 14*m^2*t^2 + 6*m^2*t + 468*m*t^5/5 - 36*m*t^4 - 262*m*t^3/3 + 22*m*t^2 + 236*m*t/15 + 327*t^6/5 - 54*t^5/5 - 379*t^4/4 + 31*t^3/3 + 717*t^2/20 - 61*t/30
  | 4 => 36*m^2*t^4 - 20*m^2*t^2 + 468*m*t^5/5 + 54*m*t^4 - 256*m*t^3/3 - 30*m*t^2 + 236*m*t/15 + 327*t^6/5 + 351*t^5/5 - 137*t^4/2 - 64*t^3 + 211*t^2/10 + 59*t/5
  | 5 => 36*m^2*t^4 + 24*m^2*t^3 - 14*m^2*t^2 - 6*m^2*t + 468*m*t^5/5 + 144*m*t^4 - 46*m*t^3/3 - 64*m*t^2 - 34*m*t/15 + 327*t^6/5 + 756*t^5/5 + 161*t^4/4 - 262*t^3/3 - 573*t^2/20 + 182*t/15
  | _ => 0

theorem oddPolynomial_zero (r : Fin 6) (m : ℚ) : oddPolynomial r m 0 = 0 := by
  fin_cases r <;> norm_num [oddPolynomial]

set_option maxHeartbeats 800000 in
theorem oddPolynomial_step (r : Fin 6) (m t : ℚ) :
    oddPolynomial r m (t+1) = oddPolynomial r m t +
      quarticClosed (2*m+4*t+oddA r) (6*t+oddB r) 1 2 (3*t+oddD r) := by
  fin_cases r <;> norm_num [oddPolynomial, oddA, oddB, oddD, quarticClosed] <;> ring

theorem odd_row_sum (r : Fin 6) (m : ℚ) (t : ℕ) :
    (∑ v ∈ range t, quarticClosed (2*m+4*v+oddA r) (6*v+oddB r) 1 2 (3*v+oddD r)) =
      oddPolynomial r m t := by
  induction t with
  | zero => simp [oddPolynomial_zero]
  | succ t ih =>
      rw [sum_range_succ, ih]
      push_cast
      exact (oddPolynomial_step r m t).symm

end MathLean.Triangle
