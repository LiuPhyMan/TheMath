# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 01.June.2023
"""

import numpy as np

from .vector import CartVector, CylinderVector
from .volume import AbsVol


# =============================================================================================== #
class PointArrays(object):
    __slots__ = ["pointList", "nPoints",
                 "x_seq", "y_seq", "z_seq",
                 "rho_seq"]

    def __init__(self, *, pointList: list):
        self.pointList = pointList
        self.nPoints = len(self.pointList)

        self.x_seq = np.array([_p.x for _p in self.pointList])
        self.y_seq = np.array([_p.y for _p in self.pointList])
        self.z_seq = np.array([_p.z for _p in self.pointList])
        self.rho_seq = np.array([_p.rhoAtCylin for _p in self.pointList])

    def __getitem__(self, item: int):
        return self.pointList[item]

    def topo_in_vol(self, *, vol: AbsVol) -> list:
        r"""
        Returns
        -------
            ["out", "out", "in", ..., "out"]
            [False, False, True, ..., False]
        """
        tmp = []
        for _point in self.pointList:
            tmp.append(vol.isPointIn(_point))
        return tmp

class CylinderPointArrays(PointArrays):

    def __init__(self, *, rho_seq, phi_seq, z_seq):
        pointList = []
        for i in range(rho_seq.size):
            pointList.append(CylinderVector(rhoPhiZ=(rho_seq.flatten()[i], phi_seq.flatten()[i],
                                            z_seq.flatten()[i])))
        super().__init__(pointList=pointList)
# =============================================================================================== #
# =============================================================================================== #
class XZPlanePointMatrix(PointArrays):
    __slots__ = ["dS"]

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
