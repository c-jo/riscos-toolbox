"""RISC OS Toolbox - Types"""

import ctypes

ObjectID = ctypes.c_int32
ComponentID = ctypes.c_int32

class IDBlock(ctypes.Structure):
    class Level(ctypes.Structure):
        _fields_ = [ ("id", ObjectID), ("component", ComponentID) ]

        def __init__(self):
            self.id = -1
            self.component = 0

        def __repr__(self):
            return "{:x}/{}".format(self.id, self.component)

    _fields_ = [ ("ancestor", Level),
                 ("parent",   Level),
                 ("self",     Level) ]

    def __init__(self):
        pass

    def __repr__(self):
        return "Acestor: {} Parent: {} Self: {}".format(self.ancestor, self.parent, self.self)

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
