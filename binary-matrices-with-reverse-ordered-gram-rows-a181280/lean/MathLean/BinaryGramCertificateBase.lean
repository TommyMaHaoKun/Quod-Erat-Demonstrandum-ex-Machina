import MathLean.BinaryGramData
import Mathlib.Tactic.FinCases
namespace MathLean.GramCount
set_option maxHeartbeats 0
set_option maxRecDepth 100000

def block (b : Fin 64) (i : Fin 128) : State :=
  ⟨128*b.val+i.val,by have := b.isLt; have := i.isLt; omega⟩

theorem forall_blocks {P : State → Prop} (h : ∀ b i, P (block b i)) : ∀ s, P s := by
  intro s
  let b : Fin 64 := ⟨s.val/128,by have := s.isLt; omega⟩
  let i : Fin 128 := ⟨s.val%128,Nat.mod_lt _ (by decide)⟩
  have he : block b i=s := by apply Fin.ext; dsimp [block,b,i]; omega
  simpa only [he] using h b i

end MathLean.GramCount
