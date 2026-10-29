"""Check the printed worked examples and compare outer words with fresh mex."""
import json
from math import gcd
from pathlib import Path
from classify import classify
from near.uniform_classification import formula, upper_towers


def compare(a, c):
    row = classify(a, c)
    p, q, H, W = (row[k] for k in ('p', 'q', 'prefix', 'block'))
    g = []
    for n in range(q+c+p):
        options = {g[n-s] for s in (a, 4*a, c) if s <= n}
        v = next(j for j in range(4) if j not in options)
        g.append(v)
        assert v == int(H[n] if n < q else W[(n-q) % p]), (a, c, n)
    assert g[q-1] != g[q+p-1]
    return len(g)


def main():
    z = classify(3, 13)
    assert (z['p'], z['q']) == (16, 31)
    assert z['prefix'] == '0001110001112223002113000111223'
    assert z['block'] == '0001112000111222'
    z = classify(2, 9)
    assert z['prefix'] == '001100112230213001123'
    assert z['block'] == '00112001122'
    p, q, symbol = formula(83, 417)
    X, Y = upper_towers(41)
    assert X == '012'+'01012'*34+'01201012'*10
    assert Y == '012'*2+'01012'*29+'01201012'*12
    T = Y+X
    assert (len(X),len(Y),p,q,pow(83,-1,p)) == (253,247,500,31374,247)
    assert (247*q-220) % p == 158
    table = [(0,0,0),(83,1,1),(332,2,2),(417,3,2),(18260,0,0),
             (31373,2,1),(31374,2,2),(31873,1,1),(31874,2,2)]
    for n,g,c in table:
        assert int(symbol(n)) == g and int(T[(247*n-220) % p]) == c
    assert symbol(q-1) != symbol(q+p-1)
    cases = {(3,13), (2,9), (83,417)}
    # Every large-c residue band, including rational boundaries and a=2.
    cases |= {(a,c) for a in range(2,12) for c in range(6*a+1,16*a+1)
              if gcd(a,c)==1}
    total = sum(compare(a,c) for a,c in sorted(cases))
    result = dict(printed_examples=True, central_table=table,
                  fresh_recurrence_games=len(cases), recurrence_positions=total)
    dest = Path(__file__).resolve().parents[1]/'certificates/examples_verified.json'
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(f'Printed examples agree; {len(cases)} fresh recurrence comparisons passed ({total} positions).')


if __name__ == '__main__':
    main()
