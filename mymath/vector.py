# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 06.July.2023
"""

from math import sqrt, cos, sin

# =============================================================================================== #
#   A point could be defined by a vector that starts from the origin.
# ----------------------------------------------------------------------------------------------- #
class CartVector(object):

    def __init__(self, *, xyz: tuple[float]) -> None:
        self.x, self.y, self.z = xyz

    def unit_vector(self):
        return CartVector(xyz=(self.x/self.length, self.y/self.length, self.z/self.length))

    @property
    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    @property
    def rhoAtCylin(self):
        return sqrt(self.x**2 + self.y**2)

    def __add__(self, other):
        return CartVector(xyz=(self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        return CartVector(xyz=(self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other):
        return CartVector(xyz=(self.x*other, self.y*other, self.z*other))

    def __repr__(self):
        x_str = f"{self.x:.2f}" if self.x >= 0.1 else f"{self.x:.2e}"
        y_str = f"{self.y:.2f}" if self.y >= 0.1 else f"{self.y:.2e}"
        z_str = f"{self.z:.2f}" if self.z >= 0.1 else f"{self.z:.2e}"
        return f"x-y-z: ({x_str}, {y_str}, {z_str})"


class CylinderVector(CartVector):

    def __init__(self, *, rhoPhiZ: tuple[float]) -> None:
        self.rho, self.phi, self.z = rhoPhiZ
        super().__init__(xyz=(self.rho*cos(self.phi), self.rho*sin(self.phi), self.z))


class SphereVector(CartVector):

    def __init__(self, *, rThetaPhi: tuple[float]) -> None:
        self.r, self.theta, self.phi = rThetaPhi
        super().__init__(xyz=(self.r*sin(self.theta)*cos(self.phi),
                              self.r*sin(self.theta)*sin(self.phi), self.r*cos(self.theta)))


class UnitSphereVector(SphereVector):

    def __init__(self, *, thetaPhi: tuple[float]) -> None:
        theta, phi = thetaPhi
        super().__init__(rThetaPhi=(1, theta, phi))


default_vectors = {
    "orig": CartVector(xyz=(0, 0, 0)),
    "xPos": CartVector(xyz=(1, 0, 0)),
    "xNeg": CartVector(xyz=(-1, 0, 0)),
    "yPos": CartVector(xyz=(0, 1, 0)),
    "yNeg": CartVector(xyz=(0, -1, 0)),
    "zPos": CartVector(xyz=(0, 0, 1)),
    "zNeg": CartVector(xyz=(0, 0, -1))}
