from ..events import EventData
from .. import Wimp

import struct

class RedrawWindow(EventData):
    event_id = Wimp.RedrawWindow

    def __init__(self, window_handle):
        self.window_handle = window_handle

    @staticmethod
    def from_block(data):
        return RedrawWindow(*struct.unpack("i", data[0:4]))
