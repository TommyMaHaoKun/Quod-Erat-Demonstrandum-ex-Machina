import sympy as s
from pathlib import Path
n,k,t=s.symbols('n k t'); L=3*n+2+2*k; A=n+k+1; C=2*n+k+2
r=s.symbols('r'); ps=s.symbols('p0:6'); P=sum(ps[j]*k**j for j in range(6)); D=(L+1-t)*(L+2-t)*(L+3-t)*C**2*(C+1)**2
expr=s.Poly(s.expand(P.subs(k,k+1)*(L+t)*(L+t+1)*A**2-P*(L+2-t)*(L+3-t)*(C+1)**2-(L+3)*(L+t)*(L+t+1)*(L+t+2)*A**2+r*L*D),k)
print('degree',expr.degree(),flush=True)
sol=s.solve(expr.all_coeffs(),list(ps)+[r]); print('solved',flush=True)
res={str(z):str(s.factor(v)) for z,v in sol.items()}
Path('certificates/wz_independent_telescoper.txt').write_text(str(res))
print(res)
