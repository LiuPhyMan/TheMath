# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 06.July.2023
"""

from scipy.interpolate import interp2d


class ScalarFieldInSymCylinderRegularCoord(object):

    def __init__(self):
        self.r_crds = None
        self.z_crds = None
        self.scalar = None

    def set_coords(self, *, r_crds, z_crds):
        self.r_crds = r_crds
        self.z_crds = z_crds

    def set_scalar(self, *, scalarValue):
        self.scalar = scalarValue
        self.interp_f = interp2d(self.r_crds, self.z_crds, self.scalar)

    def interp_value(self, *, r, z):
        return self.interp_f(r, z)
