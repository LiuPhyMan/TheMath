from math import floor, pi

import numpy as np
from scipy.integrate import cumtrapz

from ._ray import Ray as Ray_c
from ._vector import CartVector as Vec


class polarGrid(object):
  __slots__ = ['rNodePos', 'rPos', 'thetaPos', 'dS', 'nPointRing']

  def __init__(self, *, rNodePos, aspect):
    self.rNodePos = rNodePos
    self.rPos = []
    self.thetaPos = []
    self.dS = []
    self.nPointRing = []
    center = (self.rNodePos[:-1] + self.rNodePos[1:])/2
    center[0] = 0.
    dr = self.rNodePos[1:] - self.rNodePos[:-1]
    # Center point.
    self.rPos.append(0)
    self.thetaPos.append(0)
    self.dS.append(pi*self.rNodePos[1]**2)
    self.nPointRing.append(1)
    # Ring point.
    for i in range(1, self.rNodePos.size - 1):
      n = floor(2*pi*center[i]/dr[i]/aspect) + 1
      theta = [2*pi/n*_i for _i in range(n)]
      r = [center[i]]*n
      self.rPos += r
      self.thetaPos += theta
      self.dS += [pi*(self.rNodePos[i + 1]**2 - self.rNodePos[i]**2)/n]*n
      self.nPointRing.append(n)

  def plot(self, *, field, ax, vmin, vmax):
    x = self.thetaPos
    # height =

    # idx = list(accumulate(self.nPointRing))
    # for iRing in range(1, len(self.nPointRing)):
    #   r = np.linspace(self.rNodePos[iRing], self.rNodePos[iRing+1], num=2)
    #   theta = np.linspace(0, 2*pi, num=self.nPointRing[iRing]+1)
    #   r, theta = np.meshgrid(r, theta)
    #   x = r * np.cos(theta)
    #   y = r * np.sin(theta)
    #   Z = field[idx[iRing-1]:idx[iRing]]
    #   ax.pcolormesh(x, y, Z, shading='auto', vmin=vmin, vmax=vmax,
    #                 cmap='viridis')


def nonuniform_grid_from_data(nGrid, x_data, y_data):
  cumsum = cumtrapz(np.abs(np.gradient(y_data, x_data, edge_order=2)),
                    initial=0)
  if cumsum[-1]==0:
    return np.linspace(x_data[0], x_data[-1], num=nGrid)
  else:
    cumsum /= cumsum[-1]
    return np.interp(np.linspace(0, 1, nGrid), cumsum, x_data)


from ._CI_coeffs import ls_index, M_coeff_1, M_coeff_2, N_coeff_1, N_coeff_2, \
  integrate_by_DCT
