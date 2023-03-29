from ..events import EventData
import ctypes

class ToolboxEventData(EventData, ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_uint32),
        ("reference_number", ctypes.c_int32),
        ("event_code", ctypes.c_uint32),
        ("flags", ctypes.c_uint32) ]


    def __init__(self):
        super().__init__()