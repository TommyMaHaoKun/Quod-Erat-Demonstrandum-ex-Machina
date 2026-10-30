import MathLean.BinaryGramWords

namespace MathLean.GramCount

/-- Binary 4-by-n matrices with labeled row and column coordinates. -/
abbrev Matrix4n (n : ℕ) := Fin 4 → Fin n → Bool

def Matrix4nCondition {n : ℕ} (a : Matrix4n n) : Prop :=
  BinaryGram.MatrixCondition (List.ofFn (fun j i => a i j))

abbrev GoodMatrices4n (n : ℕ) := {a : Matrix4n n // Matrix4nCondition a}

def asVectorEquiv (n : ℕ) : Matrices n ≃
    {v : List.Vector BinaryGram.Column n // BinaryGram.MatrixCondition v.val} where
  toFun p := ⟨⟨p.val,p.property.1⟩,p.property.2⟩
  invFun p := ⟨p.val.val,p.val.property,p.property⟩
  left_inv _ := rfl
  right_inv _ := rfl

def columnsEquiv (n : ℕ) :
    {v : List.Vector BinaryGram.Column n // BinaryGram.MatrixCondition v.val} ≃
    {f : Fin n → BinaryGram.Column // BinaryGram.MatrixCondition (List.ofFn f)} :=
  Equiv.subtypeEquiv (Equiv.vectorEquivFin BinaryGram.Column n) (fun v => by
    have h := congrArg List.Vector.toList (List.Vector.ofFn_get v)
    rw [List.Vector.toList_ofFn] at h
    change BinaryGram.MatrixCondition v.val ↔ BinaryGram.MatrixCondition (List.ofFn v.get)
    rw [h]
    rfl)

def flipEquiv (n : ℕ) : (Fin n → BinaryGram.Column) ≃ Matrix4n n where
  toFun f i j := f j i
  invFun a j i := a i j
  left_inv _ := rfl
  right_inv _ := rfl

/-- The column-list representation is bijective with literal 4-by-n matrices. -/
def matrixShapeEquiv (n : ℕ) : Matrices n ≃ GoodMatrices4n n :=
  (asVectorEquiv n).trans ((columnsEquiv n).trans
    (Equiv.subtypeEquiv (flipEquiv n) (fun _ => Iff.rfl)))

#print axioms matrixShapeEquiv
end MathLean.GramCount
