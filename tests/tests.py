import math
import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath('../src'))

from src.num import Num
from src.sym import Sym
from src.data import *
from src.misc import *
from src.main import get_file

def round_to(n, nPlaces = 3):
    mult = math.pow(10, nPlaces)
    return math.floor(n*mult + 0.5) / mult

def print_res(function_name: str, res: bool):
    print("\n" + function_name + (": PASS" if res else ": FAIL"))

def test_data():
    data = Data(main.get_file())
    return  len(data.rows) == 398 and \
            data.cols.y[1].w == -1 and \
            data.cols.x[1].at == 1 and \
            len(data.cols.x) == 4

def test_syms():
    sym = Sym()
    values = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    for value in values:
        sym.add(value)

    res = ('a' == sym.mid()) and (1.379 == round_to(sym.div(), 3))
    print_res("test_syms", res)
    return res

def test_nums():
    num = Num()
    values = [1, 1, 1, 1, 2, 2, 3]
    for value in values:
        num.add(value)
    
    res = ((11/ 7) == num.mid()) and (0.787 == round_to(num.div(), 3))
    print_res("test_nums", res)
    return res


def test_the():
    test_data = Data(main.get_file())
    excepted_output = '\ny\tmid\t{ :Lbs- 2970.42 :Acc+ 15.57 :Mpg+ 23.84}\n \tdiv\t{ :Lbs- 846.84 :Acc+ 2.76 :Mpg+ 8.34}\nx\tmid\t{ :Clndrs 5.45 :Volume 193.43 :Model 76.01 :origin 1}\n \tdiv\t{ :Clndrs 1.7 :Volume 104.27 :Model 3.7 :origin 1.3273558482394003}'
    y_mid_report = '{'
    y_div_report = '{'
    for y in test_data.cols.y:
        y_mid_report = y_mid_report + ' :' + y.txt + ' ' + str(y.rnd(y.mid(), 2))
        y_div_report = y_div_report + ' :' + y.txt + ' ' + str(y.rnd(y.div(), 2))
    y_mid_report = y_mid_report + '}'
    y_div_report = y_div_report + '}'

    x_mid_report = '{'
    x_div_report = '{'
    for x in test_data.cols.x:
        x_mid_report = x_mid_report + ' :' + x.txt + ' ' + str(x.rnd(x.mid(), 2))
        x_div_report = x_div_report + ' :' + x.txt + ' ' + str(x.rnd(x.div(), 2))
    x_mid_report = x_mid_report + '}'
    x_div_report = x_div_report + '}'

    res_string = '\ny\tmid\t' + y_mid_report + '\n \tdiv\t' + y_div_report + '\nx\tmid\t' + x_mid_report + '\n \tdiv\t' + x_div_report
    res = res_string == excepted_output
    print_res("\ntest_data", res)
    print(res_string)
    return True

def test_clone():
    data1= Data(main.get_file())
    data2= data1.clone(data1.rows)
    return len(data1.rows) == len(data2.rows) and \
            data1.cols.y[1].w == data2.cols.y[1].w and \
            data1.cols.x[1].at == data2.cols.x[1].at and \
            len(data1.cols.x) == len(data2.cols.x)
    
def test_around():
    data= Data(main.get_file())
    for n,t in enumerate(data.around(data.rows[1])):
        if n % 50 == 0:
            print(n,misc.rnd(t["dist"],2), (t["row"]))
    return True

def test_half():
    data = Data(main.get_file())
    left,right,A,B,mid,c = data.half() 
    print(len(left), len(right), len(data.rows))
    print(misc.o(A.cells()),c)
    print(misc.o(B.cells()))
    print(misc.o(mid.cells())) 
    return True

def test_cluster():
    data = Data(get_file())
    misc.show(data.cluster(), "mid", data.cols.y,1)
    return True

def test_optimize():
    data = Data(get_file())
    misc.show(data.sway(), "mid", data.cols.y,1)
    return True