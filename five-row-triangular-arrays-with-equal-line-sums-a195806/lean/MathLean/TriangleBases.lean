import MathLean.TriangleParameters
import Mathlib.Data.Int.Interval
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Set.Card

namespace MathLean.Triangle
open scoped BigOperators

def lowerBase (x y : ℤ) : ℤ := -min 0 (min x y)
def upperBase (n : ℕ) (x y : ℤ) : ℤ := n-max 0 (max x y)
def span (x y : ℤ) : ℤ := max 0 (max x y)-min 0 (min x y)
abbrev Base (n : ℕ) (x y : ℤ) := Set.Icc (lowerBase x y) (upperBase n x y)

theorem mem_base_iff (n : ℕ) (x y a : ℤ) :
    a ∈ Set.Icc (lowerBase x y) (upperBase n x y) ↔
      (0≤a ∧ a≤n) ∧ (0≤a+x ∧ a+x≤n) ∧ (0≤a+y ∧ a+y≤n) := by
  simp only [Set.mem_Icc, lowerBase, upperBase]
  omega

theorem card_base (n : ℕ) (x y : ℤ) :
    Fintype.card (Base n x y) = ((n : ℤ)+1-span x y).toNat := by
  simp only [Base, Fintype.card_Icc, Int.card_Icc, lowerBase, upperBase, span]
  congr 1
  ring

theorem span_abs (x y : ℤ) : span x y = max (max |x| |y|) |x-y| := by
  simp only [span, abs_eq_max_neg]
  omega

def normA (p q : ℤ) : ℤ := max (max |p| |p+q|) |2*p+q|
def normB (p q : ℤ) : ℤ := max (max |q| |3*p+q|) |3*p+2*q|

theorem span_a (p q : ℤ) : span p (2*p+q) = normA p q := by
  simp only [span_abs, normA, abs_eq_max_neg]
  omega

theorem span_c (p q : ℤ) : span q (-3*p-q) = normB p q := by
  simp only [span_abs, normB, abs_eq_max_neg]
  omega

theorem span_e (p q : ℤ) : span p (-p-q) = normA p q := by
  simp only [span_abs, normA, abs_eq_max_neg]
  omega

theorem span_f (p q : ℤ) : span (3*p+q) (3*p+2*q) = normB p q := by
  simp only [span_abs, normB, abs_eq_max_neg]
  omega

abbrev Fiber (n : ℕ) (p q : ℤ) :=
  Base n p (2*p+q) × Base n q (-3*p-q) × Base n p (-p-q) × Base n (3*p+q) (3*p+2*q)

theorem card_fiber (n : ℕ) (p q : ℤ) :
    Fintype.card (Fiber n p q) =
      ((n : ℤ)+1-normA p q).toNat^2 * ((n : ℤ)+1-normB p q).toNat^2 := by
  simp only [Fiber, Fintype.card_prod, card_base, span_a, span_c, span_e, span_f]
  ring

theorem bounded_parameter_iff (n : ℕ) (v : Parameters) :
    Bounded n (parameterMap v) ↔
      v.a ∈ Set.Icc (lowerBase v.p (2*v.p+v.q)) (upperBase n v.p (2*v.p+v.q)) ∧
      v.c ∈ Set.Icc (lowerBase v.q (-3*v.p-v.q)) (upperBase n v.q (-3*v.p-v.q)) ∧
      v.e ∈ Set.Icc (lowerBase v.p (-v.p-v.q)) (upperBase n v.p (-v.p-v.q)) ∧
      v.f ∈ Set.Icc (lowerBase (3*v.p+v.q) (3*v.p+2*v.q))
        (upperBase n (3*v.p+v.q) (3*v.p+2*v.q)) := by
  simp only [mem_base_iff]
  constructor
  · intro h
    have h1 := h 1
    have h2 := h 2
    have h3 := h 3
    have h5 := h 5
    have h6 := h 6
    have h7 := h 7
    have h8 := h 8
    have h9 := h 9
    have h10 := h 10
    have h11 := h 11
    have h12 := h 12
    have h13 := h 13
    simp [parameterMap, Matrix.cons_val] at *
    omega
  · intro h i
    fin_cases i <;> simp [parameterMap, Matrix.cons_val] <;> omega

theorem parameters_difference_bounds (n : ℕ) (v : Parameters)
    (hv : Bounded n (parameterMap v)) :
    -(n : ℤ) ≤ v.p ∧ v.p ≤ n ∧ -(n : ℤ) ≤ v.q ∧ v.q ≤ n := by
  have h := (bounded_parameter_iff n v).mp hv
  simp only [mem_base_iff] at h
  omega

end MathLean.Triangle
