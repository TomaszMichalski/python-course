from collections import defaultdict
from numbers import Number

class Polynomial:
    def __init__(self):
        self.d = defaultdict(lambda: 0)

    def set_factor(self, factor, power):
        if(isinstance(factor, Number) and isinstance(power, int)):
            self.d[power] = factor

    def get_factor(self, power):
        if(isinstance(power, int)):
            return self.d[power]

    def get_factors(self):
        return self.d

    def __add__(self, other):
        if(isinstance(other, Polynomial)):
            for key, value in other.get_factors().items():
                self.d[key] = self.d[key] + other.get_factor(key)

    def __str__(self):
        res = ""
        for key, value in self.d.items():
            res = res + str(value) + "x^" + str(key) + "+"
        return res[:-1]
    
def main():
    pol = Polynomial()
    pol.set_factor(5, 3)
    pol.set_factor(6, 5)
    
    pol2 = Polynomial()
    pol2.set_factor(3, 7)
    pol2.set_factor(6, 3)

    pol + pol2
    print(pol)

if __name__ == "__main__":
    main()


