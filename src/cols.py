
from num import Num
from sym import Sym
import row
from collections import OrderedDict
import re
from enum import Enum

class Cols:

    def __init__(self, t):
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = []
        for n, s in enumerate(t):
            col = Num(n, s) if re.search("^[A-Z]+", s) != None else Sym(n, s)
            self.all.append(col)
            if not re.match(".*X$", s):
                if re.match("!$",s):
                    self.klass = col
                if(re.match("[!+-]$", s)):
                    self.y.append(col)
                else:
                    self.x.append(col)
                
    def add(self, row):
        last = [self.x,self.y]
        for _,t in enumerate(last):
            for _,col in enumerate(t):
                col.add(row.cells[col.at])


