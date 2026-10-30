import MathLean.TriangleEvaluation

/-! The six formulas of A195806, for the original bounded labeled arrays. -/
namespace MathLean.Triangle
open scoped BigOperators
open Finset

def formula (r : Fin 6) (m : ℕ) : ℕ :=
  match r.val with
  | 0 => 1+25*m+158*m^2+650*m^3+2275*m^4+4680*m^5+4680*m^6
  | 1 => 16+198*m+1133*m^2+3900*m^3+8125*m^4+9360*m^5+4680*m^6
  | 2 => 105+1087*m+4922*m^2+12350*m^3+17875*m^4+14040*m^5+4680*m^6
  | 3 => 496+4148*m+14783*m^2+28600*m^3+31525*m^4+18720*m^5+4680*m^6
  | 4 => 1759+12121*m+35258*m^2+55250*m^3+49075*m^4+23400*m^5+4680*m^6
  | 5 => 5052+29474*m+72197*m^2+94900*m^3+70525*m^4+28080*m^5+4680*m^6
  | _ => 0

theorem axisH_closed (n : ℕ) : axisH n =
    quarticClosed ((n : ℚ)+1) ((n : ℚ)+1) 2 3 (n/3 : ℕ) := by
  rw [axisH_range]
  simpa only [term, Nat.cast_zero, mul_zero, sub_zero] using
    quartic_sum ((n : ℚ)+1) ((n : ℚ)+1) 2 3 (n/3)

theorem axisK_closed (n : ℕ) : axisK n =
    quarticClosed ((n : ℚ)+1) ((n : ℚ)+1) 1 2 (n/2 : ℕ) := by
  rw [axisK_range]
  simpa only [term, Nat.cast_zero, mul_zero, sub_zero, one_mul] using
    quartic_sum ((n : ℚ)+1) ((n : ℚ)+1) 1 2 (n/2)

set_option maxHeartbeats 1600000 in
theorem chamberSum_formula (m : ℕ) (r : Fin 6) :
    (chamberSum (6*m+r.val) : ℚ) = formula r m := by
  rw [weighted_decomposition, fullSum_six, axisH_closed, axisK_closed]
  have h3 : (6*m+r.val)/3=2*m+r.val/3 := by omega
  have h2 : (6*m+r.val)/2=3*m+r.val/2 := by omega
  rw [h3,h2]
  fin_cases r <;> norm_num [formula, evenPolynomial, oddPolynomial, quarticClosed] <;> ring

/-- All six conjectured constituents, including m=0, count the original arrays. -/
theorem original_six_formulas (m : ℕ) (r : Fin 6) :
    Nat.card (Arrays (6*m+r.val)) = formula r m := by
  rw [original_chamber_count]
  exact_mod_cast chamberSum_formula m r

/-- A single formula valid for every nonnegative entry bound. -/
theorem original_all_bounds (n : ℕ) :
    Nat.card (Arrays n) = formula ⟨n%6, Nat.mod_lt n (by decide)⟩ (n/6) := by
  have hn : 6*(n/6)+n%6=n := by omega
  simpa only [hn] using original_six_formulas (n/6) ⟨n%6, Nat.mod_lt n (by decide)⟩

theorem residue_zero (m : ℕ) : Nat.card (Arrays (6*m)) =
    1+25*m+158*m^2+650*m^3+2275*m^4+4680*m^5+4680*m^6 := by
  simpa [formula] using original_six_formulas m 0
theorem residue_one (m : ℕ) : Nat.card (Arrays (6*m+1)) =
    16+198*m+1133*m^2+3900*m^3+8125*m^4+9360*m^5+4680*m^6 := by
  simpa [formula] using original_six_formulas m 1
theorem residue_two (m : ℕ) : Nat.card (Arrays (6*m+2)) =
    105+1087*m+4922*m^2+12350*m^3+17875*m^4+14040*m^5+4680*m^6 := by
  simpa [formula] using original_six_formulas m 2
theorem residue_three (m : ℕ) : Nat.card (Arrays (6*m+3)) =
    496+4148*m+14783*m^2+28600*m^3+31525*m^4+18720*m^5+4680*m^6 := by
  simpa [formula] using original_six_formulas m 3
theorem residue_four (m : ℕ) : Nat.card (Arrays (6*m+4)) =
    1759+12121*m+35258*m^2+55250*m^3+49075*m^4+23400*m^5+4680*m^6 := by
  simpa [formula] using original_six_formulas m 4
theorem residue_five (m : ℕ) : Nat.card (Arrays (6*m+5)) =
    (m+1)^2*(5052+19370*m+28405*m^2+18720*m^3+4680*m^4) := by
  calc
    Nat.card (Arrays (6*m+5)) =
        5052+29474*m+72197*m^2+94900*m^3+70525*m^4+28080*m^5+4680*m^6 := by
      simpa [formula] using original_six_formulas m 5
    _ = _ := by ring

#print axioms original_six_formulas
#print axioms original_all_bounds
#print axioms residue_five
end MathLean.Triangle
