"""Independent standard-library gamma-CDF enclosure with exact rational bounds.

All intervals have dyadic endpoints with denominator Q=2**192; integer floor
and ceiling implement outward rounding. There are no floating-point operations
in the certification path. The construction uses:

* log via 2*atanh(t)=2*sum(t**(2j+1)/(2j+1)), t=(y-1)/(y+1), 1<=y<=2.
  After N terms the remainder is in [0,2*t**(2N+1)/((2N+1)*(1-t*t))].
* exp after power-of-two reduction to |r|<=1/8, using Taylor through degree32.
  The absolute remainder is <=2*|r|**33/33!, since exp(|r|)<2.
* pi=16*atan(1/5)-4*atan(1/239), alternating arctan-series enclosures.
* logGamma(a) shifted by 32; Stirling through B_48, with error between zero
  and its first omitted term B_50/(50*49*z**49), z=a+32>32.
  This is the usual signed Stirling remainder for positive real z.
* P(k,x)=exp(k*log(x)-x-logGamma(k+1))*sum_{n>=0} x**n/(k+1)_n.
  All series terms are positive, and after term n the tail is <= next/(1-r),
  r=x/(k+n+1)<1. This uses the largest ratio among all remaining terms.

cdf_sign(k,x) returns -1 or +1 only when the complete resulting interval
is strictly below or above 1/2. It raises ArithmeticError otherwise.
Input values may be Fraction, int, or decimal strings. Python float inputs
are rejected so decimal brackets cannot silently change meaning.
"""
from fractions import Fraction
from functools import lru_cache
from math import factorial

BITS = 192
Q = 1 << BITS


