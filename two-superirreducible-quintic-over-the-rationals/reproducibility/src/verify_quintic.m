// Complete arithmetic verification for the cyclic quintic theorem.
// Tested with Magma V2.30-1. Run in a fresh Magma process.
SetSeed(1);
proofbound := map< PowerStructure(RngOrd) -> Integers() |
                     order :-> MinkowskiBound(order) >;
SetClassGroupBoundMaps(proofbound, proofbound);

Q<x> := PolynomialRing(Rationals());
h := x^5+x^4-4*x^3-3*x^2+3*x+1;
f := x^5+6*x^4-x^3-10*x^2-6*x-1;
assert IsIrreducible(f);
K<r> := NumberField(h);
alpha := r-r^2-r^3;
assert MinimalPolynomial(alpha) eq f;
assert Discriminant(Integers(K)) eq 11^4;
assert ClassNumber(K : Proof:="Full") eq 1;
print "FIELD: degree 5, discriminant 14641, unconditional class number 1";

Rx<X> := PolynomialRing(K);
q := ExactQuotient(Evaluate(f,X),X-alpha);
k := r-1;
b := -2*r^4-4*r^3+6*r^2+11*r-4;
A := 2*r^4-r^3-8*r^2+2*r+4;
B := 5*r^4+4*r^3-r^2-6*r-41;
C := -11*r^4+77*r^2-132;
ecubic := X^3+A*X^2+B*X+C;
d := k*X+b;
assert b^2 eq 11*(4-r^2);
assert b ne 0;
assert &+[Coefficient(q,i)*X^i*d^(4-i) : i in [0..4]] eq b^2*ecubic;
E := EllipticCurve([K|0,A,0,B,C]);
P1 := ProjectiveSpace(Rationals(),1);
cov := map<E -> P1 | [E.1,k*E.1+b*E.3]>;
origin_image := cov(E!0);
assert origin_image[1]/origin_image[2] eq 1/k;
assert Valuation(Norm(Discriminant(E)),3) eq 0;
assert Valuation(Norm(b),3) eq 0;
print "GOOD REDUCTION: norms of discriminant and map determinant:",
      Norm(Discriminant(E)), Norm(b);
print "MODEL: exact quartic/elliptic identity verified";

fulltorsion,fulltorsionmap := TorsionSubgroup(E);
assert Invariants(fulltorsion) eq [2,2];
success,G,MWmap := PseudoMordellWeilGroup(E);
assert success;
assert Invariants(G) eq [2,2,0];
T1 := MWmap(G.1);
T2 := MWmap(G.2);
P := MWmap(G.3);
assert #TwoSelmerGroup(E) eq 8;
assert 2*P ne E!0;
assert 2*T1 eq E!0 and 2*T2 eq E!0 and T1 ne T2;
torsion := {i*T1+j*T2 : i,j in [0,1]};
assert #torsion eq 4;
print "DESCENT: finite odd index subgroup Z/2 + Z/2 + Z";
print "RANK: 2-Selmer group order 8, full torsion order 4, infinite point P";
print "GENERATORS:", [T1,T2,P];

sat := Saturation([P],5 : TorsionFree:=true);
assert #sat eq 1;
assert &or[sat[1] eq e*P+T : e in [-1,1], T in torsion];
print "SATURATION: unchanged modulo sign and torsion through prime 5";

N,V,index_condition,L := Chabauty(MWmap,cov,3);
assert N eq 2;
assert #V eq 2;
assert &and[p in {2,3,5} : p in PrimeDivisors(index_condition)];
assert &and[cov(MWmap(v)) eq P1![1,0] : v in V];
print "CHABAUTY: prime 3, upper bound", N;
print "INDEX CONDITION:", index_condition;
print "GROUP ELEMENTS:", V;
print "IMAGES:", [cov(MWmap(v)) : v in V];
print "PASS: all points of E(K) with rational cov-image map to infinity";
print "PASS: f is 2-superirreducible over Q";
