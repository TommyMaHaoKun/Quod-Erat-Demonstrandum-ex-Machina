"""Exact finite exploration only; this is not an all-index proof."""
import argparse
import json
import time

import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=40)
    args = parser.parse_args()
    x = sp.Symbol("x")
    p = [sp.Poly(v, x, domain=sp.ZZ) for v in
         [1, x + 2, x**2 + 6*x + 5, x**3 + 10*x**2 + 25*x + 12]]
    for n in range(4, args.max_n + 1):
        p.append(sp.Poly((x+3)*p[-1].as_expr() +
                        (x-1)*p[-2].as_expr() +
                        (x-1)*p[-3].as_expr() +
                        x*p[-4].as_expr(), x, domain=sp.ZZ))
    started = time.time()
    for n in range(1, args.max_n + 1):
        negative = int(p[n].count_roots(-sp.oo, 0))
        squarefree = sp.gcd(p[n], p[n].diff()).degree() == 0
        assert p[n].degree() == n
        assert p[n].eval(0) > 0
        assert negative == n, (n, negative)
        assert squarefree, n
        print(json.dumps({"n": n, "negative_real_roots": negative,
                          "squarefree": squarefree,
                          "elapsed_seconds": round(time.time()-started, 3)}),
              flush=True)


if __name__ == "__main__":
    main()
