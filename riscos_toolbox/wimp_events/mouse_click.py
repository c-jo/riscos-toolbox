from ..events import EventData
from .. import Wimp, Point

import ctypes

class MouseClick(EventData, ctypes.Structure):
    event_id = Wimp.MouseClick

    _fields_ = [ ("mouse", Point), ("buttons", ctypes.c_uint32), ("window_handle", ctypes.c_int32), ("icon_handle", ctypes.c_int32) ]

    def __init__(self):
        super().__init__()