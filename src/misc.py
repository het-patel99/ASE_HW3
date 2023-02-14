import math
from main import seed as seed

def fmt(sControl: str, *args): #control string (format string)
    for string in args:
        print(string.format(sControl))

# show function needs to be added
def show(node, what, cols, nPlaces, level = None):
    if node:
        level = level or 0
        print("| " * level, str(len(node["data"].rows)), " ")
        if not node.get("left", None) or level == 0:
            print(o(node["data"].stats("mid", node["data"].cols.y, nPlaces)))
        else:
            print("")
        show(node.get("left", None), what, cols, nPlaces, level+1)
        show(node.get("right", None), what, cols, nPlaces, level+1)

def cosine(a, b, c):
    x1 = (a**2 + c**2 - b**2) / (2*c)
    x2 = max(0, min(1, x1))
    y  = (a**2 - x2**2)**.5
    return x2, y

def rnd(n, nPlaces = 3):
    mult = math.pow(10, nPlaces)
    return math.floor(n*mult + 0.5) / mult

def o(t, isKeys=None):
    return str(t)

def oo(t):
    print(o(t))
    return t

def map(t,fun):
    u = {}
    for k,v in enumerate(t):
        v,k = fun(v)
        print(v,k)
        u[k or (1+len(u))] = v
    return u

def kap(t, fun):
    u = {}
    for k,v in enumerate(t):
        v,k = fun(k,v)
        u[k or (1+len(u))] = v
    
    return u

def rand(lo,hi):
    lo = lo or 0
    hi = hi or 1
    seed = (16807 * seed) % 2147483647
    return lo + (hi-lo) * seed / 2147483647

def rint(lo,hi):
    return math.floor(0.5 + rand(lo,hi))

def any(t):
    return t[rint(0,len(t)-1)]

def many(t,n):
    u = {}
    for i in range(1,n):
        u[1+len(u)] = any(t)
    return u
