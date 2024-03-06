cdef class CartVector:
  cdef public double x, y, z
  cpdef dotPrdt(self, CartVector vec)
  cpdef crsPrdt(self, CartVector vec)
  cpdef CartVector unit_vector(self)
  cpdef rotByX(self, double angle)
  cpdef rotByY(self, double angle)
  cpdef rotByZ(self, double angle)

cdef class CylinderVector(CartVector):
  cdef public double rho, phi

cdef class SphereVector(CartVector):
  cdef public double r, theta, phi

cdef class UnitSphereVector(SphereVector):
  pass

