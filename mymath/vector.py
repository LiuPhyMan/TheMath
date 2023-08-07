# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 06.July.2023
"""

from math import sqrt, cos, sin


class CartVector(object):

    def __init__(self, *, xyz: tuple) -> None:
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
        return f"x-y-z: ({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


class CylinderVector(CartVector):

    def __init__(self, *, rhoPhiZ: tuple) -> None:
        self.rho, self.phi, self.z = rhoPhiZ
        super().__init__(xyz=(self.rho*cos(self.phi), self.rho*sin(self.phi), self.z))


class SphereVector(CartVector):

    def __init__(self, *, rThetaPhi: tuple) -> None:
        self.r, self.theta, self.phi = rThetaPhi
        super().__init__(xyz=(self.r*sin(self.theta)*cos(self.phi),
                              self.r*sin(self.theta)*sin(self.phi), self.r*cos(self.theta)))
