import MathLean.BinaryGramWords
import MathLean.BinaryGramCertificateTable
namespace MathLean.GramCount
set_option maxHeartbeats 0
set_option maxRecDepth 100000

variable (hinit : ∀ s, initial s=v0 s)
  (hsteps : ∀ n : Fin 16, step (table n.castSucc)=table n.succ)
  (hrel : ∀ s, v16 s = (-67108864 : ℤ)*v4 (s) +
      (62914560 : ℤ)*v5 (s) +
      (7864320 : ℤ)*v6 (s) +
      (-22609920 : ℤ)*v7 (s) +
      (4349952 : ℤ)*v8 (s) +
      (1812480 : ℤ)*v9 (s) +
      (-624640 : ℤ)*v10 (s) +
      (-15360 : ℤ)*v11 (s) +
      (24288 : ℤ)*v12 (s) +
      (-2040 : ℤ)*v13 (s) +
      (-180 : ℤ)*v14 (s) +
      (30 : ℤ)*v15 (s))

include hinit hsteps in
theorem orbit_table (n : Fin 17) : Transfer.orbit T initial n.val=table n := by
  induction n using Fin.induction with
  | zero => funext s; exact hinit s
  | succ n ih =>
    change Transfer.orbit T initial n.val=table n.castSucc at ih
    change T (Transfer.orbit T initial n.val)=table n.succ
    rw [ih]
    exact hsteps n

include hinit hsteps hrel in
theorem vector_certificate : Transfer.orbit T initial 16 =
(-67108864 : ℤ) • Transfer.orbit T initial (0+4) +
      (62914560 : ℤ) • Transfer.orbit T initial (0+5) +
      (7864320 : ℤ) • Transfer.orbit T initial (0+6) +
      (-22609920 : ℤ) • Transfer.orbit T initial (0+7) +
      (4349952 : ℤ) • Transfer.orbit T initial (0+8) +
      (1812480 : ℤ) • Transfer.orbit T initial (0+9) +
      (-624640 : ℤ) • Transfer.orbit T initial (0+10) +
      (-15360 : ℤ) • Transfer.orbit T initial (0+11) +
      (24288 : ℤ) • Transfer.orbit T initial (0+12) +
      (-2040 : ℤ) • Transfer.orbit T initial (0+13) +
      (-180 : ℤ) • Transfer.orbit T initial (0+14) +
      (30 : ℤ) • Transfer.orbit T initial (0+15) := by
  have h4 : Transfer.orbit T initial 4=table 4 := orbit_table hinit hsteps (4 : Fin 17)
  have h5 : Transfer.orbit T initial 5=table 5 := orbit_table hinit hsteps (5 : Fin 17)
  have h6 : Transfer.orbit T initial 6=table 6 := orbit_table hinit hsteps (6 : Fin 17)
  have h7 : Transfer.orbit T initial 7=table 7 := orbit_table hinit hsteps (7 : Fin 17)
  have h8 : Transfer.orbit T initial 8=table 8 := orbit_table hinit hsteps (8 : Fin 17)
  have h9 : Transfer.orbit T initial 9=table 9 := orbit_table hinit hsteps (9 : Fin 17)
  have h10 : Transfer.orbit T initial 10=table 10 := orbit_table hinit hsteps (10 : Fin 17)
  have h11 : Transfer.orbit T initial 11=table 11 := orbit_table hinit hsteps (11 : Fin 17)
  have h12 : Transfer.orbit T initial 12=table 12 := orbit_table hinit hsteps (12 : Fin 17)
  have h13 : Transfer.orbit T initial 13=table 13 := orbit_table hinit hsteps (13 : Fin 17)
  have h14 : Transfer.orbit T initial 14=table 14 := orbit_table hinit hsteps (14 : Fin 17)
  have h15 : Transfer.orbit T initial 15=table 15 := orbit_table hinit hsteps (15 : Fin 17)
  have h16 : Transfer.orbit T initial 16=table 16 := orbit_table hinit hsteps (16 : Fin 17)
  rw [h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14,h15,h16]
  funext s
  simpa only [Pi.add_apply,Pi.smul_apply,smul_eq_mul] using hrel s

include hinit hsteps hrel in
theorem propagated (n : ℕ) : Transfer.orbit T initial (n+16) =
(-67108864 : ℤ) • Transfer.orbit T initial (n+4) +
      (62914560 : ℤ) • Transfer.orbit T initial (n+5) +
      (7864320 : ℤ) • Transfer.orbit T initial (n+6) +
      (-22609920 : ℤ) • Transfer.orbit T initial (n+7) +
      (4349952 : ℤ) • Transfer.orbit T initial (n+8) +
      (1812480 : ℤ) • Transfer.orbit T initial (n+9) +
      (-624640 : ℤ) • Transfer.orbit T initial (n+10) +
      (-15360 : ℤ) • Transfer.orbit T initial (n+11) +
      (24288 : ℤ) • Transfer.orbit T initial (n+12) +
      (-2040 : ℤ) • Transfer.orbit T initial (n+13) +
      (-180 : ℤ) • Transfer.orbit T initial (n+14) +
      (30 : ℤ) • Transfer.orbit T initial (n+15) := by
  induction n with
  | zero => exact vector_certificate hinit hsteps hrel
  | succ n ih =>
    have h := congrArg T ih
    simpa only [map_add,map_zsmul,Nat.succ_add,Transfer.orbit] using h

noncomputable def count (n : ℕ) : ℚ := Nat.card (Matrices n)

theorem count_orbit (n : ℕ) : count n = (Transfer.orbit T initial n 0 : ℚ) := by
  unfold count
  exact_mod_cast matrix_count_orbit n

include hinit hsteps hrel in
theorem count_recurrence : BinaryGramFormula.Recurrence count := by
  intro n
  simp only [count_orbit]
  have h := congrFun (propagated hinit hsteps hrel n) 0
  simp only [Pi.add_apply,Pi.smul_apply,smul_eq_mul] at h
  exact_mod_cast h

include hinit hsteps in
theorem count_initial (n : Fin 16) : count n=BinaryGramFormula.initial n := by
  have ht : Transfer.orbit T initial n.val=table n.castSucc := orbit_table hinit hsteps n.castSucc
  rw [count_orbit,ht]
  exact initial_counts_checked n

include hinit hsteps hrel in
theorem matrix_count_formula_of_certificate (n : ℕ) :
    (Nat.card (Matrices n) : ℚ)=BinaryGramFormula.formula n :=
  BinaryGramFormula.eq_formula count (count_recurrence hinit hsteps hrel) (count_initial hinit hsteps) n

#print axioms matrix_count_formula_of_certificate
end MathLean.GramCount
