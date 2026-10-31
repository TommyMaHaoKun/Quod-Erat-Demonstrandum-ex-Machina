"""Independent counts of the 5 x n arrays, straight from the definition.

1. cell_count(n): dynamic programming over order ideals stored as cell
   bitmasks.  A cell may be filled next exactly when every cell that must
   carry a smaller entry (left, up, up-left, up-right neighbour) is already
   filled.  No profile description is used.
2. profile_count(n): the row-length profile walk of Lemma 1 of the paper.
3. brute(n): literal enumeration of all fillings for n <= 2.

The three agree with each other, with the double sum of Theorem 3, and with
the OEIS b-file.
"""
import itertools
import sys
from common import a_double_sum, load_bfile

ROWS = 5


def predecessors(n):
    pred = {}
    for i in range(ROWS):
        for j in range(n):
            ps = []
            # the four directions (0,1), (1,0), (1,1), (1,-1) point to larger entries
            for di, dj in ((0, 1), (1, 0), (1, 1), (1, -1)):
                ii, jj = i - di, j - dj          # cell that must be smaller
                if 0 <= ii < ROWS and 0 <= jj < n:
                    ps.append(ii * n + jj)
            pred[i * n + j] = ps
    return pred


def cell_count(n):
    pred = predecessors(n)
    need = {c: sum(1 << p for p in ps) for c, ps in pred.items()}
    cur = {0: 1}
    for _ in range(ROWS * n):
        nxt = {}
        for mask, cnt in cur.items():
            for c in range(ROWS * n):
                if not mask >> c & 1 and mask & need[c] == need[c]:
                    m2 = mask | 1 << c
                    nxt[m2] = nxt.get(m2, 0) + cnt
        cur = nxt
    return cur[(1 << ROWS * n) - 1]


def profile_ok(x, n):
    return all(x[i] == 0 or x[i - 1] >= min(n, x[i] + 1) for i in range(1, len(x)))


def profile_count(n):
    cur = {(0,) * ROWS: 1}
    for _ in range(ROWS * n):
        nxt = {}
        for x, cnt in cur.items():
            for i in range(ROWS):
                if x[i] < n:
                    y = x[:i] + (x[i] + 1,) + x[i + 1:]
                    if profile_ok(y, n):
                        nxt[y] = nxt.get(y, 0) + cnt
        cur = nxt
    return cur[(n,) * ROWS]


def brute(n):
    cells = [(i, j) for i in range(ROWS) for j in range(n)]
    cnt = 0
    for perm in itertools.permutations(range(1, ROWS * n + 1)):
        u = dict(zip(cells, perm))
        good = True
        for (i, j) in cells:
            for di, dj in ((0, 1), (1, 0), (1, 1), (1, -1)):
                c = (i + di, j + dj)
                if c in u and not u[(i, j)] < u[c]:
                    good = False
                    break
            if not good:
                break
        cnt += good
    return cnt


def main(cell_max=7, profile_max=30):
    b = load_bfile()
    report = {}
    for n in (1, 2):
        assert brute(n) == b[n]
    report["brute_force_n"] = [1, 2]
    for n in range(1, cell_max + 1):
        assert cell_count(n) == b[n], n
    report["cell_dp_max_n"] = cell_max
    for n in range(1, profile_max + 1):
        assert profile_count(n) == b[n], n
        assert a_double_sum(n) == b[n], n
    report["profile_dp_and_double_sum_max_n"] = profile_max
    report["first_values"] = [b[n] for n in range(1, 8)]
    return report


if __name__ == "__main__":
    print(main(*(int(a) for a in sys.argv[1:])))
