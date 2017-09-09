import random
from operator import *

class Value():
    def create_uniform_possibility(self):
        mp = {}
        p = 1.0 / self.range
        for i in range(self.min, self.max + 1):
            mp[i] = p
        return mp

    def __init__(self, value=None, bit=16, unsigned=True):
        self.bit = 16
        self.unsigned = unsigned
        self.range = 2 ** self.bit
        if self.unsigned:
            self.min = 0
            self.max = 2 ** self.bit - 1
        else:
            self.min = 1 - 2 ** (self.bit - 1)
            self.max = 2 ** (self.bit) - 1
        if value is None:
            self.value_map = self.create_uniform_possibility()
        else:
            if self.min <= value and value <= self.max:
                self.value_map = {value:1.0}
            else:
                print("input value " + str(value))
                print("does not contain in range")
                print(str(self.min) + " to " + str(self.max))
                assert(False)

    def observe(self):
        p = random.uniform(0.0, 1.0)
        for key in self.value_map:
            p -= self.value_map[key]
            if p <= 0:
                break
        return key

    def expect(self):
        ret = 0.0
        for key in self.value_map:
            ret += key * self.value_map[key]
        return ret

    def cut(self, value):
        if self.unsigned:
            value %= self.range
        else:
            raise NotImplementedError
        return value

    def op(self, f, A, B):
        if (isinstance(A, Value) and isinstance(B, Array)):
            return self.opvM(f, A, B)
        else:
            return self.op_(f, A, B)

    def op_(self, f, A, B):
        C = Value(0)
        mp = {}
        for b in B.value_map:
            for a in A.value_map:
                value = self.cut(f(a, b))
                if not mp.has_key(value):
                    mp[value] = 0.0
                mp[value] += A.value_map[a] * B.value_map[b]
        C.value_map = mp
        return C

    def opvM(self, f, A, B):
        C = zeros(B.shape)
        for y in range(C.shape[0]):
            for x in range(C.shape[1]):
                C[y, x] = f(A, B[y, x])
        return C

    def __add__(self, other):
        return self.op(add, self, other)

    def __sub__(self, other):
        return self.op(sub, self, other)

    def __mul__(self, other):
        return self.op(mul, self, other)

    def __div__(self, other):
        return self.op(div, self, other)

    def __and__(self, other):
        return self.op(and_, self, other)

    def __or__(self, other):
        return self.op(or_, self, other)

    def __xor__(self, other):
        return self.op(xor, self, other)

    def cop(self, op, A, B):
        C = Value(0)
        FALSE = 0
        TRUE = 1
        mp = {FALSE:0.0, TRUE:0.0}
        for b in B.value_map:
            for a in A.value_map:
                if op(a, b):
                    mp[TRUE] += A.value_map[a] * B.value_map[b]
                else:
                    mp[FALSE] += A.value_map[a] * B.value_map[b]
        C.value_map = mp
        return C

    def __lt__(self, other):
        return self.cop(lt, self, other)

    def __le__(self, other):
        return self.cop(le, self, other)

    def __eq__(self, other):
        return self.cop(eq, self, other)

    def __ne__(self, other):
        return self.cop(ne, self, other)

    def __ge__(self, other):
        return self.cop(ge, self, other)

    def __gt__(self, other):
        return self.cop(gt, self, other)

    def __not__(self):
        raise NotImplementedError()

    def __abs__(self, other):
        raise NotImplementedError()

    def __floordiv__(self, other):
        raise NotImplementedError()
    
    def __index__(self):
        raise NotImplementedError()

    def __inv__(self):
        raise NotImplementedError()

    def __invert__(self):
        return self.__inv__()

    def __lshift__(self, other):
        raise NotImplementedError()

    def __mod__(self, other):
        raise NotImplementedError()

    def __neg__(self):
        raise NotImplementedError()

    def __pos__(self):
        raise NotImplementedError()

    def __pow__(self, other):
        return self.__mul__(self)

    def __rshift__(self, other):
        raise NotImplementedError()

    def __truediv__(self, other):
        raise NotImplementedError()

    def __contains__(self, other):
        raise NotImplementedError()

    def __delitem__(self, b):
        raise NotImplementedError()

    def __getitem__(self, item):
        raise NotImplementedError()

    def __iadd__(self, other):
        return self.__add__(other)

    def __iand__(self, other):
        return self.__and__(other)

    def __iconcat__(self, other):
        raise NotImplementedError()

    def __idiv__(self, other):
        return self.__div__(other)

    def __ifloordiv__(self, other):
        raise NotImplementedError()

    def __ilshift__(self, other):
        raise NotImplementedError()

    def __imod__(self, other):
        raise NotImplementedError()

    def __imul__(self, other):
        return self.__mul__(other)

    def __ior__(self, other):
        return self.__or__(other)

    def __ipow__(self, other):
        raise NotImplementedError()

    def __irshift__(self, other):
        raise NotImplementedError()

    def __isub__(self, other):
        return self.__sub__(other)

    def __itruediv__(self, other):
        raise NotImplementedError()
        
    def __ixor__(self, other):
        return self.__xor__(other)

