from cython.parallel import prange
from libc.math cimport exp
from ._vector cimport CartVector as Vector

cdef class Ray:

  def __init__(self, Vector origin, Vector termin):
    self.origin = origin
    self.termin = termin
    self.nGrid = 1

  property length:
    def __get__(self):
      return (self.termin - self.origin).length

  cpdef discrtByN(self, int nGrid):
    self.nGrid = nGrid

  cpdef translate(self, Vector vec):
    self.origin = self.origin + vec
    self.termin = self.termin + vec

  cpdef rotByX(self, double angle):
    self.origin.rotByX(angle)
    self.termin.rotByX(angle)


  def __repr__(self):
    _str = "ORIGIN " + self.origin.__repr__()
    _str += "\n" + "TERMIN " + self.termin.__repr__()
    return _str

cdef class Rays:

  def __init__(self, list rays):
    self.rays = rays
    self.nRay = len(self.rays)

#   cpdef solveRTE(double[:] kappa, double[:] emiss, double[:] ds):
#     cdef Py_ssize_t i
#     for i in prange(self.nRay, nogil=True):
#       solveRTE(kappa, emiss, ds) .  #TODO




cdef class LightRay(Ray):

  def __init__(self, Vector origin, Vector termin):
    super().__init__(origin, termin)
    self.Iend = 0.
    self.optThick = 0.
    self.thinIend = 0.

cdef double beta_factor(double x):
  assert x >= 0
  if x < 1e-3:
    return 1-x/2
  else:
    return (1-exp(-x))/x

cpdef double solveRTE(double[:] kappa, double[:] emiss, double[:] ds):
  r""" RTE: dI/ds = j - kappa*I 
    Returns I at end."""
  cdef int N = kappa.size
  assert emiss.size == N
  assert ds.size == N
  cdef double Iend = 0
  cdef double tmp = 0
  cdef Py_ssize_t i

  for i in range(N):
    Iend = Iend*exp(-kappa[i]*ds[i])  + \
           emiss[i]*ds[i]*beta_factor(kappa[i]*ds[i])
  return Iend

cpdef double getThinIend(double[:] emiss, double[:] ds):
  """
  
  Parameters
  ----------
  emiss
  ds

  Returns
  -------

  """
  cdef int N = emiss.size
  assert ds.size == N
  cdef double Iend = 0
  cdef Py_ssize_t i
  for i in range(N):
    Iend += emiss[i]*ds[i]
  return Iend

cpdef double getOptThick(double[:] kappa, double[:] ds):
  cdef int N = kappa.size
  assert ds.size == N
  cdef double optThick = 0
  cdef Py_ssize_t i
  for i in range(N):
    optThick += kappa[i] * ds[i]
  return optThick

