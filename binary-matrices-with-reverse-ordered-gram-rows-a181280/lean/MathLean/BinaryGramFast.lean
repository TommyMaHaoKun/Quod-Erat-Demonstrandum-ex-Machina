import MathLean.BinaryGramAutomaton
import Mathlib.Tactic.NormNum
import Mathlib.Algebra.BigOperators.Fin
namespace MathLean.GramCount
open scoped BigOperators
set_option maxHeartbeats 0
set_option maxRecDepth 100000

def moves (m : Mask) : List (Mask × Parity) :=
  ([[(0,0),(4,512),(2,896),(1,1008),(0,1023)],[(1,0),(1,1),(5,512),(5,521),(3,896),(3,909),(1,1008),(1,1023)],[(2,0),(3,16),(2,19),(6,512),(7,592),(6,603),(2,896),(3,1008),(2,1023)],[(3,0),(3,1),(3,16),(3,19),(7,512),(7,521),(7,592),(7,603),(3,896),(3,909),(3,1008),(3,1023)],[(4,0),(6,128),(5,176),(4,183),(4,512),(6,896),(5,1008),(4,1023)],[(5,0),(5,1),(7,128),(7,133),(5,176),(5,183),(5,512),(5,521),(7,896),(7,909),(5,1008),(5,1023)],[(6,0),(7,16),(6,19),(6,128),(7,176),(6,183),(6,512),(7,592),(6,603),(6,896),(7,1008),(6,1023)],[(7,0),(7,1),(7,16),(7,19),(7,128),(7,133),(7,176),(7,183),(7,512),(7,521),(7,592),(7,603),(7,896),(7,909),(7,1008),(7,1023)]] : List (List (Mask × Parity))).getD m.val []

def core (v : State → ℤ) (m : Mask) (g : Parity) : ℤ :=
  ∑ c : Column, (nextMask m c).elim 0 (fun t => v (join t (xorParity g (outer c))))

def fastCore (v : State → ℤ) (m : Mask) (g : Parity) : ℤ :=
  ((moves m).map (fun p => v (join p.1 (xorParity g p.2)))).sum

def fastStep (v : State → ℤ) (s : State) : ℤ := fastCore v (mask s) (parity s)

theorem core_fast : ∀ m : Mask, ∀ (g : Parity) (v : State → ℤ), core v m g=fastCore v m g := by
  intro m
  fin_cases m <;> intro g v <;>
    norm_num [core,fastCore,moves,nextMask,outer,Fin.sum_univ_succ]

theorem step_fast (v : State → ℤ) (s : State) : step v s=fastStep v s := by
  change (∑ c : Column, (next s c).elim 0 v)=fastCore v (mask s) (parity s)
  calc
    _ = core v (mask s) (parity s) := by
      apply Finset.sum_congr rfl
      intro c _
      cases h : nextMask (mask s) c <;> simp [next,h]
    _ = _ := core_fast (mask s) (parity s) v

#print axioms step_fast
end MathLean.GramCount
