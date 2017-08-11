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

    def cut(self, value):
        if self.unsigned:
            value %= self.range
        else:
            raise NotImplementedError
        return value

    def op(self, op, A, B):
        C = Value(0)
        mp = {}
        for b in B.value_map:
            for a in A.value_map:
                value = self.cut(op(a, b))
                if not mp.has_key(value):
                    mp[value] = 0.0
                mp[value] += A.value_map[a] * B.value_map[b]
        C.value_map = mp
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
        raise NotImplementedError()

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
