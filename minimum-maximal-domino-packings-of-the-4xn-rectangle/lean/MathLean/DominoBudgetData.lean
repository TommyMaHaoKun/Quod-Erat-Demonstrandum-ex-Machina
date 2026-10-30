import MathLean.DominoBounds
import MathLean.DominoGraphPaths
import MathLean.PathLists

namespace MathLean.DominoBudget
open MathLean.Domino
set_option maxHeartbeats 0
set_option maxRecDepth 100000

abbrev Node := Fin 240

def base (x : Node) : State := ⟨x.val/4, by have := x.isLt; omega⟩
def budget (x : Node) : ℕ := x.val%4
def mk (s : State) (b : Fin 4) : Node := ⟨4*s.val+b.val, by have := s.isLt; have := b.isLt; omega⟩

theorem base_mk (s : State) (b : Fin 4) : base (mk s b)=s := by
  apply Fin.ext
  dsimp [base,mk]
  have := b.isLt
  omega

theorem budget_mk (s : State) (b : Fin 4) : budget (mk s b)=b.val := by
  dsimp [budget,mk]
  have := b.isLt
  omega

theorem node_ext (x y : Node) (hs : base x=base y) (hb : budget x=budget y) : x=y := by
  have hh := congrArg Fin.val hs
  apply Fin.ext
  dsimp [base] at hh
  dsimp [budget] at hb
  omega

def Edge (x y : Node) : Prop := Legal (base x) (base y) ∧
  (budget y : ℤ) = (budget x : ℤ)+defect (base x) (base y)

instance (x y : Node) : Decidable (Edge x y) := inferInstanceAs (Decidable (_ ∧ _))

def Final (x : Node) : Prop := (masks (base x)).1=0 ∧
  0 ≤ (budget x : ℤ)+potential (base x) ∧ (budget x : ℤ)+potential (base x) ≤ 2

instance (x : Node) : Decidable (Final x) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))

def embed (i : Fin 114) : Node :=
  ([0,4,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,132,136,140,152,156,160,164,168,172,176,180,184,188,192,196,204,208,212,216,224,1,5,9,13,17,21,25,29,33,37,41,45,49,57,65,69,93,101,109,113,117,121,125,133,137,149,153,157,161,165,169,185,189,193,197,233,2,6,10,14,18,22,26,30,38,46,114,126,130,134,138,146,158,166,186,198,230,3,11,15,27,203,223,239] : List Node).getD i.val 0

def project (x : Node) : Fin 114 :=
  ([0,50,86,107,1,51,87,0,0,52,88,108,0,53,89,109,2,54,90,0,3,55,91,0,4,56,92,110,5,57,93,0,6,58,0,0,7,59,94,0,8,60,0,0,9,61,95,0,10,62,0,0,11,0,0,0,12,63,0,0,13,0,0,0,14,64,0,0,15,65,0,0,16,0,0,0,17,0,0,0,18,0,0,0,19,0,0,0,20,0,0,0,21,66,0,0,22,0,0,0,23,67,0,0,24,0,0,0,25,68,0,0,26,69,96,0,27,70,0,0,28,71,0,0,29,72,97,0,0,0,98,0,30,73,99,0,31,74,100,0,32,0,0,0,0,0,101,0,0,75,0,0,33,76,0,0,34,77,102,0,35,78,0,0,36,79,103,0,37,80,0,0,38,0,0,0,39,0,0,0,40,0,0,0,41,81,104,0,42,82,0,0,43,83,0,0,44,84,105,0,0,0,0,111,45,0,0,0,46,0,0,0,47,0,0,0,48,0,0,0,0,0,0,112,49,0,0,0,0,0,106,0,0,85,0,0,0,0,0,113] : List (Fin 114)).getD x.val 0

def Forward (x : Node) : Prop := x ∈ ([0,1,2,3,4,5,6,7,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,130,131,132,133,134,135,136,137,138,139,140,141,142,143,146,147,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,223,224,225,226,227,230,231,233,234,235,239] : List Node)
def Backward (x : Node) : Prop := x ∈ ([0,1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,20,21,22,24,25,26,27,28,29,30,32,33,36,37,38,40,41,44,45,46,48,49,52,56,57,60,64,65,68,69,72,76,80,84,88,92,93,96,100,101,104,108,109,112,113,114,116,117,120,121,124,125,126,128,129,130,132,133,134,136,137,138,140,144,145,146,148,149,152,153,156,157,158,160,161,164,165,166,168,169,172,176,180,184,185,186,188,189,192,193,196,197,198,200,201,202,203,204,208,212,216,220,221,222,223,224,228,229,230,232,233,236,237,238,239] : List Node)
instance (x : Node) : Decidable (Forward x) := inferInstanceAs (Decidable (_ ∈ _))
instance (x : Node) : Decidable (Backward x) := inferInstanceAs (Decidable (_ ∈ _))

def Active (x : Node) : Prop := embed (project x)=x
instance (x : Node) : Decidable (Active x) := inferInstanceAs (Decidable (_ = _))

theorem project_embed : ∀ i : Fin 114, project (embed i)=i := by decide +kernel
theorem embed_start : embed 0=0 := by decide
theorem project_start : project 0=0 := by decide
theorem forward_start : Forward 0 := by decide

theorem active_iff : ∀ x : Node, Active x ↔ Forward x ∧ Backward x := by decide +kernel
theorem forward_closed : ∀ x y : Node, Edge x y → Forward x → Forward y := by decide +kernel
theorem backward_closed : ∀ x y : Node, Edge x y → Backward y → Backward x := by decide +kernel
theorem backward_final : ∀ x : Node, Final x → Backward x := by decide +kernel

theorem edge_iff : ∀ i j : Fin 114, i ∈ DominoCount.pred j ↔ Edge (embed i) (embed j) := by decide +kernel
theorem final_iff : ∀ i : Fin 114, i ∈ DominoCount.finals ↔ Final (embed i) := by decide +kernel

#print axioms forward_closed
#print axioms edge_iff
end MathLean.DominoBudget
