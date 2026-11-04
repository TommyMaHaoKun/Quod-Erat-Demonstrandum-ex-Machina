"""Dependency-free exact skein evaluation using a port-pairing diagram model.

Each encounter has an incoming port and an outgoing port.  Diagram arcs join
successive encounters.  Removing a crossing inserts one of the two smoothings
as a pairing of its four ports.  Cycle tracing then reconstructs the components
and records orientation reversals.  This implementation does not import the
Gauss smoothing or polynomial routines of the discovery engine.
"""
from functools import lru_cache


def add(*polys):
    result = {}
    for poly in polys:
        for term, c in poly.items():
            result[term] = result.get(term, 0)+c
    return {term: c for term, c in result.items() if c}


def shift(poly, a=0, z=0, c=1):
    return {(i+a, j+z): c*v for (i, j), v in poly.items() if c*v}


def multiply(left, right):
    result = {}
    for (i, j), c in left.items():
        for (k, l), d in right.items():
            t = (i+k, j+l)
            result[t] = result.get(t, 0)+c*d
    return {t: c for t, c in result.items() if c}


def canonical(components):
    labels = {}
    return tuple(tuple((labels.setdefault(abs(g), len(labels)+1)*(1 if g>0 else -1), h)
                       for g,h in component) for component in components)


def braid(strands, word):
    positions = list(range(strands))
    encounters = [[] for _ in range(strands)]
    for crossing, g in enumerate(word, 1):
        if not 1 <= abs(g) < strands:
            raise ValueError('invalid braid generator')
        i, sign = abs(g)-1, 1 if g>0 else -1
        left, right = positions[i:i+2]
        encounters[left].append((sign*crossing, sign))
        encounters[right].append((-sign*crossing, sign))
        positions[i:i+2] = [right, left]
    terminal = {label: i for i,label in enumerate(positions)}
    components, unused = [], set(range(strands))
    while unused:
        i = min(unused)
        component = []
        while i in unused:
            unused.remove(i)
            component.extend(encounters[i])
            i = terminal[i]
        components.append(component)
    return canonical(components)


def switched(diagram, crossing):
    return canonical([[(-g,-h) if abs(g)==crossing else (g,h) for g,h in comp]
                      for comp in diagram])


def smooth(diagram, crossing, oriented):
    records = []
    arcs = []
    empty = 0
    for component in diagram:
        if not component:
            empty += 1
            continue
        start = len(records)
        records.extend(component)
        for j in range(len(component)):
            arcs.append((2*(start+j)+1, 2*(start+(j+1)%len(component)), None))
    target = [i for i,(g,h) in enumerate(records) if abs(g)==crossing]
    if len(target) != 2:
        raise ValueError('crossing must have two encounters')
    x,y = target
    edges = arcs + [(2*i,2*i+1,i) for i in range(len(records)) if i not in target]
    if oriented:
        edges += [(2*x,2*y+1,None),(2*y,2*x+1,None)]
    else:
        edges += [(2*x,2*y,None),(2*x+1,2*y+1,None)]
    adjacency = [[] for _ in range(2*len(records))]
    for e,(u,v,marker) in enumerate(edges):
        adjacency[u].append(e)
        adjacency[v].append(e)
    if any(len(items)!=2 for items in adjacency):
        raise ValueError('port graph is not 2-regular')
    unused = set(range(len(edges)))
    traced = []
    directions = {}
    while unused:
        e = min(unused)
        current = edges[e][0]
        component = []
        while e in unused:
            unused.remove(e)
            u,v,marker = edges[e]
            following = v if current==u else u
            if marker is not None:
                direction = 1 if current==2*marker else -1
                component.append(marker)
                directions[marker] = direction
            current = following
            options = adjacency[current]
            e = options[0] if options[1]==e else options[1]
        traced.append(component)
    reversal = {}
    for i,direction in directions.items():
        g,h = records[i]
        reversal[abs(g)] = reversal.get(abs(g),1)*direction
    components = [[(records[i][0], records[i][1]*reversal[abs(records[i][0])])
                   for i in component] for component in traced]
    components += [[] for _ in range(empty)]
    return canonical(components)


def first_bad(diagram):
    seen = set()
    for component in diagram:
        for g,h in component:
            if abs(g) not in seen:
                if g<0:
                    return -g,h
                seen.add(g)
    return None


def writhe(diagram):
    return sum(h for comp in diagram for g,h in comp)//2


@lru_cache(maxsize=None)
def homfly(diagram):
    bad = first_bad(diagram)
    if bad is None:
        result = {(0,0):1}
        delta = {(-1,-1):1,(1,-1):-1}
        for _ in range(len(diagram)-1):
            result = multiply(result,delta)
        return result
    crossing,h = bad
    changed = homfly(switched(diagram,crossing))
    resolved = homfly(smooth(diagram,crossing,True))
    return add(shift(changed,a=2*h),shift(resolved,a=h,z=1,c=h))


@lru_cache(maxsize=None)
def kauffman(diagram):
    bad = first_bad(diagram)
    if bad is None:
        result = {(writhe(diagram),0):1}
        delta = {(1,-1):1,(-1,-1):1,(0,0):-1}
        for _ in range(len(diagram)-1):
            result = multiply(result,delta)
        return result
    crossing,h = bad
    return add(shift(kauffman(smooth(diagram,crossing,True)),z=1),
               shift(kauffman(smooth(diagram,crossing,False)),z=1),
               shift(kauffman(switched(diagram,crossing)),c=-1))


def compute(strands, word):
    diagram = braid(strands,word)
    return homfly(diagram),shift(kauffman(diagram),a=-writhe(diagram))


if __name__ == '__main__':
    import json
    import time
    started = time.monotonic()
    p,f = compute(5,[-1,2,3,-4,-1,3,-4,2,2,2,3,2])
    print(json.dumps({'homfly':[[i,j,c] for (i,j),c in sorted(p.items())],
                      'kauffman':[[i,j,c] for (i,j),c in sorted(f.items())],
                      'seconds':time.monotonic()-started,
                      'homfly_nodes':homfly.cache_info().currsize,
                      'kauffman_nodes':kauffman.cache_info().currsize}))
