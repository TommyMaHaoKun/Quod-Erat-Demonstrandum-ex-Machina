"""Check the finite data of the elementary proof, using Python integers only.

The proof bridge from these checks to ideal equality and minimality is in the
paper. This verifier is independent of the search/support-graph algorithm.
"""

from itertools import product
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def divides(a, b):
    return all(x <= y for x, y in zip(a, b))


def verify():
    generators = (6, 7, 8, 9)
    auxiliary_weights = (1, 4, 6, 7)
    rules = (
        ((0, 2, 0, 0), (1, 0, 1, 0)),
        ((0, 1, 1, 0), (1, 0, 0, 1)),
        ((0, 0, 2, 0), (0, 1, 0, 1)),
        ((0, 0, 0, 2), (3, 0, 0, 0)),
    )
    for lhs, rhs in rules:
        require(dot(lhs, generators) == dot(rhs, generators), "Toric relation")
        require(dot(lhs, auxiliary_weights) > dot(rhs, auxiliary_weights),
                "Termination weight")

    # Pure squares on y,z,w force every terminal exponent on those variables
    # to be zero or one. Exhausting that cube checks the proposed full basis.
    leading_terms = [rule[0] for rule in rules]
    for index in (1, 2, 3):
        square = tuple(2 if i == index else 0 for i in range(4))
        require(square in leading_terms, "Pure square leading term")
    terminal = [b for b in product(range(1), range(2), range(2), range(2))
                if not any(divides(a, b) for a in leading_terms)]
    degrees = sorted(dot(b, generators) for b in terminal)
    require(degrees == [0, 7, 8, 9, 16, 17], "Terminal monomial degrees")
    require(sorted(d % 6 for d in degrees) == list(range(6)),
            "Distinct residues, hence independent normal monomials")

    # 12,...,17 form a complete block of six represented integers. Adding 6
    # proves that all later integers are represented.
    represented = {dot(a, generators) for a in product(range(7), repeat=4)}
    require(all(n in represented for n in range(12, 18)), "Conductor block")
    gaps = [n for n in range(12) if n not in represented]
    require(gaps == [1, 2, 3, 4, 5, 10, 11], "Exact nonnegative gaps")

    def in_semigroup(n):
        return n >= 12 or n in (0, 6, 7, 8, 9)

    # For f < -6, f+6 is negative. This finite window covers every other
    # negative integer that could occur in the definition of PF(S).
    require(all(any(not in_semigroup(f + g) for g in generators)
                for f in range(-6, 0)), "No negative pseudo-Frobenius numbers")
    pf = [f for f in gaps if all(in_semigroup(f + g) for g in generators)]
    require(pf == [10, 11], "Pseudo-Frobenius set")
    ng = (11, 10, 10, 10)
    ng_table = [[g + p - q for q in pf] for g, p in zip(generators, ng)]
    require(all(in_semigroup(n) for row in ng_table for n in row), "NG vector")
    require(not in_semigroup(1) and not in_semigroup(11 - 1) and 1 not in pf,
            "Failure of almost symmetry")

    # Below degree 14, no monomial has any exponent greater than two. Thus
    # this enumeration exhausts all such monomials.
    low_degrees = [dot(a, generators) for a in product(range(3), repeat=4)
                   if dot(a, generators) < 14]
    require(len(low_degrees) == len(set(low_degrees)), "No relation below 14")
    relation_degrees = [dot(a, generators) for a, _ in rules]
    require(relation_degrees == [14, 15, 16, 18], "Relation degrees")
    require(len(set(relation_degrees)) == 4, "Distinct graded classes")
    require(max(relation_degrees) < min(generators) + min(relation_degrees),
            "All four classes survive modulo the homogeneous maximal ideal")
    return {
        "status": "PASS",
        "method": "exact finite checks of terminating normal-form proof",
        "minimal_generators": generators,
        "frobenius": 11,
        "gaps": gaps,
        "pseudo_frobenius": pf,
        "ng_vector": ng,
        "ng_table": ng_table,
        "almost_symmetric": False,
        "auxiliary_weights": auxiliary_weights,
        "normal_basis_degrees": degrees,
        "minimal_relation_degrees": relation_degrees,
        "minimal_relation_count": 4,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
