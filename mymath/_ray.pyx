from ._vector cimport CartVector as Vector

cdef class Ray:

  def __init__(self, Vector origin, Vector termin):
    self.origin = origin
    self.termin = termin
    self.nGrid = 1

  property length:
    def __get__(self):
      return (self.termin - self.origin).length

  cpdef discrete(self, int nGrid):
    self.nGrid = nGrid

  cpdef translate(self, Vector vec):
    self.origin = self.origin + vec
    self.termin = self.termin + vec

  def __repr__(self):
    _str = "ORIGIN " + self.origin.__repr__()
    _str += "\n" + "TERMIN " + self.termin.__repr__()
    return _str

