"""Numerical normalization check for research/zagier_transform.md, not a proof."""
import json
from pathlib import Path
import mpmath as mp

mp.mp.dps = 70
A = mp.sqrt(mp.pi) * mp.zeta(mp.mpf(3) / 2) / 2
K = 2 * mp.pi ** mp.mpf('1.5')
cases = []
for real, imag in [('0.05', '0'), ('0.2', '0'), ('0.2', '0.18'), ('0.5', '1')]:
    z = mp.mpc(real, imag)
    direct = -mp.fsum(mp.log(1 - mp.exp(-j*j*z)) for j in range(1, 201))
    remainder = -mp.fsum(
        mp.log(1 - mp.exp(-K * (1 + sign*1j) * mp.sqrt(m/z)))
        for m in range(1, 2001) for sign in [-1, 1])
    model = A/mp.sqrt(z) + mp.log(z)/2 - mp.log(2*mp.pi) + remainder
    b = min(mp.re(K*(1+sign*1j)/mp.sqrt(z)) for sign in [-1, 1])
    bound = 2*mp.exp(-b)/(1-mp.exp(-b))*(1+2/b+2/b**2)
    cases.append({'z': str(z), 'difference_abs': str(abs(direct-model)),
                  'remainder_abs': str(abs(remainder)), 'bound_E': str(bound)})
    assert abs(direct-model) < mp.mpf('1e-55')
    assert abs(remainder) <= bound
result = {'scope': 'Uncertified high precision sanity check only; proof is analytic.',
          'mpmath_version': mp.__version__, 'digits': mp.mp.dps, 'cases': cases}
out = Path(__file__).resolve().parents[1] / 'certificates' / 'transform_sanity.json'
out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
