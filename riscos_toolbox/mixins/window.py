from ..events import wimp_handler
from ..wimp_events.redraw_window import RedrawWindow
from .. import BBox, Point

import ctypes
import swi

class UserRedrawMixin:
    @wimp_handler(RedrawWindow)
    def _redraw(self, reason, id_block, event):

        class RedrawData(ctypes.Structure):
            _fields_ = [
                ("handle", ctypes.c_int32),
                ("visible", BBox),
                ("scroll", Point),
                ("redraw", BBox) ]

        rd = RedrawData()
        rd.handle = event.window_handle
        more = swi.swi("Wimp_RedrawWindow", ".I;I", ctypes.addressof(rd))
        while more:
            offset = Point( rd.visible.min.x - rd.scroll.x,
                            rd.visible.max.y - rd.scroll.y )

            self.redraw_window( rd.visible, rd.scroll, rd.redraw, offset )

            more = swi.swi("Wimp_RedrawWindow", ".I;I", ctypes.addressof(rd))

    def redraw_window(self, visible, scroll, redraw, offset):
        pass
