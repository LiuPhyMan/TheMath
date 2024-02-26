from ._vector cimport CartVector as Vector
from ._ray cimport Ray

cdef class SphereVol:
  cdef Vector origin
  cdef double radius
  cpdef isRayIn(self, Ray ray)