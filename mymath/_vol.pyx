from ._vector cimport CartVector as Vec
from ._ray cimport Ray

cdef class SphereVol:
  def __init__(self, Vec origin, double radius):
    self.origin = origin
    self.radius = radius

  cpdef isRayIn(self, Ray ray):
    cdef double dis
    dis = ((self.origin - ray.origin).crsPrdt(
      self.origin - ray.termin)).length/ray.length
    if dis < self.radius:
      return True
    else:
      return False
    # tmp = ((ray.origin - self.origin).length**2*ray.length**2 -
    #  (ray.origin - self.origin).cdot(ray.termin-ray.origin))**2
    # if tmp < self.radius**2 * ray.length**2:
    #   return True
    # else:
    #   return False

# cdef crossPoint(Ray ray, SphereVol vol):
#   return Vec(1, 2, 3)