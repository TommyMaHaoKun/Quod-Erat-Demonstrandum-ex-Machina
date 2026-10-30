import MathLean.BinaryGram
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Prod


namespace MathLean.GramCount
open scoped BigOperators
set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev State := Fin 8192
abbrev Mask := Fin 8
abbrev Parity := Fin 1024
abbrev Column := Fin 16

def mask (s : State) : Mask := ⟨s.val/1024,by have := s.isLt; omega⟩
def parity (s : State) : Parity := ⟨s.val%1024,Nat.mod_lt _ (by decide)⟩
def join (m : Mask) (g : Parity) : State := ⟨1024*m.val+g.val,by have := m.isLt; have := g.isLt; omega⟩
def nextMask (m : Mask) (c : Column) : Option Mask :=
  (#[some 0,none,none,none,none,none,none,none,some 4,none,none,none,some 2,none,some 1,some 0,some 1,some 1,none,none,none,none,none,none,some 5,some 5,none,none,some 3,some 3,some 1,some 1,some 2,none,some 3,some 2,none,none,none,none,some 6,none,some 7,some 6,some 2,none,some 3,some 2,some 3,some 3,some 3,some 3,none,none,none,none,some 7,some 7,some 7,some 7,some 3,some 3,some 3,some 3,some 4,none,none,none,some 6,none,some 5,some 4,some 4,none,none,none,some 6,none,some 5,some 4,some 5,some 5,none,none,some 7,some 7,some 5,some 5,some 5,some 5,none,none,some 7,some 7,some 5,some 5,some 6,none,some 7,some 6,some 6,none,some 7,some 6,some 6,none,some 7,some 6,some 6,none,some 7,some 6,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7,some 7] : Array (Option Mask)).getD (16*m.val+c.val) none
def outer (c : Column) : Parity :=
  (#[0,1,16,19,128,133,176,183,512,521,592,603,896,909,1008,1023] : Array Parity).getD c.val 0
def xorParity (g h : Parity) : Parity := ⟨(g.val ^^^ h.val)%1024,Nat.mod_lt _ (by decide)⟩
def next (s : State) (c : Column) : Option State :=
  (nextMask (mask s) c).map (fun m => join m (xorParity (parity s) (outer c)))

def step (v : State → ℤ) (s : State) : ℤ :=
  ∑ c : Column, (next s c).elim 0 v

end MathLean.GramCount
