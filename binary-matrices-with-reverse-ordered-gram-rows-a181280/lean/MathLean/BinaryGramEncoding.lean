import MathLean.BinaryGramAutomaton

namespace MathLean.GramCount
set_option maxHeartbeats 0
set_option maxRecDepth 100000

def decodeColumn (c : Column) : BinaryGram.Column := fun i => c.val.testBit i.val
def encodeColumn (c : BinaryGram.Column) : Column :=
  ⟨((if c 0 then 1 else 0)+(if c 1 then 2 else 0)+
    (if c 2 then 4 else 0)+(if c 3 then 8 else 0))%16,Nat.mod_lt _ (by decide)⟩

theorem column_left : ∀ c : Column, encodeColumn (decodeColumn c)=c := by decide +kernel
theorem column_right : ∀ c : BinaryGram.Column, decodeColumn (encodeColumn c)=c := by decide +kernel

def columnEquiv : Column ≃ BinaryGram.Column where
  toFun := decodeColumn
  invFun := encodeColumn
  left_inv := column_left
  right_inv := column_right

def pairIndex (i j : Fin 4) : ℕ :=
  (#[0,1,2,3,1,4,5,6,2,5,7,8,3,6,8,9] : Array ℕ).getD (4*i.val+j.val) 0

def decodeGram (g : Parity) : BinaryGram.Gram := fun i j => g.val.testBit (pairIndex i j)
def comparison (m : Mask) (i : Fin 3) : Ordering := if m.val.testBit i.val then .lt else .eq

def fullState (s : State) : BinaryGram.State := ⟨comparison (mask s),decodeGram (parity s)⟩

theorem mask_join (m : Mask) (g : Parity) : mask (join m g)=m := by
  apply Fin.ext
  dsimp [mask,join]
  have := g.isLt
  omega

theorem parity_join (m : Mask) (g : Parity) : parity (join m g)=g := by
  apply Fin.ext
  dsimp [parity,join]
  have := g.isLt
  omega

theorem comparison_step : ∀ (m : Mask) (c : Column) (t : Mask),
    nextMask m c=some t → ∀ i : Fin 3,
      BinaryGram.firstDifference (comparison m i)
        (BinaryGram.compareBit (decodeColumn c i.castSucc) (decodeColumn c i.succ)) = comparison t i := by
  decide +kernel

theorem invalid_comparison : ∀ (m : Mask) (c : Column), nextMask m c=none →
    ∃ i : Fin 3, comparison m i=.eq ∧ decodeColumn c i.castSucc=true ∧ decodeColumn c i.succ=false := by
  decide +kernel

def parityAt (b : Fin 16) (g : Fin 64) : Parity :=
  ⟨64*b.val+g.val,by have := b.isLt; have := g.isLt; omega⟩

theorem parity_step_0 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 0 g) (outer c)) i j =
      xor (decodeGram (parityAt 0 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_1 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 1 g) (outer c)) i j =
      xor (decodeGram (parityAt 1 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_2 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 2 g) (outer c)) i j =
      xor (decodeGram (parityAt 2 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_3 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 3 g) (outer c)) i j =
      xor (decodeGram (parityAt 3 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_4 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 4 g) (outer c)) i j =
      xor (decodeGram (parityAt 4 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_5 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 5 g) (outer c)) i j =
      xor (decodeGram (parityAt 5 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_6 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 6 g) (outer c)) i j =
      xor (decodeGram (parityAt 6 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_7 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 7 g) (outer c)) i j =
      xor (decodeGram (parityAt 7 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_8 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 8 g) (outer c)) i j =
      xor (decodeGram (parityAt 8 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_9 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 9 g) (outer c)) i j =
      xor (decodeGram (parityAt 9 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_10 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 10 g) (outer c)) i j =
      xor (decodeGram (parityAt 10 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_11 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 11 g) (outer c)) i j =
      xor (decodeGram (parityAt 11 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_12 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 12 g) (outer c)) i j =
      xor (decodeGram (parityAt 12 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_13 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 13 g) (outer c)) i j =
      xor (decodeGram (parityAt 13 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_14 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 14 g) (outer c)) i j =
      xor (decodeGram (parityAt 14 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_15 : ∀ (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt 15 g) (outer c)) i j =
      xor (decodeGram (parityAt 15 g) i j) (decodeColumn c i && decodeColumn c j) := by decide +kernel

theorem parity_step_blocks : ∀ (b : Fin 16) (g : Fin 64) (c : Column) (i j : Fin 4),
    decodeGram (xorParity (parityAt b g) (outer c)) i j =
      xor (decodeGram (parityAt b g) i j) (decodeColumn c i && decodeColumn c j) := by
  intro b
  fin_cases b
  · exact parity_step_0
  · exact parity_step_1
  · exact parity_step_2
  · exact parity_step_3
  · exact parity_step_4
  · exact parity_step_5
  · exact parity_step_6
  · exact parity_step_7
  · exact parity_step_8
  · exact parity_step_9
  · exact parity_step_10
  · exact parity_step_11
  · exact parity_step_12
  · exact parity_step_13
  · exact parity_step_14
  · exact parity_step_15

theorem parity_step : ∀ (g : Parity) (c : Column) (i j : Fin 4),
    decodeGram (xorParity g (outer c)) i j =
      xor (decodeGram g i j) (decodeColumn c i && decodeColumn c j) := by
  intro g c i j
  let b : Fin 16 := ⟨g.val/64,by have := g.isLt; omega⟩
  let a : Fin 64 := ⟨g.val%64,Nat.mod_lt _ (by decide)⟩
  have h := parity_step_blocks b a c i j
  have hg : parityAt b a=g := by apply Fin.ext; dsimp [parityAt,b,a]; omega
  simpa only [hg] using h

theorem full_step (s : State) (c : Column) (t : State) (h : next s c=some t) :
    BinaryGram.step (fullState s) (decodeColumn c)=fullState t := by
  cases hm : nextMask (mask s) c with
  | none => simp [next,hm] at h
  | some m =>
    have ht : join m (xorParity (parity s) (outer c))=t := by simpa [next,hm] using h
    rw [← ht]
    simp only [BinaryGram.step,fullState,mask_join,parity_join]
    congr 1
    · funext i
      exact comparison_step (mask s) c m hm i
    · funext i j
      exact (parity_step (parity s) c i j).symm

theorem invalid_not_accept (s : State) (c : Column) (cs : List BinaryGram.Column)
    (h : next s c=none) : ¬ BinaryGram.Accept (BinaryGram.run (BinaryGram.step (fullState s) (decodeColumn c)) cs) := by
  have hm : nextMask (mask s) c=none := by
    cases he : nextMask (mask s) c with
    | none => rfl
    | some m => simp [next,he] at h
  obtain ⟨i,hi,ha,hb⟩ := invalid_comparison (mask s) c hm
  have hs : (BinaryGram.step (fullState s) (decodeColumn c)).comparisons i=.gt := by
    simp [BinaryGram.step,fullState,hi,ha,hb,BinaryGram.firstDifference,BinaryGram.compareBit]
  have hr := BinaryGram.run_comparisons cs (BinaryGram.step (fullState s) (decodeColumn c)) i
  rw [hs] at hr
  intro hp
  have hc := hp.1 i
  rw [hr] at hc
  cases hc

def Final (s : State) : Prop := mask s=7 ∧
  ∀ i : Fin 3, BinaryGram.gramComparison (decodeGram (parity s)) i.castSucc i.succ=.gt

instance (s : State) : Decidable (Final s) := inferInstanceAs (Decidable (_ ∧ _))

theorem comparison_final : ∀ m : Mask, (∀ i, comparison m i=.lt) ↔ m=7 := by decide +kernel

theorem final_iff (s : State) : Final s ↔ BinaryGram.Accept (fullState s) := by
  simp only [Final,BinaryGram.Accept,fullState,comparison_final]

def RunAccept (s : State) : List Column → Prop
  | [] => Final s
  | c::cs => match next s c with
    | none => False
    | some t => RunAccept t cs

instance runAcceptDecidable (s : State) (cs : List Column) : Decidable (RunAccept s cs) := by
  induction cs generalizing s with
  | nil => exact inferInstanceAs (Decidable (Final s))
  | cons c cs ih =>
    unfold RunAccept
    cases next s c with
    | none => exact isFalse id
    | some t => exact ih t

theorem run_iff (s : State) (cs : List Column) :
    RunAccept s cs ↔ BinaryGram.Accept (BinaryGram.run (fullState s) (cs.map decodeColumn)) := by
  induction cs generalizing s with
  | nil => exact final_iff s
  | cons c cs ih =>
    simp only [RunAccept,List.map_cons,BinaryGram.run,List.foldl_cons]
    cases hn : next s c with
    | none =>
      simp only [hn]
      exact iff_false_intro (invalid_not_accept s c (cs.map decodeColumn) hn) |>.symm
    | some t =>
      simp only [hn]
      rw [full_step s c t hn]
      exact ih t

theorem full_start : fullState 0=BinaryGram.initial := by
  unfold fullState BinaryGram.initial
  congr 1
  · funext i
    fin_cases i <;> rfl
  · funext i j
    fin_cases i <;> fin_cases j <;> rfl

/-- The compact automaton accepts exactly the original row and Gram conditions. -/
theorem accepts_matrix (cs : List Column) :
    RunAccept 0 cs ↔ BinaryGram.MatrixCondition (cs.map decodeColumn) := by
  rw [run_iff,full_start,BinaryGram.accepts_iff_matrixCondition]

#print axioms accepts_matrix
end MathLean.GramCount
