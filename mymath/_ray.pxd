from ._vector cimport CartVector as Vector

cdef class Ray:
  cdef public Vector origin, termin
  cdef public int nGrid
  cpdef discrtByN(self, int nGrid)
  cpdef translate(self, Vector vec)
  cpdef rotByX(self, double angle)
  #   pass

cdef class LightRay(Ray):
  cdef public double Iend
  cdef public double thinIend
  cdef public double optThick