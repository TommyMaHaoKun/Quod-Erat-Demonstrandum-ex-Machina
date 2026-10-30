import MathLean.BinaryGramData
import MathLean.BinaryGramFormula
namespace MathLean.GramCount
set_option maxHeartbeats 0
set_option maxRecDepth 100000

def table (n : Fin 17) : State → ℤ :=
  ([v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16] : List (State → ℤ)).getD n.val (fun _ => 0)

theorem initial_counts_checked : ∀ n : Fin 16, (table n.castSucc 0 : ℚ)=BinaryGramFormula.initial n := by decide +kernel

end MathLean.GramCount
