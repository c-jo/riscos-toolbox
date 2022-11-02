"""RISC OS Toolbox - Types"""

import ctypes

class Point(ctypes.Structure):
    _fields_ = [ ("x", ctypes.c_int), ("y", ctypes.c_int) ]

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

class BBox(ctypes.Structure):
    _fields_ = [ ("min", Point ), ("max", Point) ]

    def __init__(self, min_x, min_y, max_x, max_y):
        self.min.x = min_x
        self.min.y = min_y
        self.max.x = max_x
        self.max.y = max_y

    def __repr__(self):
        return "[{},{} - {},{}]". \
            format(self.min.x, self.min.y, self.max.x, self.max.y)

    def zero():
        return BBox(0,0,0,0)
