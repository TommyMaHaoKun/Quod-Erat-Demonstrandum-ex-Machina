"""Certified constants for the local analytic-major-arc argument.

Requires python-flint 0.6.0 or compatible Arb bindings.  This checks numerical
inequalities, not the analytic lemmas in paper/tail_analysis.md.  All decimal
constants used for assertions are exact rational Arb inputs.
"""
import json
from pathlib import Path
from flint import arb, ctx
import flint

if not __debug__:
    raise RuntimeError('The certificate checker requires assertions; do not use -O.')

ctx.prec = 256


def q(a, b=1):
    return arb(a) / b


def constants(k):
    d = q(1, k)
    A = (1 + d).gamma() * (1 + d).zeta()
    K = (2 * arb.pi()) ** (1 + d)
    beta = q(k - 1, 2 * k) * arb.pi()
    b0 = K * beta.cos()
    a = A - K * beta.cos()
    b = K * beta.sin()
    theta = (b / a).atan() / (1 + d)
    # Exact global minimum over r >= 0 of A(1-Re(1+ir)^(-d))
    # + Re[K exp(-i beta)(1+ir)^(-d)].
    rate = A - (a*a + b*b).sqrt() * theta.cos() ** (1 + d)
    theta3 = arb(3).atan()
    radius3 = arb(10) ** (-d / 2)
    b3 = K * radius3 * (beta + d * theta3).cos()
    loss3 = A * (1 - radius3 * (d * theta3).cos())
    negative_ray_loss = A / k + A * (1 - arb(3) ** (-d) * (d * arb.pi()/2).cos())
    assert A > q(101*k,100)
    assert A < q(21*k,20)
    assert a > 0
    assert rate > q(7,5)
    assert b3 > q(3,8)
    assert b0 > 2
    assert loss3 > q(7,6)
    assert negative_ray_loss > 2
    enclosures = {
        4: ((416502,416503,100000),(59939,59941,100000),
            (179026,179029,100000),(119272,119275,100000),
            (228243,228246,100000)),
        5: ((513401,513403,100000),(46350,46353,100000),
            (158462,158465,100000),(118249,118252,100000),
            (224122,224126,100000)),
        6: ((611293,611296,100000),(37759,37762,100000),
            (140266,140270,100000),(117621,117625,100000),
            (221504,221509,100000)),
    }
    for value,(lo,hi,den) in zip((A,b3,rate,loss3,negative_ray_loss),enclosures[k]):
        assert value > q(lo,den)
        assert value < q(hi,den)
    return {key: str(value) for key, value in locals().items()
            if key in ('A','K','rate','b0','b3','loss3','negative_ray_loss')}


def main():
    data = {str(k): constants(k) for k in (4,5,6)}
    uniform = {}
    for x0, bound in ((12,61),(15,28)):
        b = q(3*x0,8)
        polynomial = arb(1)
        falling = 1
        for j in range(1,7):
            falling *= 7-j
            polynomial += falling / b**j
        E = 6 * (-b).exp() * polynomial / (1-(-b).exp())
        exponential_constant = 6 * polynomial * E.exp() / (1-(-b).exp())
        assert E < (q(11,25) if x0==12 else q(23,250))
        assert exponential_constant < bound
        uniform[str(x0)] = {'E_at_3x0_over_8':str(E),
                           'exp_remainder_constant':str(exponential_constant),
                           'rational_upper_constant':bound}
    assert q(40,39) ** 6 < 2
    data['uniform'] = uniform
    x = arb(15)
    Xu = q(21,20)*x
    J = [q(1008,5)*Xu.sqrt()*arb(3)**(j+1)/(j+1)*(-q(7,5)*x).exp()
         for j in range(3)]
    I = [2/x+1/x**2, 8/x+6/x**2+2/x**3,
         32/x+32/x**2+20/x**3+6/x**4]
    horizontal = [q(108,5)*q(16,5)**j/x.sqrt()*(-q(7,6)*x).exp()
                  +16*Xu.sqrt()*(-2*x).exp()*I[j] for j in range(3)]
    S = 1040*Xu**2*(-q(99,20)*x).exp()
    eps = [J[j]+horizontal[j]+S for j in range(3)]
    cost = Xu*(4*eps[0]+4*eps[1]+eps[2]+eps[0]*eps[2])
    assert cost < q(1,2000)
    data['central_error_assembly_at_x15'] = {
        'eps': [str(e) for e in eps], 'X_times_weighted_cost':str(cost),
        'rational_upper_bound':'1/2000',
        'includes':['transformation','horizontal rays','negative Wright terms'],
        'excludes':['intermediate arcs','far arcs']}
    data['python_flint_version'] = flint.__version__
    data['precision_bits'] = ctx.prec
    data['status'] = 'CERTIFIED_NUMERICAL_CONSTANTS_ONLY'
    out = Path(__file__).resolve().parents[1] / 'certificates' / 'tail_constants.json'
    out.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
