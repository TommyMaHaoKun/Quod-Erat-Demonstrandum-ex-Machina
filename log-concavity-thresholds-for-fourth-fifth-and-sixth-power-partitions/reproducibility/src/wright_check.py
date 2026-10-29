"""Exact rational checks for constants in the Wright-model lower bound.

This does not verify the contour comparison with the partition function.
The analytic inequalities themselves are proved in paper/wright_lower_bound.md.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math
import sys

ROOT=Path(__file__).resolve().parents[1]

def exp_bounds(x, terms=80):
    """Rational enclosure for exp(x), x>=0, by Taylor and geometric tail."""
    x=Q(x)
    if x<0 or x>=terms+2:
        raise ValueError('Need 0<=x<terms+2')
    total=term=Q(1)
    for n in range(1,terms+1):
        term*=x/n
        total+=term
    first_omitted=term*x/(terms+1)
    upper=total+first_omitted/(1-x/(terms+2))
    return total,upper

def run():
    if sys.flags.optimize or not __debug__:
        raise SystemExit('Run the verifier without -O or PYTHONOPTIMIZE.')
    checks=[]
    def require(name, condition, detail):
        if not condition:
            raise ArithmeticError(name)
        checks.append({'name':name,'result':'PASS','detail':detail})
    pi_upper=Q(22,7)
    # pi<22/7 follows from the positive integral
    # int_0^1 x^4(1-x)^4/(1+x^2) dx = 22/7-pi.
    for k in (4,5,6):
        c2=Q(k+1,2*k*k)/pi_upper
        require('normalization_k%d'%k,c2>Q(7,40)**2,
                '(k+1)/(2*(22/7)*k^2) > (7/40)^2')
        exponent=Q(k+1,20)+Q(k+1,120*k)
        require('Stirling_exponent_k%d'%k,exponent<=Q(259,720),
                str(exponent)+' <= 259/720')
        require('positive_normalization_k%d'%k,Q(k,2*(k+1))/pi_upper>Q(1,4)**2,
                'k/(2*(22/7)*(k+1)) > 1/16')
    require('floor_ratio',Q(1)-Q(2,10)>Q(8,9)**2,
            '1-2/10 > (8/9)^2')
    _,upper=exp_bounds(Q(259,720))
    require('exponential_lower',upper<Q(100,69),
            'Taylor upper bound for exp(259/720) < 100/69')
    product=Q(7,40)*Q(8,9)*Q(69,100)
    require('single_term_product',product>Q(1,10),str(product)+' > 1/10')
    # At X=10 the required exponential inequality is exp(50)>5,200,000.
    # A single positive term of its Taylor series is already larger.
    term=Q(50**10,math.factorial(10))
    require('negative_terms_small',term>5200000,
            '50^10/10! > 5,200,000, hence 520*10^2*exp(-50)<1/100')
    require('final_model_bound',Q(99,1000)>Q(1,12),'99/1000 > 1/12')
    for k in (4,5,6):
        c2=Q(k+1,2*k*k)/pi_upper
        require('block_normalization_k%d'%k,(Q(k)-Q(1,3))**2*c2>Q(4,5)**2,
                '(k-1/3)^2*(k+1)/(2*(22/7)*k^2) > 16/25')
        require('block_Stirling_k%d'%k,Q(k+1,100*k)<=Q(1,80),
                '(k+1)/(100*k) <= 1/80')
    require('block_sqrt_factor',Q(5,6)-Q(1,10)>Q(5,6)**2,
            '5/6-1/10 > (5/6)^2, so L-1 > 25*X/36')
    require('block_exponent',Q(21,20)+Q(1,80)==Q(17,16),
            '21/20+1/80=17/16')
    _,block_exp_upper=exp_bounds(Q(17,16))
    require('block_exp_bound',block_exp_upper<3,
            'rational Taylor upper bound for exp(17/16) < 3')
    require('block_sum',Q(4,5)*Q(5,18)==Q(2,9),'(4/5)*(5/18)=2/9')
    require('block_final_bound',Q(99,100)*Q(2,9)>Q(1,5),'(99/100)*(2/9)>1/5')
    # Stronger Hplus/M>1/2 for X>=15. All constants below are rational.
    # Machin's identity follows by tangent addition and angles in (0,pi/2).
    machin_lower=16*(Q(1,5)-Q(1,5)**3/3)-4*Q(1,239)
    require('pi_lower_Machin',machin_lower>Q(157,50),
            '16*(1/5-(1/5)^3/3)-4/239 > 157/50')
    require('large_block_floor',Q(1,15)<Q(4,15)**2,
            '1/15 < (4/15)^2, so 1/sqrt(X)<4/15 for X>=15')
    require('large_block_sqrt',Q(11,15)-Q(1,15)>Q(4,5)**2,
            '11/15-1/15 > (4/5)^2')
    require('mesh_step',4**2*15>15**2,'(4*sqrt(15))^2 > 15^2')
    for k in (4,5,6):
        require('large_block_Stirling_k%d'%k,Q(k+1,12*k*11)<Q(1,100),
                '(k+1)/(12*k*11) < 1/100')
        require('large_block_normalization_k%d'%k,Q(k+1,2)/pi_upper>Q(89,100)**2,
                '(k+1)/(2*(22/7)) > (89/100)^2')
    gaussian_a=Q(105,22)
    require('Gaussian_full_integral',Q(157,50)/gaussian_a>Q(81,100)**2,
            '(157/50)/(105/22) > (81/100)^2')
    gaussian_exp_lower,_=exp_bounds(gaussian_a)
    require('Gaussian_tail',gaussian_exp_lower>100/gaussian_a,
            'Taylor lower bound for exp(105/22) > 100/(105/22)')
    _,stirling_exp_upper=exp_bounds(Q(1,100))
    require('large_block_exp',stirling_exp_upper<Q(100,99),
            'Taylor upper bound for exp(1/100) < 100/99')
    half_product=Q(4,5)*Q(99,100)*Q(89,100)*Q(11,15)
    require('half_normalization',half_product==Q(64614,125000) and half_product>Q(1,2),
            '(4/5)*(99/100)*(89/100)*(11/15)=64614/125000 > 1/2')
    report={'scope':'Exact constants for the Wright-model lemma only.',
            'result':'PASS','checks':checks,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target=ROOT/'certificates'/'wright_constants.json'
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    run()
