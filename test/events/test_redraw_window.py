import riscos_toolbox.wimp_events.redraw_window as redraw_window

import unittest
import struct

class RedrawWindow(unittest.TestCase):

    def test_from_init(self):
        rw = redraw_window.RedrawWindow()
        assert(rw.event_id == 1)

    def test_from_block(self):
        rw = redraw_window.RedrawWindow.from_poll_block(
            struct.pack("i",42)
        )
        assert(rw.event_id == 1)
        assert(rw.window_handle == 42)
