from math import exp

import numpy as np
from matplotlib import pyplot as plt

from .pointArray import PointArrays
from .volume import AbsVol


class AbsRay(object):
    __slots__ = ["origin", "termin", "unit_direct", "length",
                 "nGrid", "nNode",
                 "nodes", "centrs",
                 "ds"]

    def __init__(self, *, origin, termin=None, direct=None):
        self.origin = origin
        if termin is None:
            self.termin = self.origin + direct
        elif direct is None:
            self.termin = termin
        else:
            raise Exception("")
        self.unit_direct = (self.termin - self.origin).unit_vector()
        self.length = (self.termin - self.origin).length

    def uniform_discrete(self, *, nGrid: int):
        self.nGrid = nGrid
        self.nNode = self.nGrid + 1
        self.nodes = PointArrays(pointList=[self.origin*(1 - _n/nGrid) + self.termin*(_n/nGrid)
                                            for _n in range(nGrid + 1)])
        self.centrs = PointArrays(pointList=[self.origin*(1 - 3*_n/2/nGrid) +
                                             self.termin*(3*_n/2/nGrid) for _n in range(nGrid)])
        # uniform discrete
        self.ds = np.array([(self.nodes.pointList[i + 1] - self.nodes.pointList[i]).length
                            for i in range(self.nGrid)])

    # ------------------------------------------------------------------------------------------- #
    def topo_vol(self, *, vol: AbsVol, ds_err: float):
        r"""
        return "in", "out", "in-out", "out-in", "out-in-out"
        """
        n = int(self.length/ds_err) + 1
        self.uniform_discrete(nGrid=n)
        #
        topo = self.nodes.topo_in_vol(vol=vol)
        #
        if np.all(topo):
            return "in"
        elif np.any(topo):
            if (topo[0] is True) and (topo[-1] is False):
                return "in-out"
            elif (topo[0] is False) and (topo[-1] is True):
                return "out-in"
            else:
                return "out-in-out"
        else:
            return "out"

    def cut_in_vol(self, *, vol, ds_err):
        assert self.topo_vol(vol=vol, ds_err=ds_err) != "out"
        n = int(self.length/ds_err) + 1
        self.uniform_discrete(nGrid=n)
        # --------------------------------------------------------------------------------------- #
        isOnLine = False
        start_index = 0
        end_index = -1
        for _i, _vec in enumerate(self.nodes.pointList):
            if (isOnLine is False) and vol.isPointIn(_vec):
                start_index = _i
                isOnLine = True
            if (isOnLine is True) and vol.isPointOut(_vec):
                end_index = _i
                break
            continue
        self.__init__(origin=self.nodes.pointList[start_index],
                      termin=self.nodes.pointList[end_index])

    def __repr__(self):
        return f"Origin: {self.origin.__repr__()}\tTermin: {self.termin.__repr__()}"


class LightRay(AbsRay):
    __slots__ = ["I", "j", "k"]

    def __init__(self, *, origin, termin=None, direct=None):
        super().__init__(origin=origin, termin=termin, direct=direct)

    def init_I(self):
        self.I = np.zeros(self.nNode)
        self.j = np.zeros(self.nGrid)
        self.k = np.zeros(self.nGrid)

    @property
    def Iend(self):
        return self.I[-1]

    def set_emission(self, *, emission):
        self.j = emission

    def set_absorption(self, *, absorb):
        self.k = absorb

    def solve_I(self):
        # TODO
        for iNode in range(self.nNode - 1):
            tao = self.k[iNode]*self.ds[iNode]
            self.I[iNode + 1] = self.I[iNode]*exp(-self.k[iNode])*self.ds[iNode] + \
                                self.j[iNode]*(1 - 0.5*tao + tao**2/6 - tao**3/24)*self.ds[iNode]

    def plot(self):
        f = plt.figure()
        ax = f.add_subplot()
        ax.plot(self.I)


# =============================================================================================== #
class MultiRays(object):
    __slots__ = ["rayClass", "nRays", "rayList"]

    def __init__(self, *, start_points: PointArrays, end_points: PointArrays, RayClass: object):
        assert start_points.nPoints == end_points.nPoints
        self.rayClass = RayClass
        self._set_rayList(start_points=start_points, end_points=end_points)

    def _set_rayList(self, *, start_points, end_points):
        assert start_points.nPoints == end_points.nPoints
        self.nRays = start_points.nPoints
        self.rayList = []
        for _i in range(self.nRays):
            self.rayList.append(self.rayClass(origin=start_points.pointList[_i],
                                              termin=end_points.pointList[_i]))

    def cut_in_vol(self, *, vol, ds_err):
        start_points = []
        end_points = []
        for _ray in self.rayList:
            if _ray.topo_vol(vol=vol, ds_err=ds_err) == "out":
                continue
            else:
                _ray.cut_in_vol(vol=vol, ds_err=ds_err)
                start_points.append(_ray.origin)
                end_points.append(_ray.termin)
        self._set_rayList(start_points=PointArrays(pointList=start_points),
                          end_points=PointArrays(pointList=end_points))

    # def
# =============================================================================================== #
