"""RISC OS Toolbox - Window"""

from ..base import Object, get_object
from ..events import ToolboxEvent
from ..gadgets import Gadget

from .. import BBox

import swi
import ctypes

class Window(Object):
    class_id = 0x82880
    # Events
    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1
    # Constants
    NoFocus = -1
    InvisibleCaret = -2

    InternalBottomLeftToolbar = 1<<0
    InternaTopLeftToolbar = 1<<1
    ExternalBottomLeftToolbar = 1<<2
    ExternalTopLeftToolbar = 1<<3

    def get_toolbar_id(self, tool_bar):
        return swi.swi("Toolbox_ObjectMiscOp", "IiI;i",
                       tool_bar, self.id, 19)

    def set_toolbar_id(self, tool_bar, window_id):
        swi.swi("Toolbox_ObjectMiscOp", "IiIi",
                tool_bar, self.id, 18, window_id)

    @property
    def wimp_handle(self):
        return self._miscop_get_unsigned(0)

    def add_gadget(self, gadget):
        gadget_id = swi.swi("Toolbox_ObjectMiscOp","IiIi;I",
                     0, self.id, 1, ctypes.addressof(gadget))
        self.components[gadget_id] = \
            Gadget.create(gadget.type, self, gadget_id)

    def remove_gadget(self, gadget):
        swi.swi("Toolbox_ObjectMiscOp","IiIi",
                0, self.id, 2, gadget.id)
        del(self.components[gadget.id])

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

class AboutToBeShownEvent(ToolboxEvent):
    event_id = Window.AboutToBeShown
