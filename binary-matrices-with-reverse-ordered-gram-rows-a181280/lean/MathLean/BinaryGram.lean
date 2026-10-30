import Mathlib.Data.List.Lex
import Mathlib.Data.Fin.Basic
import Mathlib.Tactic.FinCases

/-! Semantic layer for A181280. Columns and rows retain their labels.
The Gram entries are over F₂, represented by Bool xor/and.
-/
namespace MathLean.BinaryGram

abbrev Column := Fin 4 → Bool
abbrev Gram := Fin 4 → Fin 4 → Bool

def compareBit (a b : Bool) : Ordering :=
  if a = b then .eq else if a then .gt else .lt

def firstDifference (a b : Ordering) : Ordering :=
  if a = .eq then b else a

theorem firstDifference_assoc (a b c : Ordering) :
    firstDifference (firstDifference a b) c = firstDifference a (firstDifference b c) := by
  cases a <;> rfl

/-- Lexicographic comparison with the leftmost column compared first. -/
def rowComparison (cs : List Column) (i j : Fin 4) : Ordering :=
  match cs with
  | [] => .eq
  | c::tail => firstDifference (compareBit (c i) (c j)) (rowComparison tail i j)

/-- Independent mathematical definition of the binary Gram matrix. -/
def gram (cs : List Column) (i j : Fin 4) : Bool :=
  match cs with
  | [] => false
  | c::tail => xor (c i && c j) (gram tail i j)

structure State where
  comparisons : Fin 3 → Ordering
  parity : Gram

def initial : State := ⟨fun _ => .eq, fun _ _ => false⟩

def step (s : State) (c : Column) : State :=
  ⟨fun i => firstDifference (s.comparisons i) (compareBit (c i.castSucc) (c i.succ)),
   fun i j => xor (s.parity i j) (c i && c j)⟩

def run (s : State) (cs : List Column) : State := cs.foldl step s

theorem run_comparisons (cs : List Column) (s : State) (i : Fin 3) :
    (run s cs).comparisons i =
      firstDifference (s.comparisons i) (rowComparison cs i.castSucc i.succ) := by
  induction cs generalizing s with
  | nil => cases h : s.comparisons i <;> simp [run, rowComparison, firstDifference, h]
  | cons c cs ih =>
    simpa only [run, List.foldl_cons, step, rowComparison, firstDifference_assoc] using ih (step s c)

theorem xor_assoc (a b c : Bool) : xor (xor a b) c = xor a (xor b c) := by
  cases a <;> cases b <;> cases c <;> rfl

theorem run_parity (cs : List Column) (s : State) (i j : Fin 4) :
    (run s cs).parity i j = xor (s.parity i j) (gram cs i j) := by
  induction cs generalizing s with
  | nil => cases h : s.parity i j <;> simp [run, gram, h]
  | cons c cs ih =>
    simpa only [run, List.foldl_cons, step, gram, xor_assoc] using ih (step s c)

/-- Compare the four entries of two Gram rows in their original order. -/
def gramComparison (g : Gram) (i j : Fin 4) : Ordering :=
  firstDifference (compareBit (g i 0) (g j 0))
    (firstDifference (compareBit (g i 1) (g j 1))
      (firstDifference (compareBit (g i 2) (g j 2)) (compareBit (g i 3) (g j 3))))

def Accept (s : State) : Prop :=
  (∀ i, s.comparisons i = .lt) ∧
  (∀ i : Fin 3, gramComparison s.parity i.castSucc i.succ = .gt)

def MatrixCondition (cs : List Column) : Prop :=
  (∀ i : Fin 3, rowComparison cs i.castSucc i.succ = .lt) ∧
  (∀ i : Fin 3, gramComparison (gram cs) i.castSucc i.succ = .gt)

/-- The scan recognizes precisely increasing rows with decreasing Gram rows.
The final all-length counting theorem still needs the compressed 8192-state
transition operator and its recurrence certificate. -/
theorem accepts_iff_matrixCondition (cs : List Column) :
    Accept (run initial cs) ↔ MatrixCondition cs := by
  have hp : (run initial cs).parity = gram cs := by
    funext i j
    simpa [initial] using run_parity cs initial i j
  have hc : (run initial cs).comparisons = fun i => rowComparison cs i.castSucc i.succ := by
    funext i
    simpa [initial, firstDifference] using run_comparisons cs initial i
  simp only [Accept, MatrixCondition, hp, hc]

#print axioms accepts_iff_matrixCondition
end MathLean.BinaryGram
