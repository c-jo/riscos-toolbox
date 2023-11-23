from . import Gadget
from ..events import ToolboxEvent

import ctypes
import swi


class ScrollList(Gadget):
    _type = 0x401a

    GetState     = 0
    SetState     = 1
    AddItem      = 2
    DeleteItems  = 3
    SelectItem   = 4
    DeselectItem = 5
    GetSelected  = 6
    MakeVisible  = 7
    SetColour    = 8
    GetColour    = 9
    SetFont      = 10
    GetItemText  = 11
    CountItems   = 12
    SetItemText  = 13

    Selection = 0x140181

    @property
    def state(self):
        return swi.swi("Toolbox_ObjectMiscOp", "0iIi;I",
                       self.window.id, 16410, self.id)

    @state.setter
    def state(self, state):
        swi.swi("Toolbox_ObjectMiscOp", "0IIIi",
                self.window.id, 16411, self.id, state)

    def add_item(self, text, index):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIis00i',
                0, self.window.id, ScrollList.AddItem, self.id, text, index)

    def delete_items(self, start, end):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIiii',
                0, self.window.id, ScrollList.Deleteitems, self.id, start, end)

    def get_selected(self, offset=-1):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiIii;i',
                       0, self.window.id, 16416, ScrollList.GetSelected, self.id, offset)

    def make_visible(self, index):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIii',
                0, self.window.id, ScrollList.MakeVisible, self.id, index)

    @property
    def multisel(self):
        return self.state & 1 != 0

    @multisel.setter
    def multisel(self, multisel):
        self.state = 1 if multisel else 0


class ScrollListSelectionEvent(ToolboxEvent):
    event_id = ScrollList.Selection

    Flags_Set         = 1 << 0
    Flags_DoubleClick = 1 << 1
    Flags_AdjustClick = 1 << 2

    _fields_ = [
        ('sel_flags', ctypes.c_uint32),
        ('item', ctypes.c_int32)
    ]

    @property
    def set(self):
        return self.sel_flags & ScrollListSelectionEvent.Flags_Set != 0

    @property
    def double_click(self):
        return self.sel_flags & ScrollListSelectionEvent.Flags_DoubleClick != 0

    @property
    def adjust_click(self):
        return self.sel_flags & ScrollListSelectionEvent.Flags_AdjustClick != 0
