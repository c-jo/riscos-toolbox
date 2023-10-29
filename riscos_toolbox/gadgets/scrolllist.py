from . import Gadget
from ..events import ToolboxEvent

import ctypes
import swi

class ScrollList(Gadget):
    Selection = 0x140181

    @property
    def state(self):
        return swi.swi("Toolbox_ObjectMiscOp","0iIi;I",
                       self.window.id, 16410, self.id)

    @state.setter
    def state(self, state):
        swi.swi("Toolbox_ObjectMiscOp","0iIiI",
                self.window.id, 16411, self.id, state)

    def add_item(self, text, index):
        swi.swi('Toolbox_ObjectMiscOp','0IIIs00I',
                self.window.id, 16412, self.id, text, index)

    def delete_items(self, start, end):
        swi.swi('Toolbox_ObjectMiscOp','0IIIII',
                self.window.id, 16413, self.id, start, end)

    def get_selected(self, offset=-1):
        return swi.swi('Toolbox_ObjectMiscOp','0IIIi;i',
                        self.window.id, 16416, self.id, offset)

    def make_visible(self, index):
        swi.swi('Toolbox_ObjectMiscOp','0III',
                self.window.id, 16417, self.id, index)

    @property
    def multisel(self):
        return self.state & 1 != 0

    @multisel.setter
    def multisel(self, multisel):
        self.state = 1 if multisel else 0

class ScrollListSelectionEvent(ToolboxEvent):
    event_id = ScrollList.Selection

    Flags_Set         = 1<<0
    Flags_DoubleClick = 1<<1
    Flags_AdjustClick = 1<<2

    _fields_ = [ ("sel_flags", ctypes.c_uint32), ("item", ctypes.c_int32) ]

