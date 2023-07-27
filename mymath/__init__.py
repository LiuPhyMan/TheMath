# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 20.July.2023
"""
from math import pi, cos, factorial
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


def ls_index(l, s):
    return factorial(s + 1)/2*(1 - (1 - (-1)**(l + 1))/2/(l + 1))


def coeff1(p, q):
    if (p, q) == (0, 0):
        return [[80/3, (1, 1), (1, 1)],
                [8, (0, 2), (2, 2)]]
    elif (p, q) == (0, 1):
        return [[280/3, (1, 2), (1, 1)],
                [-112/3, (1, 2), (1, 2)],
                [28, (0, 3), (2, 2)],
                [-8, (0, 3), (2, 3)]]
    elif (p, q) == (1, 1):
        return [[560/3, (3, 1), (1, 1)],
                [980/3, (1, 3), (1, 1)],
                [-784/3, (1, 3), (1, 2)],
                [128/3, (1, 3), (1, 3)],
                [308/3, (2, 2), (2, 2)],
                [294/3, (0, 4), (2, 2)],
                [-56, (0, 4), (2, 3)],
                [8, (0, 4), (2, 4)],
                [16, (1, 3), (3, 3)]]
    else:
        raise Exception("")


def coeff2(p, q):
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
