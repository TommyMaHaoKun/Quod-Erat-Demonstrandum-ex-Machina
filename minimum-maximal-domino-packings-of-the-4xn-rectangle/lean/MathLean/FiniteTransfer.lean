import MathLean.Transfer
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset

/-! The entries of an iterated transfer operator count finite paths.
An edge is a type, so distinct labels with the same endpoints are counted
separately. No recurrence or path-counting assertion is assumed. -/
namespace MathLean.FiniteTransfer
open MathLean.Transfer
open scoped BigOperators

variable {S : Type} [Fintype S] [DecidableEq S]

def Paths (E : S → S → Type) (start : S) : ℕ → S → Type
  | 0, t => {u : Unit // start = t}
  | n+1, t => Σ s : S, Paths E start n s × E s t

instance pathsFintype (E : S → S → Type) [∀ s t, Fintype (E s t)] (start : S) :
    (n : ℕ) → (t : S) → Fintype (Paths E start n t)
  | 0, t => inferInstanceAs (Fintype {u : Unit // start = t})
  | n+1, t => by
    letI (s : S) : Fintype (Paths E start n s) := pathsFintype E start n s
    exact inferInstanceAs (Fintype (Σ s : S, Paths E start n s × E s t))

def initial (start : S) : S → ℤ := fun s => if start = s then 1 else 0

def transfer (E : S → S → Type) [∀ s t, Fintype (E s t)] :
    (S → ℤ) →ₗ[ℤ] (S → ℤ) where
  toFun v t := ∑ s, (Fintype.card (E s t) : ℤ) * v s
  map_add' := by
    intro v w
    funext t
    simp [mul_add, Finset.sum_add_distrib]
  map_smul' := by
    intro c v
    funext t
    simp [Finset.mul_sum, mul_comm, mul_left_comm, mul_assoc]

/-- Every coordinate of the transfer vector is the exact path count. -/
theorem card_paths (E : S → S → Type) [∀ s t, Fintype (E s t)]
    (start : S) (n : ℕ) (t : S) :
    (Fintype.card (Paths E start n t) : ℤ) = orbit (transfer E) (initial start) n t := by
  induction n generalizing t with
  | zero =>
    change (Fintype.card {u : Unit // start = t} : ℤ) = initial start t
    by_cases h : start = t <;> simp [initial, h]
  | succ n ih =>
    change (Fintype.card (Σ s : S, Paths E start n s × E s t) : ℤ) = _
    simp only [Fintype.card_sigma, Fintype.card_prod, Nat.cast_sum, Nat.cast_mul]
    simp_rw [ih]
    simp [orbit, transfer, mul_comm]

def accepted (P : S → Prop) [DecidablePred P] : (S → ℤ) →ₗ[ℤ] ℤ where
  toFun v := ∑ t : {s // P s}, v t.val
  map_add' := by intro v w; simp [Finset.sum_add_distrib]
  map_smul' := by intro c v; simp [Finset.mul_sum]

/-- Summing final coordinates counts precisely all accepting paths. -/
theorem card_accepted_paths (E : S → S → Type) [∀ s t, Fintype (E s t)]
    (start : S) (P : S → Prop) [DecidablePred P] (n : ℕ) :
    (Fintype.card (Σ t : {s // P s}, Paths E start n t.val) : ℤ) =
      accepted P (orbit (transfer E) (initial start) n) := by
  simp only [Fintype.card_sigma, Nat.cast_sum]
  simp_rw [card_paths]
  rfl

#print axioms card_accepted_paths
end MathLean.FiniteTransfer
