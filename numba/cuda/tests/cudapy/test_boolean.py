from __future__ import print_function, absolute_import
import numpy as np
from numba.cuda.testing import unittest
from numba import cuda


def boolean_test(A, vertial):
    if vertial:
        A[0] = 123
    else:
        A[0] = 321


class TestCudaBoolean(unittest.TestCase):
    def test_boolean(self):
        func = cuda.jit('void(float64[:], bool_)')(boolean_test)
        A = np.array([0], dtype='float64')
        func(A, True)
        self.assertTrue(A[0] == 123)
        func(A, False)
        self.assertTrue(A[0] == 321)


if __name__ == '__main__':
    unittest.main()
