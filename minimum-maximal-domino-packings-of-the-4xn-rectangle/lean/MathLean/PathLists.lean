import MathLean.FiniteTransfer
import Mathlib.Data.List.Induction
import Mathlib.Data.Set.Card

namespace MathLean.PathLists
variable {S : Type} [Fintype S] [DecidableEq S]

def Chain (R : S → S → Prop) : S → List S → Prop
  | _, [] => True
  | s, t::ts => R s t ∧ Chain R t ts

def finish : S → List S → S
  | s, [] => s
  | _, t::ts => finish t ts

theorem finish_append (s : S) (xs ys : List S) :
    finish s (xs++ys) = finish (finish s xs) ys := by
  induction xs generalizing s with
  | nil => rfl
  | cons x xs ih => exact ih x

theorem chain_append (R : S → S → Prop) (s : S) (xs ys : List S) :
    Chain R s (xs++ys) ↔ Chain R s xs ∧ Chain R (finish s xs) ys := by
  induction xs generalizing s with
  | nil => simp [Chain,finish]
  | cons x xs ih => simp [Chain,finish,ih,and_assoc]

def Edge (R : S → S → Prop) (s t : S) := {u : Unit // R s t}

def states (R : S → S → Prop) (s : S) :
    {n : ℕ} → {t : S} → FiniteTransfer.Paths (Edge R) s n t → List S
  | 0, _, _ => []
  | n+1, t, p => states R s p.2.1 ++ [t]

theorem states_length (R : S → S → Prop) (s : S) {n : ℕ} {t : S}
    (p : FiniteTransfer.Paths (Edge R) s n t) : (states R s p).length=n := by
  induction n generalizing t with
  | zero => rfl
  | succ n ih => simp [states,ih]

theorem states_finish (R : S → S → Prop) (s : S) {n : ℕ} {t : S}
    (p : FiniteTransfer.Paths (Edge R) s n t) : finish s (states R s p)=t := by
  cases n with
  | zero => exact p.property
  | succ n => simp [states,finish_append,finish]

theorem states_chain (R : S → S → Prop) (s : S) {n : ℕ} {t : S}
    (p : FiniteTransfer.Paths (Edge R) s n t) : Chain R s (states R s p) := by
  induction n generalizing t with
  | zero => trivial
  | succ n ih =>
    rw [states,chain_append,states_finish]
    exact ⟨ih p.2.1,p.2.2.property,trivial⟩

theorem states_injective (R : S → S → Prop) (s : S) {n : ℕ} {t : S} :
    Function.Injective (fun p : FiniteTransfer.Paths (Edge R) s n t => states R s p) := by
  induction n generalizing t with
  | zero => intro p q _; exact Subtype.ext (Subsingleton.elim p.val q.val)
  | succ n ih =>
    intro p q he
    rcases p with ⟨u,p,e⟩
    rcases q with ⟨v,q,f⟩
    change states R s p ++ [t] = states R s q ++ [t] at he
    have hpq := List.append_cancel_right he
    have huv : u=v := (states_finish R s p).symm.trans
      ((congrArg (finish s) hpq).trans (states_finish R s q))
    subst v
    have h := ih hpq
    subst q
    congr 2
    exact Subtype.ext (Subsingleton.elim e.val f.val)

theorem states_surjective (R : S → S → Prop) (s : S) (n : ℕ) :
    ∀ (t : S) (ts : List S), ts.length=n → Chain R s ts → finish s ts=t →
      ∃ p : FiniteTransfer.Paths (Edge R) s n t, states R s p=ts := by
  induction n with
  | zero =>
    intro t ts hn hc ht
    have hnil : ts=[] := List.length_eq_zero.mp hn
    subst ts
    exact ⟨⟨(),ht⟩,rfl⟩
  | succ n ih =>
    intro t ts hn hc ht
    induction ts using List.reverseRecOn with
    | nil => simp at hn
    | append_singleton xs v _ =>
      have hv : v=t := by simpa [finish_append,finish] using ht
      clear ht
      subst t
      obtain ⟨hx,he⟩ := (chain_append R s xs [v]).mp hc
      have hlen : xs.length=n := by simpa using hn
      obtain ⟨p,hp⟩ := ih (finish s xs) xs hlen hx rfl
      refine ⟨⟨finish s xs,p,⟨(),he.1⟩⟩,?_⟩
      simp only [states,hp]

abbrev Accepted (R : S → S → Prop) (P : S → Prop) (s : S) (n : ℕ) :=
  Σ t : {t // P t}, FiniteTransfer.Paths (Edge R) s n t.val

abbrev AcceptedLists (R : S → S → Prop) (P : S → Prop) (s : S) (n : ℕ) :=
  {ts : List S // ts.length=n ∧ Chain R s ts ∧ P (finish s ts)}

def toList (R : S → S → Prop) (P : S → Prop) (s : S) (n : ℕ)
    (p : Accepted R P s n) : AcceptedLists R P s n :=
  ⟨states R s p.2, states_length R s p.2, states_chain R s p.2,
    (states_finish R s p.2).symm ▸ p.1.property⟩

theorem toList_bijective (R : S → S → Prop) (P : S → Prop) (s : S) (n : ℕ) :
    Function.Bijective (toList R P s n) := by
  constructor
  · intro p q he
    rcases p with ⟨⟨u,hu⟩,p⟩
    rcases q with ⟨⟨v,hv⟩,q⟩
    have hpq := congrArg Subtype.val he
    change states R s p=states R s q at hpq
    have huv : u=v := (states_finish R s p).symm.trans
      ((congrArg (finish s) hpq).trans (states_finish R s q))
    subst v
    have h := states_injective R s hpq
    subst q
    rfl
  · intro ts
    obtain ⟨p,hp⟩ := states_surjective R s n (finish s ts.val) ts.val
      ts.property.1 ts.property.2.1 rfl
    exact ⟨⟨⟨finish s ts.val,ts.property.2.2⟩,p⟩,Subtype.ext hp⟩

noncomputable def listEquiv (R : S → S → Prop) (P : S → Prop) (s : S) (n : ℕ) :
    Accepted R P s n ≃ AcceptedLists R P s n :=
  Equiv.ofBijective (toList R P s n) (toList_bijective R P s n)

#print axioms listEquiv
end MathLean.PathLists
