# -*- coding: utf-8 -*-
"""
@author:    Liu.Jinbao
@contact:   liu.jinbao@outlook.com
@time:      06.July.2023
"""

from .vector import CartVector


class AbsVol(object):

    def __init__(self):
        pass

    def isPointIn(self, point: CartVector):
        pass

    def isPointOut(self, point: CartVector):
        return not self.isPointIn(point)


class CylinderVol(AbsVol):

    def __init__(self, *, rMax: float, zRange: tuple) -> None:
        self.rMax = rMax
        self.zRange = zRange
        super().__init__()

    def isPointIn(self, point: CartVector):
        if (point.rhoAtCylin <= self.rMax) and (self.zRange[0] <= point.z <= self.zRange[1]):
            return True
        else:
            return False


class BoxVolume(AbsVol):

    def __init__(self, *, xRange: tuple, yRange: tuple, zRange: tuple) -> None:
        self.xRange = xRange
        self.yRange = yRange
        self.zRange = zRange
        super().__init__()

    def isPointIn(self, point: CartVector):
        if (self.xRange[0] <= point.x <= self.xRange[1]) and \
                (self.yRange[0] <= point.y <= self.yRange[1]) and \
                (self.zRange[0] <= point.z <= self.zRange[1]):
            return True
        else:
            return False
