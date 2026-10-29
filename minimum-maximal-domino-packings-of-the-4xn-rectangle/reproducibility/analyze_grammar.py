from transfer import *
import json
from collections import defaultdict, deque
p=json.load(open('potential.json'))['potential']
p=[x+4 for x in p]
zero=defaultdict(list)
for i,j,c in EDGES:
    d=3*c-4+p[i]-p[j]
    assert d>=0
    if d==0: zero[i].append(j)
def closure(start,adj):
    seen=set(start); todo=list(start)
    while todo:
        i=todo.pop()
        for j in adj[i]:
            if j not in seen: seen.add(j); todo.append(j)
    return seen
rz=defaultdict(list)
for i in zero:
    for j in zero[i]:rz[j].append(i)
reach=closure([START],zero)
coreach=closure([INDEX[0,9]],rz)
print('zero bridge to bad terminal',[(i,STATES[i]) for i in sorted(reach&coreach)])
print('zero edges bridge',[(STATES[i],STATES[j]) for i in reach&coreach for j in zero[i] if j in reach&coreach])
# Layered graph with defect budget at most three.
verts=[(i,b) for b in range(4) for i in range(len(STATES))]
adj=defaultdict(list);radj=defaultdict(list)
for i,b in verts:
    for j,c in OUT[i]:
        d=3*c-4+p[i]-p[j]
        if b+d<=3:
            adj[i,b].append((j,b+d));radj[j,b+d].append((i,b))
accept={(i,b) for i in TERMINAL for b in range(4) if 0<=b+p[i]<=2}
active=closure([(START,0)],adj)&closure(accept,radj)
print('active',len(active),'edges',sum(j in active for i in active for j in adj[i]))
# SCCs by mutual reachability, sufficient for this small graph.
left=set(range(len(STATES)));scc=[]
while left:
    i=min(left); comp=closure([i],zero)&closure([i],rz)
    left-=comp
    if len(comp)>1 or i in zero[i]: scc.append(comp)
print('nontrivial zero SCCs')
for comp in scc:
    print([(i,STATES[i]) for i in sorted(comp)])
    print('arcs',[(STATES[i],STATES[j]) for i in sorted(comp) for j in zero[i] if j in comp])

vertices=sorted(active,key=lambda x:(x[1],x[0]));idx={v:i for i,v in enumerate(vertices)}
edges=[(idx[i],idx[j]) for i in vertices for j in adj[i] if j in active]
acc=[idx[x] for x in vertices if x in accept]
cur=[0]*len(vertices);cur[idx[START,0]]=1
seq=[]; vectors=[]
for n in range(len(vertices)+40):
    vectors.append(cur);seq.append(sum(cur[j] for j in acc))
    nxt=[0]*len(vertices)
    for i,j in edges:nxt[j]+=cur[i]
    cur=nxt
print('seq',seq[:25])
q=[1,0,0,-3,0,0,3,0,0,-1]
num=[sum(q[k]*seq[n-k] for k in range(min(n,9)+1)) for n in range(len(seq))]
print('numerator',[(i,x) for i,x in enumerate(num) if x])
# Find row-vector annihilation for eventual denominator.
for n in range(9,len(vectors)):
    comb=[sum(q[k]*vectors[n-k][j] for k in range(10)) for j in range(len(vertices))]
    if not any(comb):print('vector annihilation at',n);break
else: print('no row vector annihilation')
json.dump(dict(potential=p,vertices=vertices,edges=edges,accept=acc,start=idx[START,0],sequence=seq,numerator=num[:max(i for i,x in enumerate(num) if x)+1]),open('grammar_data.json','w'),indent=2)
