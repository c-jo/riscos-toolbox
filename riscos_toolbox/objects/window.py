"""RISC OS Toolbox - Window"""

from ..base import Object, get_object
from ..events import wimp_handler
from .. import Wimp, BBox, Point
from ..wimp_events.redraw_window import RedrawWindow
import swi
import ctypes

class Window(Object):
    class_id = 0x82880
    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1

    NoFocus = -1
    InvisibleCaret = -2

    class Toolbars:
        def __init__(self, window):
            self.window = window

        @property
        def internal_bottom_left(self):
            return get_object(
                swi.swi("Toolbox_ObjectMiscOp", "III;I",
                        1<<0, self.window.id, 19))

        @internal_bottom_left.setter
        def internal_top_left(self, window):
            swi.swi("Toolbox_ObjectMiscOp", "IIII;I",
                    1<<0, self.window.id, 18, window.id)

    def __init__(self, *args):
        super().__init__(*args)
        self.gadgets = self.components
        self.toolbars = Window.Toolbars(self)

    @property
    def wimp_handle(self):
        return self._miscop_get_unsigned(0)

    @property
    def help_message(self):
        return self._miscop_get_string(8)

    @help_message.setter
    def help_message(self, message):
        self._miscop_set_string(7, message)

    @property
    def title(self):
        return self._miscop_get_string(12)

    @title.setter
    def title(self, title):
        self._miscop_set_string(11, title)

    @property
    def default_focus(self):
        return self._miscop_get_signed(13)

    @default_focus.setter
    def default_focus(self, focus):
        self._miscop_set_signed(12, focus)

    @property
    def extent(self):
        extent = BBox.zero()
        swi.swi('Toolbox_ObjectMiscOp', 'IIII',
                0, self.id, 16, ctypes.addressof(extent))
        return extent

    @extent.setter
    def extent(self, extent):
        swi.swi('Toolbox_ObjectMiscOp', 'IIII',
                0, self.id, 15, ctypes.addressof(extent))

    def force_redraw(self, bbox=None):
        if bbox is None:
            bbox = self.extent
        swi.swi('Toolbox_ObjectMiscOp','IIII',
                0, self.id, 17, ctypes.addressof(bbox))

class UserRedrawMixin:
    @wimp_handler(RedrawWindow)
    def redraw(self, reason, id_block, event):

        class RedrawData(ctypes.Structure):
            _fields_ = [ ("handle", ctypes.c_int32),
                  ("visible", BBox), ("scroll", Point), ("redraw", BBox) ]

        rd = RedrawData()
        rd.handle = event.window_handle
        more = swi.swi("Wimp_RedrawWindow", ".I;I", ctypes.addressof(rd))
        while more:
            offset = Point( rd.visible.min.x - rd.scroll.x,
                            rd.visible.max.y - rd.scroll.y )

            self.on_redraw( rd.visible, rd.scroll, rd.redraw, offset )

            more = swi.swi("Wimp_RedrawWindow", ".I;I", ctypes.addressof(rd))

    def on_redraw(self, visible, scroll, redraw, offset):
        pass
