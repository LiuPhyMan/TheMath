from math import floor, pi
import numpy as np

from scipy.integrate import cumtrapz

from ._ray import Ray as Ray_c
from ._vector import CartVector as Vec


class polarGrid(object):
  __slots__ = ['rPos', 'thetaPos', 'dS']

  def __init__(self, *, rNodePos, aspect):
    self.rPos = []
    self.thetaPos = []
    self.dS = []
    center = (rNodePos[:-1] + rNodePos[1:])/2
    center[0] = 0.
    dr = rNodePos[1:] - rNodePos[:-1]
    # Center point.
    self.rPos.append(0)
    self.thetaPos.append(0)
    self.dS.append(pi*rNodePos[1]**2)
    # Ring point.
    for i in range(1, rNodePos.size - 1):
      n = floor(2*pi*center[i]/dr[i]/aspect) + 1
      theta = [2*pi/n*_i for _i in range(n)]
      r = [center[i]]*n
      self.rPos += r
      self.thetaPos += theta
      self.dS += [pi*(rNodePos[i + 1]**2 - rNodePos[i]**2)/n]*n

  def plot(self, field):
    pass


def nonuniform_grid_from_data(nGrid, x_data, y_data):
  cumsum = cumtrapz(np.abs(np.gradient(y_data, x_data, edge_order=2)),
                    initial=0)
  cumsum /= cumsum[-1]
  return np.interp(np.linspace(0, 1, nGrid), cumsum, x_data)
