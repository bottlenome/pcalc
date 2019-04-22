from unittest import TestCase
from pcalc import *


class TestPcalc(TestCase):
    def test_initalize_uint16(self):
        x = Value()
        self.assertEqual(x.min, 0)
        self.assertEqual(x.max, 65535)
        assert(sum(x.value_map.values()) - 1.0 < 0.0000000001)
        try:
            x = Value(65536)
        except AssertionError:
            pass

        x = Value(0, bit=32, unsigned=False)
        self.assertEqual(x.min, -2147483647)
        self.assertEqual(x.max, 2147483647)
        assert(sum(x.value_map.values()) - 1.0 < 0.0000000001)
        try:
            x = Value(2147483648, bit=32, unsigned=False)
        except AssertionError:
            pass

    def test_operator_uint16(self):
        a = Value(257)
        b = Value(123)
        c = a + b
        self.assertEqual(c.observe(), 257 + 123)
        c = a - b
        self.assertEqual(c.observe(), 257 - 123)
        c = a * b
        self.assertEqual(c.observe(), (257 * 123))
        c = a / b
        self.assertEqual(c.observe(), (257 / 123))
        c = (a & b)
        self.assertEqual(c.observe(), (257 & 123))
        c = a | b
        self.assertEqual(c.observe(), (257 | 123))
        c = a ^ b
        self.assertEqual(c.observe(), (257 ^ 123))

        TRUE = 1
        FALSE = 0
        c = (a < b)
        self.assertEqual(c.observe(), FALSE)
        c = (a <= b)
        self.assertEqual(c.observe(), FALSE)
        c = (a == b)
        self.assertEqual(c.observe(), FALSE)
        c = (a != b)
        self.assertEqual(c.observe(), TRUE)
        c = (a > b)
        self.assertEqual(c.observe(), TRUE)
        c = (a >= b)
        self.assertEqual(c.observe(), TRUE)

        a += b
        self.assertEqual(a.observe(), (257 + 123))
        a = Value(257)
        a -= b
        self.assertEqual(a.observe(), 257 - 123)
        a = Value(257)
        a *= b
        self.assertEqual(a.observe(), 257 * 123)
        a = Value(257)
        a /= b
        self.assertEqual(a.observe(), 257 / 123)
        a = Value(257)
        a &= b
        self.assertEqual(a.observe(), 257 & 123)
        a = Value(257)
        a |= b
        self.assertEqual(a.observe(), 257 | 123)
        a = Value(257)
        a ^= b
        self.assertEqual(a.observe(), 257 ^ 123)

        # border
        a = Value(65535)
        b = Value(1)
        c = a + b
        self.assertEqual(c.observe(), 0)

        a = Value(0)
        b = Value(1)
        c = a - b
        self.assertEqual(c.observe(), 65535)

        a = Value(10000)
        b = Value(123)
        c = a * b
        self.assertEqual(c.observe(), (10000 * 123) % 65536)

    def test_operator_int32(self):
        a = Value(257, bit=32, unsigned=False)
        b = Value(123, bit=32, unsigned=False)
        c = a + b
        self.assertEqual(c.observe(), 257 + 123)
        c = a - b
        self.assertEqual(c.observe(), 257 - 123)
        c = a * b
        self.assertEqual(c.observe(), (257 * 123))
        c = a / b
        self.assertEqual(c.observe(), (257 / 123))
        c = (a & b)
        self.assertEqual(c.observe(), (257 & 123))
        c = a | b
        self.assertEqual(c.observe(), (257 | 123))
        c = a ^ b
        self.assertEqual(c.observe(), (257 ^ 123))

        TRUE = 1
        FALSE = 0
        c = (a < b)
        self.assertEqual(c.observe(), FALSE)
        c = (a <= b)
        self.assertEqual(c.observe(), FALSE)
        c = (a == b)
        self.assertEqual(c.observe(), FALSE)
        c = (a != b)
        self.assertEqual(c.observe(), TRUE)
        c = (a > b)
        self.assertEqual(c.observe(), TRUE)
        c = (a >= b)
        self.assertEqual(c.observe(), TRUE)

        a += b
        self.assertEqual(a.observe(), (257 + 123))
        a = Value(257, bit=32, unsigned=False)
        a -= b
        self.assertEqual(a.observe(), 257 - 123)
        a = Value(257, bit=32, unsigned=False)
        a *= b
        self.assertEqual(a.observe(), 257 * 123)
        a = Value(257, bit=32, unsigned=False)
        a /= b
        self.assertEqual(a.observe(), 257 / 123)
        a = Value(257, bit=32, unsigned=False)
        a &= b
        self.assertEqual(a.observe(), 257 & 123)
        a = Value(257, bit=32, unsigned=False)
        a |= b
        self.assertEqual(a.observe(), 257 | 123)
        a = Value(257, bit=32, unsigned=False)
        a ^= b
        self.assertEqual(a.observe(), 257 ^ 123)

        # border
        a = Value(2147483647, bit=32, unsigned=False)
        b = Value(1, bit=32, unsigned=False)
        c = a + b
        self.assertEqual(c.observe(), -2147483647)

        a = Value(-2147483647, bit=32, unsigned=False)
        b = Value(1, bit=32, unsigned=False)
        c = a - b
        self.assertEqual(c.observe(), 2147483647)

        a = Value(100000, bit=32, unsigned=False)
        b = Value(123456, bit=32, unsigned=False)
        c = a * b
        right = 100000 * 123456 - (a.range - 1) * 3
        self.assertEqual(c.observe(), right)

    def test_array(self):
        a = Array((2, 3))
        self.assertEqual(a.shape, (2, 3))
        self.assertEqual(a.size, 6)
        self.assertEqual(a.dtype, "uint16")
        v = a[0, 0]
        a = zeros((2, 3))
        self.assertEqual(a.shape, (2, 3))
        self.assertEqual(a.size, 6)
        v = a[0, 0]
        self.assertEqual(v.observe(), 0)
        a = array([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(a.shape, (2, 3))
        self.assertEqual(a.size, 6)
        v = a[1, 1]
        self.assertEqual(v.observe(), 5)
        self.assertEqual(a[0, 0].observe(), 1)
        self.assertEqual(a[0, 1].observe(), 2)
        self.assertEqual(a[0, 2].observe(), 3)
        self.assertEqual(a[1, 0].observe(), 4)
        self.assertEqual(a[1, 1].observe(), 5)
        self.assertEqual(a[1, 2].observe(), 6)

        a = Array((2, 3), data=[1, 2, 3, 4, 5, 6], dtype="int32")
        self.assertEqual(a.dtype, "int32")

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

        b = randarray(6)
        try:
            a - b
        except: ValueError

        c = a + a
        self.assertEqual(c[0, 0].observe(), 2)
        self.assertEqual(c[0, 1].observe(), 4)
        self.assertEqual(c[0, 2].observe(), 6)
        self.assertEqual(c[1, 0].observe(), 8)
        self.assertEqual(c[1, 1].observe(), 10)
        self.assertEqual(c[1, 2].observe(), 12)

        c = b - a
        self.assertEqual(c[0, 0].observe(), 0)
        self.assertEqual(c[0, 1].observe(), 0)
        self.assertEqual(c[0, 2].observe(), 0)
        self.assertEqual(c[1, 0].observe(), 0)
        self.assertEqual(c[1, 1].observe(), 0)
        self.assertEqual(c[1, 2].observe(), 0)


    def test_zeros(self):
        a = zeros((2, 1))
        self.assertEqual(a[0, 0].observe(), 0)
        self.assertEqual(a[1, 0].observe(), 0)

        a = zeros((2, 1), dtype="int32")

if __name__ == '__main__':
    import unittest
    unittest.main()
