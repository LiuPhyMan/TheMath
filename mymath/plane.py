# -*- coding: utf-8 -*-
"""
@author: Liu.Jinbao
@contact: liu.jinbao@outlook.com
@time: 06.July.2023
"""
from .vector import CartVector
from .vector import default_vectors


class Plane(object):

    def __init__(self, *, origin: CartVector | str, direct: CartVector | str):
        r"""
        Input a vector or string of 'orig', 'xPos', 'xNeg', 'yPos', 'yNeg', 'zPos' or 'zNeg'.
        """
        if isinstance(origin, str):
            self.origin = default_vectors[origin]
        else:
            self.origin = origin
        if isinstance(direct, str):
            self.direct = default_vectors[direct]
        else:
            self.direct = direct
