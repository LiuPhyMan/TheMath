import numpy as np
from .volume import AbsVol
from .pointArray import PointArrays


class Ray(object):

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

    def discrete(self, *, nGrid: int):
        self.nGrid = nGrid
        self.nNode = self.nGrid + 1
        self.nodes = PointArrays(pointList=[self.origin*(1 - _n/nGrid) + self.termin*(_n/nGrid)
                                            for _n in range(nGrid + 1)])
        self.centrs = PointArrays(pointList=[self.origin*(1 - 3*_n/2/nGrid) +
                                             self.termin*(3*_n/2/nGrid) for _n in range(nGrid)])

    # ------------------------------------------------------------------------------------------- #
    def topo_vol(self, *, vol: AbsVol, ds_err: float):
        r"""
        return "in", "out", "in-out", "out-in", "out-in-out"
        """
        n = int(self.length/ds_err) + 1
        self.discrete(nGrid=n)
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
        self.discrete(nGrid=n)
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


# =============================================================================================== #
class RayArrays(object):

    def __init__(self, *, start_points: PointArrays, end_points: PointArrays):
        assert start_points.nPoints == end_points.nPoints
        self.nRays = start_points.nPoints
        self.rayList = []
        for _i in range(self.nRays):
            self.rayList.append(Ray(origin=start_points.pointList[_i],
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
        self.__init__(start_points=PointArrays(pointList=start_points),
                      end_points=PointArrays(pointList=end_points))
