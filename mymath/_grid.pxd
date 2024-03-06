cdef class PointArray:
  cdef public double[:] x
  cdef public double[:] y
  cdef public double[:] z
  cdef public double[:] rho

cdef class RayGrid(PointArray):
  cdef public PointArray node
  cdef public PointArray cntr
  cdef public double[:] ds

cdef class UniformRayGrid(RayGrid):
  pass

cdef class NonUniformRayGrid(RayGrid):
  pass

cdef class ExpRayGrid(NonUniformRayGrid):
  pass
