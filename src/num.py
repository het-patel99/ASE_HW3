import math

## Num class Summarizes a stram of numbers
## Represents a column of character values
class Num():
    
    ## constructor created for Num class
    def __init__(self, at = 0, txt = ""):
        self.at = at
        self.txt = txt

        self.n = 0
        self.mu = 0
        self.m2 = 0

        self.lo = float('inf')
        self.hi = float('-inf')

        self.w = -1 if '-$' in txt else 1

    def at(self) -> int:
        return self.at

    def txt(self) -> str:
        return self.txt

    ## add method adds the n value also,
    ## It upadtes the values of lo,hi d, mu,m2 which is used for,
    ## calculating standard devaiation. 
    def add(self, value):
        if value != '?':
            float_value = float(value)
            self.n = self.n + 1
            d = float_value - self.mu
            self.mu = self.mu + (d / self.n)
            self.m2 = self.m2 + (d * (float_value - self.mu))
            self.lo = min(float_value, self.lo)
            self.hi = max(float_value, self.hi)

    ## mid method return the mean. 
    def mid(self):
        return self.mu

    # div method uses Welford's algorithmn to calculate standard deviation,
    # here is the link for Welford's algorithmn http://t.ly/nn_W
    def div(self): 
        if((self.m2 < 0) or (self.n < 2)):
            return 0
        return pow((self.m2 / (self.n - 1)), 0.5)

    def rnd(self, x, n):
        if x == "?":
            return x
        mult = math.pow(10, n)
        return math.floor(x*mult + 0.5) / mult