from num import *
from misc import *
from sym import *
from data import *
from main import the
def test_nums():
    val = Num()
    lst = [1,1,1,1,2,2,3]
    for a in lst:
        val.add(a)
    return 11/7 == val.mid() and 0.787 == rnd(val.div())
    
def test_syms():
    value = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    sym1 = Sym()
    for x in value:
        sym1.add(x)
    return "a"==sym1.mid() and 1.379 == rnd(sym1.div())

def test_the():
    print("results of THE function:")
    print(str(the))
    return True

def test_csv():
    csv_path = "../etc/data/auto93.csv"
    data = Data(csv_path)
    return data.count == 8*399

def test_data():
    csv_path = "../etc/data/auto93.csv"
    data = Data(csv_path)
    return  len(data.rows) == 398 and \
            data.cols.y[0].w == -1 and \
            data.cols.x[1].at == 1 and \
            len(data.cols.x) == 4
    
def test_clone():
    csv_path = "../etc/data/auto93.csv"
    data1 = Data(csv_path)
    data2 = data1.clone(data1.rows)
    return  len(data1.rows) == len(data2.rows) and \
            data1.cols.y[1].w == data2.cols.y[1].w and \
            data1.cols.x[1].at == data2.cols.x[1].at and \
            len(data1.cols.x) == len(data2.cols.x)

def test_around():
    csv_path = "../etc/data/auto93.csv"
    data = Data(csv_path)

    for n, t in enumerate(data.around(data.rows[1])):
        if n % 50 == 0:
            print(n, rnd(t["dist"], 2), (t["row"]))
    return True

def test_half():
    csv_path = "../etc/data/auto93.csv"
    data = Data(csv_path)

    left, right, A, B, mid, c = data.half()
    print(len(left), len(right), len(data.rows))
    print(o(A), c)
    print(o(mid))
    print(o(B))
    return True

def test_cluster():
    csv_path = "../etc/data/auto93.csv"
    data = Data(csv_path)
    print("\nThe Results of CLUSTER function are as follows:")
    show(data.cluster(), "mid", data.cols.y, 1)
    return True

def test_optimize():
    csv_path = "../etc/data/auto93.csv"
    data = Data(csv_path)
    print("\nThe Results of SWAY function are as follows:")
    show(data.sway(), "mid", data.cols.y, 1)
    return True