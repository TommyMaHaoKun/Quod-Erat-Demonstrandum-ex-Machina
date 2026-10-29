"""Independent floating-point regression checks (NOT part of the proof).

Requires NumPy and mpmath.  The checks are:
  A. brute-force maximization over the probability simplex (grid search plus
     zooming refinement, no Lagrange formulas) versus the branch formula of
     Lemma 2.1;
  B. the endpoint inequality E(psi) <= E(2pi-3phi) on a dense parameter grid,
     using the branch formula, and constancy of E when r = 2;
  C. the endpoint inequality using brute-force maxima only;
  D. an experiment for the odd-polygon corollary: maximum over all vertex
     triples, and a replicator-dynamics search over all measures on P_N.
Writes certificates/numeric_regression_report.json relative to this script.
"""
from pathlib import Path
import json
import math
import random
import numpy as np
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
rng = random.Random(20261028)


def quad(u, v, a, b, c):
    w = 1.0 - u - v
    return 2.0*(u*v*a + u*w*b + v*w*c)


def brute_max(a, b, c):
    """Maximize 2(uv a + uw b + vw c) on the simplex without using any formula."""
    n = 400
    t = np.linspace(0.0, 1.0, n + 1)
    U, V = np.meshgrid(t, t, indexing='ij')
    mask = U + V <= 1.0 + 1e-15
    vals = np.where(mask, quad(U, V, a, b, c), -np.inf)
    i, j = np.unravel_index(np.argmax(vals), vals.shape)
    u0, v0, best = U[i, j], V[i, j], vals[i, j]
    h = 2.0/n
    for _ in range(45):
        uu = np.linspace(u0 - h, u0 + h, 41)
        vv = np.linspace(v0 - h, v0 + h, 41)
        U, V = np.meshgrid(uu, vv, indexing='ij')
        ok = (U >= 0) & (V >= 0) & (U + V <= 1.0)
        vals = np.where(ok, quad(U, V, a, b, c), -np.inf)
        i, j = np.unravel_index(np.argmax(vals), vals.shape)
        if vals[i, j] >= best:
            u0, v0, best = U[i, j], V[i, j], vals[i, j]
        h *= 0.5
    # also test the three edges exactly (maximum of a single edge is at its midpoint)
    return max(best, a/2, b/2, c/2)


def sides(r, phi, psi):
    a = (2*math.sin((phi - psi)/2))**r   # |A-B|^r
    b = (2*math.sin((phi + psi)/2))**r   # |A-C|^r
    c = (2*math.sin(phi))**r             # |B-C|^r
    return a, b, c


def sides_mp(r, phi, psi):
    return ((2*mp.sin((phi - psi)/2))**r, (2*mp.sin((phi + psi)/2))**r, (2*mp.sin(phi))**r)


def formula(a, b, c):
    """Lemma 2.1 / Clark-Laugesen with c the largest entry."""
    if a + b > c:
        return 2*a*b*c/(4*a*b - (a + b - c)**2)
    return c/2


report = {}

# ---- A ---------------------------------------------------------------------
worst = 0.0
samples = 0
cases = []
for _ in range(250):
    r = rng.choice([2.0, 2.0 + 1e-6, rng.uniform(2, 4), rng.uniform(4, 30), rng.uniform(30, 120)])
    phi = rng.uniform(math.pi/2 + 1e-9, 2*math.pi/3)
    psi = rng.choice([0.0, 2*math.pi - 3*phi, rng.uniform(0, 2*math.pi - 3*phi)])
    cases.append((r, phi, psi))
cases += [(2.0, 2*math.pi/3, 0.0), (5.0, 2*math.pi/3, 0.0), (3.0, math.pi/2 + 1e-6, 0.0)]
for r, phi, psi in cases:
    a, b, c = sides(r, phi, psi)
    bf, fm = brute_max(a, b, c), formula(a, b, c)
    rel = abs(bf - fm)/fm
    worst = max(worst, rel)
    samples += 1
    if rel > 1e-9:
        raise SystemExit(f'A failed at r={r}, phi={phi}, psi={psi}: brute {bf} formula {fm}')
report['A_bruteforce_vs_formula'] = {'samples': samples, 'max_relative_difference': worst}
print('A PASS', samples, worst)

# ---- B ---------------------------------------------------------------------
rs = [2.0, 2.0 + 1e-9, 2.0 + 1e-4, 2.1, 2.5, 3.0, 4.0, 6.0, 10.0, 20.0, 50.0, 100.0, 200.0]
phis = [math.pi/2 + (math.pi/6)*k/240 for k in range(1, 241)]
worst_excess = -math.inf
count = 0
min_gap_interior = mp.inf
r2_dev = 0.0
for r in rs:
    for phi in phis:
        end = 2*math.pi - 3*phi
        Eend = formula(*sides(r, phi, end))
        for j in range(0, 201):
            psi = end*j/200
            E = formula(*sides(r, phi, psi))
            excess = (E - Eend)/Eend
            worst_excess = max(worst_excess, excess)
            count += 1
            if r == 2.0:
                r2_dev = max(r2_dev, abs(E - 2.0))
