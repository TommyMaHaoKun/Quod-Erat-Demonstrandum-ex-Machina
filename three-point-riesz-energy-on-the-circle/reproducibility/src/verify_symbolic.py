"""Exact symbolic verification of every algebraic/trigonometric identity used in the proof.

Requires SymPy.  Each check is an exact simplification to zero (no floating point).
Writes certificates/symbolic_verification_report.json relative to this script.
"""
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
checks = []


def record(name, expr, statement):
    value = sp.simplify(expr)
    ok = value == 0
    checks.append({'name': name, 'statement': statement, 'passed': bool(ok)})
    if not ok:
        raise SystemExit(f'FAILED: {name}: residual {value}')
    print('PASS', name)


# ---------------------------------------------------------------------------
# Lemma 2.1 (quadratic maximization on the simplex).
# a=|AB|^r, b=|AC|^r, c=|BC|^r; weights u at A, v at B, w at C.
a, b, c, e = sp.symbols('a b c e', positive=True)
M = sp.Matrix([[0, a, b], [a, 0, c], [b, c, 0]])
D = 2*a*b + 2*b*c + 2*c*a - a**2 - b**2 - c**2
record('D_alt_form', D - (4*a*b - (a + b - c)**2), 'D = 4ab-(a+b-c)^2')
record('det_M', M.det() - 2*a*b*c, 'det M = 2abc')
lam = 2*a*b*c/D
x = sp.Matrix([c*(a + b - c), b*(a + c - b), a*(b + c - a)])/D
for i in range(3):
    record(f'critical_eq_{i}', (M*x)[i] - lam, 'M x = lambda 1 at the claimed critical point')
record('critical_sum', sum(x) - 1, 'claimed critical weights sum to 1')
record('critical_value', (x.T*M*x)[0] - lam, 'Q(x) = lambda = 2abc/D')
record('inv_sum', (sp.ones(1, 3)*M.inv()*sp.ones(3, 1))[0] - D/(2*a*b*c),
       '1^T M^{-1} 1 = D/(2abc), so the critical point is unique when D != 0')
u, v = sp.symbols('u v', nonnegative=True)
Q_edge = 2*u*(1 - u)*a
record('edge_value', Q_edge.subs(u, sp.Rational(1, 2)) - a/2, 'edge maximum a/2 at u=v=1/2')
record('F_minus_half_c', lam - c/2 - c*(a + b - c)**2/(2*D),
       'F - c/2 = c(a+b-c)^2/(2D)')

# ---------------------------------------------------------------------------
# Endpoint comparison identity (Proposition 3.2): b_end = c, a_end = e.
F_end = 2*c**2/(4*c - e)
record('endpoint_value', lam.subs(b, c).subs(a, e) - F_end, 'F at (e,c,c) equals 2c^2/(4c-e)')
xe = x.subs(b, c).subs(a, e)
record('endpoint_weight_A', xe[0] - c/(4*c - e), 'endpoint weight at A = c/(4c-e)')
record('endpoint_weight_B', xe[1] - c/(4*c - e), 'endpoint weight at B = c/(4c-e)')
record('endpoint_weight_C', xe[2] - (2*c - e)/(4*c - e), 'endpoint weight at C = (2c-e)/(4c-e)')
record('comparison_identity', (F_end - lam) - 2*c*(e*a*b - c*(a + b - c)**2)/((4*c - e)*D),
       'F_end - F = 2c[e ab - c(a+b-c)^2]/((4c-e)D)')

# ---------------------------------------------------------------------------
# Trigonometric layer (Lemma 3.1).  p,q,s,k are the squared half-chords.
phi, psi = sp.symbols('phi psi', real=True)
p = sp.sin((phi - psi)/2)**2
q = sp.sin((phi + psi)/2)**2
s = sp.sin(phi)**2
k = sp.cos(phi)*(sp.cos(phi) - sp.cos(psi))


def trig_zero(expr):
    return sp.simplify(sp.expand_trig(sp.expand(sp.expand_trig(expr).rewrite(sp.exp))))


for name, expr, st in [
    ('k_identity', p + q - s - k, 'p+q-s = cos(phi)(cos(phi)-cos(psi))'),
    ('k_product_form', k + 2*sp.cos(phi)*sp.sin((phi - psi)/2)*sp.sin((phi + psi)/2),
     'k = -2 cos(phi) sin((phi-psi)/2) sin((phi+psi)/2)'),
    ('k_square', k**2 - 4*sp.cos(phi)**2*p*q, 'k^2 = 4 cos(phi)^2 p q'),
    ('endpoint_chord', sp.sin((phi - (2*sp.pi - 3*phi))/2)**2 - 4*s*sp.cos(phi)**2,
     '|A_end-B|^2/4 = sin^2(2phi) = 4 s cos(phi)^2'),
    ('endpoint_AC', sp.sin((phi + (2*sp.pi - 3*phi))/2)**2 - s, '|A_end-C| = |B-C|'),
    ('chord_AB', (sp.cos(psi) - sp.cos(phi))**2 + (sp.sin(psi) - sp.sin(phi))**2 - 4*p,
     '|A-B|^2 = 4 sin^2((phi-psi)/2)'),
    ('chord_AC', (sp.cos(psi) - sp.cos(phi))**2 + (sp.sin(psi) + sp.sin(phi))**2 - 4*q,
     '|A-C|^2 = 4 sin^2((phi+psi)/2)'),
    ('chord_BC', (2*sp.sin(phi))**2 - 4*s, '|B-C|^2 = 4 sin^2(phi)'),
]:
    value = trig_zero(expr)
    ok = value == 0
    checks.append({'name': name, 'statement': st, 'passed': bool(ok)})
    if not ok:
        raise SystemExit(f'FAILED: {name}: residual {value}')
    print('PASS', name)

# ---------------------------------------------------------------------------
# Majorization step (Lemma 3.3): if p+q=k+s and k<s, then with lam=(s-p)/(s-k),
# p = lam k + (1-lam) s and q = (1-lam) k + lam s.
P, Qv, S, K = sp.symbols('P Q S K', positive=True)
L = (S - P)/(S - K)
record('major_p', (L*K + (1 - L)*S - P), 'p = lam k + (1-lam) s')
record('major_q', ((1 - L)*K + L*S - Qv).subs(Qv, K + S - P), 'q = (1-lam) k + lam s when p+q=k+s')

# ---------------------------------------------------------------------------
# Corollary 4.2: isosceles energy formula G(gamma) = 2^(r-1) sin^r g / (1-2^(r-2) cos^r g)
# With sin(2g)=2 sin(g) cos(g): c=(2 sg)^r = 2^r sg^r and e=(4 sg cg)^r = 4^r sg^r cg^r,
# for positive sg=sin(g), cg=cos(g) (0<g<pi/2).
r, sg, cg = sp.symbols('r s_g c_g', positive=True)
cc = 2**r*sg**r
ee = 4**r*sg**r*cg**r
G = 2**(r - 1)*sg**r/(1 - 2**(r - 2)*cg**r)
expr = sp.powsimp(sp.expand_power_base(2*cc**2/(4*cc - ee) - G, force=True), force=True)
record('isosceles_formula', sp.simplify(sp.together(sp.powsimp(expr.rewrite(sp.exp), force=True))),
       'F_end in angle form equals Fan formula 2^(r-1) sin^r g/(1-2^(r-2) cos^r g)')

report = {'status': 'PASS', 'tool': f'SymPy {sp.__version__}', 'checks': checks,
          'count': len(checks)}
out = ROOT/'certificates'/'symbolic_verification_report.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f'ALL {len(checks)} SYMBOLIC CHECKS PASSED')
