"""RISC OS Toolbox - Window"""

from ..base import Object
from ..types import BBox, Point
from ..events import WimpEvent
from .. import Wimp

import swi
import ctypes

class Window(Object):
    class_id = 0x82880
    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1

    NoFocus = -1
    InvisibleCaret = -2

    def __init__(self, id):
        super().__init__(id)
        self.gadgets = self.components
        self._wimp_handle = None

    @property
    def wimp_handle(self):
        if self._wimp_handle is None:
            self._wimp_handle = self._miscop_get_unsigned(0)
        return self._wimp_handle

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
    @WimpEvent(Wimp.RedrawWindow)
    def redraw(self, reason, id_block, poll_block):
        block = poll_block

        more = swi.swi("Wimp_RedrawWindow", ".b;I", poll_block)
        while more:
            visible = BBox ( block.tosigned(1), block.tosigned(2),
                             block.tosigned(3), block.tosigned(4) )
            scroll =  Point( block.tosigned(5), block.tosigned(6) )
            redraw =  BBox ( block.tosigned(7), block.tosigned(8),
                             block.tosigned(9), block.tosigned(10) )

            offset = Point( visible.min.x - scroll.x,
                            visible.max.y - scroll.y )

            self.on_redraw( visible, scroll, redraw, offset )

            more = swi.swi("Wimp_GetRectangle", ".b;I", poll_block)

    def on_redraw(self, visible, scroll, redraw, offset):
        pass

