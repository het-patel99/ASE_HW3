import math, csv
from typing import List
import misc
import cols
import row
from main import the

def get_csv_contents(filepath):
    csv_list = []
    with open(filepath, 'r') as file:
        csv_file = csv.reader(file)
        for i in csv_file:
            csv_list.append(i)
    return csv_list

class Data:

    ## constructor created for data.py class
    def __init__(self, src):
        self.rows = []
        self.cols =  None
        self.count = 0
        ## if the src is string then
        ## it reads the file and then calls the add method to add each row
        src_type = type(src)
        if src_type == str :
            csv_list = get_csv_contents(src)
            for row in csv_list:
                trimmed_row = []
                for item in row:
                    trimmed_row.append(item.strip())
                    self.count+=1
                self.add(trimmed_row)

        else: # else we were passed the columns as a string
            self.add(src)
        # else:
        #     raise Exception("Unsupported type in Data constructor")

    ## add method adds the row read from csv file
    ## It also checks if the col names is being read has already being read or not
    ## if yes then it uses old rows
    ## else add the col rows.
    def add(self, t: 'list[str]'):

        if(self.cols is None):
            self.cols = cols.Cols(t)
        else:
            new_row = row.Rows(t)
            self.rows.append(new_row.cells)
            self.cols.add(new_row)

    def clone(self, copyList = None):
        new_data = Data(self.cols.names)
        for row in copyList:
            new_data.add(row)
        return new_data

    def stats(self, what, cols, nPlaces):
        def fun(k,col):
            fun1 = getattr(col,what)
            return col.rnd(fun1(),nPlaces), col.txt
        
        return misc.kap(cols,fun)

    def better(self, row1, row2):
        s1,s2,ys = 0,0,self.cols.y
        for _,col in enumerate(ys):
            x = col.norm(row1[col.at])
            y = col.norm[row2[col.at]]
            s1 = s1 - math.exp(col.w * (x-y) / len(ys))
            s2 = s2 - math.exp(col.w * (y-x) / len(ys))
        return s1/len(ys) < s2/len(ys)

    def dist(self, row1, row2, cols = None):
        n, d = 0,0
        for _,col in enumerate(cols or self.cols.x):
            n = n + 1
            d = d + col.dist(row1[col.at], row2[col.at]) ** the["p"]
        return (d/n)**(1/the["p"])

    def around(self, row1, rows = None , cols= None):
        if not rows:
            rows = self.rows
        def func(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}
        u = map(func,rows)
        return sorted(u,key = lambda x: x['dist'])

    def half(self, rows = None, cols = None, above = None):
        rows = rows or self.rows
        some = misc.many(rows,the["Sample"])
        A = above or misc.any(some)
        B = self.around(A,some)[(the["Far"]*len(rows)//1)]["row"]
        C = self.dist(A,B,cols)
        left = []
        right = []
        mid = None
        def project(row):
            dic = {
                "row": row,
                "dist": misc.cosine(self.dist(row, A,cols), self.dist(row, B,cols), C)
            }
            return dic

        res = [project(i) for i in rows]
        sorted(res,key=lambda x: x["dist"])
        for n, tmp in enumerate(res):
            if n <= len(rows) / 2:
                left.append(tmp["row"])
                mid = tmp["row"]
            else:
                right.append(tmp["row"])

        return left, right, A, B, mid, C

    def cluster(self, rows = None, min = None, cols = None, above = None):
        rows = rows or self.rows
        min = min or len(rows)** the["min"]
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}
        if len(rows)>2*min:
            left, right, node["A"], node["B"], node["mid"], temp = self.half(rows,cols,above)
            node["left"] = self.cluster(left,min,cols,node["A"])
            node["right"] = self.cluster(right,min,cols,node["B"])
        return node

    def sway(self,rows = None,min = None,cols = None,above = None):
        rows = rows or self.rows
        min = min or len(rows)**the["min"]
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}
        if len(rows)>2*min:
            left, right, node["A"], node["B"], node["mid"],temp = self.half(rows,cols,above)
            if self.better(node["B"],node["A"]):
                left,right,node["A"],node["B"] = right,left,node["B"],node["A"]
            else:
                node["left"] = self.sway(left,min,cols,node["A"])
        return node