class Array():
    def __init__(self, shape, data=None):
        self.shape = shape
        self.dim = len(shape)
        if self.dim != 2:
            raise NotImplementedError
        size = 1
        for x in shape:
            size *= x
        self.size = size
        if data is None:
            self.datas = [Value() for _ in range(size)]
        else:
            assert(len(data) == size)
            self.datas = [Value(v) for v in data]

    # c, z, y, x
    def __getitem__(self, key):
        if type(key) == tuple:
            assert(len(key) == self.dim)
            y = key[0]
            x = key[1]
            return self.datas[y * self.shape[1] + x]
        elif type(key) == int:
            return self.datas[key]
        else:
            print("invalid type:", type(key), "value:", key)
            raise NotImplementedError
        print(key)

    def __setitem__(self, index, value):
        if type(index) == tuple:
            assert(len(index) == self.dim)
            y = index[0]
            x = index[1]
            index = y * self.shape[1] + x
            self.datas[index] = value
        elif type(index) == int:
            self.datas[index] = value
        else:
            print("invalid type:", type(index), "value:", value)
            raise NotImplementedError

    def __pow__(self, m):
        ret = zeros(self.shape)
        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                index = y * self.shape[1] + x
                ret.datas[index] = self.datas[index] ** m
        return ret

    def observe(self):
        ret = []
        for y in range(self.shape[0]):
            row = []
            for x in range(self.shape[1]):
                index = y * self.shape[1] + x
                row.append(self.datas[index].observe())
            ret.append(row)
        return ret

    def op(self, f, A, B):
        C = zeros(B.shape)
        if f == "add":
            f = lambda x, y: A[y, x] + B[y, x]
        elif f == "sub":
            f = lambda x, y: A[y, x] - B[y, x]
        else:
            raise NotImplementedError

        for y in range(C.shape[0]):
            for x in range(C.shape[1]):
                C[y, x] = f(x, y)
        return C

    def __add__(self, other):
        return self.op("add", self, other)

    def __sub__(self, other):
        return self.op("sub", self, other)

    def sum(self):
        x = self[0]
        for i in range(1, self.size):
            x += self[i]
        return x
    

def array(data, dtype="uint16"):
    l = []
    shape = (len(data), len(data[0]))
    for y in range(len(data)):
        assert(len(data[y]) == shape[1])
        for x in range(len(data[y])):
            l.append(data[y][x])
    return Array(shape, data=l)

def zeros(shape, dtype="uint16"):
    size = 1
    for x in shape:
        size *= x
    return Array(shape, data=[0 for v in range(size)])

def randarray(shape, dtype="uint16"):
    if type(shape) == int:
        size = shape
        shape = (shape, 1)
    else:
        size = 1
        for x in shape:
            size *= x
    if dtype == "uint16":
        int_min = 0
        int_max = 2 ** 16

    return Array(shape, data=[random.randint(int_min, int_max) for _ in range(size)])

if __name__ == "__main__":
    # initalize
    x = Value()
    assert(sum(x.value_map.values()) - 1.0 < 0.0000000001)
    try:
        x = Value(65536)
        assert(False)
    except:
        pass

    # unsingned
    # normal
    a = Value(257)
    b = Value(123)
    c = a + b
    assert(c.observe() == 257 + 123)
    c = a - b
    assert(c.observe() == 257 - 123)
    c = a * b
    assert(c.observe() == (257 * 123))
    c = a / b
    assert(c.observe() == (257 / 123))
    c = (a & b)
    assert(c.observe() == (257 & 123))
    c = a | b
    assert(c.observe() == (257 | 123))
    c = a ^ b
    assert(c.observe() == (257 ^ 123))

    TRUE = 1
    FALSE = 0
    c = (a < b)
    assert(c.observe() == FALSE)
    c = (a <= b)
    assert(c.observe() == FALSE)
    c = (a == b)
    assert(c.observe() == FALSE)
    c = (a != b)
    assert(c.observe() == TRUE)
    c = (a > b)
    assert(c.observe() == TRUE)
    c = (a >= b)
    assert(c.observe() == TRUE)

    a += b
    assert(a.observe() == (257 + 123))
    a = Value(257)
    a -= b
    assert(a.observe() == 257 - 123)
    a = Value(257)
    a *= b
    assert(a.observe() == 257 * 123)
    a = Value(257)
    a /= b
    assert(a.observe() == 257 / 123)
    a = Value(257)
    a &= b
    assert(a.observe() == 257 & 123)
    a = Value(257)
    a |= b
    assert(a.observe() == 257 | 123)
    a = Value(257)
    a ^= b
    assert(a.observe() == 257 ^ 123)

    # border
    a = Value(65535)
    b = Value(1)
    c = a + b
    assert(c.observe() == 0)

    a = Value(0)
    b = Value(1)
    c = a - b
    assert(c.observe() == 65535)

    a = Value(10000)
    b = Value(123)
    c = a * b
    assert(c.observe() == (10000 * 123) % 65536)

    a = Array((2, 3))
    assert(a.shape == (2, 3))
    assert(a.size == 6)
    v = a[0, 0]
    a = zeros((2, 3))
    assert(a.shape == (2, 3))
    assert(a.size == 6)
    v = a[0, 0]
    assert(v.observe() == 0)
    a = array([[1, 2, 3], [4, 5, 6]])
    assert(a.shape == (2, 3))
    assert(a.size == 6)
    v = a[1, 1]
    assert(v.observe() == 5)
    assert(a[0, 0].observe() == 1)
    assert(a[0, 1].observe() == 2)
    assert(a[0, 2].observe() == 3)
    assert(a[1, 0].observe() == 4)
    assert(a[1, 1].observe() == 5)
    assert(a[1, 2].observe() == 6)

    for i in a:
        pass
