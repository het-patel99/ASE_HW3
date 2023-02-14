import math
import re
from main import the

def show(node, what, cols, nPlaces, lvl=None):
    if node:
        lvl = lvl or 0
        print("| " * lvl, str(len(node["data"].rows)), " ")
        if not node.get("left", None) or lvl == 0:
            print(o(node["data"].stats("mid", node["data"].cols.y, nPlaces)))
        else:
            print("")
        show(node.get("left", None), what, cols, nPlaces, lvl+1)
        show(node.get("right", None), what, cols, nPlaces, lvl+1)

# Numeric Functions

def rint(lo, hi):
    return int(math.floor(0.5 + rand(lo, hi)))

def any(t):
    return t[rint(len(t))]

def many(t,n):
    u = {}
    for i in range(1,n):
        u[1+len(u)] = any(t)
    return u

def rand(lo, hi):
    lo, hi = lo or 0, hi or 1
    Seed = (16807 * the["seed"]) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

def cosine(a, b, c):
    x1 = (a**2 + c**2 - b**2) / (2*c)
    x2 = max(0, min(1, x1))
    y  = (a**2 - x2**2)**.5
    return x2, y


def sort(t):
    #Doubt
    return t

# function sort(t, fun) --> t; return `t`,  sorted by `fun` (default= `<`)
#   table.sort(t,fun); return t end

def lt(x):
    def fun(a, b):
        return a[x] < b[x]

def keys(t):
    #Doubt
    pass

def push(t, x):
    t.append(x)

def any(t):
    return t[rint(0, len(t) - 1)]

def many(t, n):
    u = []
    for i in range(n):
        u.append(any(t))
    return u

# String Functions

def coerce(s): #Doubt
    if s == "true":
        return True
    elif s == "false":
        return False
    elif re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$", s) is not None:
        return float(s)
    else:
        return s

def rnd(n, nPlaces=3):
    mult = 10**(nPlaces or 3)
    return math.floor(n * mult + 0.5) / mult 


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

def oo(t):
    print(o(t))
    return t

def o(t, isKeys=None):
    return str(t)
# Main

def settings(s, t):
    return dict(re.findall(r"\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s))