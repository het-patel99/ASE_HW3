import misc
import cols
import row
import math, csv
from typing import List

# reading the CSV file
def csv_content(src):
    res = []
    with open(src, mode='r') as file:
        csvFile = csv.reader(file)
        for row in csvFile:
            res.append(row)
    return res

class Data:

    def __init__(self, src):
        self.rows = []
        self.cols = None
        self.count = 0

        if type(src) == str:
            csv_list = csv_content(src)
            for line,row in enumerate(csv_list):
                row_cont = []
                for oth_line,val in enumerate(row):
                    row_cont.append(val.strip())
                    self.count+=1
                self.add(row_cont)

        else:
            self.add(src)


    def add(self, t):
        if (self.cols):
            
            nrow = row.Rows(t)
            self.rows.append(nrow.cells)
            self.cols.add(nrow)
        else:
            self.cols = cols.Cols(t)

    def stats(self,what,cols,nPlaces):
        def fun(k,col):
            f = getattr(col,what)
            return col.rnd(f(),nPlaces), col.txt
        
        return misc.kap(cols,fun)

    def clone(self,init= []):
        data = Data(self.cols.names)
        for val in init:
            data.add(val)
        return data

    def better(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.y
        for _,col in enumerate(ys):
            x = col.norm(row1[col.at])
            y = col.norm(row2[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        
        return s1/len(ys) < s2/len(ys)


    def dist(self, row1, row2, cols=None):
        n, d = 0, 0
        for _, col in enumerate(cols or self.cols.x):
            n = n + 1
            val = col.dist(row1[col.at], row2[col.at])
            d = d + val ** 2
        return (d / n) ** (1 / 2)
    
    def around(self, row1, rows = None , cols= None):
        if not rows:
            rows = self.rows
        def fun(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}
        u = map(fun,rows)
        return sorted(u,key = lambda x: x['dist'])


    def half(self, rows=None, cols=None, above=None):
        def dist1(row1, row2):
            return self.dist(row1, row2, cols)

        def project(row):
            dic = {
                "row": row,
                "dist": misc.cosine(dist1(row, A), dist1(row, B), c),
            }
            return dic
            
        if not rows:
            rows = self.rows

        some = misc.many(rows, 512)
        A = above or misc.any(some)
        B = self.around(A, some)[int(0.95 * len(rows))]["row"]
        c = dist1(A, B)
        left, right = [], []
        mid = None
        res = [project(row) for row in rows]
        sorted(res,key=lambda x: x["dist"])
        for n, tmp in enumerate(res):
            if n <= len(rows) / 2:
                left.append(tmp["row"])
                mid = tmp["row"]
            else:
                right.append(tmp["row"])

        return left, right, A, B, mid, c



    def cluster(self, rows=None, min_size=None, cols=None, above=None):
        rows = rows or self.rows
        min_val = min_size or (len(rows)) ** 0.5
        if not cols:
            cols = self.cols.x
        node = {"data": self.clone(rows)}
        if len(rows) > 2 * min_val:
            left, right, node["A"], node["B"], node["mid"], temp = self.half(rows, cols, above)
            node["left"] = self.cluster(left, min_val, cols, node["A"])
            node["right"] = self.cluster(right, min_val, cols, node["B"])
        
        return node



    def sway(self, rows=None, min=None, cols=None, above=None):
        rows = rows or self.rows
        min = min or len(rows) ** 0.5
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}

        if len(rows) > 2 * min:
            left, right, node["A"], node["B"], node["min"], _ = self.half(rows, cols, above)
            if self.better(node["B"], node["A"]):
                left, right, node["A"], node["B"] = right, left, node["B"], node["A"]
            node["left"] = self.sway(left, min, cols, node["A"])

        return node