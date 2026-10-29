"""Independently regenerate column patterns, then audit the finite certificates.

No import of transfer.py or analyze_grammar.py.  Python 3.9+ standard library.
Run from the supplement directory: python independent_grammar_audit.py
"""
import json
import itertools
from collections import Counter, defaultdict, deque


def closure(seeds, arcs):
    seen = set(seeds)
    todo = list(seeds)
    while todo:
        for successor in arcs[todo.pop()]:
            if successor not in seen:
                seen.add(successor)
                todo.append(successor)
    return seen


def column_completions(incoming, previous_holes):
    """Fill the first undecided row, producing each physical column pattern."""
    def fill(used, outgoing, holes, cost):
        if used == 15:
            yield (outgoing, holes, cost)
            return
        bit = (15 ^ used) & -(15 ^ used)
        # Uncovered cell: forbid vertical and previous-column uncovered neighbours.
        if not (previous_holes & bit or holes & ((bit << 1) | (bit >> 1))):
            yield from fill(used | bit, outgoing, holes | bit, cost)
        # Start a horizontal domino crossing into the next column.
        yield from fill(used | bit, outgoing | bit, holes, cost + 1)
        # Vertical domino occupies two consecutive rows.
        if bit < 8 and not used & (bit << 1):
            yield from fill(used | bit | (bit << 1), outgoing, holes, cost + 1)
    yield from fill(incoming, 0, 0, 0)


def strongly_connected(vertices, adjacency):
    reverse = defaultdict(list)
    for vertex in vertices:
        for successor in adjacency[vertex]:
            reverse[successor].append(vertex)
    remaining = set(vertices)
    components = []
    while remaining:
        vertex = min(remaining)
        component = closure([vertex], adjacency) & closure([vertex], reverse)
        components.append(component)
        remaining -= component
    return components


