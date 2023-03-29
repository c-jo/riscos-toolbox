"""RISC OS Toolbox - Scale"""

import swi
import ctypes

from ..base import Object
from ..events import EventData
from ..toolbox_events import ToolboxEventData

class Scale(Object):
    class_id = 0x82c00

    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    ApplyFactor       = class_id + 2

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def window_id(self):
        return swi.swi("Toolbox_ObjectMiscOp","0II;.I",self.id, 0)

    @property
    def value(self):
        return swi.swi("Toolbox_ObjectMiscOp","0II;I",self.id, 2)

    @value.setter
    def value(self, value):
        return swi.swi("Toolbox_ObjectMiscOp","0III",self.id, 1, value)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 6)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI',
                self.id, 6, buf, buf_size)
        return buf.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 5, title)

class ApplyFactorEvent(ToolboxEventData):
    event_id = Scale.ApplyFactor

    _fields_ = [ ("factor", ctypes.c_int32) ]

    def __init__(self):
        super().__init__()
