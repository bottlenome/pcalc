import pcalc

def sphere(x):
    return (x ** 2).sum()

class Rosenbrock():
    def __init__(self, dim):
        self.dim = dim
        self.y = pcalc.randarray(dim)

    # (a - x)^2 + b(y - x^2)^2
    def fitness(self, x):
        a = pcalc.Value(1)
        b = pcalc.Value(100)
        return ((a - x) ** 2 + b * (self.y - x ** 2) ** 2).sum()


if __name__ == "__main__":
    a = pcalc.array([[1, 2, 3], [4, 5, 6]])
    b = sphere(a) 
    assert(b.observe() == sum([1, 4, 9, 16, 25, 36]))

    c = pcalc.Value(2)
    result = (c - a).observe()
    assert(result[0][0] == 1)
    assert(result[0][1] == 0)
    assert(result[0][2] == 65536 - 1)
    assert(result[1][0] == 65536 - 2)
    assert(result[1][1] == 65536 - 3)
    assert(result[1][2] == 65536 - 4)
   
    r = Rosenbrock(6)
    print(r.fitness(a).observe())