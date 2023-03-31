import riscos_toolbox.wimp_events.redraw_window as redraw_window

import unittest
import struct

class RedrawWindow(unittest.TestCase):

    def test_from_init(self):
        rw = redraw_window.RedrawWindow(123)
        assert(rw.event_id == 1)
        assert(rw.window_handle == 123)

    def test_from_block(self):
        block = struct.pack("i",42)
        rw = redraw_window.RedrawWindow.from_block(block)
        assert(rw.event_id == 1)
        assert(rw.window_handle == 42)
