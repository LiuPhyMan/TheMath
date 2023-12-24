# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 06.July.2023
"""
from math import cos, sin, sqrt, log, pi

from scipy.special import wofz

from .plane import Plane
from .pointArray import PointArrays
from .ray import AbsRay, MultiRays
from .vector import CartVector


def dot_product(vec0: CartVector, vec1: CartVector) -> float:
    return vec0.x*vec1.x + vec0.y*vec1.y + vec0.z*vec1.z


def ray_plane_intersection(*, _r: AbsRay, _p: Plane) -> CartVector:
    r"""
    Parameters
    ----------
    _l: line
    _p: plane
    """
    d = dot_product(_p.origin - _r.origin, _p.direct)/ \
        dot_product(_r.unit_direct, _p.direct)
    assert d >= 0, d
    return _r.origin + _r.unit_direct*d


def cos_angle_vect(vec0: CartVector, vec1: CartVector):
    return dot_product(vec0.unit_vector(), vec1.unit_vector())


def vectorRotate(vec: CartVector, byAxis: str, angle: float) -> CartVector:
    r"""

    Parameters
    ----------
    byAxis: 'x', 'y' or 'z'.
    angle: right-hand rule rotate.

    Returns
    -------
    A new CartVector.

    """
    match byAxis:
        case "x":
            return CartVector(xyz=(vec.x, cos(angle)*vec.y - sin(angle)*vec.z,
                                   sin(angle)*vec.y + cos(angle)*vec.z))
        case _:
            raise Exception("")


def pointArraysRotate(pntArry: PointArrays, byAxis: str, angle: float) -> PointArrays:
    new_point_list = []
    for _p in pntArry.pointList:
        new_point_list.append(vectorRotate(_p, byAxis, angle))
    return PointArrays(pointList=new_point_list)


def multiRaysRotate(multi_rays: MultiRays, byAxis: str, angle: float) -> MultiRays:
    return MultiRays(start_points=pointArraysRotate(multi_rays.startPoints, byAxis, angle),
                     end_points=pointArraysRotate(multi_rays.endPoints, byAxis, angle))


def voigt(dx, *, fwhm_G, fwhm_L):
    sigma = fwhm_G/sqrt(2*log(2))/2
    gamma = fwhm_L/2
    if (sigma/gamma) < 1e-6:
        return gamma/pi/(dx**2 + gamma**2)
    z = (dx + 1j*gamma)/sigma/sqrt(2)
    return wofz(z).real/sigma/sqrt(2*pi)
