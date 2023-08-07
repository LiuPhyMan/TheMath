# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 01.June.2023
"""

from math import sqrt, cos, sin
import numpy as np
from .vector import CartVector
from .volume import AbsVol


# =============================================================================================== #
class PointArrays(object):

    def __init__(self, *, pointList: list):
        self.pointList = pointList
        self.nPoints = len(self.pointList)

    def topo_in_vol(self, *, vol: AbsVol):
        tmp = []
        for _point in self.pointList:
            tmp.append(vol.isPointIn(_point))
        return tmp


# =============================================================================================== #
# =============================================================================================== #
class XZPlanePointMatrix(PointArrays):

    def __init__(self, *, xRange: tuple, zRange: tuple, nXGrid: int, nZGrid: int, Y: float):
        assert (xRange[0] < xRange[1]) and (zRange[0] < zRange[1])
        x = np.linspace(xRange[0], xRange[1], nXGrid)
        z = np.linspace(zRange[0], zRange[1], nZGrid)
        xx, zz = np.meshgrid(x, z)
        xx, zz = xx.flatten(), zz.flatten()
        points = []
        for _i in range(xx.size):
            points.append(CartVector(xyz=(xx[_i], Y, zz[_i])))
        super().__init__(pointList=points)
        self.dS = (xRange[1] - xRange[0])/nXGrid*(zRange[1] - zRange[0])/nZGrid
