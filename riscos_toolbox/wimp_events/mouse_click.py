from ..events import Event
from .. import Wimp, Point

import ctypes

class MouseClick(Event, ctypes.Structure):
    event_id = Wimp.MouseClick

    _fields_ = [
        ("mouse", Point),
        ("buttons", ctypes.c_uint32),
        ("window_handle", ctypes.c_int32),
        ("icon_handle", ctypes.c_int32) ]

