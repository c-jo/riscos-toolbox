from ..events import Event
from .. import Wimp

import ctypes

class RedrawWindow(Event, ctypes.Structure):
    event_id = Wimp.RedrawWindow

    _fields_ = [
        ("window_handle", ctypes.c_uint32) ]