def main():
    with open('potential.json', encoding='utf-8') as handle:
        certificate = json.load(handle)
    with open('grammar_data.json', encoding='utf-8') as handle:
        supplied = json.load(handle)
    states = [(incoming, holes) for incoming in range(16) for holes in range(16)
              if not incoming & holes and not holes & (holes << 1)]
    assert states == [tuple(s) for s in certificate['states']]
    index = {state: i for i, state in enumerate(states)}
    potential = [value + 4 for value in certificate['potential']]
    assert potential == supplied['potential']
    arcs = []
    for i, (incoming, previous_holes) in enumerate(states):
        for outgoing, holes, cost in column_completions(incoming, previous_holes):
            arcs.append((i, index[outgoing, holes], cost))
    assert len(arcs) == len(set(arcs))
    assert len(arcs) == len({(i, j) for i, j, cost in arcs})
    start = index[0, 0]
    terminals = [index[s] for s in states if s[0] == 0]
    assert potential[start] == 0
    assert {potential[i] for i in terminals} == {-1, 0}
    assert [states[i] for i in terminals if potential[i] < 0] == [(0, 9)]
    zero, zero_reverse = defaultdict(list), defaultdict(list)
    histogram = Counter()
    for i, j, cost in arcs:
        defect = 3 * cost - 4 + potential[i] - potential[j]
        assert defect >= 0
        histogram[defect] += 1
        if defect == 0:
            zero[i].append(j)
            zero_reverse[j].append(i)
    assert histogram == {0: 111, 1: 99, 2: 59, 3: 20, 4: 15}
    bridge = closure([start], zero) & closure([index[0, 9]], zero_reverse)
    bridge_arcs = [(i, j) for i in bridge for j in zero[i] if j in bridge]
    assert bridge == {start, index[0, 9]}
    assert bridge_arcs == [(start, index[0, 9])]
    print('Independent physical column enumeration:', len(states), 'states,', len(arcs), 'arcs')
    print('Nonnegative reduced costs and exceptional zero-path certificate: PASS')
    print('Defect histogram:', dict(sorted(histogram.items())))

    adjacency, reverse = defaultdict(list), defaultdict(list)
    vertices = [(i, budget) for budget in range(4) for i in range(len(states))]
    for i, budget in vertices:
        for origin, j, cost in arcs:
            if origin != i:
                continue
            new_budget = budget + 3 * cost - 4 + potential[i] - potential[j]
            if new_budget <= 3:
                adjacency[i, budget].append((j, new_budget))
                reverse[j, new_budget].append((i, budget))
    accept = {(i, budget) for i in terminals for budget in range(4)
              if 0 <= budget + potential[i] <= 2}
    active = closure([(start, 0)], adjacency) & closure(accept, reverse)
    ordered = sorted(active, key=lambda item: (item[1], item[0]))
    position = {vertex: i for i, vertex in enumerate(ordered)}
    edge_list = [(position[v], position[w]) for v in ordered
                 for w in adjacency[v] if w in active]
    accept_indices = [position[v] for v in ordered if v in accept]
    assert ordered == [tuple(vertex) for vertex in supplied['vertices']]
    assert sorted(edge_list) == sorted(map(tuple, supplied['edges']))
    assert accept_indices == supplied['accept']
    assert position[start, 0] == supplied['start']
    vectors = []
    current = [0] * len(ordered)
    current[position[start, 0]] = 1
    for n in range(41):
        vectors.append(current)
        assert sum(current[i] for i in accept_indices) == supplied['sequence'][n]
        following = [0] * len(ordered)
        for i, j in edge_list:
            following[j] += current[i]
        current = following
    assert all(vectors[26][i] - 3 * vectors[23][i] + 3 * vectors[20][i]
               - vectors[17][i] == 0 for i in range(len(ordered)))
    print('Regenerated trimmed grammar:', len(ordered), 'vertices,', len(edge_list), 'arcs')
    print('Full 114-coordinate row-vector identity at n=26: PASS')

    # SCC structure explains the degree-two quasipolynomial denominator.
    active_arcs = {v: [w for w in adjacency[v] if w in active] for v in active}
    components = strongly_connected(active, active_arcs)
    component_of = {v: i for i, component in enumerate(components) for v in component}
    cyclic = {i for i, component in enumerate(components)
              if len(component) > 1 or next(iter(component)) in active_arcs[next(iter(component))]}
    for i in cyclic:
        component = components[i]
        assert len(component) == 3
        assert all(sum(w in component for w in active_arcs[v]) == 1 for v in component)
    dag = defaultdict(set)
    indegree = [0] * len(components)
    for v in active:
        for w in active_arcs[v]:
            i, j = component_of[v], component_of[w]
            if i != j and j not in dag[i]:
                dag[i].add(j)
                indegree[j] += 1
    queue = deque(i for i in range(len(components)) if indegree[i] == 0)
    best = [-1000] * len(components)
    start_component = component_of[start, 0]
    best[start_component] = int(start_component in cyclic)
    while queue:
        i = queue.popleft()
        for j in dag[i]:
            best[j] = max(best[j], best[i] + int(j in cyclic))
            indegree[j] -= 1
            if not indegree[j]:
                queue.append(j)
    max_cycles = max(best[component_of[v]] for v in accept if v in active)
    assert max_cycles == 3
    print('Cyclic SCCs:', len(cyclic), '; all simple directed 3-cycles')
    print('Maximum cyclic SCCs along an accepted path:', max_cycles)
    print('Cyclic state sets:', [[(states[v[0]], v[1]) for v in sorted(components[i])]
                                 for i in sorted(cyclic)])

    # Every periodic zero-defect motif is horizontal and has one hole per
    # row per three columns.  Its row phases are a proper 3-colouring of P4.
    base_components = strongly_connected(range(len(states)), zero)
    base_cycles = [component for component in base_components
                   if len(component) > 1 or next(iter(component)) in zero[next(iter(component))]]
    assert len(base_cycles) == 8
    cost_of = {(i, j): cost for i, j, cost in arcs}
    normalized_phases = set()
    for component in base_cycles:
        assert len(component) == 3
        ordered_cycle = [min(component)]
        for unused in range(2):
            successors = [j for j in zero[ordered_cycle[-1]] if j in component]
            assert len(successors) == 1
            ordered_cycle.append(successors[0])
        assert set(ordered_cycle) == component
        assert ordered_cycle[0] in zero[ordered_cycle[-1]]
        for i, j in zip(ordered_cycle, ordered_cycle[1:] + ordered_cycle[:1]):
            # The cost equals outgoing horizontal count, leaving zero verticals.
            assert cost_of[i, j] == bin(states[j][0]).count('1')
        phases = []
        for row in range(4):
            hole_columns = [column for column, i in enumerate(ordered_cycle)
                            if states[i][1] & (1 << row)]
            assert len(hole_columns) == 1
            phases.append(hole_columns[0])
        assert all(phases[row] != phases[row + 1] for row in range(3))
        normalized_phases.add(tuple((phase - phases[0]) % 3 for phase in phases))
    expected_phases = {(0,) + suffix for suffix in itertools.product(range(3), repeat=3)
                       if all(a != b for a, b in zip((0,) + suffix, suffix))}
    assert normalized_phases == expected_phases
    assert len(normalized_phases) == 8
    print('Eight base cycles: all horizontal, exactly the proper 3-colourings of P4 modulo shift')
    print('Normalized hole phases:', sorted(normalized_phases))


if __name__ == '__main__':
    main()
