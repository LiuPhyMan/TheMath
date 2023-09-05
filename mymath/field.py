# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 06.July.2023
"""

import numpy as np
from scipy.interpolate import RegularGridInterpolator as regular_interp, NearestNDInterpolator \
    as unstruct_interp

from .pointArray import PointArrays
from .vector import CartVector


class AbsScalarFieldSymCylin(object):
    __slots__ = ["r_crds", "z_crds", "scalar", "interp_f"]

    def __init__(self, *, r_crds, z_crds, scalar=None):
        self.r_crds = r_crds
        self.z_crds = z_crds
        self.scalar = scalar
        self.interp_f = None

    def set_scalar(self, *, scalarValue):
        pass

    def getPointValue(self, point: CartVector):
        return self.interp_f(point.rhoAtCylin, point.z)

    def getMultiPointValues(self, point_arrys: PointArrays):
        # return np.array([self.getPointValue(_p) for _p in point_arrys.pointList])
        return self.interp_f(point_arrys.rho_seq, point_arrys.z_seq)

    # def mapToNewField(self, *, map_f):
    #     r"""
    #     map_f: old_scalar -> new_scalar
    #     """
    #     new_scalar = np.zeros_like(self.scalar)
    #     for i in range(new_scalar.shape[0]):
    #         for j in range(new_scalar.shape[1]):
    #             new_scalar[i, j] = map_f(self.scalar[i, j])
    #     return ScalarFieldInSymCylinderRegularCoord(r_crds=self.r_crds, z_crds=self.z_crds,
    #                                                 scalar=new_scalar)


class ScalarFieldSymCylinRegularGrid(AbsScalarFieldSymCylin):

    def __init__(self, *, r_crds, z_crds, scalar=None):
        super().__init__(r_crds=r_crds, z_crds=z_crds, scalar=scalar)

    def set_scalar(self, *, scalarValue):
        self.scalar = scalarValue
        self.interp_f = regular_interp((self.r_crds, self.z_crds), self.scalar, method="cubic")


class ScalarFieldSymCylinUnstructGrid(AbsScalarFieldSymCylin):

    def __init__(self, *, r_crds, z_crds, scalar=None):
        super().__init__(r_crds=r_crds, z_crds=z_crds, scalar=scalar)

    def set_scalar(self, *, scalarValue):
        self.scalar = scalarValue
        self.interp_f = unstruct_interp((self.r_crds, self.z_crds), self.scalar)
