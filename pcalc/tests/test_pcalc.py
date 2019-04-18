from pcalc import *

def test_initalize_uint16():
    x = Value()
    assert(x.min == 0)
    assert(x.max == 65535)
    assert(sum(x.value_map.values()) - 1.0 < 0.0000000001)
    try:
        x = Value(65536)
        assert(False)
    except:
        pass
    
    x = Value(0, bit=32, unsigned=False)
    assert(x.min == -2147483647)
    assert(x.max == 2147483647)
    assert(sum(x.value_map.values()) - 1.0 < 0.0000000001)
    try:
        x = Value(2147483648, bit=32, unsigned=False)
        assert(False)
    except:
        pass

def test_operator_uint16():
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

def test_operator_int32():
    a = Value(257, bit=32, unsigned=False)
    b = Value(123, bit=32, unsigned=False)
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
    a = Value(257, bit=32, unsigned=False)
    a -= b
    assert(a.observe() == 257 - 123)
    a = Value(257, bit=32, unsigned=False)
    a *= b
    assert(a.observe() == 257 * 123)
    a = Value(257, bit=32, unsigned=False)
    a /= b
    assert(a.observe() == 257 / 123)
    a = Value(257, bit=32, unsigned=False)
    a &= b
    assert(a.observe() == 257 & 123)
    a = Value(257, bit=32, unsigned=False)
    a |= b
    assert(a.observe() == 257 | 123)
    a = Value(257, bit=32, unsigned=False)
    a ^= b
    assert(a.observe() == 257 ^ 123)

    # border
    a = Value(2147483647, bit=32, unsigned=False)
    b = Value(1, bit=32, unsigned=False)
    c = a + b
    assert(c.observe() == -2147483647)

    a = Value(-2147483647, bit=32, unsigned=False)
    b = Value(1, bit=32, unsigned=False)
    c = a - b
    assert(c.observe() == 2147483647)

    a = Value(100000, bit=32, unsigned=False)
    b = Value(123456, bit=32, unsigned=False)
    c = a * b
    right = 100000 * 123456 - (a.range - 1) * 3
    assert(c.observe() == right)

def test_array():
    a = Array((2, 3))
    assert(a.shape == (2, 3))
    assert(a.size == 6)
    assert(a.dtype == "uint16")
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

    a = Array((2, 3), data=[1, 2, 3, 4, 5, 6], dtype="int32")
    assert(a.dtype == "int32")
    
    try:
        a[0, 3]
        assert(False)
    except IndexError:
        pass

    try:
        a[2, 0]
        assert(False)
    except IndexError:
        pass

def test_zeros():
    a = zeros((2,1))
    assert(a[0, 0].observe() == 0)
    assert(a[1, 0].observe() == 0)

    a = zeros((2, 1), dtype="int32")
