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
