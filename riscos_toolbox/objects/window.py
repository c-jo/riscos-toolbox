"""RISC OS Toolbox - Window"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
from ..gadgets import Gadget
from .. import Point, BBox

import swi
import ctypes


class Window(Object):
    class_id = 0x82880
    # Events
    AboutToBeShown = class_id + 0
    HasBeenHidden = class_id + 16
    # Constants
    NoFocus = -1
    InvisibleCaret = -2

    InternalBottomLeftToolbar = 1 << 0
    InternalTopLeftToolbar = 1 << 1
    ExternalBottomLeftToolbar = 1 << 2
    ExternalTopLeftToolbar = 1 << 3

    def get_toolbar_id(self, tool_bar):
        return swi.swi('Toolbox_ObjectMiscOp', 'III;I',
                       tool_bar, self.id, 19)

    def set_toolbar_id(self, tool_bar, window_id):
        swi.swi('Toolbox_ObjectMiscOp', 'IIII',
                tool_bar, self.id, 18, window_id)

    @property
    def wimp_handle(self):
        return self._miscop_get_unsigned(0)

    def add_gadget(self, gadget):
        gadget_id = swi.swi("Toolbox_ObjectMiscOp", "IIII;I",
                            0, self.id, 1, ctypes.addressof(gadget))
        self.components[gadget_id] = \
            Gadget.create(gadget.type, self, gadget_id)

    def remove_gadget(self, gadget):
        swi.swi("Toolbox_ObjectMiscOp", "IIII",
                0, self.id, 2, gadget.id)
        del self.components[gadget.id]

    @property
    def menu_id(self):
        return self._miscop_get_unsigned(4)

    @menu_id.setter
    def menu_id(self, menu_id):
        self._miscop_set_unsigned(3, menu_id)

    @property
    def pointer(self):
        swi.swi('Toolbox_ObjectMiscOp', 'IIII;....I', 0, self.id, 4)

        buf_size = swi.swi('Toolbox_ObjectMiscOp', 'III00;....I',
                           0, self.id, 4)
        buf = swi.block((buf_size + 3) // 4)
        hot_spot = Point(
            swi.swi('Toolbox_ObjectMiscOp', 'IIIbI;.....ii', 0, self.id, 4,
                    buf, buf_size))
        return (buf.nullstring(), hot_spot)

    @pointer.setter
    def pointer(self, pointer):
        (sprite_name, hot_spot) = pointer
        swi.swi('Toolbox_ObjectMiscOp', 'IIIIsii', 0, self.id, 5,
                sprite_name, hot_spot.x, hot_spot.y)

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
        swi.swi('Toolbox_ObjectMiscOp', 'IIII',
                0, self.id, 17, ctypes.addressof(bbox))

# Window Events


class WindowAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = Window.AboutToBeShown


class WindowHasBeenHidden(ToolboxEvent):
    event_id = Window.HasBeenHidden
