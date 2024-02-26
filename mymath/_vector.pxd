cdef class CartVector:
  cdef public double x, y, z
  # cpdef double length(self)
  cpdef dotPrdt(self, CartVector vec)
  cpdef crsPrdt(self, CartVector vec)
  cpdef CartVector unit_vector(self)

cdef class CylinderVector(CartVector):
  cdef public double rho, phi

cdef class SphereVector(CartVector):
  cdef public double r, theta, phi

cdef class UnitSphereVector(SphereVector):
  pass
