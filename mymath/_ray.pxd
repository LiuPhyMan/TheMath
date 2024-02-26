from ._vector cimport CartVector as Vector

cdef class Ray:
  cdef public Vector origin, termin
  cdef public int nGrid
  cpdef discrete(self, int nGrid)
  cpdef translate(self, Vector vec)
  #   pass