# strict gap for r>2 away from the endpoint, in 600-digit arithmetic (the true gap is about (2cos(phi))^r/4 on the two-point branch and can be
# far below double precision when r is large and phi is close to pi/2)
mp.mp.dps = 600
for r in [mp.mpf('2.1'), mp.mpf('2.5'), 3, 6, 20, 50, 200]:
    for kk in range(1, 240, 8):
        phi = mp.pi/2 + (mp.pi/6)*kk/240
        end = 2*mp.pi - 3*phi
        Eend = formula(*sides_mp(r, phi, end))
        for j in range(0, 181, 10):
            gap = (Eend - formula(*sides_mp(r, phi, end*j/200)))/Eend
            min_gap_interior = min(min_gap_interior, gap)
if not min_gap_interior > 0:
    raise SystemExit('B strictness failed')
if worst_excess > 1e-12:
    raise SystemExit(f'B failed: E(psi) exceeds endpoint by relative {worst_excess}')
report['B_endpoint_grid'] = {'evaluations': count, 'r_values': rs,
                             'max_relative_excess_over_endpoint': worst_excess,
                             'max_abs_deviation_from_2_when_r_eq_2': r2_dev,
                             'min_relative_gap_r_ge_2.1_psi_le_0.9_endpoint_600_digits': mp.nstr(min_gap_interior, 6)}
print('B PASS', count, worst_excess, r2_dev, mp.nstr(min_gap_interior, 6))

# ---- C ---------------------------------------------------------------------
worstC = -math.inf
nC = 0
for _ in range(60):
    r = rng.uniform(2, 40)
    phi = rng.uniform(math.pi/2 + 1e-3, 2*math.pi/3 - 1e-3)
    end = 2*math.pi - 3*phi
    Eend = brute_max(*sides(r, phi, end))
    for psi in [0.0, end*rng.random(), end*rng.random(), end*0.99]:
        worstC = max(worstC, (brute_max(*sides(r, phi, psi)) - Eend)/Eend)
        nC += 1
if worstC > 1e-9:
    raise SystemExit(f'C failed: {worstC}')
report['C_endpoint_bruteforce_only'] = {'comparisons': nC, 'max_relative_excess': worstC}
print('C PASS', nC, worstC)

# ---- D (experiment for Corollary 4.3) ---------------------------------------
D_rows = []
for N in range(3, 32, 2):
    for r in [2.5, 3.0, 6.0, 15.0]:
        pts = [(math.cos(2*math.pi*j/N), math.sin(2*math.pi*j/N)) for j in range(N)]
        dist = np.array([[math.dist(p, q)**r for q in pts] for p in pts])
        theta = (N - 1)*math.pi/(2*N)
        G = 2**(r - 1)*math.sin(theta)**r/(1 - 2**(r - 2)*math.cos(theta)**r)
        best_triple = 0.0
        for i in range(N):
            for j in range(i + 1, N):
                for k in range(j + 1, N):
                    s3 = sorted([dist[i, j], dist[i, k], dist[j, k]])
                    best_triple = max(best_triple, formula(s3[0], s3[1], s3[2]))
        best_measure = 0.0
        for start in range(12):
            x = np.array([rng.random() + 1e-3 for _ in range(N)])
            x /= x.sum()
            for _ in range(4000):
                y = dist @ x
                val = x @ y
                x = x*y/val
            best_measure = max(best_measure, float(x @ dist @ x))
        D_rows.append({'N': N, 'r': r, 'conjectured_value': G, 'max_over_triples': best_triple,
                       'replicator_best_over_measures': best_measure})
        if abs(best_triple - G)/G > 1e-12 or best_measure > G*(1 + 1e-9):
            raise SystemExit(f'D failed N={N} r={r}: G={G} triple={best_triple} meas={best_measure}')
report['D_odd_polygon_experiment'] = {'rows': len(D_rows),
                                      'max_rel_triple_minus_G': max(abs(t['max_over_triples'] - t['conjectured_value'])/t['conjectured_value'] for t in D_rows),
                                      'max_rel_measure_excess': max((t['replicator_best_over_measures'] - t['conjectured_value'])/t['conjectured_value'] for t in D_rows),
                                      'details': D_rows}
print('D PASS', len(D_rows))

# ---- E (Proposition 5.1: reversed regime 0<r<2, endpoint is a minimizer) --------
worstE = -math.inf
nE = 0
for r in [0.1, 0.5, 1.0, 1.5, 1.9, 1.999]:
    for kk in range(1, 240, 4):
        phi = math.pi/2 + (math.pi/6)*kk/240
        end = 2*math.pi - 3*phi
        a, b, c = sides(r, phi, end)
        Eend = brute_max(a, b, c) if kk % 40 == 1 else formula(a, b, c)
        for j in range(0, 201, 20):
            a, b, c = sides(r, phi, end*j/200)
            if not a + b > c:
                raise SystemExit('E failed: two-point branch occurred for r<2')
            worstE = max(worstE, (Eend - formula(a, b, c))/Eend)
            nE += 1
if worstE > 1e-12:
    raise SystemExit(f'E failed: {worstE}')
report['E_reversed_regime_r_lt_2'] = {'comparisons': nE, 'max_relative_excess_of_endpoint': worstE}
print('E PASS', nE, worstE)

report['status'] = 'PASS'
report['note'] = 'Floating-point regression checks only; the proof in the paper is analytic.'
out = ROOT/'certificates'/'numeric_regression_report.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('ALL NUMERIC REGRESSION CHECKS PASSED')
