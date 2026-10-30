import MathLean.DominoCountData

namespace MathLean.DominoCount
open MathLean.Transfer
open scoped BigOperators
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem initial_checked : table 0 = initial := by decide +kernel

theorem checkedStep0 : step v0 = v1 := by decide +kernel
#check checkedStep0

theorem checkedStep1 : step v1 = v2 := by decide +kernel
#check checkedStep1

theorem checkedStep2 : step v2 = v3 := by decide +kernel
#check checkedStep2

theorem checkedStep3 : step v3 = v4 := by decide +kernel
#check checkedStep3

theorem checkedStep4 : step v4 = v5 := by decide +kernel
#check checkedStep4

theorem checkedStep5 : step v5 = v6 := by decide +kernel
#check checkedStep5

theorem checkedStep6 : step v6 = v7 := by decide +kernel
#check checkedStep6

theorem checkedStep7 : step v7 = v8 := by decide +kernel
#check checkedStep7

theorem checkedStep8 : step v8 = v9 := by decide +kernel
#check checkedStep8

theorem checkedStep9 : step v9 = v10 := by decide +kernel
#check checkedStep9

theorem checkedStep10 : step v10 = v11 := by decide +kernel
#check checkedStep10

theorem checkedStep11 : step v11 = v12 := by decide +kernel
#check checkedStep11

theorem checkedStep12 : step v12 = v13 := by decide +kernel
#check checkedStep12

theorem checkedStep13 : step v13 = v14 := by decide +kernel
#check checkedStep13

theorem checkedStep14 : step v14 = v15 := by decide +kernel
#check checkedStep14

theorem checkedStep15 : step v15 = v16 := by decide +kernel
#check checkedStep15

theorem checkedStep16 : step v16 = v17 := by decide +kernel
#check checkedStep16

theorem checkedStep17 : step v17 = v18 := by decide +kernel
#check checkedStep17

theorem checkedStep18 : step v18 = v19 := by decide +kernel
#check checkedStep18

theorem checkedStep19 : step v19 = v20 := by decide +kernel
#check checkedStep19

theorem checkedStep20 : step v20 = v21 := by decide +kernel
#check checkedStep20

theorem checkedStep21 : step v21 = v22 := by decide +kernel
#check checkedStep21

theorem checkedStep22 : step v22 = v23 := by decide +kernel
#check checkedStep22

theorem checkedStep23 : step v23 = v24 := by decide +kernel
#check checkedStep23

theorem checkedStep24 : step v24 = v25 := by decide +kernel
#check checkedStep24

theorem checkedStep25 : step v25 = v26 := by decide +kernel
#check checkedStep25

theorem steps_checked : ∀ n : Fin 26, step (table n.castSucc) = table n.succ := by
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
  · exact checkedStep16
  · exact checkedStep17
  · exact checkedStep18
  · exact checkedStep19
  · exact checkedStep20
  · exact checkedStep21
  · exact checkedStep22
  · exact checkedStep23
  · exact checkedStep24
  · exact checkedStep25


theorem vector_checked : ∀ i : Fin 114,
    table 26 i - 3*table 23 i + 3*table 20 i - table 17 i = 0 := by decide +kernel

end MathLean.DominoCount
