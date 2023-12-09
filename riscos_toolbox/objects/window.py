"""RISC OS Toolbox - Window"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
from ..gadgets import Gadget
from .. import Point, BBox

import swi
import ctypes


class Window(Object):
    class_id = 0x82880
    # Methods
    GetWimpHandle = 0
    AddGadget = 1
    RemoveGadget = 2
    SetMenu = 3
    GetMenu = 4
    SetPointer = 5
    GetPointer = 6
    SetHelpMessage = 7
    GetHelpMessage = 8
    AddKeyboardShortcuts = 9
    RemoveKeyboardShortcuts = 10
    SetTitle = 11
    GetTitle = 12
    SetDefaultFocus = 13
    GetDefaultFocus = 14
    SetExtent = 15
    GetExtent = 16
    ForceRedraw = 17
    SetToolBars = 18
    GetToolBars = 19
    # Events
    AboutToBeShown = class_id + 0
    HasBeenHidden = class_id + 16
    # Constants
    NoFocus = -1
    InvisibleCaret = -2
    GenerateAboutToBeShown = 0x00000001
    AutoOpen = 0x00000002
    AutoClose = 0x00000004
    GenerateHasBeenHidden = 0x00000008
    IsToolBar = 0x00000010

    InternalBottomLeftToolbar = 1 << 0
    InternalTopLeftToolbar = 1 << 1
    ExternalBottomLeftToolbar = 1 << 2
    ExternalTopLeftToolbar = 1 << 3

    @property
    def wimp_handle(self):
        return self._miscop_get_signed(Window.GetWimpHandle)

    def add_gadget(self, gadget):
        gadget_id = swi.swi("Toolbox_ObjectMiscOp", "IiII;I",
                            0, self.id, Window.AddGadget, ctypes.addressof(gadget))
        self.components[gadget_id] = \
            Gadget.create(gadget.type, self, gadget_id)

    def remove_gadget(self, gadget):
        swi.swi("Toolbox_ObjectMiscOp", "IiIi",
                0, self.id, Window.RemoveGadget, gadget.id)
        del self.components[gadget.id]

    @property
    def menu_id(self):
        return self._miscop_get_signed(Window.GetMenu)

    @menu_id.setter
    def menu_id(self, menu_id):
        self._miscop_set_signed(Window.SetMenu, menu_id)

    def get_pointer(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', 'IiI00;....i',
                           0, self.id, Window.GetPointer)
        buf = swi.block((buf_size + 3) // 4)
        hot_spot = Point(
            *swi.swi('Toolbox_ObjectMiscOp', 'IiIbi;.....ii',
                    0, self.id, Window.GetPointer, buf, buf_size))
        return (buf.nullstring(), hot_spot)

    def set_pointer(self, sprite_name, hot_spot):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIsii',
                0, self.id, Window.SetPointer,
                sprite_name, hot_spot.x, hot_spot.y)

    @property
    def help_message(self):
        return self._miscop_get_string(Window.GetHelpMessage)

    @help_message.setter
    def help_message(self, message):
        self._miscop_set_string(Window.SetHelpMessage, message)

    @property
    def title(self):
        return self._miscop_get_string(Window.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(Window.SetTitle, title)

    @property
    def default_focus(self):
        return self._miscop_get_unsigned(Window.GetDefaultFocus)

    @default_focus.setter
    def default_focus(self, focus):
        self._miscop_set_unsigned(Window.SetDefaultFocus, focus)

    def add_remove_keyboard_shortcuts(self, shortcuts, op):
        raise RuntimeError("Adding or removing of keyboard shortcuts is not yet implemented.")

    def add_keyboard_shortcuts(self, shortcuts):
        self.add_remove_keyboard_shortcuts(shortcuts, Window.AddKeyboardShortcuts)

    def remove_keyboard_shortcuts(self, shortcuts):
        self.add_remove_keyboard_shortcuts(shortcuts, Window.RemoveKeyboardShortcuts)

    @property
    def extent(self):
        extent = BBox.zero()
        swi.swi('Toolbox_ObjectMiscOp', 'IiII',
                0, self.id, Window.GetExtent, ctypes.addressof(extent))
        return extent

    @extent.setter
    def extent(self, extent):
        swi.swi('Toolbox_ObjectMiscOp', 'IiII',
                0, self.id, Window.SetExtent, ctypes.addressof(extent))

    def force_redraw(self, bbox=None):
        if bbox is None:
            bbox = self.extent
        swi.swi('Toolbox_ObjectMiscOp', 'IiII',
                0, self.id, Window.ForceRedraw, ctypes.addressof(bbox))

    def get_toolbar_id(self, tool_bar):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiI;i',
                       tool_bar, self.id, Window.GetToolBars)

    def set_toolbar_id(self, tool_bar, window_id):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIi',
                tool_bar, self.id, Window.SetToolBars, window_id)


class WindowAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = Window.AboutToBeShown


class WindowHasBeenHidden(ToolboxEvent):
    event_id = Window.HasBeenHidden
