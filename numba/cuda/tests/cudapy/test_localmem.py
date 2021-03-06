from __future__ import print_function, absolute_import, division
import numpy
from numba import cuda, int32, complex128
from numba.cuda.testing import unittest


def culocal(A, B):
    C = cuda.local.array(100, dtype=int32)
    for i in range(C.shape[0]):
        C[i] = A[i]
    for i in range(C.shape[0]):
        B[i] = C[i]


def culocalcomplex(A, B):
    C = cuda.local.array(100, dtype=complex128)
    for i in range(C.shape[0]):
        C[i] = A[i]
    for i in range(C.shape[0]):
        B[i] = C[i]


class TestCudaLocalMem(unittest.TestCase):
    def test_local_array(self):
        jculocal = cuda.jit('void(int32[:], int32[:])')(culocal)
        self.assertTrue('.local' in jculocal.ptx)
        A = numpy.arange(100, dtype='int32')
        B = numpy.zeros_like(A)
        jculocal(A, B)
        self.assertTrue(numpy.all(A == B))

    def test_local_array_complex(self):
        sig = 'void(complex128[:], complex128[:])'
        jculocalcomplex = cuda.jit(sig)(culocalcomplex)
        self.assertTrue('.local' in jculocalcomplex.ptx)
        A = (numpy.arange(100, dtype='complex128') - 1) / 2j
        B = numpy.zeros_like(A)
        jculocalcomplex(A, B)
        self.assertTrue(numpy.all(A == B))


if __name__ == '__main__':
    unittest.main()
