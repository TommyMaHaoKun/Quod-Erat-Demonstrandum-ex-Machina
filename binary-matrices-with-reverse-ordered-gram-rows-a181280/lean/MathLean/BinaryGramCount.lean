import MathLean.BinaryGramCertificate00
import MathLean.BinaryGramCertificate01
import MathLean.BinaryGramCertificate02
import MathLean.BinaryGramCertificate03
import MathLean.BinaryGramCertificate04
import MathLean.BinaryGramCertificate05
import MathLean.BinaryGramCertificate06
import MathLean.BinaryGramCertificate07
import MathLean.BinaryGramCertificate08
import MathLean.BinaryGramCertificate09
import MathLean.BinaryGramCertificate10
import MathLean.BinaryGramCertificate11
import MathLean.BinaryGramCertificate12
import MathLean.BinaryGramCertificate13
import MathLean.BinaryGramCertificate14
import MathLean.BinaryGramCertificate15
import MathLean.BinaryGramInitialCertificate
import MathLean.BinaryGramRelationCertificate
import MathLean.BinaryGramCertificateTable
import MathLean.BinaryGramConclusion
import MathLean.BinaryGramMatrix
namespace MathLean.GramCount
set_option maxHeartbeats 0
set_option maxRecDepth 100000

theorem steps_checked : ∀ n : Fin 16, step (table n.castSucc)=table n.succ := by
  intro n
  fin_cases n
  · exact checkedStep0
  · exact checkedStep1
  · exact checkedStep2
  · exact checkedStep3
  · exact checkedStep4
  · exact checkedStep5
  · exact checkedStep6
  · exact checkedStep7
  · exact checkedStep8
  · exact checkedStep9
  · exact checkedStep10
  · exact checkedStep11
  · exact checkedStep12
  · exact checkedStep13
  · exact checkedStep14
  · exact checkedStep15

theorem matrix_count_formula (n : ℕ) :
    (Nat.card (Matrices n) : ℚ)=BinaryGramFormula.formula n :=
  matrix_count_formula_of_certificate initial_checked steps_checked relation_checked n

#print axioms matrix_count_formula

theorem matrix_4xn_count_formula (n : ℕ) :
    (Nat.card (GoodMatrices4n n) : ℚ)=BinaryGramFormula.formula n := by
  rw [← Nat.card_congr (matrixShapeEquiv n)]
  exact matrix_count_formula n

theorem a181280_formula (n : ℕ) (hn : 4 ≤ n) :
    (Nat.card (GoodMatrices4n n) : ℚ)=BinaryGramFormula.rawFormula n := by
  rw [matrix_4xn_count_formula,BinaryGramFormula.formula,if_neg (by omega)]

theorem a181280_small (n : ℕ) (hn : n < 4) :
    (Nat.card (GoodMatrices4n n) : ℚ)=0 := by
  rw [matrix_4xn_count_formula,BinaryGramFormula.formula,if_pos hn]

#print axioms a181280_formula
end MathLean.GramCount