def ceildiv(a, b):
    assert b > 0
    return -((-a) // b)


def rational(x):
    if isinstance(x, float):
        raise TypeError('Use an exact Fraction or decimal string, not float')
    return x if isinstance(x, Fraction) else Fraction(x)


class IV:
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        self.lo = int(lo)
        self.hi = int(lo if hi is None else hi)
        assert self.lo <= self.hi

    @staticmethod
    def exact(x):
        x = rational(x)
        n = x.numerator * Q
        return IV(n // x.denominator, ceildiv(n, x.denominator))

    def __add__(self, other):
        other = asiv(other)
        return IV(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return IV(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-asiv(other))

    def __rsub__(self, other):
        return asiv(other) + (-self)

    def __mul__(self, other):
        other = asiv(other)
        vals = (self.lo*other.lo, self.lo*other.hi,
                self.hi*other.lo, self.hi*other.hi)
        return IV(min(vals)//Q, ceildiv(max(vals), Q))

    __rmul__ = __mul__

    def inv(self):
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError('Interval contains zero')
        if self.hi < 0:
            return -(-self).inv()
        return IV(Q*Q//self.hi, ceildiv(Q*Q, self.lo))

    def __truediv__(self, other):
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError()
            if other < 0:
                return (-self)/(-other)
            return IV(self.lo//other, ceildiv(self.hi, other))
        return self * asiv(other).inv()

    def __rtruediv__(self, other):
        return asiv(other) * self.inv()

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError('Only nonnegative integer powers supported')
        result, base = IV(Q), self
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def fractions(self):
        return Fraction(self.lo, Q), Fraction(self.hi, Q)


def asiv(x):
    return x if isinstance(x, IV) else IV.exact(x)


def _log_unit(y):
    # Precondition: 1 <= y <= 2. Any rounding of y is included.
    t = (y-1)/(y+1)
    t2 = t*t
    term, total = t, IV(0)
    N = 90
    for j in range(N):
        total = total + term/(2*j+1)
        term = term*t2
    remainder = 2*term/((2*N+1)*(1-t2))
    return 2*total + IV(0, max(0, remainder.hi))


LOG2 = _log_unit(IV.exact(2))


@lru_cache(maxsize=65536)
def log_exact(x):
    x = rational(x)
    if x <= 0:
        raise ValueError('log requires positive input')
    n, d = x.numerator, x.denominator
    e = n.bit_length()-d.bit_length()
    if e >= 0:
        y = Fraction(n, d << e)
    else:
        y = Fraction(n << (-e), d)
    if y < 1:
        y *= 2
        e -= 1
    elif y >= 2:
        y /= 2
        e += 1
    assert 1 <= y < 2
    return _log_unit(IV.exact(y)) + e*LOG2


def log(x):
    if isinstance(x, IV):
        a = log_exact(Fraction(x.lo, Q))
        b = log_exact(Fraction(x.hi, Q))
        return IV(a.lo, b.hi)
    return log_exact(rational(x))


def exp(x):
    x = asiv(x)
    n = max(abs(x.lo), abs(x.hi))
    s = 0
    while n > Q//8:
        n = ceildiv(n, 2)
        s += 1
    r = x/(1 << s)
    term, total = IV(Q), IV(Q)
    for j in range(1,33):
        term = term*r/j
        total = total + term
    a = IV(max(abs(r.lo), abs(r.hi)))
    rem = 2*(a**33)/factorial(33)
    total = total + IV(-rem.hi, rem.hi)
    for _ in range(s):
        total = total*total
    return total


def _atan_inverse(q, n):
    t = IV.exact(Fraction(1,q))
    t2 = t*t
    power, total = t, IV(0)
    for j in range(n):
        term = power/(2*j+1)
        total = total + (term if j%2 == 0 else -term)
        power = power*t2
    rem = power/(2*n+1)
    return total + (IV(0,rem.hi) if n%2 == 0 else IV(-rem.hi,0))


PI = 16*_atan_inverse(5, 60)-4*_atan_inverse(239, 20)
LOG2PI = log(2*PI)


def _bernoulli(n):
    a = [Fraction(0)]*(n+1)
    out=[]
    for m in range(n+1):
        a[m]=Fraction(1,m+1)
        for j in range(m,0,-1):
            a[j-1]=j*(a[j-1]-a[j])
        out.append(a[0])
    return out


BERNOULLI = _bernoulli(50)


@lru_cache(maxsize=16384)
def loggamma(a):
    a = rational(a)
    if a <= 0:
        raise ValueError('logGamma requires positive input')
    shift=32
    z = a+shift
    zz = IV.exact(z)
    result = (zz-Fraction(1,2))*log_exact(z)-zz+LOG2PI/2
    # Form each small Stirling term as an exact Fraction before conversion.
    # Otherwise dyadic underflow in z**(-49), multiplied by large B_50,
    # would unnecessarily widen the valid enclosure.
    for n in range(1,25):
        term=BERNOULLI[2*n]/(2*n*(2*n-1)*z**(2*n-1))
        result=result+IV.exact(term)
    remainder=IV.exact(BERNOULLI[50]/(50*49*z**49))
    result=result+IV(min(0,remainder.lo),max(0,remainder.hi))
    for j in range(shift):
        result=result-log_exact(a+j)
    return result


def cdf_interval(k, x):
    k, x = rational(k), rational(x)
    if k <= 0 or x < 0:
        raise ValueError('Require k>0, x>=0')
    if x == 0:
        return IV(0)
    prefactor=exp(k*log_exact(x)-x-loggamma(k+1))
    xx=IV.exact(x)
    term=total=IV(Q)
    n=0
    while True:
        ratio=xx/IV.exact(k+n+1)
        nxt=term*ratio
        if ratio.hi < Q:
            tail=nxt/(1-ratio)
            if tail.hi < (1 << 30):
                total=total+IV(0,tail.hi)
                break
        n+=1
        term=nxt
        total=total+term
        if n>10000:
            raise ArithmeticError('CDF series convergence limit exceeded')
    return prefactor*total


def cdf_sign(k, x):
    value=cdf_interval(k,x)
    if value.hi < Q//2:
        return -1
    if value.lo > Q//2:
        return 1
    raise ArithmeticError('CDF interval contains one half')


def verify_median_bracket(k, lower, upper):
    k,lower,upper=map(rational,(k,lower,upper))
    if not 0<lower<upper:
        raise ValueError('Require 0 < lower < upper')
    if cdf_sign(k,lower) != -1 or cdf_sign(k,upper) != 1:
        raise ArithmeticError('Invalid median bracket')
    return True


def verify_certificate(directory):
    """Verify rational median brackets and a convexity/secant covering proof.

    At k in [a,b], strict convexity of the gamma median gives
      nu'(k) <= (nu(c)-nu(b))/(c-b) <= (U_c-L_b)/(c-b) = D,
    while nu(k)/k**2 >= L_a/b**2. Thus if B=D-log(2)*L_a/b**2>0,
      A'(k) <= exp(log(2)/a)*B-1.
    All comparisons below use enclosing rational intervals.
    """
    import csv,hashlib,time
    from pathlib import Path
    directory=Path(directory)
    start=time.perf_counter()
    nodes={}
    min_cdf_gap=None
    bracket_path=directory/'median_brackets.csv'
    interval_path=directory/'intervals.csv'
    with bracket_path.open(newline='',encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            k,lower,upper=map(rational,(row['k'],row['lower'],row['upper']))
            if k in nodes:
                raise ArithmeticError('Duplicate median node')
            if not 0<lower<upper:
                raise ArithmeticError('Bad bracket order')
            lo=cdf_interval(k,lower)
            hi=cdf_interval(k,upper)
            if not lo.hi<Q//2<hi.lo:
                raise ArithmeticError('Median bracket failed at '+str(k))
            gap=min(Q//2-lo.hi,hi.lo-Q//2)
            min_cdf_gap=gap if min_cdf_gap is None else min(gap,min_cdf_gap)
            nodes[k]=(lower,upper)
    previous=Fraction(1,10)
    max_product=None
    max_cell=None
    count=0
    min_B=None
    with interval_path.open(newline='',encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            a,b,c=map(rational,(row['a'],row['b'],row['c']))
            if a!=previous or not a<b<c:
                raise ArithmeticError('Interval coverage/order failed')
            if any(z not in nodes for z in (a,b,c)):
                raise ArithmeticError('Uncertified median node')
            La=nodes[a][0]
            Lb=nodes[b][0]
            Uc=nodes[c][1]
            D=(Uc-Lb)/(c-b)
            B=IV.exact(D)-LOG2*IV.exact(La/(b*b))
            if B.lo<=0:
                raise ArithmeticError('Nonpositive B enclosure')
            product=exp(LOG2/IV.exact(a))*B
            if 1000000*product.hi>=999973*Q:
                raise ArithmeticError('Derivative bound failed at '+str(a))
            if max_product is None or product.hi>max_product:
                max_product=product.hi
                max_cell=[str(a),str(b),str(c)]
            min_B=B.lo if min_B is None else min(min_B,B.lo)
            previous=b
            count+=1
    if count==0 or previous!=7:
        raise ArithmeticError('Cover does not end at 7')
    return {
        'status':'PASS',
        'arithmetic':'exact integers with outward-rounded dyadic intervals',
        'bits':BITS,
        'median_nodes':len(nodes),
        'median_bracket_endpoint_checks':2*len(nodes),
        'cover_intervals':count,
        'covered_closed_interval':['1/10','7'],
        'verified_product_threshold':'999973/1000000',
        'minimum_cdf_distance_from_half_lower_bound':str(Fraction(min_cdf_gap,Q)),
        'minimum_B_lower_bound':str(Fraction(min_B,Q)),
        'maximum_secant_product_upper_bound':str(Fraction(max_product,Q)),
        'uniform_negative_derivative_margin_lower_bound':str(Fraction(Q-max_product,Q)),
        'maximum_secant_product_approximation':float(Fraction(max_product,Q)),
        'maximum_cell':max_cell,
        'certificate_sha256':{
            p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (bracket_path,interval_path)},
        'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_seconds':round(time.perf_counter()-start,3)
    }


if __name__ == '__main__':
    import argparse,json
    from pathlib import Path
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('k',nargs='?')
    p.add_argument('x',nargs='?')
    p.add_argument('--certificate',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    if args.certificate:
        report=verify_certificate(args.certificate)
    elif args.k is None and args.x is None:
        report=verify_certificate(Path(__file__).resolve().parents[1]/'certificates')
    else:
        if args.k is None or args.x is None:
            p.error('Supply k x or --certificate DIRECTORY')
        v=cdf_interval(args.k,args.x)
        a,b=v.fractions()
        report={'k':args.k,'x':args.x,'cdf_lower':str(a),'cdf_upper':str(b),
                'sign_relative_to_half':-1 if v.hi<Q//2 else 1 if v.lo>Q//2 else 0}
    text=json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.write_text(text,encoding='utf-8')
    print(text,end='')
