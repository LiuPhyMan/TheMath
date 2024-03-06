from ._vector cimport CartVector as Vector # noqa
import numpy as np

cdef class PointArray:

  def __init__(self, double[:] x_seq, double[:] y_seq, double[:] z_seq):
    self.x = x_seq
    self.y = y_seq
    self.z = z_seq
    self.rho = np.sqrt(np.asarray(self.x)**2 + np.asarray(self.y)**2)


cdef class RayGrid:

  def __init__(self, PointArray node):
    self.node = node
    self.cntr = PointArray(np.add(self.node.x[:-1], self.node.x[1:])/2,
                           np.add(self.node.y[:-1], self.node.y[1:])/2,
                           np.add(self.node.z[:-1], self.node.z[1:])/2)

cdef class UniformRayGrid(RayGrid):

  def __init__(self, Vector origin, Vector termin, int nGrid):
    super().__init__(PointArray(np.linspace(origin.x, termin.x, nGrid+1),
                                np.linspace(origin.y, termin.y, nGrid+1),
                                np.linspace(origin.z, termin.z, nGrid+1)))
    self.ds = np.ones(nGrid) * (origin-termin).length/nGrid


cdef class NonUniformRayGrid(RayGrid):

  def __init__(self, Vector origin, Vector termin, double[:] normGrid):
    super().__init__(PointArray(origin.x+np.asarray(normGrid)*(termin.x-origin.x),
                                origin.y+np.asarray(normGrid)*(termin.y-origin.y),
                                origin.z+np.asarray(normGrid)*(termin.z-origin.z)))
    self.ds = np.subtract(normGrid[1:], normGrid[:-1])*(termin-origin).length


cdef class ExpRayGrid(NonUniformRayGrid):

  def __init__(self, Vector origin, Vector termin, int nGrid, double ratio):
    cdef double[:] normGrid
    normGrid = (np.power(ratio, np.arange(nGrid+1)/(nGrid-1))-1) / \
               (ratio**(nGrid/(nGrid-1))-1)
    super().__init__(origin, termin, normGrid)
