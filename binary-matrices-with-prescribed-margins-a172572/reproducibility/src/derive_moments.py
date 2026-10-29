import sympy as s
from functools import lru_cache
n=s.symbols('n', integer=True, positive=True)
a,b,c=s.symbols('a b c')
@lru_cache(None)
def M(j,k):
 if j<0 or k<0 or k>6: return 0
 if (j+k)%2: return 0
 if j==0: return {0:5*n*a,2:a,4:b,6:c}[k]
 if k==1:
  return s.factor((j*M(j-1,0)+5*n*j*M(j-1,2)+20*n*n*M(j,3))/(j+1+4*n))
 return s.factor((k*M(j-1,k-1)-n*(6-k)*M(j-1,k+1)-(j-1)*M(j-2,k))/(k-1))
vec=s.Matrix([a,b,c])
nextvals=[]
for k in (2,4,6):
 nextvals.append(s.factor(sum(s.binomial(6-k,t)*(-n)**t*M(6-k-t,t) for t in range(7-k))))
A=s.Matrix([[s.factor(s.diff(v,z)) for z in vec] for v in nextvals])
print('A='); print(A)
print('LATEX A=',s.latex(A))
print('M11=',M(1,1));print('M13=',M(1,3));print('M31=',M(3,1));print('M22=',M(2,2))
H=lambda x: 2*(2*x+1)/(x+1)**4
T=s.simplify(H(n)*A)
row=s.Matrix([[5*n,0,0]])
rows=[row]
prod=s.eye(3)
for j in range(1,4):
 prod=T.subs(n,n+j-1)*prod
 rows.append(s.simplify(s.Matrix([[5*(n+j),0,0]])*prod))
P=5084*n**6+68634*n**5+383756*n**4+1137319*n**3+1884032*n**2+1653960*n+601185
Q=31372*n**5+313720*n**4+1227805*n**3+2354425*n**2+2220988*n+827860
coeffs=[6000*(n+1)**2*(2*n+1)*(2*n+3)*(62*n*n+341*n+470),-4*(2*n+3)*Q,-6*P,(n+3)**4*(62*n*n+217*n+191)]
print('Residual=',[s.factor(sum(coeffs[j]*rows[j][k] for j in range(4))) for k in range(3)])
print('OBS DET=',s.factor(s.Matrix.vstack(*rows[:3]).det()))
