"""Independent exact matching enumeration on an explicitly constructed graph.

This verifier does not import or use the column-transfer implementation.
The recursion takes the first unprocessed vertex v and either leaves it
unmatched, or matches it to one of its unprocessed neighbours.  Unmatched
vertices must form an independent set.  A forbidden mask records remaining
vertices adjacent to an already chosen unmatched vertex; such vertices must
be matched.  Hence each completed branch is exactly one maximal matching.

Memoization only shares identical remaining graph subproblems; it neither
changes the branching rule nor uses a conjectured minimum or period.  --raw
disables memoization and traverses every admissible partial matching.

Run: python independent_check.py --max-n 12 --output independent_results.json
     python independent_check.py --max-n 4 --raw
"""

import argparse
import functools
import json
import time


def rectangular_grid(rows, columns):
    """Explicit graph, labelled column-major: vertex c*rows+r."""
    adjacency = [0] * (rows * columns)
    for column in range(columns):
        for row in range(rows):
            vertex = column * rows + row
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                rr, cc = row + dr, column + dc
                if 0 <= rr < rows and 0 <= cc < columns:
                    adjacency[vertex] |= 1 << (cc * rows + rr)
    return tuple(adjacency)


def minimum_maximal_matchings(adjacency, memoize=True):
    """Return (minimum cardinality, number attaining it, recursion statistics).

    Invariant: all vertices outside remaining have already been decided;
    all chosen edges are disjoint; all chosen unmatched vertices form an
    independent set; forbidden consists of remaining vertices adjacent to
    an already chosen unmatched vertex.  Previously chosen edges need no
    record because their endpoints have been removed.
    """
    infinity = len(adjacency) + 1
    calls = 0

    def branch(remaining, forbidden):
        nonlocal calls
        calls += 1
        if not remaining:
            return 0, 1
        first = remaining & -remaining
        vertex = first.bit_length() - 1
        rest = remaining ^ first
        best, ways = infinity, 0
        if not forbidden & first:
            best, ways = visit(rest, (forbidden | adjacency[vertex]) & rest)
        neighbours = adjacency[vertex] & rest
        while neighbours:
            partner = neighbours & -neighbours
            neighbours ^= partner
            reduced = rest ^ partner
            candidate, count = visit(reduced, forbidden & reduced)
            candidate += 1
            if candidate < best:
                best, ways = candidate, count
            elif candidate == best:
                ways += count
        return best, ways

    visit = functools.lru_cache(maxsize=None)(branch) if memoize else branch
    minimum, count = visit((1 << len(adjacency)) - 1, 0)
    statistics = {"evaluated_subproblems": calls, "memoized": memoize}
    if memoize:
        statistics["cache_hits"] = visit.cache_info().hits
    return minimum, count, statistics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=12)
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.max_n < 1:
        parser.error("--max-n must be positive")
    results = []
    for n in range(1, args.max_n + 1):
        started = time.perf_counter()
        minimum, count, statistics = minimum_maximal_matchings(
            rectangular_grid(4, n), not args.raw
        )
        row = {"n": n, "m": minimum, "A": count, **statistics}
        row["seconds"] = round(time.perf_counter() - started, 6)
        results.append(row)
        print(json.dumps(row), flush=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump({"method": "first-vertex graph matching recursion", "results": results},
                      handle, indent=2)
            handle.write("\n")


if __name__ == "__main__":
    main()
