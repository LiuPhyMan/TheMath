# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 02.July.2023
"""
from math import pi, cos, factorial, log

import numpy as np


def integrate_by_DCT(f, N):
    a = []
    n = np.arange(1, int(N/2))
    tmp1 = [f(cos(n*pi/N)) + f(-cos(n*pi/N)) for n in range(1, int(N/2))]
    for k in range(int(N/2) + 1):
        temp = np.dot(tmp1, np.cos(n*pi/N*2*k)) + f(0)*(-1)**k + (f(-1) + f(1))/2
        a.append(temp*2/N)
    coef = [1] + [2/(1 - 4*k**2) for k in range(1, int(N/2))] + [1/(1 - N**2)]
    return np.dot(a, coef)


def Gauss2D(r, z, r_fwhm, z_fwhm, _min, _max):
    cst1 = 4*log(2)
    return _min + (_max - _min)*np.exp(-cst1*(r/r_fwhm)**2 - cst1*(z/z_fwhm)**2)


def ls_index(l, s):
    return factorial(s + 1)/2*(1 - (1 - (-1)**(l + 1))/2/(l + 1))


def M_coeff_1(p, q):
    match (p, q):
        case (0, 0):
            return [[80/3, (1, 1), (1, 1)],
                    [8, (0, 2), (2, 2)]]
        case (0, 1):
            return [[280/3, (1, 2), (1, 1)],
                    [-112/3, (1, 2), (1, 2)],
                    [28, (0, 3), (2, 2)],
                    [-8, (0, 3), (2, 3)]]
        case (1, 1):
            return [[560/3, (3, 1), (1, 1)],
                    [980/3, (1, 3), (1, 1)],
                    [-784/3, (1, 3), (1, 2)],
                    [128/3, (1, 3), (1, 3)],
                    [308/3, (2, 2), (2, 2)],
                    [294/3, (0, 4), (2, 2)],
                    [-56, (0, 4), (2, 3)],
                    [8, (0, 4), (2, 4)],
                    [16, (1, 3), (3, 3)]]
        case _:
            raise Exception("")


def M_coeff_2(p, q):
    if (p, q) == (0, 0):
        return [[-80/3, (1, 1), (1, 1)],
                [8, (1, 1), (2, 2)]]
    elif (p, q) == (0, 1):
        return [[-280/3, (2, 1), (1, 1)],
                [112/3, (2, 1), (1, 2)],
                [28, (2, 1), (2, 2)],
                [-8, (2, 1), (2, 3)]]
    elif (p, q) == (1, 1):
        return [[-1540/3, (2, 2), (1, 1)],
                [784/3, (2, 2), (1, 2)],
                [-128/3, (2, 2), (1, 3)],
                [602/3, (2, 2), (2, 2)],
                [-56, (2, 2), (2, 3)],
                [8, (2, 2), (2, 4)],
                [-16, (2, 2), (3, 3)]]
    else:
        raise Exception("")


# ------------------------------------------------------------------------------------------------ #
def N_coeff_1(p, q):
    match (p, q):
        case (0, 0):
            return [[8, (0, 1), (1, 1)]]
        case (0, 1):
            return [[20, (0, 2), (1, 1)],
                    [-8, (0, 2), (1, 2)]]
        case (0, 2):
            return [[35, (0, 3), (1, 1)],
                    [-28, (0, 3), (1, 2)],
                    [4, (0, 3), (1, 3)]]
        case (0, 3):
            return [[105/2, (0, 4), (1, 1)],
                    [-63, (0, 4), (1, 2)],
                    [18, (0, 4), (1, 3)],
                    [-4/3, (0, 4), (1, 4)]]
        case (0, 4):
            return [[1155/16, (0, 5), (1, 1)],
                    [-231/2, (0, 5), (1, 2)],
                    [99/2, (0, 5), (1, 3)],
                    [-22/3, (0, 5), (1, 4)],
                    [1/3, (0, 5), (1, 5)]]
        case (1, 1):
            return [[60, (2, 1), (1, 1)],
                    [50, (0, 3), (1, 1)],
                    [-40, (0, 3), (1, 2)],
                    [8, (0, 3), (1, 3)],
                    [16, (1, 2), (2, 2)]]
        case (1, 2):
            return [[210, (2, 2), (1, 1)],
                    [175/2, (0, 4), (1, 1)],
                    [-84, (2, 2), (1, 2)],
                    [-105, (0, 4), (1, 2)],
                    [38, (0, 4), (1, 3)],
                    [-4, (0, 4), (1, 4)],
                    [56, (1, 3), (2, 2)],
                    [-16, (1, 3), (2, 3)]]
        case (1, 3):
            return [[(2415/4, 18/23), (2, 3), (1, 1)],
                    [(2415/4, 5/23), (0, 5), (1, 1)],
                    [(-588, 9/14), (2, 3), (1, 2)],
                    [(-588, 5/14), (0, 5), (1, 2)],
                    [(162, 1/3), (2, 3), (1, 3)],
                    [(162, 2/3), (0, 5), (1, 3)],
                    [-64/3, (0, 5), (1, 4)],
                    [4/3, (0, 5), (1, 5)],
                    [126, (1, 4), (2, 2)],
                    [-72, (1, 4), (2, 3)],
                    [8, (1, 4), (2, 4)]]
        case (2, 2):
            return [[175, (4, 1), (1, 1)],
                    [735, (2, 3), (1, 1)],
                    [1225/8, (0, 5), (1, 1)],
                    [-588, (2, 3), (1, 2)],
                    [-245, (0, 5), (1, 2)],
                    [108, (2, 3), (1, 3)],
                    [133, (0, 5), (1, 3)],
                    [-28, (0, 5), (1, 4)],
                    [2, (0, 5), (1, 5)],
                    [112, (3, 2), (2, 2)],
                    [196, (1, 4), (2, 2)],
                    [-112, (1, 4), (2, 3)],
                    [16, (1, 4), (2, 4)],
                    [16, (2, 3), (3, 3)]]
        case (2, 3):
            return [[(42735/16, 120/407), (4, 2), (1, 1)],
                    [(42735/16, 252/407), (2, 4), (1, 1)],
                    [(42735/16, 35/407), (0, 6), (1, 1)],
                    [(-22071/8, 120/1051), (4, 2), (1, 2)],
                    [(-22071/8, 756/1051), (2, 4), (1, 2)],
                    [(-22071/8, 175/1051), (0, 6), (1, 2)],
                    [(2001/2, 450/667), (2, 4), (1, 3)],
                    [(2001/2, 217/667), (0, 6), (1, 3)],
                    [(-499/3, 198/499), (2, 4), (1, 4)],
                    [(-499/3, 301/499), (0, 6), (1, 4)],
                    [41/3, (0, 6), (1, 5)],
                    [-2/3, (0, 6), (1, 6)],
                    [(945, 8/15), (3, 3), (2, 2)],
                    [(945, 7/15), (1, 5), (2, 2)],
                    [(-522, 8/29), (3, 3), (2, 3)],
                    [(-522, 21/29), (1, 5), (2, 3)],
                    [100, (1, 5), (2, 4)],
                    [-8, (1, 5), (2, 5)],
                    [72, (2, 4), (3, 3)],
                    [-16, (2, 4), (3, 4)]]
        case (3, 3):
            return [[(105/32, 112), (6, 1), (1, 1)],
                    [(105/32, 1080), (4, 3), (1, 1)],
                    [(105/32, 1134), (2, 5), (1, 1)],
                    [(105/32, 105), (0, 7), (1, 1)],
                    [(-189/8, 120), (4, 3), (1, 2)],
                    [(-189/8, 252), (2, 5), (1, 2)],
                    [(-189/8, 35), (0, 7), (1, 2)],
                    [(9/8, 440), (4, 3), (1, 3)],
                    [(9/8, 2700), (2, 5), (1, 3)],
                    [(9/8, 651), (0, 7), (1, 3)],
                    [-594, (2, 5), (1, 4)],
                    [-301, (0, 7), (1, 4)],
                    [(3/2, 26), (2, 5), (1, 5)],
                    [(3/2, 41), (0, 7), (1, 5)],
                    [-6, (0, 7), (1, 6)],
                    [2/9, (0, 7), (1, 7)],
                    [(189/4, 8), (5, 2), (2, 2)],
                    [(189/4, 48), (3, 4), (2, 2)],
                    [(189/4, 21), (1, 6), (2, 2)],
                    [(-162, 8), (3, 4), (2, 3)],
                    [(-162, 7), (1, 6), (2, 3)],
                    [176, (3, 4), (2, 4)],
                    [450, (1, 6), (2, 4)],
                    [-72, (1, 6), (2, 5)],
                    [4, (1, 6), (2, 6)],
                    [120, (4, 3), (3, 3)],
                    [324, (2, 5), (3, 3)],
                    [-144, (2, 5), (3, 4)],
                    [16, (2, 5), (3, 5)],
                    [32/3, (3, 4), (4, 4)]]


def N_coeff_2(p, q):
    match (p, q):
        case (0, 0):
            return [[-8, (0.5, 0.5), (1, 1)]]
        case (0, 1):
            return [[-20, (1.5, 0.5), (1, 1)],
                    [8, (1.5, 0.5), (1, 2)]]
        case (0, 2):
            return [[-35, (2.5, 0.5), (1, 1)],
                    [28, (2.5, 0.5), (1, 2)],
                    [-4, (2.5, 0.5), (1, 3)]]
        case (0, 3):
            return [[-105/2, (3.5, 0.5), (1, 1)],
                    [63, (3.5, 0.5), (1, 2)],
                    [-18, (3.5, 0.5), (1, 3)],
                    [4/3, (3.5, 0.5), (1, 4)],
                    ]
        case (1, 1):
            return [[-110, (1.5, 1.5), (1, 1)],
                    [40, (1.5, 1.5), (1, 2)],
                    [-8, (1.5, 1.5), (1, 3)],
                    [16, (1.5, 1.5), (2, 2)]]
        case (1, 2):
            return [[-595/2, (2.5, 1.5), (1, 1)],
                    [189, (2.5, 1.5), (1, 2)],
                    [-38, (2.5, 1.5), (1, 3)],
                    [4, (2.5, 1.5), (1, 4)],
                    [56, (2.5, 1.5), (2, 2)],
                    [-16, (2.5, 1.5), (2, 3)]]
        case (1, 3):
            return [[-2415/4, (3.5, 1.5), (1, 1)],
                    [588, (3.5, 1.5), (1, 2)],
                    [-162, (3.5, 1.5), (1, 3)],
                    [64/3, (3.5, 1.5), (1, 4)],
                    [-4/3, (3.5, 1.5), (1, 5)],
                    [126, (3.5, 1.5), (2, 2)],
                    [-72, (3.5, 1.5), (2, 3)],
                    [8, (3.5, 1.5), (2, 4)]]
        case (2, 2):
            return [[-8505/8, (2.5, 2.5), (1, 1)],
                    [833, (2.5, 2.5), (1, 2)],
                    [-241, (2.5, 2.5), (1, 3)],
                    [28, (2.5, 2.5), (1, 4)],
                    [-2, (2.5, 2.5), (1, 5)],
                    [308, (2.5, 2.5), (2, 2)],
                    [-112, (2.5, 2.5), (2, 3)],
                    [16, (2.5, 2.5), (2, 4)],
                    [-16, (2.5, 2.5), (3, 3)]]
        case (2, 3):
            return [[-42735/16, (3.5, 2.5), (1, 1)],
                    [22071/8, (3.5, 2.5), (1, 2)],
                    [-2001/2, (3.5, 2.5), (1, 3)],
                    [499/3, (3.5, 2.5), (1, 4)],
                    [-41/3, (3.5, 2.5), (1, 5)],
                    [2/3, (3.5, 2.5), (1, 6)],
                    [945, (3.5, 2.5), (2, 2)],
                    [-522, (3.5, 2.5), (2, 3)],
                    [100, (3.5, 2.5), (2, 4)],
                    [-8, (3.5, 2.5), (2, 5)],
                    [-72, (3.5, 2.5), (3, 3)],
                    [16, (3.5, 2.5), (3, 4)]]
        case (3, 3):
            return [[-255255/32, (3.5, 3.5), (1, 1)],
                    [76923/8, (3.5, 3.5), (1, 2)],
                    [-34119/8, (3.5, 3.5), (1, 3)],
                    [895, (3.5, 3.5), (1, 4)],
                    [-201/2, (3.5, 3.5), (1, 5)],
                    [6, (3.5, 3.5), (1, 6)],
                    [-2/9, (3.5, 3.5), (1, 7)],
                    [14553/4, (3.5, 3.5), (2, 2)],
                    [-2430, (3.5, 3.5), (2, 3)],
                    [626, (3.5, 3.5), (2, 4)],
                    [-72, (3.5, 3.5), (2, 5)],
                    [4, (3.5, 3.5), (2, 6)],
                    [-444, (3.5, 3.5), (3, 3)],
                    [144, (3.5, 3.5), (3, 4)],
                    [-16, (3.5, 3.5), (3, 5)],
                    [32/3, (3.5, 3.5), (4, 4)]]


def coeff3(p, q):
    match p, q:
        case 0, 0:
            return [[8, (0, 1), (1, 1)]]
        case 0, 1:
            return [[20, (0, 2), (1, 1)],
                    [-8, 0, 2, 1, 2]]
        case 0, 2:
            return [[35, 0, 3, 1, 1],
                    [-8, 0, 2, 1, 2]]
        case 0, 3:
            return [[105/2, 0, 4, 1, 1],
                    [-63, 0, 4, 1, 2],
                    [18, 0, 4, 1, 3],
                    [-4/3, 0, 4, 1, 4]]
        case 0, 4:
            return [[1155/16, 0, 5, 1, 1],
                    [-231/2, 0, 5, 1, 2],
                    [99/2, 0, 5, 1, 3],
                    [-22/3, 0, 5, 1, 4],
                    [1/3, 0, 5, 1, 5]]
        case 0, 5:
            return [[3003/32, 0, 6, 1, 1],
                    [-3003/16, 0, 6, 1, 2],
                    [429/4, 0, 6, 1, 3],
                    [-143/6, 0, 6, 1, 4],
                    [13/6, 0, 6, 1, 5],
                    [-1/15, 0, 6, 1, 6]]
        case 1, 1:
            return [[60, 2, 1, 1, 1],
                    [50, 0, 3, 1, 1],
                    [-40, 0, 3, 1, 2],
                    [8, 0, 3, 1, 3],
                    [16, 1, 2, 2, 2]]
        case 1, 2:
            return [[210, 2, 2, 1, 1],
                    [175/2, 0, 4, 1, 1],
                    [-84, 2, 2, 1, 2],
                    [-105, 0, 4, 1, 2],
                    [38, 0, 4, 1, 3],
                    [-4, 0, 4, 1, 4],
                    [56, 1, 3, 2, 2],
                    [-16, 1, 3, 2, 3]]
