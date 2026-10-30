import MathLean.BinaryGramEncoding
import MathLean.Transfer
import Mathlib.Data.Fintype.Card
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Set.Card

namespace MathLean.GramCount
open scoped BigOperators
set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev AcceptedWords (s : State) (n : ℕ) :=
  {v : List.Vector Column n // RunAccept s v.val}

def wordCount (n : ℕ) (s : State) : ℤ := Fintype.card (AcceptedWords s n)

def splitWords (s : State) (n : ℕ) : AcceptedWords s (n+1) ≃
    (Σ c : Column, {v : List.Vector Column n // RunAccept s (c::v.val)}) where
  toFun p := ⟨p.val.head,⟨p.val.tail,by
    have h := congrArg Subtype.val (List.Vector.cons_head_tail p.val)
    change p.val.head :: p.val.tail.val = p.val.val at h
    rw [h]
    exact p.property⟩⟩
  invFun p := ⟨List.Vector.cons p.1 p.2.val,p.2.property⟩
  left_inv p := Subtype.ext (List.Vector.cons_head_tail p.val)
  right_inv p := by rcases p with ⟨c,v,h⟩; rfl

theorem wordCount_zero (s : State) : wordCount 0 s=if Final s then 1 else 0 := by
  have he : (fun v : List.Vector Column 0 => RunAccept s v.val)=(fun _ => Final s) := by
    funext v
    rw [List.length_eq_zero_iff.mp v.property]
    rfl
  have e : AcceptedWords s 0 ≃ {v : List.Vector Column 0 // Final s} :=
    Equiv.subtypeEquivRight (fun v => iff_of_eq (congrFun he v))
  unfold wordCount
  rw [Fintype.card_congr e]
  by_cases h : Final s <;> simp [h]

theorem wordCount_succ (n : ℕ) (s : State) : wordCount (n+1) s=step (wordCount n) s := by
  unfold wordCount
  rw [Fintype.card_congr (splitWords s n),Fintype.card_sigma,Nat.cast_sum]
  unfold step
  apply Finset.sum_congr rfl
  intro c _
  cases hn : next s c with
  | none => simp [RunAccept,hn]
  | some t => simp [RunAccept,hn,AcceptedWords]

def T : (State → ℤ) →ₗ[ℤ] (State → ℤ) where
  toFun := step
  map_add' a b := by
    funext s
    simp only [step,Pi.add_apply,← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro c _
    cases next s c <;> simp
  map_smul' k a := by
    funext s
    change (∑ c : Column, (next s c).elim 0 (fun t => k*a t)) =
      k * ∑ c : Column, (next s c).elim 0 a
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro c _
    cases next s c <;> simp

def initial (s : State) : ℤ := if Final s then 1 else 0

theorem wordCount_orbit (n : ℕ) : wordCount n=Transfer.orbit T initial n := by
  induction n with
  | zero => funext s; exact wordCount_zero s
  | succ n ih =>
    funext s
    rw [wordCount_succ,ih]
    rfl

abbrev Matrices (n : ℕ) :=
  {cs : List BinaryGram.Column // cs.length=n ∧ BinaryGram.MatrixCondition cs}

theorem decode_encode_list (cs : List BinaryGram.Column) :
    (cs.map encodeColumn).map decodeColumn=cs := by
  simp only [List.map_map,Function.comp_def,column_right]
  exact List.map_id _

theorem encode_decode_list (cs : List Column) :
    (cs.map decodeColumn).map encodeColumn=cs := by
  simp only [List.map_map,Function.comp_def,column_left]
  exact List.map_id _

/-- Ordered binary columns are retained individually; the map neither
permutes rows nor identifies different column orders. -/
def matrixEquiv (n : ℕ) : AcceptedWords 0 n ≃ Matrices n where
  toFun p := ⟨p.val.val.map decodeColumn,by
    exact ⟨by simpa using p.val.property,(accepts_matrix p.val.val).mp p.property⟩⟩
  invFun p := ⟨⟨p.val.map encodeColumn,by simpa using p.property.1⟩,by
    apply (accepts_matrix _).mpr
    rw [decode_encode_list]
    exact p.property.2⟩
  left_inv p := Subtype.ext (Subtype.ext (encode_decode_list p.val.val))
  right_inv p := Subtype.ext (decode_encode_list p.val)

theorem matrix_count_orbit (n : ℕ) :
    (Nat.card (Matrices n) : ℤ) = Transfer.orbit T initial n 0 := by
  rw [← Nat.card_congr (matrixEquiv n),Nat.card_eq_fintype_card]
  exact congrFun (wordCount_orbit n) 0

#print axioms matrix_count_orbit
end MathLean.GramCount
