"""Explicit optimal constructions; independent elementary verification.

Run with: python structure_construction.py
Coordinates are zero-based (row, column); each domino is a pair of cells.
"""

BLOCKS = {
    'S': (1, [((1, 0), (2, 0))]),
    'F': (1, [((0, 0), (1, 0)), ((2, 0), (3, 0))]),
    'P': (3, [((1, 0), (2, 0)), ((0, 1), (0, 2)),
              ((2, 1), (3, 1)), ((1, 2), (2, 2))]),
    'B': (3, [((1, 0), (1, 1)), ((3, 0), (3, 1)),
              ((0, 1), (0, 2)), ((2, 1), (2, 2))]),
    'Q': (3, [((3, 0), (3, 1)), ((1, 0), (2, 0)),
              ((0, 1), (1, 1)), ((1, 2), (2, 2))]),
}


def construction(n):
    if n < 1:
        raise ValueError('n must be positive')
    if n < 6:
        word = ('S', 'SF', 'SFS', 'SFSF', 'SFSFS')[n-1]
    else:
        k, rem = divmod(n - 6, 3)
        word = 'P' + 'B' * k + 'Q' + ('', 'F', 'FS')[rem]
    edges = from_word(word)
    assert max(c for edge in edges for r, c in edge) < n
    return edges


def from_word(word):
    edges = []
    offset = 0
    for symbol in word:
        width, local_edges = BLOCKS[symbol]
        for edge in local_edges:
            edges.append(tuple((r, c + offset) for r, c in edge))
        offset += width
    return edges


def verify(n, edges):
    covered = set()
    for u, v in edges:
        assert 0 <= u[0] < 4 and 0 <= v[0] < 4
        assert 0 <= u[1] < n and 0 <= v[1] < n
        assert abs(u[0]-v[0]) + abs(u[1]-v[1]) == 1
        assert u not in covered and v not in covered
        covered.update((u, v))
    holes = {(r,c) for r in range(4) for c in range(n)} - covered
    for r, c in holes:
        assert (r+1, c) not in holes and (r, c+1) not in holes
    target = 1 if n == 1 else (4*n+2)//3
    assert len(edges) == target


def row_reflection(edges):
    return [tuple((3-r, c) for r, c in edge) for edge in edges]


def family_at_multiple_of_three(k):
    """The complete family for n=3k, using the proved A(n) theorem."""
    if k < 1:
        raise ValueError('k must be positive')
    if k == 1:
        words = ('B', 'P', 'Q')
    else:
        words = tuple(('P' if left else '') + 'B'*(k-left-right)
                      + ('Q' if right else '')
                      for left in (0, 1) for right in (0, 1))
    family = [from_word(word) for word in words]
    family += [row_reflection(edges) for edges in list(family)]
    if k == 1:
        family.append(from_word('SFS'))
    if k == 2:
        array = ('.aa.b.', 'c.ddbe', 'cfgg.e', '.f.hh.')
        extra = {}
        for r, row in enumerate(array):
            for c, letter in enumerate(row):
                if letter != '.':
                    extra.setdefault(letter, []).append((r, c))
        edges = [tuple(cells) for cells in extra.values()]
        family.extend((edges, row_reflection(edges)))
    return family


if __name__ == '__main__':
    for n in range(1, 201):
        verify(n, construction(n))
    print('Explicit constructions checked for every n=1,...,200.')
    for k in range(1, 51):
        family = family_at_multiple_of_three(k)
        for edges in family:
            verify(3*k, edges)
        keys = {frozenset(frozenset(edge) for edge in edges) for edges in family}
        assert len(keys) == len(family) == (7 if k == 1 else 10 if k == 2 else 8)
    print('Explicit divisible-by-three families valid and distinct for k=1,...,50.')
