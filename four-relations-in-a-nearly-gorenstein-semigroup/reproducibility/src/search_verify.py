#!/usr/bin/env python3
"""Exact certificate for S=<6,7,8,9>; standard library only.

Run from any directory:
  python src/search_verify.py
Optional --write regenerates the checked JSON certificate in certificates/.

The proof that the support graph gives the exact minimal number of binomial
relations is stated in the paper. This verifier separately enumerates full
factorizations and their connected components through the proven finite bound.
"""
import argparse
import json
from math import gcd
from pathlib import Path

G = (6, 7, 8, 9)
ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "search_counterexample_6_7_8_9.json"


def factorizations(n, generators=G):
    """All tuples of nonnegative exponents with the indicated exact degree."""
    if len(generators) == 1:
        return [(n // generators[0],)] if n >= 0 and n % generators[0] == 0 else []
    result = []
    for e in range(n // generators[0] + 1):
        result.extend((e,) + rest for rest in factorizations(n - e * generators[0], generators[1:]))
    return result


def components(vertices):
    """Connected components: edges join factorizations sharing a generator."""
    remaining = set(range(len(vertices)))
    comps = []
    while remaining:
        stack = [min(remaining)]
        comp = []
        remaining.remove(stack[0])
        while stack:
            i = stack.pop()
            comp.append(i)
            neighbors = {j for j in remaining if any(x and y for x, y in zip(vertices[i], vertices[j]))}
            remaining -= neighbors
            stack.extend(sorted(neighbors, reverse=True))
        comps.append(sorted(comp))
    return comps


def compute():
    assert gcd(gcd(G[0], G[1]), gcd(G[2], G[3])) == 1
    # Six consecutive represented values prove all integers >=12 lie in S.
    conductor = 12
    conductor_block = {str(n): factorizations(n) for n in range(conductor, conductor + G[0])}
    assert all(conductor_block.values())
    gap_set = [n for n in range(conductor) if not factorizations(n)]
    assert gap_set == [1, 2, 3, 4, 5, 10, 11]
    F = max(gap_set)
    assert all(factorizations(g) == [tuple(int(i == j) for i in range(4))] for j, g in enumerate(G))
    def member(n):
        return n >= 0 and bool(factorizations(n))
    # Every f < -6 fails because f+6 < 0. Exhaust the remaining negative
    # candidates -6,...,-1 and record a generator witnessing failure.
    negative_pf_witnesses = {
        str(f): next(g for g in G if not member(f + g))
        for f in range(-G[0], 0)
    }
    assert all(not member(int(f) + g) for f, g in negative_pf_witnesses.items())
    pf = [f for f in gap_set if all(member(f + g) for g in G)]
    assert pf == [10, 11]
    ng_vector = [11, 10, 10, 10]
    ng_matrix = [[g + p - q for q in pf] for g, p in zip(G, ng_vector)]
    assert all(p in pf for p in ng_vector)
    assert all(member(n) for row in ng_matrix for n in row)
    witness = 1
    assert witness in gap_set and F - witness in gap_set and witness not in pf
    apery = [next(n for n in range(r, conductor + G[0], G[0]) if member(n)) for r in range(G[0])]
    assert apery == [0, 7, 8, 9, 16, 17]
    # For n>F+8+9, n-gi-gj>F for all i!=j. Thus every support-graph
    # vertex and edge is present; its graph and the full factorization graph
    # are connected. The exact finite search therefore covers all Betti degrees.
    bound = F + G[-2] + G[-1]
    degree_rows = []
    betti = []
    for n in range(bound + 1):
        fs = factorizations(n)
        cs = components(fs)
        row = {"degree": n, "factorizations": fs, "components_by_index": cs}
        degree_rows.append(row)
        if len(cs) > 1:
            betti.append({"degree": n, "factorizations": fs, "component_count": len(cs)})
    rho = sum(row["component_count"] - 1 for row in betti)
    assert [row["degree"] for row in betti] == [14, 15, 16, 18]
    assert rho == 4
    # Independently verify all data needed for the terminating normal-form proof.
    relations = [((0,2,0,0),(1,0,1,0)), ((0,1,1,0),(1,0,0,1)),
                 ((0,0,2,0),(0,1,0,1)), ((0,0,0,2),(3,0,0,0))]
    measure = (1, 4, 6, 7)
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    for left, right in relations:
        assert dot(left, G) == dot(right, G)
        assert dot(left, measure) > dot(right, measure)
    normal_bases = [(0,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(0,1,0,1),(0,0,1,1)]
    assert sorted(dot(b, G) % G[0] for b in normal_bases) == list(range(G[0]))
    for e2 in range(4):
        for e3 in range(4):
            for e4 in range(4):
                monomial = (0,e2,e3,e4)
                divisible = any(all(x >= y for x, y in zip(monomial, left)) for left, _ in relations)
                assert (not divisible) == (monomial in normal_bases)
    return {
        "claim": "Counterexample to rho in {5,6}: S=<6,7,8,9> has rho=4.",
        "arithmetic": "exact integers",
        "generators": G, "conductor": conductor, "conductor_block_factorizations": conductor_block,
        "gaps": gap_set, "Frobenius_number": F, "Apery_modulo_6": apery,
        "negative_PF_exclusion": {
            "general_case": "Every f < -6 has f+6 < 0, hence f+6 is outside S.",
            "remaining_negative_candidates_generator_witnesses": negative_pf_witnesses,
        },
        "pseudo_Frobenius_numbers": pf, "NG_vector": ng_vector,
        "NG_membership_matrix_columns_PF": ng_matrix,
        "non_almost_symmetric_witness": {"x": witness, "F_minus_x": F-witness, "x_is_PF": False},
        "all_Betti_degrees_search_bound": bound, "all_degree_factorizations": degree_rows,
        "Betti_elements": betti, "minimal_relation_count": rho,
        "relations_exponent_pairs": relations, "termination_weights": measure,
        "normal_form_bases": normal_bases,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = compute()
    normalized = json.loads(json.dumps(data))
    if args.write:
        CERTIFICATE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    saved = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert saved == normalized, "Saved certificate differs from exact recomputation"
    print("VERIFIED: minimal generators [6,7,8,9]; PF=[10,11]; nearly Gorenstein; not almost symmetric.")
    print("VERIFIED: complete Betti degrees [14,15,16,18], two components each; rho=4.")
    print("VERIFIED: terminating four-relation normal-form data and six residue classes.")


if __name__ == "__main__":
    main()
