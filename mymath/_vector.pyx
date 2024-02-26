from libc.math cimport sqrt, cos, sin

# @functools.total_ordering
cdef class CartVector:
  def __init__(self, double x, double y, double z):
    self.x = x
    self.y = y
    self.z = z

  # cpdef double length(self):
  #   return sqrt(self.x**2 + self.y**2 + self.z**2)

  property length:
    def __get__(self):
      return sqrt(self.x**2 + self.y**2 + self.z**2)

  cpdef CartVector unit_vector(self):
    return CartVector(self.x/self.length,
                      self.y/self.length,
                      self.z/self.length)

  cpdef dotPrdt(self, CartVector vec):
    return self.x*vec.x + self.y*vec.y + self.z*vec.z

  cpdef crsPrdt(self, CartVector vec):
    return CartVector(self.y*vec.z - self.z*vec.y,
                      self.z*vec.x - self.x*vec.z,
                      self.x*vec.y - self.y*vec.x)

  cpdef rotByX(self, double angle):
    self.y = cos(angle)*self.y - sin(angle)*self.z
    self.z = sin(angle)*self.y + cos(angle)*self.z

  cpdef rotByY(self, double angle):
    self.x = cos(angle)*self.x + sin(angle)*self.z
    self.z = -sin(angle)*self.x + cos(angle)*self.z

  cpdef rotByZ(self, double angle):
    self.x = cos(angle)*self.x - sin(angle)*self.y
    self.y = sin(angle)*self.x + cos(angle)*self.y

  def __add__(self, CartVector other):
    return CartVector(self.x + other.x, self.y + other.y, self.z + other.z)

  def __mul__(self, double other):
    return CartVector(self.x*other, self.y*other, self.z*other)

  def __sub__(self, CartVector other):
    return CartVector(self.x - other.x, self.y - other.y, self.z - other.z)

  def __repr__(self):
    x_str = f"{self.x:.2f}" if self.x >= 0.1 else f"{self.x:.2e}"
    y_str = f"{self.y:.2f}" if self.y >= 0.1 else f"{self.y:.2e}"
    z_str = f"{self.z:.2f}" if self.z >= 0.1 else f"{self.z:.2e}"
    return f"x-y-z: ({x_str}, {y_str}, {z_str})"

# =========================================================================== #
cdef class CylinderVector(CartVector):
  def __init__(self, double rho, double phi, double z):
    self.rho, self.phi = rho, phi
    super().__init__(self.rho*cos(self.phi), self.rho*sin(self.phi), z)

  def __repr__(self):
    _str = f"rho-phi-z: ({self.rho:.2e}, {self.phi:.2e}, {self.z:.2e})"
    return _str + "\n" + 4*" " + super().__repr__()

cdef class SphereVector(CartVector):
  def __init__(self, double r, double theta, double phi):
    self.r, self.theta, self.phi = r, theta, phi
    super().__init__(self.r*sin(self.theta)*cos(self.phi),
                     self.r*sin(self.theta)*sin(self.phi),
                     self.r*cos(self.theta))

  def __repr__(self):
    _str = f"r-theta-phi: ({self.r:.2e}, {self.theta:.2e}, {self.phi:.2e})"
    return _str + "\n" + 6*" " + super().__repr__()

cdef class UnitSphereVector(SphereVector):
  def __init__(self, double theta, double phi):
    super().__init__(1, theta, phi)
