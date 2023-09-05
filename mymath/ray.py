from math import exp

import numpy as np
from matplotlib import pyplot as plt

from .pointArray import PointArrays
from .volume import AbsVol


class AbsRay(object):
    __slots__ = ["origin", "termin", "unit_direct", "length",
                 "nGrid", "nNode",
                 "nodes", "centrs",
                 "nodes_lgth", "centr_lgth",
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

    def uniform_discrete(self, *, nGrid: int=None, def_ds: float=None) -> None:
        if (def_ds is not None) and (nGrid is None):
            self.nGrid = int(self.length / def_ds) + 1
        elif (def_ds is None) and (nGrid is not None):
            self.nGrid = nGrid
        else:
            raise Exception("")
        assert self.nGrid > 1
        self.nNode = self.nGrid + 1
        self.nodes = PointArrays(pointList=[self.origin*(1 - _n/self.nGrid) + self.termin*(_n/self.nGrid)
                                            for _n in range(self.nGrid + 1)])
        self.centrs = PointArrays(pointList=[self.origin*(1 - (2*_i + 1)/2/self.nGrid) +
                                             self.termin*((2*_i + 1)/2/self.nGrid)
                                             for _i in range(self.nGrid)])
        # uniform discrete
        self.ds = np.array([(self.nodes.pointList[i + 1] - self.nodes.pointList[i]).length
                            for i in range(self.nGrid)])
        self.nodes_lgth = np.linspace(0, self.length, num=self.nNode)
        self.centr_lgth = np.array([self.nodes_lgth[i] + self.ds[i]/2 for i in range(self.nGrid)])

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
                end_index = _i - 1
                break
            continue
        self.__init__(origin=self.nodes.pointList[start_index],
                      termin=self.nodes.pointList[end_index])

    def __repr__(self):
        return f"Origin: {self.origin.__repr__()}\tTermin: {self.termin.__repr__()}"


class LightRay(AbsRay):
    __slots__ = ["I", "j", "k", "area"]

    def __init__(self, *, origin, termin=None, direct=None):
        super().__init__(origin=origin, termin=termin, direct=direct)
        self.area = 1

    def set_area(self, area: float) -> None:
        self.area = area

    def init_I(self):
        self.I = np.zeros(self.nNode)
        self.j = np.zeros(self.nGrid)
        self.k = np.zeros(self.nGrid)

    @property
    def Iend(self):
        return self.I[-1]

    @property
    def Pend(self):
        return self.Iend * self.area

    @property
    def tau(self):
        r""" optical depth. unit of 1.
        Maybe:
        >1, optical thick
        <1, optical thin"""
        return np.dot(self.k, self.ds)

    def set_emission(self, emission):
        assert emission.size == self.nGrid
        self.j = emission

    def set_uniform_emission(self, emiss: float) -> None:
        assert emiss >= 0
        self.j = np.ones(self.nGrid)*emiss

    def set_absorption(self, absorb):
        assert absorb.size == self.nGrid
        self.k = absorb

    def set_uniform_absorption(self, absorb: float) -> None:
        assert absorb >= 0
        self.k = np.ones(self.nGrid)*absorb

    def solve_I(self):
        self.I[0] = 0
        for iNode in range(self.nNode - 1):
            dtao = self.k[iNode]*self.ds[iNode]
            if dtao < 1e-2:
                tmp = 1 - 0.5*dtao + dtao**2/6 - dtao**3/24 + dtao**4/120
            else:
                tmp = (1-exp(-dtao))/dtao
            assert tmp > 0, (self.k[iNode], self.ds[iNode], tmp)
            self.I[iNode + 1] = self.I[iNode]*exp(-dtao) + self.j[iNode]*tmp*self.ds[iNode]

    def plot(self):
        f = plt.figure()
        ax = f.add_subplot()
        ax.plot(self.nodes_lgth, self.I)


# =============================================================================================== #
class MultiRays(object):
    __slots__ = ["nRays", "rayList", "startPoints", "endPoints"]

    def __init__(self, *, start_points: PointArrays, end_points: PointArrays) -> None:
        assert start_points.nPoints == end_points.nPoints
        self.startPoints = start_points
        self.endPoints = end_points
        self._set_rayList(start_points=start_points, end_points=end_points)

    def __getitem__(self, item):
        return self.rayList[item]

    def _set_rayList(self, *, start_points, end_points):
        assert start_points.nPoints == end_points.nPoints
        self.nRays = start_points.nPoints
        self.rayList = []
        for _i in range(self.nRays):
            self.rayList.append(LightRay(origin=start_points.pointList[_i],
                                         termin=end_points.pointList[_i]))

    def cut_in_vol(self, *, vol: AbsVol, ds_err: float) -> None:
        start_points = []
        end_points = []
        for _ray in self.rayList:
            if _ray.topo_vol(vol=vol, ds_err=ds_err) == "out":
                continue
            else:
                _ray.cut_in_vol(vol=vol, ds_err=ds_err)
                if _ray.length <= ds_err:
                    continue
                else:
                    start_points.append(_ray.origin)
                    end_points.append(_ray.termin)
        self._set_rayList(start_points=PointArrays(pointList=start_points),
                          end_points=PointArrays(pointList=end_points))

    # def
# =============================================================================================== #
